"""EVOD-25: frozen comparison inputs, split closure and uncertainty.

The predictor demo is a train-selected GC threshold versus a known motif oracle,
not a DOGMA/Hermon benchmark. Native-model probes test execution contracts only.
"""

from collections import defaultdict
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import random
import statistics
import sys

DNA = "ACGT"
COMP = str.maketrans(DNA, "TGCA")


def positive(n, name):
    if isinstance(n, bool) or not isinstance(n, int) or n < 1:
        raise ValueError(name + " must be a positive integer")
    return n


def canonical(sequence):
    if (
        not isinstance(sequence, str)
        or not sequence
        or any(c not in DNA for c in sequence)
    ):
        raise ValueError("Nonempty canonical ACGT sequence required")
    return sequence


def rc(sequence):
    return canonical(sequence).translate(COMP)[::-1]


def motif_oracle(sequence):
    canonical(sequence)
    return int("ACGT" in sequence)  # ACGT is its own reverse complement


def dataset(n=400, length=32, seed=25):
    positive(n, "record count")
    if isinstance(length, bool) or not isinstance(length, int) or length < 4:
        raise ValueError("Motif task requires length >= 4")
    rng = random.Random(seed)
    records = []
    for i in range(n):
        target = i % 2
        for _ in range(100000):
            sequence = "".join(rng.choice(DNA) for _ in range(length))
            if target:
                j = rng.randrange(length - 3)
                sequence = sequence[:j] + "ACGT" + sequence[j + 4 :]
            if motif_oracle(sequence) == target:
                records.append(
                    {
                        "id": f"record-{i:04d}",
                        "sequence": sequence,
                        "label": target,
                        "groups": [],
                    }
                )
                break
        else:
            raise RuntimeError("Bounded rejection sampler exhausted")
    return records


def closure(records, relations=()):
    """Transitive exact/RC, declared-group and explicit-relation components.

    Relations/group tags are supplied biological curation, not inferred homology.
    Each tuple in relations joins record IDs. A group tag is globally namespaced.
    """
    ids = [record["id"] for record in records]
    if len(ids) != len(set(ids)) or not all(isinstance(i, str) and i for i in ids):
        raise ValueError("Unique nonempty string record IDs required")
    parent = {i: i for i in ids}

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    def union(a, b):
        if a not in parent or b not in parent:
            raise ValueError("Relation mentions an unknown record")
        a, b = find(a), find(b)
        if a != b:
            parent[max(a, b)] = min(a, b)

    seen = {}
    for record in records:
        sequence = canonical(record["sequence"])
        if type(record["label"]) is not int or record["label"] not in (0, 1):
            raise ValueError("Binary integer labels required")
        groups = record["groups"]
        if not isinstance(groups, list) or not all(
            isinstance(g, str) and g for g in groups
        ):
            raise ValueError("Group tags must be nonempty strings")
        keys = [("strand", min(sequence, rc(sequence)))]
        keys += [("group", group) for group in groups]
        for key in keys:
            if key in seen:
                union(record["id"], seen[key])
            else:
                seen[key] = record["id"]
    for a, b in relations:
        union(a, b)
    components = defaultdict(list)
    for i in ids:
        components[find(i)].append(i)
    return tuple(sorted(tuple(sorted(v)) for v in components.values()))


def assign_splits(records, relations=(), seed=25, fractions=(0.6, 0.2, 0.2)):
    if (
        len(fractions) != 3
        or any(
            isinstance(f, bool)
            or not isinstance(f, (float, int))
            or not math.isfinite(f)
            or f <= 0
            for f in fractions
        )
        or not math.isclose(sum(fractions), 1, abs_tol=1e-12)
    ):
        raise ValueError("Three positive split fractions summing to one required")
    components = list(closure(records, relations))
    if len(components) < 3:
        raise ValueError("At least three independent components required")
    random.Random(seed).shuffle(components)
    n_train = int(len(components) * fractions[0])
    n_val = int(len(components) * fractions[1])
    if min(n_train, n_val, len(components) - n_train - n_val) < 1:
        raise ValueError("Requested split leaves an empty partition")
    assignment = {}
    for i, component in enumerate(components):
        split = (
            "train" if i < n_train else "validation" if i < n_train + n_val else "test"
        )
        for record_id in component:
            assignment[record_id] = split
    audit_splits(records, assignment, relations)
    return assignment


def audit_splits(records, assignment, relations=()):
    ids = {record["id"] for record in records}
    if set(assignment) != ids or any(
        v not in ("train", "validation", "test") for v in assignment.values()
    ):
        raise ValueError("Every record needs exactly one declared partition")
    for component in closure(records, relations):
        if len({assignment[i] for i in component}) != 1:
            raise ValueError("Dependency component crosses a split boundary")
    return True


def experiment_hash(records, assignment, objective, relations=()):
    relations = list(relations)
    audit_splits(records, assignment, relations)
    # Explicit caller-owned objective; hash binds it, not its scientific validity.
    payload = {
        "records": sorted(records, key=lambda x: x["id"]),
        "assignment": assignment,
        "objective": objective,
        "relations": sorted(tuple(sorted(pair)) for pair in relations),
    }
    encoded = json.dumps(
        payload, sort_keys=True, separators=(",", ":"), allow_nan=False
    )
    return hashlib.sha256(encoded.encode()).hexdigest()


def composition(sequence):
    canonical(sequence)
    return sum(c in "GC" for c in sequence) / len(sequence)


def fit_threshold(train):
    if not train:
        raise ValueError("Training records required")
    scores = sorted({composition(record["sequence"]) for record in train})
    # Include all-positive and all-negative rules, including score exactly one.
    candidates = [-1.0, *((a + b) / 2 for a, b in zip(scores, scores[1:])), 2.0]
    return max(
        candidates,
        key=lambda t: sum(
            int(composition(r["sequence"]) >= t) == r["label"] for r in train
        ),
    )  # first candidate resolves ties deterministically


def binary_metrics(labels, predictions):
    if not labels or len(labels) != len(predictions):
        raise ValueError("Nonempty aligned labels and predictions required")
    if any(type(v) is not int or v not in (0, 1) for v in [*labels, *predictions]):
        raise ValueError("Binary integer vectors required")
    counts = {name: 0 for name in ("tp", "tn", "fp", "fn")}
    for y, p in zip(labels, predictions):
        counts[("tn", "fp", "fn", "tp")[2 * y + p]] += 1
    positives = counts["tp"] + counts["fn"]
    negatives = counts["tn"] + counts["fp"]
    balanced = (
        None
        if min(positives, negatives) == 0
        else 0.5 * (counts["tp"] / positives + counts["tn"] / negatives)
    )
    return {
        **counts,
        "accuracy": (counts["tp"] + counts["tn"]) / len(labels),
        "balanced_accuracy": balanced,
    }


def deltas(labels, a, b):
    binary_metrics(labels, a)
    binary_metrics(labels, b)
    return [int(p == y) - int(q == y) for y, p, q in zip(labels, a, b)]


def exact_paired_variance(difference):
    """Conditional iid-record variance estimate of the mean, not seed variance."""
    if len(difference) < 2 or any(v not in (-1, 0, 1) for v in difference):
        raise ValueError("At least two paired correctness differences required")
    return statistics.variance(difference) / len(difference)


def quantile(sorted_values, probability):
    x = (len(sorted_values) - 1) * probability
    lo = math.floor(x)
    hi = math.ceil(x)
    return (
        sorted_values[lo] * (hi - x) + sorted_values[hi] * (x - lo)
        if lo != hi
        else sorted_values[lo]
    )


def paired_bootstrap(labels, a, b, clusters=None, repetitions=2000, seed=25):
    """Uniform cluster resampling; keep A/B pairing and all rows within a draw.

    Target is record-weighted accuracy difference. Unequal cluster sizes produce
    a ratio of resampled totals, not an equal-weight mean of cluster means.
    The percentile interval is descriptive/approximate, not guaranteed coverage.
    """
    positive(repetitions, "bootstrap repetitions")
    difference = deltas(labels, a, b)
    clusters = list(range(len(labels))) if clusters is None else list(clusters)
    if len(clusters) != len(labels):
        raise ValueError("One cluster ID per evaluation record required")
    groups = defaultdict(list)
    for d, group in zip(difference, clusters):
        groups[group].append(d)
    groups = list(groups.values())
    if len(groups) < 2:
        raise ValueError("At least two independent resampling units required")
    rng = random.Random(seed)
    draws = []
    for _ in range(repetitions):
        sample = [groups[rng.randrange(len(groups))] for _ in groups]
        draws.append(sum(map(sum, sample)) / sum(map(len, sample)))
    draws.sort()
    return {
        "observed_delta": statistics.mean(difference),
        "bootstrap_mean": statistics.mean(draws),
        "lo95": quantile(draws, 0.025),
        "hi95": quantile(draws, 0.975),
        "units": len(groups),
        "records": len(labels),
        "repetitions": repetitions,
    }


def load_prior(chapter):
    path = Path(__file__).parents[1] / f"ch{chapter:02d}/reference.py"
    spec = importlib.util.spec_from_file_location(f"evod25_prior{chapter}", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def native_probe():
    """No training or accuracy comparison: exercise actual native model contracts."""
    import torch

    torch.set_num_threads(1)
    dogma_module, hermon_module = load_prior(22), load_prior(23)
    torch.manual_seed(25)
    dogma = dogma_module.DOGMA(d=8, k=3, classes=4).double().eval()
    hermon = hermon_module.HermonDNA(d=8, h=2, layers=1, max_len=32).double().eval()
    x = torch.tensor([[0, 1, 2, 3, 0, 2, 1, 3]], dtype=torch.long)
    with torch.no_grad():
        full, state, _ = dogma.run(x)
        first, carry, _ = dogma.run(x[:, :3])
        second, end, _ = dogma.run(x[:, 3:], carry)
        dogma_error = float((full - torch.cat([first, second], 1)).abs().max())
        carry_error = max(float((a - b).abs().max()) for a, b in zip(state, end))
        causal = hermon.causal_logits(x)
        # Repeated-prefix oracle, deliberately NOT a KV-cache implementation.
        prefix = torch.stack(
            [hermon.causal_logits(x[:, : i + 1])[:, -1] for i in range(x.shape[1])], 1
        )
        hermon_error = float((causal - prefix).abs().max())
    return {
        "dogma_chunk_feature_error": dogma_error,
        "dogma_terminal_state_error": carry_error,
        "hermon_repeated_prefix_error": hermon_error,
        "budgets": [
            {
                "model": "DOGMA reference",
                "parameters": sum(p.numel() for p in dogma.parameters()),
                "parameter_bytes": sum(
                    p.numel() * p.element_size() for p in dogma.parameters()
                ),
                "native_state_bytes": sum(s.numel() * s.element_size() for s in state),
                "per_layer_causal_edges": 0,
            },
            {
                "model": "Hermon reference",
                "parameters": sum(p.numel() for p in hermon.parameters()),
                "parameter_bytes": sum(
                    p.numel() * p.element_size() for p in hermon.parameters()
                ),
                "native_state_bytes": 0,
                "per_layer_causal_edges": 2 * x.shape[1] * (x.shape[1] + 1) // 2,
            },
        ],
        "dtype": "float64",
        "batch": 1,
        "bases": 8,
        "budget_scope": "static inventories/semantic edges, no measured peak/latency/FLOPs",
        "hermon_state_note": "stateless repeated-prefix call, not a production KV inventory",
    }


def results():
    records = dataset()
    assignment = assign_splits(records)
    train = [r for r in records if assignment[r["id"]] == "train"]
    test = [r for r in records if assignment[r["id"]] == "test"]
    threshold = fit_threshold(train)
    labels = [r["label"] for r in test]
    a = [motif_oracle(r["sequence"]) for r in test]
    b = [int(composition(r["sequence"]) >= threshold) for r in test]
    experiment = {
        "train": len(train),
        "validation": sum(v == "validation" for v in assignment.values()),
        "test": len(test),
        "threshold": threshold,
        "oracle": binary_metrics(labels, a),
        "gc_baseline": binary_metrics(labels, b),
        "paired": paired_bootstrap(labels, a, b),
        "envelope_hash": experiment_hash(
            records, assignment, "offline ACGT motif classification"
        ),
    }
    labels2 = [1] * 32
    a2, b2 = [1] * 16 + [0] * 16, [0] * 16 + [1] * 16
    counterexample = {
        "iid_rows": paired_bootstrap(labels2, a2, b2, seed=25),
        "four_clusters": paired_bootstrap(
            labels2, a2, b2, [i // 8 for i in range(32)], seed=25
        ),
        "assumption": "assigned within-cluster dependence, four independent clusters",
    }
    native = native_probe()
    return {
        "kind": "synthetic harness outputs and untrained native execution checks",
        "experiment": experiment,
        "counterexample": counterexample,
        "native": native,
        "budgets": native["budgets"],
        "intervals": [
            {**counterexample["iid_rows"], "units": "32 iid rows"},
            {**counterexample["four_clusters"], "units": "4 clusters"},
        ],
    }


TABLES = [
    (
        "budgets",
        ["Reference", "Parameters", "Param. bytes", "State bytes", "Causal edges"],
        [
            "model",
            "parameters",
            "parameter_bytes",
            "native_state_bytes",
            "per_layer_causal_edges",
        ],
        "lrrrr",
    ),
    (
        "intervals",
        ["Resampling", "Delta", "2.5 percentile", "97.5 percentile"],
        ["units", "observed_delta", "lo95", "hi95"],
        "lrrr",
    ),
]
PLOTS = []
LISTINGS = [
    "closure",
    "audit_splits",
    "fit_threshold",
    "paired_bootstrap",
    "native_probe",
]

if __name__ == "__main__":
    print(json.dumps(results(), indent=2))
