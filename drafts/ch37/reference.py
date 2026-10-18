"""Iteration scheduling bound to Chapter 36; KV representation experiments.

Serial CPU execution with abstract ticks, conservative full-length reservation,
no fused ragged device kernel and no production fairness or concurrency claim.
"""
from dataclasses import dataclass, field
import math
import torch
from pathlib import Path
import importlib.util
import sys


def load_paging():
    name = "evod_batch_a_36"
    if name not in sys.modules:
        spec = importlib.util.spec_from_file_location(
            name, Path(__file__).parent.parent / "ch36/reference.py")
        m = importlib.util.module_from_spec(spec)
        sys.modules[name] = m
        spec.loader.exec_module(m)
    return sys.modules[name]


paging = load_paging()
native = paging.native


@dataclass
class Request:
    rid: str
    arrival: int
    prompt: tuple
    output: int
    phase: str = "waiting"
    prefilled: int = 0
    generated: list = field(default_factory=list)
    token_ticks: list = field(default_factory=list)
    handle: object = None
    reservation: int = 0


class Scheduler:
    def __init__(self, model, capacity, page_size, token_budget=4, chunk=2):
        self.pool = paging.PagedKV(model, capacity, page_size)
        self.budget, self.chunk = paging.positive(token_budget), paging.positive(chunk)
        self.requests, self.tick, self.trace = [], 0, []

    def owner(self, r):
        return ("teaching-tenant", r.rid)

    def submit(self, rid, arrival, prompt, output):
        native.owner_pair(("teaching-tenant", rid))
        if (type(arrival) is not int or arrival < self.tick
                or type(output) is not int or output < 1):
            raise ValueError("future/nonnegative arrival and positive output")
        prompt = native.tokens_copy(prompt, self.pool.model.max_len)
        if not prompt or len(prompt)+output-1 > self.pool.model.max_len:
            raise ValueError("nonempty prompt and bounded consumed length")
        if any(r.rid == rid for r in self.requests):
            raise ValueError("unique request identity")
        required = math.ceil((len(prompt)+output-1)/self.pool.page_size)
        if required > self.pool.capacity:
            raise MemoryError("request exceeds entire arena")
        r = Request(rid, arrival, prompt, output, reservation=required)
        self.requests.append(r)
        return r

    def admit(self):
        reserved = sum(r.reservation for r in self.requests
                       if r.phase in ("prefill", "decode"))
        for r in self.requests:
            if (r.phase == "waiting" and r.arrival <= self.tick
                    and reserved+r.reservation <= self.pool.capacity):
                r.handle = self.pool.empty(self.owner(r))
                r.phase = "prefill"
                reserved += r.reservation

    def plan(self):
        # Rotating list avoids permanently privileging the first ready decoder.
        n = len(self.requests)
        ordered = self.requests[self.tick % n:]+self.requests[:self.tick % n] if n else []
        remaining, work = self.budget, []
        for phase in ("decode", "prefill"):
            for r in ordered:
                if r.phase != phase or remaining == 0:
                    continue
                count = 1 if phase == "decode" else min(
                    self.chunk, len(r.prompt)-r.prefilled, remaining)
                work.append((r, phase, count))
                remaining -= count
        return work

    def cancel(self, rid):
        r = next(r for r in self.requests if r.rid == rid)
        if r.phase in ("done", "cancelled"):
            return
        if r.handle is not None:
            self.pool.release(r.handle, self.owner(r))
            r.handle = None
        r.phase = "cancelled"

    def step(self):
        self.admit()
        work = self.plan()
        record = []
        for r, phase, count in work:
            tokens = r.prompt[r.prefilled:r.prefilled+count] if phase == "prefill" else (r.generated[-1],)
            logits = self.pool.consume(r.handle, self.owner(r), tokens)
            if phase == "prefill":
                r.prefilled += count
            emit = phase == "decode" or r.prefilled == len(r.prompt)
            if emit:
                r.generated.append(int(logits[-1].argmax()))
                r.token_ticks.append(self.tick+1)  # completion boundary
                r.phase = "decode"
                if len(r.generated) == r.output:
                    self.pool.release(r.handle, self.owner(r))
                    r.handle, r.phase = None, "done"
            record.append((r.rid, phase, count, int(emit)))
        self.tick += 1
        stats = self.audit()
        self.trace.append({"tick": self.tick, "work": record, **stats})
        return record

    def audit(self):
        stats = self.pool.audit()
        active = [r for r in self.requests if r.phase in ("prefill", "decode")]
        reserved = sum(r.reservation for r in active)
        assert stats["used_pages"] <= reserved <= self.pool.capacity
        assert len(self.pool._states) == len(active)
        for r in active:
            state = self.pool.state(r.handle, self.owner(r))
            expected = r.prefilled+max(0, len(r.generated)-1)
            assert len(state.tokens) == expected
        return {**stats, "reserved_pages": reserved,
                "unreserved_pages": self.pool.capacity-reserved}

    def run(self, max_ticks=1000):
        for _ in range(paging.positive(max_ticks)):
            if all(r.phase in ("done", "cancelled") for r in self.requests):
                return self.trace
            self.step()
        raise RuntimeError("bounded simulation did not finish")


def metrics(r):
    if not r.token_ticks:
        raise ValueError("no emitted tokens")
    gaps = [b-a for a,b in zip(r.token_ticks, r.token_ticks[1:])]
    return {"ttft": r.token_ticks[0]-r.arrival,
            "itl_max": max(gaps) if gaps else None,
            "completion": r.token_ticks[-1]-r.arrival}


def finite_tensor(x):
    if not isinstance(x, torch.Tensor) or x.numel() == 0 or not bool(torch.isfinite(x).all()):
        raise ValueError("nonempty finite tensor")
    return x.detach().double()


def int8_symmetric(x, scale=None):
    x = finite_tensor(x)
    peak = x.abs().max().item()
    scale = (peak/127 if peak else 1.0) if scale is None else scale
    if not isinstance(scale, (float, int)) or not math.isfinite(scale) or scale <= 0:
        raise ValueError("finite positive scale")
    q = torch.clamp(torch.round(x/scale), -127, 127).to(torch.int8)
    return q, float(scale)


def represent(x, mode):
    x = finite_tensor(x)
    if mode == "int8":
        q, s = int8_symmetric(x)
        return q.double()*s
    if mode not in ("fp64", "fp16", "bf16"):
        raise ValueError("declared storage representation")
    dtype = {"fp64":torch.float64, "fp16":torch.float16, "bf16":torch.bfloat16}[mode]
    y = x.to(dtype).double()
    if not bool(torch.isfinite(y).all()):
        raise ValueError("representation overflow; fallback required")
    return y


def quality(ref, test):
    ref, test = finite_tensor(ref), finite_tensor(test)
    if ref.shape != test.shape:
        raise ValueError("matching shapes")
    err = ref-test
    p, q = ref.softmax(-1), test.softmax(-1)
    return {"max_abs": err.abs().max().item(),
            "relative_l2": (err.norm()/ref.norm().clamp_min(1e-12)).item(),
            "argmax_fraction": (ref.argmax(-1)==test.argmax(-1)).double().mean().item(),
            "kl": (p*(ref.log_softmax(-1)-test.log_softmax(-1))).sum(-1).mean().item()}


def gate(report, max_abs, relative_l2, min_argmax=1.0):
    limits = (max_abs, relative_l2, min_argmax)
    if (any(not math.isfinite(x) for x in limits) or min(limits) < 0
            or min_argmax > 1):
        raise ValueError("finite nonnegative quality limits")
    if any(not math.isfinite(x) for x in report.values()):
        return False
    return (0 <= report["max_abs"] <= max_abs
            and 0 <= report["relative_l2"] <= relative_l2
            and min_argmax <= report["argmax_fraction"] <= 1)


def precision_rollout(model, tokens, mode):
    """Round stored K/V after each token; arithmetic remains float64.

    This intentionally approximate cache is re-sealed for the native reader.
    It is not labeled an exact Chapter 36 pool entry or compressed allocation.
    """
    owner = ("precision", mode)
    cache = native.empty(model, owner)
    outputs = []
    for token in native.tokens_copy(tokens, model.max_len):
        logits, cache = native.consume(model, cache, owner, (token,))
        outputs.append(logits)
        layers = tuple(native.LayerKV(represent(x.k, mode), represent(x.v, mode))
                       for x in cache.layers)
        cache = native.sealed(owner, cache.artifact, cache.tokens, layers)
    if not outputs:
        raise ValueError("nonempty precision experiment")
    return torch.cat(outputs)


def results():
    model = native.tiny_model()
    scheduler = Scheduler(model, 12, 2, 4, 2)
    for rid, arrival, prompt, output in (("A",0,(0,1,2,3,0),3),
                                       ("B",1,(1,),2), ("C",2,(2,3,0),1)):
        scheduler.submit(rid, arrival, prompt, output)
    scheduler.run()
    tokens = (0,1,2,3,0,1,3,2)
    baseline = native.full_oracle(model, tokens)
    return {"timeline": scheduler.trace,
            "iterations": [{"end":row["tick"],
                            "processed":sum(x[2] for x in row["work"]),
                            "emitted":sum(x[3] for x in row["work"]),
                            "used":row["used_pages"], "reserved":row["reserved_pages"]}
                           for row in scheduler.trace],
            "latency": [{"request":r.rid, **metrics(r),
                         "itl_max":metrics(r)["itl_max"] if r.output>1 else "--"}
                        for r in scheduler.requests],
            "precision": [{"mode":m, **quality(baseline, precision_rollout(model,tokens,m))}
                          for m in ("fp64","fp16","bf16","int8")]}


TABLES = [("latency", ["Request","TTFT ticks","Max ITL","Completion"],
           ["request","ttft","itl_max","completion"],"lrrr"),
          ("iterations",["End tick","Consumed","Emitted","Pages used","Reserved"],
           ["end","processed","emitted","used","reserved"],"rrrrr"),
          ("precision", ["KV format","Max logit error","Relative L2","Argmax fraction"],
           ["mode","max_abs","relative_l2","argmax_fraction"],"lrrr")]
PLOTS = []
LISTINGS = ["Scheduler.plan", "Scheduler.step", "int8_symmetric", "precision_rollout"]
