"""EVOD-22 DOGMA reference model and synthetic falsification harness.

The implementation is intentionally small and transparent. It is not an optimized
DOGMA Engine and does not establish genomic capability.
"""

import json
import math
from typing import NamedTuple
import torch
from torch import nn

COMP = torch.tensor([3, 2, 1, 0], dtype=torch.long)


def rc_ids(x):
    if x.dtype != torch.long or x.ndim != 2 or bool(((x < 0) | (x >= 4)).any()):
        raise ValueError("reverse complement accepts a [batch,time] int64 ACGT record")
    return COMP.to(x.device)[x.flip(-1)]


class DOGMAState(NamedTuple):
    h: torch.Tensor
    memory: torch.Tensor


def positive_int(value, name):
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ValueError(name + " must be a positive integer")


class DOGMACell(nn.Module):
    """Selective recurrent state plus K explicit memory loci.

    fast state h is request-owned. Memory m is request-owned. Parameters are model-owned.
    The gate depends only on the current token embedding and previous fast state.
    """

    def __init__(self, vocab=4, d=16, k=4):
        super().__init__()
        positive_int(d, "width")
        positive_int(k, "loci")
        if vocab != 4:
            raise ValueError("this reference freezes the ACGT vocabulary")
        self.d = d
        self.k = k
        self.emb = nn.Embedding(vocab, d)
        self.propose = nn.Linear(2 * d, d)
        self.gate = nn.Linear(2 * d, d)
        self.read_key = nn.Linear(d, k)
        self.write_gate = nn.Linear(d, k)
        self.write_val = nn.Linear(d, d)
        self.mix = nn.Linear(2 * d, d)

    def step(self, ids, h, m, *, disable_read=False):
        e = self.emb(ids)
        q = torch.cat([e, h], -1)
        cand = torch.tanh(self.propose(q))
        g = torch.sigmoid(self.gate(q))
        h = (1 - g) * h + g * cand
        a = torch.softmax(self.read_key(h), -1)
        read = torch.einsum("bk,bkd->bd", a, m)
        if disable_read:
            read = torch.zeros_like(read)  # same-parameter path intervention
        wg = torch.sigmoid(self.write_gate(h))
        val = torch.tanh(self.write_val(h))
        m = (1 - wg[..., None]) * m + wg[..., None] * val[:, None, :]
        y = torch.tanh(self.mix(torch.cat([h, read], -1)))
        return y, h, m, g, wg


class DOGMA(nn.Module):
    def __init__(self, vocab=4, d=16, k=4, classes=2):
        super().__init__()
        positive_int(classes, "classes")
        self.cell = DOGMACell(vocab, d, k)
        self.head = nn.Linear(d, classes)

    def initial_state(self, batch):
        positive_int(batch, "batch")
        w = self.cell.emb.weight
        return DOGMAState(
            w.new_zeros((batch, self.cell.d)),
            w.new_zeros((batch, self.cell.k, self.cell.d)),
        )

    def run(self, x, state=None, *, trace=False, disable_read=False):
        if x.ndim != 2 or x.dtype != torch.long or x.shape[0] < 1:
            raise ValueError("tokens require nonempty batch and int64 [batch,time]")
        if x.device != self.cell.emb.weight.device or bool(((x < 0) | (x >= 4)).any()):
            raise ValueError("tokens violate device/vocabulary contract")
        b, t = x.shape
        state = self.initial_state(b) if state is None else state
        if not isinstance(state, DOGMAState):
            raise ValueError("carry requires the complete DOGMAState")
        h, m = state
        expected = ((b, self.cell.d), (b, self.cell.k, self.cell.d))
        for tensor, shape in zip(state, expected):
            if (
                tensor.shape != shape
                or tensor.dtype != self.cell.emb.weight.dtype
                or tensor.device != x.device
                or not bool(torch.isfinite(tensor).all())
            ):
                raise ValueError("carry shape/dtype/device/finiteness mismatch")
        ys = []
        traces = []
        for i in range(t):
            y, h, m, g, wg = self.cell.step(x[:, i], h, m, disable_read=disable_read)
            ys.append(y)
            if trace:
                traces.append(
                    {
                        "t": i,
                        "gate_mean": float(g.mean().detach()),
                        "write_mean": float(wg.mean().detach()),
                    }
                )
        output = torch.stack(ys, 1) if ys else h.new_empty((b, 0, self.cell.d))
        return output, DOGMAState(h, m), traces

    def causal_features(self, x, trace=False):
        y, _, traces = self.run(x, trace=trace)
        return y, traces

    def causal_logits(self, x):
        y, _ = self.causal_features(x)
        return self.head(y)

    def offline_dual_logits(self, x):
        if x.ndim != 2 or x.shape[1] == 0:
            raise ValueError("offline mean pooling requires at least one base")
        # Full-record encoder. Shared parameters; reverse branch is realigned.
        f, _ = self.causal_features(x)
        r, _ = self.causal_features(rc_ids(x))
        r = r.flip(1)
        # Strand-invariant record feature by averaging aligned branches and positions.
        z = (f + r).mean(1) / 2
        return self.head(z)


class GRUBase(nn.Module):
    def __init__(self, vocab=4, d=16, classes=2):
        super().__init__()
        self.e = nn.Embedding(vocab, d)
        self.r = nn.GRU(d, d, batch_first=True)
        self.h = nn.Linear(d, classes)

    def forward(self, x):
        y, _ = self.r(self.e(x))
        return self.h(y[:, -1])


class MLPBase(nn.Module):
    def __init__(self, length=24, vocab=4, d=16, classes=2):
        super().__init__()
        self.e = nn.Embedding(vocab, d)
        self.n = nn.Sequential(
            nn.Linear(length * d, 64), nn.ReLU(), nn.Linear(64, classes)
        )

    def forward(self, x):
        return self.n(self.e(x).flatten(1))


class CNNBase(nn.Module):
    """Task-relevant learned three-base detector, not just a flattened baseline."""

    def __init__(self, channels=12, classes=2):
        super().__init__()
        self.conv = nn.Conv1d(4, channels, 3)
        self.head = nn.Linear(channels, classes)

    def forward(self, x):
        onehot = torch.nn.functional.one_hot(x, 4).to(self.conv.weight.dtype)
        features = torch.relu(self.conv(onehot.transpose(1, 2))).amax(-1)
        return self.head(features)


def motif_oracle(x):
    """Independent string specification, with the exact ACG/CGT target rule."""
    words = ["".join("ACGT"[int(i)] for i in row) for row in x]
    return torch.tensor([int("ACG" in s or "CGT" in s) for s in words])


def record_keys(x):
    r = rc_ids(x)
    return {min(tuple(a), tuple(b)) for a, b in zip(x.tolist(), r.tolist())}


def make_data(n=512, length=24, seed=7):
    """Whole-record classification: label=1 iff motif ACG occurs in either strand orientation.
    Positive examples are explicitly implanted; negatives are rejection sampled.
    """
    positive_int(n, "examples")
    if not isinstance(length, int) or isinstance(length, bool) or length < 3:
        raise ValueError("motif task requires length >= 3")
    g = torch.Generator().manual_seed(seed)
    xs = []
    ys = []
    motif = torch.tensor([0, 1, 2])
    rcm = rc_ids(motif[None, :])[0]
    while len(xs) < n:
        x = torch.randint(0, 4, (length,), generator=g)
        pos = any(
            torch.equal(x[i : i + 3], motif) or torch.equal(x[i : i + 3], rcm)
            for i in range(length - 2)
        )
        target = len(xs) % 2
        if target == 1 and not pos:
            j = int(torch.randint(0, length - 2, (1,), generator=g))
            x[j : j + 3] = motif
            pos = True
        if target == 0 and pos:
            continue
        xs.append(x)
        ys.append(target)
    return torch.stack(xs), torch.tensor(ys)


def params(m):
    return sum(p.numel() for p in m.parameters())


def train_eval(model, xtr, ytr, xte, yte, dual=False, epochs=30, seed=0):
    torch.manual_seed(seed)
    opt = torch.optim.AdamW(model.parameters(), lr=3e-3)
    lossf = nn.CrossEntropyLoss()
    for _ in range(epochs):
        opt.zero_grad()
        logits = model.offline_dual_logits(xtr) if dual else model(xtr)
        loss = lossf(logits, ytr)
        loss.backward()
        opt.step()
    with torch.no_grad():
        logits = model.offline_dual_logits(xte) if dual else model(xte)
        acc = (logits.argmax(-1) == yte).float().mean().item()
        loss = lossf(logits, yte).item()
    return {"accuracy": acc, "loss": loss, "params": params(model)}


def experiment(seeds=(11, 23, 37), epochs=30):
    """Multi-seed implementation pilot; NOT a matched-budget architecture benchmark."""
    xtr, ytr = make_data(512, 24, 137)
    xte, yte = make_data(128, 24, 139)
    if record_keys(xtr) & record_keys(xte):
        raise RuntimeError("exact/reverse-complement train/test contamination")
    assert torch.equal(motif_oracle(xtr), ytr)
    assert torch.equal(motif_oracle(xte), yte)
    constructors = {
        "DOGMA dual": lambda: DOGMA(d=12, k=3),
        "GRU": lambda: GRUBase(d=12),
        "MLP": lambda: MLPBase(d=12),
        "CNN width-3": lambda: CNNBase(12),
        "DOGMA random": lambda: DOGMA(d=12, k=3),
    }
    rows = []
    for seed in seeds:
        for name, build in constructors.items():
            torch.manual_seed(seed)
            model = build()
            a, b = ytr, yte
            if name == "DOGMA random":
                a = torch.randint(
                    0,
                    2,
                    ytr.shape,
                    generator=torch.Generator().manual_seed(seed + 1000),
                )
                b = torch.randint(
                    0,
                    2,
                    yte.shape,
                    generator=torch.Generator().manual_seed(seed + 2000),
                )
            value = train_eval(
                model, xtr, a, xte, b, "DOGMA" in name, epochs=epochs, seed=seed
            )
            rows.append(
                {
                    "seed": seed,
                    "model": name,
                    **value,
                    "epochs": epochs,
                    "strand_passes": 2 if "DOGMA" in name else 1,
                }
            )
    summaries = []
    for name in constructors:
        values = [r["accuracy"] for r in rows if r["model"] == name]
        mean = sum(values) / len(values)
        sd = (
            math.sqrt(sum((v - mean) ** 2 for v in values) / (len(values) - 1))
            if len(values) > 1
            else 0
        )
        summaries.append(
            {
                "model": name,
                "mean_accuracy": mean,
                "sample_sd": sd,
                "params": next(r["params"] for r in rows if r["model"] == name),
            }
        )
    return rows, summaries


def checks():
    torch.manual_seed(3)
    m = DOGMA(d=8, k=2)
    x = torch.tensor([[0, 1, 2, 3, 0, 1]])
    full = m.causal_logits(x)
    # Prefix invariance: logits through position 3 cannot depend on appended suffix.
    x2 = torch.tensor([[0, 1, 2, 3, 3, 3]])
    pref = torch.allclose(full[:, :4], m.causal_logits(x2)[:, :4], atol=1e-7)
    loss = full.square().mean()
    loss.backward()
    grad = sum(float(p.grad.abs().sum()) for p in m.parameters() if p.grad is not None)
    # Offline dual is RC invariant by construction up to floating arithmetic.
    inv = torch.allclose(
        m.offline_dual_logits(x), m.offline_dual_logits(rc_ids(x)), atol=1e-6
    )
    return {
        "causal_prefix_invariance": pref,
        "gradient_l1": grad,
        "offline_rc_invariance": inv,
    }


def assigned_trace():
    """Constant parameters chosen for an independent hand-computed transition."""
    m = DOGMA(d=1, k=1).double()
    with torch.no_grad():
        for p in m.parameters():
            p.zero_()
        m.cell.propose.bias.fill_(math.atanh(0.5))
        m.cell.write_gate.bias.fill_(math.log(1 / 3))
        m.cell.write_val.bias.fill_(math.atanh(0.8))
        m.cell.mix.weight.copy_(torch.tensor([[1.0, 1.0]], dtype=torch.float64))
    state = m.initial_state(1)
    rows = []
    for t in range(1, 5):
        old = state.memory.item()
        y, state, _ = m.run(torch.tensor([[0]]), state)
        rows.append(
            {
                "t": t,
                "h": state.h.item(),
                "old_memory": old,
                "new_memory": state.memory.item(),
                "y": y.item(),
            }
        )
    return rows


def results():
    torch.set_num_threads(1)
    pilot, summary = experiment()
    return {
        "checks": checks(),
        "assigned_trace": assigned_trace(),
        "pilot": pilot,
        "summary": summary,
        "environment": {
            "torch": torch.__version__,
            "dtype": "float32 pilot / float64 trace",
            "device": "cpu",
            "threads": 1,
            "train_seed": 137,
            "test_seed": 139,
        },
        "random_population_floor_nats": math.log(2),
        "evidence": "implementation pilot; parameter/compute budgets NOT matched",
    }


TABLES = [
    (
        "assigned_trace",
        ["Step", "Fast state", "Old memory", "New memory", "Feature"],
        ["t", "h", "old_memory", "new_memory", "y"],
        "rrrrr",
    ),
    (
        "summary",
        ["Model", "Mean accuracy", "Seed SD", "Parameters"],
        ["model", "mean_accuracy", "sample_sd", "params"],
        "lrrr",
    ),
]
PLOTS = []
LISTINGS = ["DOGMACell.step", "DOGMA.run", "train_eval"]


def main():
    torch.set_num_threads(1)
    print(json.dumps(results(), indent=2))


if __name__ == "__main__":
    main()
