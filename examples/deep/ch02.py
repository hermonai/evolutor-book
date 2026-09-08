"""Small evaluation references; no DOGMA/Hermon training or benchmark claim."""
import hashlib
import json
import math
from pathlib import Path
import statistics
import sys
import torch
from torch import nn
from torch.nn import functional as F

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code/evo_torch"))
from evo_torch.causality import prefix_intervention_error


def reverse_complement(sequence):
    if not sequence or set(sequence) - set("ACGT"):
        raise ValueError("nonempty uppercase DNA required")
    return sequence.translate(str.maketrans("ACGT", "TGCA"))[::-1]


def split_records(records, seed=11, fractions=(0.6, 0.2, 0.2)):
    """Union exact/RC identity and declared metadata groups, then split components.

    This does not calculate homology, phylogeny or coordinate overlap.
    """
    if len(fractions) != 3 or any(not math.isfinite(f) or f <= 0 for f in fractions):
        raise ValueError("three positive finite fractions required")
    if not math.isclose(sum(fractions), 1.0):
        raise ValueError("fractions must sum to one")
    by_id = {r["id"]: r for r in records}
    if not records or len(by_id) != len(records):
        raise ValueError("nonempty unique record IDs required")
    if any(not isinstance(r["id"], str) or not r["id"] or not isinstance(r["group"], str)
           or not r["group"] for r in records):
        raise ValueError("nonempty ID and metadata group required")
    parent = {key: key for key in by_id}

    def find(key):
        while parent[key] != key:
            parent[key] = parent[parent[key]]
            key = parent[key]
        return key

    owners = {}
    for key in sorted(by_id):
        r = by_id[key]
        canonical = min(r["sequence"], reverse_complement(r["sequence"]))
        for relation in (("sequence", canonical), ("metadata", r["group"])):
            if relation in owners:
                a, b = find(key), find(owners[relation])
                parent[max(a, b)] = min(a, b)
            else:
                owners[relation] = key
    components = {}
    for key in sorted(by_id):
        components.setdefault(find(key), []).append(key)
    if len(components) < 3:
        raise ValueError("fewer than three independent components; cannot make three nonempty folds")
    groups = sorted(components.values(), key=lambda ids: (
        -len(ids), hashlib.sha256((str(seed) + json.dumps(ids)).encode()).hexdigest()))
    folds = [[], [], []]
    for ids in groups:
        i = min(range(3), key=lambda j: (len(folds[j]) / fractions[j], j))
        folds[i].extend(ids)
    return {name: sorted(ids) for name, ids in zip(("train", "validation", "test"), folds)}


def token_metrics(logits, targets):
    """Unweighted next-base loss; all supplied positions are scored."""
    if logits.ndim != 3 or targets.shape != logits.shape[:2] or targets.numel() == 0:
        raise ValueError("expected nonempty logits [B,T,V] and targets [B,T]")
    if not torch.isfinite(logits).all():
        raise ValueError("non-finite logits")
    if targets.dtype != torch.long or targets.min() < 0 or targets.max() >= logits.shape[-1]:
        raise ValueError("target indices outside vocabulary")
    loss = F.cross_entropy(logits.reshape(-1, logits.shape[-1]), targets.reshape(-1))
    nats = float(loss)
    return {"nats_per_base": nats, "perplexity": math.exp(nats),
            "bits_per_base": nats / math.log(2),
            "accuracy": float((logits.argmax(-1) == targets).double().mean())}


class PrefixCounts(nn.Module):
    """Deterministic causal smoothed prefix frequencies, not a trained model."""
    def forward(self, ids):
        counts = F.one_hot(ids, 4).to(torch.float64).cumsum(1) + 1
        return counts.log()


class FutureCopy(nn.Module):
    """Deliberately invalid: reads the next input token before predicting it."""
    def forward(self, ids):
        future = torch.cat((ids[:, 1:], ids[:, -1:]), dim=1)
        return 8 * F.one_hot(future, 4).to(torch.float64)


def intervention_suite(model, ids, atol=1e-12):
    if ids.ndim != 2 or ids.shape[0] < 1 or ids.shape[1] < 2:
        raise ValueError("nonempty batch and prefix/future required")
    if ids.dtype != torch.long or ids.min() < 0 or ids.max() >= 4:
        raise ValueError("DNA token indices required")
    if not math.isfinite(atol) or atol < 0:
        raise ValueError("finite nonnegative tolerance required")
    # The existing helper performs +1-mod-V suffix interventions and restores mode.
    errors = [prefix_intervention_error(model, ids, prefix_length=t, vocab_size=4)
              for t in range(1, ids.shape[1])]
    if not all(math.isfinite(e) for e in errors):
        raise ValueError("non-finite intervention output cannot pass")
    return {"errors": errors, "maximum": max(errors), "passes": max(errors) <= atol,
            "atol": atol, "dtype": "float64 reference on CPU"}


def delay_oracle(sequence, lag):
    if type(lag) is not int or lag < 1 or lag >= len(sequence):
        raise ValueError("lag must leave at least one scored position")
    return tuple(sequence[:-lag])


def seed_summary(values):
    values = tuple(float(v) for v in values)
    if len(values) < 2 or not all(math.isfinite(v) for v in values):
        raise ValueError("at least two finite values required")
    return {"individual": values, "mean": statistics.mean(values),
            "median": statistics.median(values), "sample_sd": statistics.stdev(values),
            "min": min(values), "max": max(values)}


def toy_parameter_counts(width, ffn_width, vocab=4):
    """Declared bias-free one-layer toy formulas, not whole production architectures."""
    if any(type(n) is not int or n < 1 for n in (width, ffn_width, vocab)):
        raise ValueError("positive integer dimensions required")
    return {"recurrent": 2 * vocab * width + width * width,
            "attention_ffn": 2 * vocab * width + 4 * width * width + 2 * width * ffn_width}


def sample_records():
    return [
        {"id": "a1", "sequence": "AACG", "group": "locus-a"},
        {"id": "a2", "sequence": "CGTT", "group": "locus-b"},
        {"id": "b1", "sequence": "ACGA", "group": "locus-b"},
        {"id": "c1", "sequence": "CCCC", "group": "locus-c"},
        {"id": "c2", "sequence": "GGGG", "group": "locus-c"},
        {"id": "d1", "sequence": "ATAT", "group": "locus-d"},
        {"id": "e1", "sequence": "AGAG", "group": "locus-e"},
        {"id": "f1", "sequence": "ACAC", "group": "locus-f"},
    ]


def results():
    runs = []
    for seed in (11, 29, 47):
        generator = torch.Generator(device="cpu").manual_seed(seed)
        full = torch.randint(4, (8, 33), generator=generator)
        inputs, targets = full[:, :-1], full[:, 1:]
        runs.append({"seed": seed,
                     "uniform": token_metrics(torch.zeros(8, 32, 4, dtype=torch.float64), targets),
                     "causal": token_metrics(PrefixCounts()(inputs), targets),
                     "leaky": token_metrics(FutureCopy()(inputs)[:, :-1], targets[:, :-1])})
    fixed = torch.tensor([[0, 1, 2, 3, 0, 1, 2, 3]])
    spec = ROOT / "research/EVO-EXP01-ch02-spec.json"
    return {"experiment_id": "EVO-EXP01-CH02-SMOKE", "spec_sha256": hashlib.sha256(spec.read_bytes()).hexdigest(),
            "scope": "CPU reference evaluation only; parent training experiment remains NOT RUN.",
            "torch_version": torch.__version__, "splits": split_records(sample_records()),
            "runs": runs, "causal_intervention": intervention_suite(PrefixCounts(), fixed),
            "leaky_intervention": intervention_suite(FutureCopy(), fixed),
            "illustrative_seed_summary_not_training": seed_summary([0.51, 0.97, 0.99]),
            "delay_example": {"input": [0, 1, 2, 3, 0, 1], "lag": 2,
                              "scored_positions_zero_based": [2, 3, 4, 5],
                              "targets": delay_oracle([0, 1, 2, 3, 0, 1], 2)},
            "parameter_example": toy_parameter_counts(16, 32)}


if __name__ == "__main__":
    print(json.dumps(results(), indent=2))
