"""EVOD-23 transparent Hermon reference. No optimized engine or genomic benchmark."""

import json
import math
import statistics
import torch
from torch import nn

COMP = torch.tensor([3, 2, 1, 0], dtype=torch.long)


def positive(value):
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValueError("positive integer required")
    return value


def rc_ids(x):
    if x.ndim != 2 or x.dtype != torch.long or bool(((x < 0) | (x > 3)).any()):
        raise ValueError("ACGT int64 [batch,time] required")
    return COMP.to(x.device)[x.flip(-1)]


def causal_mask(t, device):
    positive(t)
    return torch.triu(torch.ones(t, t, dtype=torch.bool, device=device), diagonal=1)


def legality(valid, causal):
    """True means disallowed. Invalid queries and keys have no attention edges."""
    if valid.ndim != 2 or valid.dtype != torch.bool:
        raise ValueError("boolean [batch,time] validity required")
    blocked = ~(valid[:, :, None] & valid[:, None, :])
    return (
        blocked | causal_mask(valid.shape[1], valid.device)[None] if causal else blocked
    )


class MHA(nn.Module):
    def __init__(self, d=32, h=4):
        super().__init__()
        positive(d)
        positive(h)
        if d % h:
            raise ValueError("width must divide into equal heads")
        self.d, self.h, self.dh = d, h, d // h
        self.qkv = nn.Linear(d, 3 * d)
        self.out = nn.Linear(d, d)

    def forward(self, x, mask=None):
        if (
            x.ndim != 3
            or x.shape[0] == 0
            or x.shape[1] == 0
            or x.shape[-1] != self.d
            or x.dtype != self.qkv.weight.dtype
            or x.device != self.qkv.weight.device
            or not bool(torch.isfinite(x).all())
        ):
            raise ValueError("finite activation [B,T,D] matching model required")
        b, t, d = x.shape
        q, k, v = self.qkv(x).view(b, t, 3, self.h, self.dh).permute(2, 0, 3, 1, 4)
        scores = q @ k.transpose(-2, -1) / math.sqrt(self.dh)
        if mask is None:
            mask = torch.zeros(b, t, t, dtype=torch.bool, device=x.device)
        elif (
            mask.dtype != torch.bool
            or mask.device != x.device
            or mask.shape not in ((t, t), (b, t, t))
        ):
            raise ValueError("boolean [T,T] or [B,T,T] mask required")
        if mask.ndim == 2:
            mask = mask.expand(b, -1, -1)
        active = (~mask).any(-1)
        scores = scores.masked_fill(mask[:, None], float("-inf"))
        # Softmax on an all-masked row is undefined. Choose zero attention, not NaN.
        safe = torch.where(active[:, None, :, None], scores, torch.zeros_like(scores))
        a = torch.softmax(safe, -1) * active[:, None, :, None]
        y = (a @ v).transpose(1, 2).contiguous().view(b, t, d)
        return self.out(y) * active[:, :, None], a


class Block(nn.Module):
    def __init__(self, d=32, h=4, ff=64):
        super().__init__()
        positive(ff)
        self.n1 = nn.LayerNorm(d)
        self.attn = MHA(d, h)
        self.n2 = nn.LayerNorm(d)
        self.ff = nn.Sequential(nn.Linear(d, ff), nn.GELU(), nn.Linear(ff, d))

    def forward(self, x, mask=None):
        y, a = self.attn(self.n1(x), mask)
        x = x + y
        return x + self.ff(self.n2(x)), a


class HermonDNA(nn.Module):
    def __init__(self, vocab=4, max_len=64, d=32, h=4, layers=2, classes=2):
        super().__init__()
        if vocab != 4:
            raise ValueError("reference vocabulary is canonical ACGT")
        for v in (max_len, d, h, layers, classes):
            positive(v)
        self.d = d
        self.max_len = max_len
        self.tok = nn.Embedding(vocab, d)
        self.pos = nn.Embedding(max_len, d)
        self.blocks = nn.ModuleList([Block(d, h, 2 * d) for _ in range(layers)])
        self.norm = nn.LayerNorm(d)
        self.lm = nn.Linear(d, vocab)
        self.cls = nn.Linear(d, classes)

    def validity(self, x, valid):
        if (
            x.ndim != 2
            or x.dtype != torch.long
            or x.shape[0] == 0
            or not 0 < x.shape[1] <= self.max_len
            or x.device != self.tok.weight.device
            or bool(((x < 0) | (x > 3)).any())
        ):
            raise ValueError("nonempty ACGT batch within maximum length required")
        if valid is None:
            return torch.ones_like(x, dtype=torch.bool)
        if (
            valid.shape != x.shape
            or valid.dtype != torch.bool
            or valid.device != x.device
        ):
            raise ValueError("validity shape/dtype/device mismatch")
        return valid

    def encode(self, x, causal=False, valid=None):
        valid = self.validity(x, valid)
        # Valid-token ordinal: inserting padding does not shift biological positions.
        pos = (valid.long().cumsum(1) - 1).clamp_min(0)
        z = (self.tok(x) + self.pos(pos)) * valid[:, :, None]
        mask = legality(valid, causal)
        attention = []
        for block in self.blocks:
            z, a = block(z, mask)
            z = z * valid[:, :, None]  # norm/FFN biases must not revive invalid queries
            attention.append(a)
        return self.norm(z) * valid[:, :, None], attention

    def causal_logits(self, x, valid=None):
        valid = self.validity(x, valid)
        return self.lm(self.encode(x, True, valid)[0]) * valid[:, :, None]

    def offline_logits(self, x, valid=None):
        valid = self.validity(x, valid)
        n = valid.sum(1)
        if bool((n == 0).any()):
            raise ValueError(
                "offline pooling requires at least one valid base per record"
            )
        z = self.encode(x, False, valid)[0]
        return self.cls(z.sum(1) / n[:, None])

    def offline_rc_symmetric_logits(self, x, valid=None):
        valid = self.validity(x, valid)
        return (
            self.offline_logits(x, valid)
            + self.offline_logits(rc_ids(x), valid.flip(-1))
        ) / 2


def attention_oracle(module, x, mask=None):
    """Independent row-by-row allowed-index oracle; no masked softmax reuse."""
    b, t, d = x.shape
    raw = torch.nn.functional.linear(x, module.qkv.weight, module.qkv.bias)
    q, k, v = [
        z.view(b, t, module.h, module.dh).transpose(1, 2) for z in raw.chunk(3, -1)
    ]
    weights = torch.zeros(b, module.h, t, t, dtype=x.dtype, device=x.device)
    rows = []
    for bi in range(b):
        heads = []
        for hi in range(module.h):
            output = []
            for i in range(t):
                allowed = (
                    torch.ones(t, dtype=torch.bool, device=x.device)
                    if mask is None
                    else ~(mask[i] if mask.ndim == 2 else mask[bi, i])
                )
                if bool(allowed.any()):
                    scores = torch.stack(
                        [
                            torch.dot(q[bi, hi, i], k[bi, hi, j])
                            for j in range(t)
                            if allowed[j]
                        ]
                    ) / math.sqrt(module.dh)
                    p = scores.softmax(0)
                    weights[bi, hi, i, allowed] = p
                    output.append((p[:, None] * v[bi, hi, allowed]).sum(0))
                else:
                    output.append(
                        torch.zeros(module.dh, dtype=x.dtype, device=x.device)
                    )
            heads.append(torch.stack(output))
        rows.append(torch.stack(heads))
    y = torch.stack(rows).transpose(1, 2).reshape(b, t, d)
    active = weights.sum(1).sum(-1) > 0
    return torch.nn.functional.linear(y, module.out.weight, module.out.bias) * active[
        :, :, None
    ], weights


def motif_oracle(x):
    """ACGT is its own reverse complement; this task has one distinct pattern."""
    strings = ["".join("ACGT"[v] for v in row) for row in x.tolist()]
    return torch.tensor([int("ACGT" in s) for s in strings])


def make_motif(n=640, T=32, seed=23):
    positive(n)
    positive(T)
    if T < 4:
        raise ValueError("motif requires four bases")
    g = torch.Generator().manual_seed(seed)
    xs = []
    ys = []
    while len(xs) < n:
        x = torch.randint(0, 4, (T,), generator=g)
        y = len(xs) % 2
        present = bool(motif_oracle(x[None])[0])
        if y and not present:
            j = int(torch.randint(0, T - 3, (1,), generator=g))
            x[j : j + 4] = torch.tensor([0, 1, 2, 3])
        if not y and present:
            continue
        xs.append(x)
        ys.append(y)
    return torch.stack(xs), torch.tensor(ys)


class MotifCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv = nn.Conv1d(4, 8, 4)
        self.head = nn.Linear(8, 2)

    def offline_rc_symmetric_logits(self, x):
        def one(s):
            z = nn.functional.one_hot(s, 4).float().transpose(1, 2)
            return self.head(torch.relu(self.conv(z)).amax(-1))

        return (one(x) + one(rc_ids(x))) / 2


def train_eval(model, xtr, ytr, xte, yte, epochs=25):
    positive(epochs)
    opt = torch.optim.AdamW(model.parameters(), lr=3e-3)
    ce = nn.CrossEntropyLoss()
    losses = []
    model.train()
    for _ in range(epochs):
        opt.zero_grad()
        loss = ce(model.offline_rc_symmetric_logits(xtr), ytr)
        loss.backward()
        opt.step()
        losses.append(float(loss.detach()))
    model.eval()
    with torch.no_grad():
        z = model.offline_rc_symmetric_logits(xte)
        return {
            "loss": ce(z, yte).item(),
            "accuracy": (z.argmax(-1) == yte).float().mean().item(),
            "params": sum(p.numel() for p in model.parameters()),
            "train_loss": losses,
        }


def checks():
    torch.manual_seed(5)
    mha = MHA(16, 4).double()
    x = torch.randn(2, 6, 16, dtype=torch.float64)
    mask = causal_mask(6, x.device)
    y, a = mha(x, mask)
    yo, ao = attention_oracle(mha, x, mask)
    model = HermonDNA(max_len=16, d=16, h=4, layers=1).double()
    seq = torch.tensor([[0, 1, 2, 3, 0, 1]])
    seq2 = torch.tensor([[0, 1, 2, 3, 3, 3]])
    return {
        "attention_output_error": float((y - yo).abs().max().detach()),
        "attention_weight_error": float((a - ao).abs().max().detach()),
        "causal_prefix_invariance": torch.allclose(
            model.causal_logits(seq)[:, :4],
            model.causal_logits(seq2)[:, :4],
            atol=1e-12,
            rtol=0,
        ),
        "offline_rc_symmetry": torch.allclose(
            model.offline_rc_symmetric_logits(seq),
            model.offline_rc_symmetric_logits(rc_ids(seq)),
            atol=1e-12,
            rtol=0,
        ),
    }


def experiment(seeds=(11, 23, 37), epochs=25):
    xtr, ytr = make_motif(512, 32, 137)
    xte, yte = make_motif(128, 32, 139)
    assert torch.equal(motif_oracle(xtr), ytr) and torch.equal(motif_oracle(xte), yte)

    def keys(x):
        return {
            min(tuple(row), tuple(rc))
            for row, rc in zip(x.tolist(), rc_ids(x).tolist())
        }

    assert not keys(xtr) & keys(xte)
    g = torch.Generator().manual_seed(907)
    random_train = torch.randint(0, 2, ytr.shape, generator=g)
    random_test = torch.randint(0, 2, yte.shape, generator=g)
    rows = []
    for seed in seeds:
        for name in ("Hermon", "CNN width-4", "Hermon random"):
            torch.manual_seed(seed)
            m = (
                MotifCNN()
                if name == "CNN width-4"
                else HermonDNA(max_len=32, d=24, h=4, layers=2)
            )
            yt, ye = (
                (random_train, random_test) if name == "Hermon random" else (ytr, yte)
            )
            rows.append(
                {
                    "seed": seed,
                    "model": name,
                    "epochs": epochs,
                    **train_eval(m, xtr, yt, xte, ye, epochs),
                }
            )
    summary = []
    for name in ("Hermon", "CNN width-4", "Hermon random"):
        selected = [r for r in rows if r["model"] == name]
        acc = [r["accuracy"] for r in selected]
        summary.append(
            {
                "model": name,
                "accuracy": statistics.mean(acc),
                "sd": statistics.stdev(acc) if len(acc) > 1 else 0,
                "params": selected[0]["params"],
            }
        )
    return {
        "runs": rows,
        "pilot": summary,
        "exact_motif_oracle_accuracy": 1.0,
        "data_seeds": [137, 139],
        "random_label_seed": 907,
        "split": "exact sequence and reverse-complement disjoint; not homology-tested",
        "budget": "same examples, 25 full-batch epochs, two orientation passes; not parameter/FLOP matched",
    }


def assigned_attention():
    q = torch.tensor([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]], dtype=torch.float64)
    v = torch.tensor([[1.0, 0.0], [0.0, 2.0], [3.0, 1.0]], dtype=torch.float64)
    weights = (
        (q @ q.T / math.sqrt(2))
        .masked_fill(causal_mask(3, q.device), float("-inf"))
        .softmax(-1)
    )
    y = weights @ v
    return [
        {
            "query": i + 1,
            "a1": weights[i, 0].item(),
            "a2": weights[i, 1].item(),
            "a3": weights[i, 2].item(),
            "o1": y[i, 0].item(),
            "o2": y[i, 1].item(),
        }
        for i in range(3)
    ]


def results():
    torch.set_num_threads(1)
    experiment_result = experiment()
    return {
        "checks": checks(),
        "attention_trace": assigned_attention(),
        **experiment_result,
        "environment": {
            "torch": torch.__version__,
            "device": "cpu",
            "threads": 1,
            "pilot_dtype": "float32",
            "oracle_dtype": "float64",
        },
        "evidence": "local implementation pilot, not genomic capability or architecture ranking",
    }


TABLES = [
    (
        "attention_trace",
        ["Query", "A1", "A2", "A3", "O1", "O2"],
        ["query", "a1", "a2", "a3", "o1", "o2"],
        "rrrrrr",
    ),
    (
        "pilot",
        ["Model", "Mean accuracy", "Seed SD", "Parameters"],
        ["model", "accuracy", "sd", "params"],
        "lrrr",
    ),
]
PLOTS = []
LISTINGS = ["MHA.forward", "HermonDNA.encode", "attention_oracle", "train_eval"]

if __name__ == "__main__":
    print(json.dumps(results(), indent=2))
