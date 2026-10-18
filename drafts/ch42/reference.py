"""Legal-alternative selection and a committed-redo-only WAL crash model.

No undo, torn pages, actual fsync, concurrent transactions or ARIES claim.
Each appended assignment is an independently committed unit once flushed.
"""
from dataclasses import dataclass
import copy
import math


@dataclass(frozen=True)
class Plan:
    name: str
    contract: str
    latency_ms: float
    memory_mib: float
    risk: float


def cost(plan, weights=(1., .1, 10.)):
    numbers = (plan.latency_ms, plan.memory_mib, plan.risk, *weights)
    if (len(weights) != 3 or any(type(x) not in (int, float) or
            not math.isfinite(x) or x < 0 for x in numbers) or plan.risk > 1):
        raise ValueError("finite nonnegative costs/weights, risk in [0,1]")
    return sum(a * b for a, b in zip(numbers[:3], weights))


def choose(plans, contract, memory_limit, risk_limit, weights=(1., .1, 10.)):
    if (type(memory_limit) not in (int, float) or not math.isfinite(memory_limit)
            or memory_limit < 0 or type(risk_limit) not in (int, float) or
            not math.isfinite(risk_limit) or not 0 <= risk_limit <= 1):
        raise ValueError("finite resource/risk constraints")
    if len({p.name for p in plans}) != len(plans):
        raise ValueError("unique alternative names")
    for p in plans:
        cost(p, weights)
    eligible = [p for p in plans if p.contract == contract and
                p.memory_mib <= memory_limit and p.risk <= risk_limit]
    if not eligible:
        raise RuntimeError("no legal physical alternative")
    return min(eligible, key=lambda p: (cost(p, weights), p.name))


class WalStore:
    def __init__(self):
        self.log, self.durable_lsn, self.data, self.page_lsn = [], 0, {}, {}

    def append(self, key, value):
        if type(key) is not str or not key or type(value) not in (str, int):
            raise ValueError("named scalar assignment")
        self.log.append((len(self.log) + 1, key, value))
        return len(self.log)

    def flush_log(self, lsn):
        if type(lsn) is not int or not self.durable_lsn <= lsn <= len(self.log):
            raise ValueError("flush only existing contiguous log prefix")
        self.durable_lsn = lsn

    def write_page(self, key, value, lsn):
        if type(key) is not str or type(value) not in (str, int):
            raise ValueError("page assignment must retain scalar type")
        if type(lsn) is not int or not 1 <= lsn <= self.durable_lsn:
            raise RuntimeError("WAL: assignment is not durable")
        if self.log[lsn - 1] != (lsn, key, value):
            raise ValueError("page content must match its log record")
        if lsn < self.page_lsn.get(key, 0):
            raise RuntimeError("stale page write")
        self.data[key], self.page_lsn[key] = value, lsn

    def crash(self):
        image = WalStore()
        image.log = copy.deepcopy(self.log[:self.durable_lsn])
        image.durable_lsn = self.durable_lsn
        image.data, image.page_lsn = copy.deepcopy(self.data), dict(self.page_lsn)
        return image

    def recover(self):
        for lsn, key, value in self.log[:self.durable_lsn]:
            if self.page_lsn.get(key, 0) < lsn:
                self.write_page(key, value, lsn)


def replay_prefix(log, durable):
    """Independent last-assignment specification; does not use page LSN logic."""
    result = {}
    for _, key, value in log[:durable]:
        result[key] = value
    return result


def crash_cuts():
    s, rows = WalStore(), []
    operations = [lambda: s.append("active", "v1"), lambda: s.flush_log(1),
                  lambda: s.write_page("active", "v1", 1),
                  lambda: s.append("active", "v2"), lambda: s.flush_log(2),
                  lambda: s.write_page("active", "v2", 2)]
    for cut in range(7):
        c = s.crash()
        c.recover()
        assert c.data == replay_prefix(s.log, s.durable_lsn)
        rows.append({"cut": cut, "durable": s.durable_lsn,
                     "page": s.page_lsn.get("active", 0),
                     "recovered": c.data.get("active", "absent")})
        if cut < len(operations):
            operations[cut]()
    return rows


def results():
    plans = [Plan("native-A", "native-v1", 5., 4., .03),
             Plan("native-B", "native-v1", 4., 8., .02),
             Plan("wrong-contract", "attention-v1", .1, .1, 0.)]
    return {"crashes": crash_cuts(), "alternatives": [
        {"name": p.name, "cost": cost(p), "legal": int(p.contract == "native-v1")}
        for p in plans], "chosen": choose(plans, "native-v1", 16, .1).name}


TABLES = [("crashes", ["Cut", "Durable LSN", "Page LSN", "Recovered"],
           ["cut", "durable", "page", "recovered"], "rrrl"),
          ("alternatives", ["Alternative", "Weighted cost", "Contract legal"],
           ["name", "cost", "legal"], "lrr")]
PLOTS = []
LISTINGS = ["choose", "WalStore.write_page", "WalStore.recover", "replay_prefix"]
