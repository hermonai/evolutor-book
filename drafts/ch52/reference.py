"""Failure-aware research ledger and content closure; no scientific acceptance."""
from dataclasses import dataclass, asdict, replace
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]


def capability_module():
    name = "evod52_capability_contract"
    if name not in sys.modules:
        s = importlib.util.spec_from_file_location(name, ROOT / "drafts/ch51/reference.py")
        m = importlib.util.module_from_spec(s); sys.modules[name] = m; s.loader.exec_module(m)
    return sys.modules[name]


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


@dataclass(frozen=True)
class Claim:
    cid: str
    text: str
    level: str
    falsifier: str
    scope: str
    implementation_digest: str = ""
    tests_digest: str = ""
    evidence: tuple = ()


@dataclass(frozen=True)
class Experiment:
    eid: str
    claim_id: str
    baseline: str
    budget: str
    metric: str
    threshold: float
    seeds: tuple
    artifact_digest: str
    data_digest: str
    suite: str
    unit: str
    outcome: str = "planned"
    lower_bound: float | None = None
    evaluator: str = ""
    independent: bool = False
    held_out: bool = False


@dataclass(frozen=True)
class Failure:
    fid: str
    claim_id: str
    experiment_id: str
    category: str
    symptom: str
    counterexample: str
    resolved_by: str = ""


class Ledger:
    def __init__(self):
        self.claims, self.experiments, self.failures = {}, {}, {}

    def evidence_records(self):
        m = capability_module()
        return tuple(m.Evidence(e.eid, e.claim_id, e.suite, e.artifact_digest,
                                e.data_digest, e.baseline, e.budget, e.unit,
                                e.lower_bound if e.lower_bound is not None else float("-inf"),
                                e.threshold, e.held_out, e.outcome, e.evaluator, e.independent)
                     for e in self.experiments.values())

    def _capability(self, c):
        m = capability_module()
        return m.Claim(c.cid, c.level, c.scope, c.falsifier,
                       c.implementation_digest, c.tests_digest, c.evidence)

    def add_claim(self, c):
        if (not isinstance(c, Claim) or not c.cid or not c.text or c.cid in self.claims
                or c.level in ("benchmark-demonstrated", "replicated")
                or not capability_module().valid(self._capability(c))):
            raise ValueError("new claim must have valid non-empirical starting evidence")
        self.claims[c.cid] = c

    def add_experiment(self, e):
        import math
        m = capability_module()
        if (not isinstance(e, Experiment) or not e.eid or e.eid in self.experiments
                or e.claim_id not in self.claims or not all((e.baseline, e.budget, e.metric, e.suite, e.unit))
                or not isinstance(e.seeds, tuple) or not e.seeds
                or any(type(v) is not int for v in e.seeds) or len(set(e.seeds)) != len(e.seeds)
                or not m.sha(e.artifact_digest) or not m.sha(e.data_digest)
                or not math.isfinite(e.threshold) or type(e.independent) is not bool
                or type(e.held_out) is not bool
                or e.outcome not in ("planned", "success", "failure")
                or (e.outcome == "planned" and e.lower_bound is not None)
                or (e.outcome != "planned" and
                    (not e.evaluator or e.lower_bound is None or not math.isfinite(e.lower_bound)))):
            raise ValueError("complete plan or observed experiment required")
        self.experiments[e.eid] = e

    def add_failure(self, f):
        if (not isinstance(f, Failure) or not f.fid or f.fid in self.failures
                or f.claim_id not in self.claims or f.experiment_id not in self.experiments
                or self.experiments[f.experiment_id].claim_id != f.claim_id
                or not all((f.category, f.symptom, f.counterexample)) or f.resolved_by):
            raise ValueError("failure must link the same claim and experiment")
        self.failures[f.fid] = f

    def resolve(self, fid, eid):
        f, e = self.failures[fid], self.experiments[eid]
        if (f.resolved_by or e.claim_id != f.claim_id or eid == f.experiment_id
                or not capability_module().supports(
                    next(x for x in self.evidence_records() if x.eid == eid), f.claim_id)):
            raise ValueError("distinct supporting resolution experiment required")
        self.failures[fid] = replace(f, resolved_by=eid)

    def promote(self, cid, new_level, evidence_ids=()):
        c = self.claims[cid]
        if new_level in ("benchmark-demonstrated", "replicated") and any(
                f.claim_id == cid and not f.resolved_by for f in self.failures.values()):
            raise ValueError("unresolved counterexample blocks empirical promotion")
        updated = capability_module().promote(self._capability(c), new_level,
                    self.evidence_records(), evidence=evidence_ids or c.evidence)
        self.claims[cid] = replace(c, level=updated.level, evidence=updated.evidence)

    def capsule(self):
        obj = {"schema": "evod52-ledger-v1",
               "claims": [asdict(x) for x in sorted(self.claims.values(), key=lambda x: x.cid)],
               "experiments": [asdict(x) for x in sorted(self.experiments.values(), key=lambda x: x.eid)],
               "failures": [asdict(x) for x in sorted(self.failures.values(), key=lambda x: x.fid)]}
        return {"ledger": obj, "sha256": digest(obj)}


def safe_path(root, name):
    root, rel = Path(root).resolve(), Path(name)
    if rel.is_absolute() or ".." in rel.parts or str(rel) != name or not name:
        raise ValueError("canonical relative file path")
    path = root / rel
    if any(p.is_symlink() for p in [path, *list(path.parents)[:len(rel.parts)-1]]):
        raise ValueError("symlink excluded from capsule")
    path.resolve().relative_to(root)
    return path


def file_manifest(root, names):
    names = tuple(names)
    if len(set(names)) != len(names):
        raise ValueError("duplicate closure path")
    files = {}
    for name in sorted(names):
        path = safe_path(root, name)
        if not path.is_file():
            raise ValueError("regular file required")
        files[name] = hashlib.sha256(path.read_bytes()).hexdigest()
    return {"files": files, "sha256": digest(files)}


def verify_files(root, manifest):
    if (set(manifest) != {"files", "sha256"} or not isinstance(manifest["files"], dict)
            or digest(manifest["files"]) != manifest["sha256"]):
        raise ValueError("manifest envelope mismatch")
    missing, changed = [], []
    for name, expected in manifest["files"].items():
        path = safe_path(root, name)
        if not capability_module().sha(expected):
            raise ValueError("file digest syntax")
        if not path.is_file():
            missing.append(name)
        elif hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            changed.append(name)
    return {"missing": sorted(missing), "changed": sorted(changed)}


def dependency_order(files, edges):
    """Validate a declared acyclic dependency closure; infer no hidden imports."""
    files = set(files)
    if set(edges) != files or any(set(v)-files for v in edges.values()):
        raise ValueError("every artifact and dependency must be in the closure")
    done, active, order = set(), set(), []

    def visit(node):
        if node in active:
            raise ValueError("cyclic declared dependency")
        if node in done:
            return
        active.add(node)
        for dep in sorted(edges[node]):
            visit(dep)
        active.remove(node); done.add(node); order.append(node)

    for node in sorted(files):
        visit(node)
    return tuple(order)


def expected_uniform_ce(prob):
    """Expected nats for an independent uniform target, not a sample lower bound."""
    import math
    p = tuple(prob)
    if (len(p) < 2 or any(not math.isfinite(v) or v <= 0 for v in p)
            or not math.isclose(sum(p), 1., abs_tol=1e-12, rel_tol=0)):
        raise ValueError("positive normalized probability vector")
    return -sum(math.log(v) for v in p)/len(p)


def results():
    L = Ledger()
    L.add_claim(Claim("C1", "candidate beats baseline under declared budget", "hypothesized",
                      "lower confidence bound fails threshold", "synthetic protocol illustration only"))
    L.add_experiment(Experiment("E1", "C1", "assigned baseline", "2 synthetic cases", "quality difference",
                                0., (1,), "a"*64, "d"*64, "toy-v1", "synthetic case",
                                "failure", -.1, "author fixture"))
    L.add_failure(Failure("F1", "C1", "E1", "baseline-regression", "assigned candidate loses",
                         "case 1: baseline quality .8; candidate quality .7"))
    names = ["drafts/ch23/reference.py", "drafts/ch31/reference.py", "drafts/ch35/reference.py"]
    names += [f"drafts/ch{ch}/reference.py" for ch in range(48,53)]
    manifest = file_manifest(ROOT, names)
    return {"ledger_counts": [{"kind": "Claims", "count": len(L.claims)},
                              {"kind": "Experiments", "count": len(L.experiments)},
                              {"kind": "Preserved failures", "count": len(L.failures)}],
            "claim_level": L.claims["C1"].level, "capsule_sha256": L.capsule()["sha256"],
            "reference_closure": manifest,
            "reference_verification": verify_files(ROOT, manifest),
            "uniform_ce": expected_uniform_ce([.25]*4),
            "biased_ce": expected_uniform_ce([.7,.1,.1,.1])}


TABLES = [("ledger_counts", ["Synthetic ledger record", "Count"], ["kind", "count"], "lr")]
PLOTS = []
LISTINGS = ["Ledger.add_failure", "Ledger.promote", "Ledger.capsule", "verify_files", "dependency_order"]
