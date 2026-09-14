"""A restartable CPU float64 teaching run on synthetic DNA strings."""

import copy
import hashlib
import io
import json
import torch
from torch import nn
from torch.nn import functional as F

ALPHABET = "ACGTN"
PAD = 5
IGNORE = -100
CORPUS = (
    ("train-a", "ACGTACGT"),
    ("train-b", "ACGTT"),
    ("train-c", "TTACGN"),
    ("train-d", "CGTAC"),
    ("train-e", "GATTACA"),
    ("train-f", "TGCATGCA"),
)
VALIDATION = (("valid-a", "ACGACG"), ("valid-b", "TTGCA"))
CONFIG = {
    "batch_size": 2,
    "width": 8,
    "dropout": 0.25,
    "lr": 0.15,
    "momentum": 0.9,
    "dtype": "float64",
    "device": "cpu",
    "alphabet": ALPHABET,
    "pad": PAD,
    "ignore": IGNORE,
}


def corpus_digest(corpus=CORPUS):
    return hashlib.sha256(
        json.dumps(corpus, separators=(",", ":")).encode()
    ).hexdigest()


def validate_split(train=CORPUS, validation=VALIDATION):
    complement = str.maketrans("ACGTN", "TGCAN")

    def identities(rows):
        return {
            min(seq, seq.translate(complement)[::-1]) for _, seq in rows
        }

    if {name for name, _ in train} & {name for name, _ in validation}:
        raise ValueError("group identity crosses the split")
    if identities(train) & identities(validation):
        raise ValueError(
            "exact sequence or reverse complement crosses the split"
        )


def collate(rows):
    if not rows or any(
        len(seq) < 2 or set(seq) - set(ALPHABET) for _, seq in rows
    ):
        raise ValueError(
            "nonempty canonical ACGTN sequences of length at least two required"
        )
    length = max(len(seq) - 1 for _, seq in rows)
    x = torch.full((len(rows), length), PAD, dtype=torch.long)
    y = torch.full_like(x, IGNORE)
    for i, (_, seq) in enumerate(rows):
        ids = [ALPHABET.index(base) for base in seq]
        x[i, : len(ids) - 1] = torch.tensor(ids[:-1])
        targets = [v if v < 4 else IGNORE for v in ids[1:]]
        y[i, : len(targets)] = torch.tensor(targets)
    return x, y


def masked_loss(logits, targets):
    if logits.shape[:-1] != targets.shape or logits.shape[-1] != 4:
        raise ValueError("expected logits [B,T,4] and targets [B,T]")
    count = int((targets != IGNORE).sum())
    if count == 0:
        raise ValueError("an empty scored-target set has no mean loss")
    total = F.cross_entropy(
        logits.reshape(-1, 4),
        targets.reshape(-1),
        ignore_index=IGNORE,
        reduction="sum",
    )
    return total, count


class Predictor(nn.Module):
    def __init__(self):
        super().__init__()
        self.embedding = nn.Embedding(6, 8, padding_idx=PAD)
        self.dropout = nn.Dropout(0.25)
        self.projection = nn.Linear(8, 4)
        self.double()

    def forward(self, x):
        return self.projection(self.dropout(torch.tanh(self.embedding(x))))


class Run:
    def __init__(self, corpus=CORPUS):
        self.corpus = tuple(corpus)
        if len({name for name, _ in self.corpus}) != len(self.corpus):
            raise ValueError("row IDs must be unique")
        collate(
            self.corpus
        )  # validate before creating any mutable training state
        torch.manual_seed(2026)
        self.model = Predictor()
        self.optimizer = torch.optim.SGD(
            self.model.parameters(), lr=0.15, momentum=0.9
        )
        self.sampler = torch.Generator().manual_seed(91)
        self.order = torch.randperm(
            len(self.corpus), generator=self.sampler
        ).tolist()
        self.cursor = 0
        self.epoch = 0
        self.updates = 0

    def step(self):
        if self.cursor == len(self.order):
            self.order = torch.randperm(
                len(self.corpus), generator=self.sampler
            ).tolist()
            self.cursor = 0
            self.epoch += 1
        ids = self.order[self.cursor : self.cursor + CONFIG["batch_size"]]
        x, y = collate([self.corpus[i] for i in ids])
        self.model.train()
        self.optimizer.zero_grad(set_to_none=True)
        total, count = masked_loss(self.model(x), y)
        loss = total / count
        loss.backward()
        self.optimizer.step()
        self.optimizer.zero_grad(set_to_none=True)
        self.cursor += len(ids)
        self.updates += 1
        return {
            "update": self.updates,
            "epoch": self.epoch,
            "ids": [self.corpus[i][0] for i in ids],
            "scored_targets": count,
            "loss": float(loss.detach()),
        }

    def checkpoint(self):
        state = {
            "schema": 1,
            "config": CONFIG,
            "corpus_sha256": corpus_digest(self.corpus),
            "torch_version": str(torch.__version__),
            "model": self.model.state_dict(),
            "optimizer": self.optimizer.state_dict(),
            "sampler_rng": self.sampler.get_state(),
            "torch_rng": torch.get_rng_state(),
            "order": self.order,
            "cursor": self.cursor,
            "epoch": self.epoch,
            "updates": self.updates,
        }
        stream = io.BytesIO()
        torch.save(
            state, stream
        )  # serialize now, not a live state_dict alias
        return stream.getvalue()

    @classmethod
    def restore(cls, blob, corpus=CORPUS, omit=None):
        state = torch.load(
            io.BytesIO(blob), map_location="cpu", weights_only=True
        )
        if state["schema"] != 1 or state["config"] != CONFIG:
            raise ValueError("checkpoint schema/config mismatch")
        if state["corpus_sha256"] != corpus_digest(corpus):
            raise ValueError("checkpoint corpus/order identity mismatch")
        if state["torch_version"] != str(torch.__version__):
            raise ValueError(
                "exact replay requires the recorded PyTorch version"
            )
        run = cls(corpus)  # initialization consumes RNG before restoration
        run.model.load_state_dict(state["model"])
        if omit != "optimizer":
            run.optimizer.load_state_dict(state["optimizer"])
        run.sampler.set_state(state["sampler_rng"])
        run.order = list(state["order"])
        run.cursor = 0 if omit == "cursor" else state["cursor"]
        run.epoch = state["epoch"]
        run.updates = state["updates"]
        if omit != "rng":
            torch.set_rng_state(
                state["torch_rng"]
            )  # restore after constructing modules
        return run

    def evaluate(self, rows=VALIDATION):
        was_training = self.model.training
        self.model.eval()
        total, count = 0.0, 0
        try:
            with torch.no_grad():
                for row in rows:
                    x, y = collate([row])
                    value, n = masked_loss(self.model(x), y)
                    total += float(value)
                    count += n
        finally:
            self.model.train(was_training)
        if count == 0:
            raise ValueError("empty evaluation set")
        return total / count


def parameter_vector(run):
    return torch.cat(
        [p.detach().reshape(-1) for p in run.model.parameters()]
    ).clone()


def replay(cut=2, total=8, omit=None):
    if not 0 < cut < total:
        raise ValueError("cut must be inside the run")
    with torch.random.fork_rng():
        baseline = Run()
        prefix = [baseline.step() for _ in range(cut)]
        blob = baseline.checkpoint()
        tail = [baseline.step() for _ in range(total - cut)]
        expected = parameter_vector(baseline)
        final_state = copy.deepcopy(baseline.optimizer.state_dict())
        restored = Run.restore(blob, omit=omit)
        actual = [restored.step() for _ in range(total - cut)]
        return {
            "prefix": prefix,
            "expected_tail": tail,
            "actual_tail": actual,
            "max_parameter_error": float(
                (expected - parameter_vector(restored)).abs().max()
            ),
            "same_batch_trace": [r["ids"] for r in tail]
            == [r["ids"] for r in actual],
            "same_loss_trace": [r["loss"] for r in tail]
            == [r["loss"] for r in actual],
            "expected_optimizer": final_state,
            "actual_optimizer": restored.optimizer.state_dict(),
        }


def results():
    validate_split()
    with torch.random.fork_rng():
        run = Run()
        before = run.evaluate()
        rows = [run.step() for _ in range(8)]
        after = run.evaluate()
        checks = {}
        for omit in (None, "optimizer", "rng", "cursor"):
            r = replay(omit=omit)
            checks["complete" if omit is None else "missing_" + omit] = {
                k: r[k]
                for k in (
                    "max_parameter_error",
                    "same_batch_trace",
                    "same_loss_trace",
                )
            }
        x, y = collate([("example-a", "ACGT"), ("example-b", "AN")])
        zero, count = masked_loss(
            torch.zeros((*y.shape, 4), dtype=torch.float64), y
        )
        return {
            "scope": "synthetic one-base-context CPU teaching model; not a genomic benchmark",
            "torch_version": str(torch.__version__),
            "config": CONFIG,
            "corpus_sha256": corpus_digest(),
            "train_rows": len(CORPUS),
            "validation_rows": len(VALIDATION),
            "parameter_count": sum(
                p.numel() for p in run.model.parameters()
            ),
            "uniform_logits": {
                "scored_targets": count,
                "mean_loss": float(zero / count),
            },
            "training": rows,
            "validation": {"before": before, "after": after},
            "restart": checks,
        }


if __name__ == "__main__":
    torch.set_num_threads(1)
    print(json.dumps(results(), indent=2))
