"""Synthetic trace analysis and cost bounds; no hardware benchmark performed."""
from dataclasses import dataclass
import math
import statistics


def finite(value, positive=False):
    if (type(value) not in (int, float) or not math.isfinite(value)
            or (value <= 0 if positive else value < 0)):
        raise ValueError("finite nonnegative/positive scalar")
    return float(value)


def percentile(xs, q):
    if not xs or type(q) not in (int, float) or not math.isfinite(q) or not 0 < q <= 1:
        raise ValueError("nonempty finite samples and 0 < q <= 1")
    return sorted(finite(x) for x in xs)[math.ceil(q * len(xs)) - 1]


def arithmetic_intensity(flops, bytes_moved):
    return finite(flops) / finite(bytes_moved, True)


def roofline_bound(flops, bytes_moved, peak_flops, bandwidth):
    return min(finite(peak_flops, True),
               finite(bandwidth, True) * arithmetic_intensity(flops, bytes_moved))


def classify(ai, peak_flops, bandwidth):
    ridge = finite(peak_flops, True) / finite(bandwidth, True)
    return "memory-region" if finite(ai) < ridge else "compute-region"


@dataclass(frozen=True)
class Request:
    arrival_ms: float
    first_token_ms: object
    token_times_ms: tuple = ()
    ok: bool = True
    terminal_ms: object = None

    def validate(self):
        finite(self.arrival_ms)
        if type(self.ok) is not bool or type(self.token_times_ms) is not tuple:
            raise ValueError("boolean outcome and immutable timestamps")
        if self.first_token_ms is None:
            if self.ok or self.token_times_ms:
                raise ValueError("only failed requests can have zero tokens")
            if self.terminal_ms is None or finite(self.terminal_ms) < self.arrival_ms:
                raise ValueError("tokenless failure requires terminal timestamp")
            return
        times = (self.arrival_ms, self.first_token_ms) + self.token_times_ms
        for t in times:
            finite(t)
        if any(b < a for a, b in zip(times, times[1:])):
            raise ValueError("monotonic same-clock timestamps")
        if self.terminal_ms is not None and finite(self.terminal_ms) < times[-1]:
            raise ValueError("terminal time before last token")

    def completion_ms(self):
        self.validate()
        if self.terminal_ms is not None:
            return self.terminal_ms
        return self.token_times_ms[-1] if self.token_times_ms else self.first_token_ms

    def ttft(self):
        self.validate()
        return None if self.first_token_ms is None else self.first_token_ms - self.arrival_ms

    def itls(self):
        self.validate()
        ts = (() if self.first_token_ms is None else (self.first_token_ms,)) + self.token_times_ms
        return tuple(b - a for a, b in zip(ts, ts[1:]))


def metrics(reqs, start_ms, end_ms, ttft_slo, itl_slo):
    finite(start_ms)
    finite(end_ms)
    finite(ttft_slo)
    finite(itl_slo)
    if not reqs or end_ms <= start_ms:
        raise ValueError("nonempty completed cohort and positive window")
    for r in reqs:
        r.validate()
        if (r.arrival_ms < start_ms or r.arrival_ms >= end_ms
                or r.completion_ms() > end_ms):
            raise ValueError("cohort outside declared observation window")
    tt = [r.ttft() for r in reqs if r.ttft() is not None]
    itl = [x for r in reqs for x in r.itls()]
    good = sum(r.ok and r.ttft() is not None and r.ttft() <= ttft_slo
               and all(x <= itl_slo for x in r.itls()) for r in reqs)
    tokens = sum((0 if r.first_token_ms is None else 1) + len(r.token_times_ms)
                 for r in reqs)
    seconds = (end_ms - start_ms) / 1000
    return dict(requests=len(reqs), output_tokens=tokens,
                p50_ttft=percentile(tt, .5) if tt else None,
                p95_ttft=percentile(tt, .95) if tt else None,
                p95_itl=percentile(itl, .95) if itl else None,
                output_tokens_per_s=tokens / seconds,
                goodput_req_per_s=good / seconds, slo_attainment=good / len(reqs))


def speedup(base_ms, new_ms):
    return finite(base_ms, True) / finite(new_ms, True)


def amdahl(fraction, local_speedup):
    if finite(fraction) > 1:
        raise ValueError("fraction <= 1")
    return 1 / (1 - fraction + fraction / finite(local_speedup, True))


def critical_path(spans):
    """DAG durations in ms; span=(name,duration,predecessor_names)."""
    end = {}
    for label, duration, predecessors in spans:
        if label in end or any(p not in end for p in predecessors):
            raise ValueError("unique topologically ordered DAG")
        end[label] = finite(duration) + max((end[p] for p in predecessors), default=0)
    if not end:
        raise ValueError("nonempty DAG")
    return max(end.values())


def paired_ratio(base, new):
    if len(base) != len(new) or len(base) < 2:
        raise ValueError("at least two matched runs")
    ratios = [speedup(a, b) for a, b in zip(base, new)]
    return dict(n=len(ratios), mean=statistics.mean(ratios),
                stdev=statistics.stdev(ratios), minimum=min(ratios), maximum=max(ratios))


def attention_cost(layers, heads, width, tokens, nbytes):
    if any(type(x) is not int or x < 1 for x in (layers, heads, width, tokens, nbytes)):
        raise ValueError("positive integer geometry")
    # QK and AV, two FLOP per multiply/add; omit softmax and projections.
    return dict(flops=4 * layers * heads * width * tokens,
                bytes=2 * layers * heads * width * tokens * nbytes)


def native_cost(batch, width, vocab, nbytes, staged=False):
    if any(type(x) is not int or x < 1 for x in (batch, width, vocab, nbytes)):
        raise ValueError("positive integer geometry")
    return dict(flops=2 * batch * width * vocab + 4 * batch * width,
                bytes=batch * (3 * width + vocab) * nbytes +
                (4 * batch * width * nbytes if staged else 0))


def results():
    reqs = [Request(0, 40, (55, 70, 85)), Request(10, 70, (90, 110, 130)),
            Request(20, 150, (180, 210))]
    m = metrics(reqs, 0, 250, 100, 25)
    rows = []
    for label, c in [("Decode KV", attention_cost(24, 8, 128, 4096, 2)),
                     ("Native resident", native_cost(8, 64, 4, 8)),
                     ("Native staged", native_cost(8, 64, 4, 8, True))]:
        rows.append(dict(kind=label, flops=c["flops"], nbytes=c["bytes"],
                         ai=arithmetic_intensity(c["flops"], c["bytes"])))
    return dict(metrics=m, costs=rows, speedup=speedup(100, 80),
                amdahl=amdahl(.2, 2), evidence="synthetic trace and analytic payload only",
                real_backend_measurements=[])


TABLES = [("costs", ["Region", "Modeled ops", "Logical bytes", "Ops/byte"],
           ["kind", "flops", "nbytes", "ai"], "lrrr")]
PLOTS = []
LISTINGS = ["percentile", "Request.validate", "metrics", "critical_path",
            "roofline_bound", "paired_ratio"]
