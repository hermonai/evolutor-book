"""Genomic evaluation contracts. Synthetic data; no fitted biological predictor."""
from dataclasses import dataclass
import math
import random


def dna(seq, allow_empty=False):
    if not isinstance(seq, str):
        raise ValueError("DNA string required")
    seq = seq.upper()
    if (not seq and not allow_empty) or set(seq) - set("ACGTN"):
        raise ValueError("nonempty ACGTN sequence required")
    return seq


def rc(seq):
    return dna(seq, True).translate(str.maketrans("ACGTN", "TGCAN"))[::-1]


def gc(seq):
    seq = dna(seq)
    called = [b for b in seq if b != "N"]
    return None if not called else sum(b in "GC" for b in called) / len(called)


def onehot(seq):
    seq = dna(seq)
    return [[int(b == a) for a in "ACGT"] for b in seq], [b != "N" for b in seq]


@dataclass(frozen=True)
class Example:
    eid: str
    assembly: str
    contig: str
    start: int
    end: int
    homology: str
    seq: str
    label: int


def components(examples):
    """Close overlap and declared homology links transitively; half-open intervals."""
    ex = tuple(examples)
    if len({x.eid for x in ex}) != len(ex):
        raise ValueError("duplicate example id")
    for x in ex:
        if (type(x.start) is not int or type(x.end) is not int
                or x.start < 0 or x.end <= x.start or x.end-x.start != len(dna(x.seq))
                or type(x.label) is not int or x.label not in (0, 1)
                or not all((x.eid, x.assembly, x.contig))):
            raise ValueError("invalid genomic record")
    parent = list(range(len(ex)))

    def find(i):
        while parent[i] != i:
            i = parent[i]
        return i

    for i, a in enumerate(ex):
        for j, b in enumerate(ex[:i]):
            overlap = (a.assembly == b.assembly and a.contig == b.contig
                       and max(a.start, b.start) < min(a.end, b.end))
            homolog = bool(a.homology and a.homology == b.homology)
            if overlap or homolog:
                parent[find(i)] = find(j)
    groups = {}
    for i, x in enumerate(ex):
        groups.setdefault(find(i), []).append(x.eid)
    return tuple(sorted(tuple(sorted(v)) for v in groups.values()))


def group_split(examples, test_ids):
    """Selecting one ID holds out its entire connected component."""
    ex = tuple(examples)
    ids = set(test_ids)
    if ids - {x.eid for x in ex}:
        raise ValueError("unknown holdout id")
    held = {i for g in components(ex) if ids.intersection(g) for i in g}
    return tuple(x for x in ex if x.eid not in held), tuple(x for x in ex if x.eid in held)


def motif_score(seq, motif="ACG"):
    seq, motif = dna(seq), dna(motif)
    return sum(seq[i:i+len(motif)] == motif for i in range(len(seq)-len(motif)+1))


def invariant_score(seq):
    return (motif_score(seq) + motif_score(rc(seq))) / 2


def paired(y, p, probabilities=False):
    y, p = tuple(y), tuple(p)
    if not y or len(y) != len(p) or any(type(a) is not int or a not in (0, 1) for a in y):
        raise ValueError("aligned nonempty binary labels")
    if any(not isinstance(v, (int, float)) or not math.isfinite(v) or not 0 <= v <= 1 for v in p):
        raise ValueError("finite probabilities in [0,1]")
    if not probabilities and any(v not in (0, 1) for v in p):
        raise ValueError("binary predictions required")
    return y, p


def confusion(y, p):
    y, p = paired(y, p)
    return tuple(sum(a == u and b == v for a, b in zip(y, p))
                 for u, v in ((1, 1), (0, 0), (0, 1), (1, 0)))


def accuracy(y, p):
    y, p = paired(y, p)
    return sum(a == b for a, b in zip(y, p)) / len(y)


def mcc(y, p):
    tp, tn, fp, fn = confusion(y, p)
    den = math.sqrt((tp+fp)*(tp+fn)*(tn+fp)*(tn+fn))
    return None if den == 0 else (tp*tn-fp*fn)/den


def brier(y, prob):
    y, prob = paired(y, prob, True)
    return sum((a-b)**2 for a, b in zip(y, prob))/len(y)


def average_precision(y, score):
    """Threshold-group AP: all equal scores enter together; no tie-order bonus."""
    y, score = paired(y, score, True)
    positives = sum(y)
    if not positives:
        return None
    tp = seen = 0
    ap = 0.0
    for threshold in sorted(set(score), reverse=True):
        indices = [i for i, s in enumerate(score) if s == threshold]
        new = sum(y[i] for i in indices)
        tp += new
        seen += len(indices)
        ap += (new/positives)*(tp/seen)
    return ap


def cluster_interval(y, p, groups, draws=1000, seed=7):
    """Percentile interval for fixed-predictor row accuracy under cluster resampling."""
    y, p = paired(y, p)
    groups = tuple(groups)
    if len(groups) != len(y) or type(draws) is not int or draws < 20:
        raise ValueError("aligned groups and at least 20 draws")
    units = sorted(set(groups))
    if len(units) < 2:
        raise ValueError("at least two independent units required")
    rows = {g: [i for i, h in enumerate(groups) if h == g] for g in units}
    rng = random.Random(seed)
    values = []
    for _ in range(draws):
        idx = [i for _ in units for i in rows[rng.choice(units)]]
        values.append(sum(y[i] == p[i] for i in idx)/len(idx))
    values.sort()
    return values[int(.025*(draws-1))], values[int(.975*(draws-1))]


def snv(seq, pos, ref, alt):
    seq, ref, alt = dna(seq), dna(ref), dna(alt)
    if (type(pos) is not int or not 0 <= pos < len(seq) or len(ref) != 1
            or len(alt) != 1 or ref == alt or "N" in ref+alt or seq[pos] != ref):
        raise ValueError("normalized matching single nucleotide substitution")
    return seq[:pos]+alt+seq[pos+1:]


def results():
    y, p = [1, 1, 0, 0], [1, 0, 1, 0]
    seq = "AACGTT"
    return {"metrics": [
        {"metric": "Accuracy", "value": accuracy(y, p)},
        {"metric": "MCC", "value": mcc(y, p)},
        {"metric": "Brier", "value": brier(y, [.8, .4, .6, .1])},
        {"metric": "AP", "value": average_precision(y, [.8, .4, .6, .1])}],
        "rc": rc("AACGTN"), "score": invariant_score(seq),
        "delta": invariant_score(snv(seq, 2, "C", "A"))-invariant_score(seq),
        "cluster_interval": cluster_interval(y, p, ["a", "a", "b", "b"], 200)}


TABLES = [("metrics", ["Synthetic statistic", "Value"], ["metric", "value"], "lr")]
PLOTS = []
LISTINGS = ["group_split", "average_precision", "cluster_interval", "snv"]
