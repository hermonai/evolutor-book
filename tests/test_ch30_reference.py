"""Serialized protocol specification, independent bounded interleavings, forced failures."""

import importlib.util
import itertools
from pathlib import Path
import sys
import threading
import pytest

spec = importlib.util.spec_from_file_location(
    "evod30", Path(__file__).parents[1] / "drafts/ch30/reference.py"
)
r = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = r
spec.loader.exec_module(r)


def make(**kwargs):
    req = r.Request("r", "tenant", "a" * 64, 100, **kwargs)
    reg = r.StateRegistry()
    rt = r.Runtime(req, reg)
    rt.admit("w", 0)
    rt.allocate("s", 0)
    return rt


def check(rt):
    a = rt.accounting()
    assert a["launched"] == a["settled"] + a["pending"]
    assert a["generated"] == a["queued"] + a["dequeued"] + a["discarded_output"]
    assert a["generated"] == a["revision"] <= rt.req.max_tokens
    assert len(rt.queue) <= rt.req.queue_items
    assert sum(len(v) for _, v in rt.queue) <= rt.req.queue_bytes
    assert [e.seq for e in rt.events] == list(range(len(rt.events)))
    assert [e.time_ms for e in rt.events] == sorted(e.time_ms for e in rt.events)
    assert sum(e.kind == "terminal" for e in rt.events) <= 1
    if rt.cleaned:
        assert rt.lease is None and rt.worker is None and not rt.queue
        assert rt.pending is None and rt.reason is not None


@pytest.mark.parametrize(
    "kwargs",
    [
        {"max_tokens": 0},
        {"queue_items": 0},
        {"queue_bytes": 0},
        {"item_bytes": 0},
        {"max_tokens": True},
        {"item_bytes": 9},
        {"deadline_ms": -1},
        {"model_id": "mutable-current"},
        {"model_id": "A" * 64},
        {"request_id": ""},
        {"tenant_id": None},
    ],
)
def test_request_guards(kwargs):
    fields = dict(request_id="r", tenant_id="t", model_id="a" * 64, deadline_ms=100)
    fields.update(kwargs)
    with pytest.raises(ValueError):
        r.Request(**fields)


def test_immutable_model_binding():
    req = r.Request("r", "t", "a" * 64, 100)
    with pytest.raises(Exception):
        req.model_id = "b" * 64
    rt = make()
    assert rt.lease.owner == ("tenant", "r", "a" * 64)


@pytest.mark.parametrize("policy", [(False, True), (True, False)])
def test_admission_before_allocation(policy):
    reg = r.StateRegistry()
    rt = r.Runtime(r.Request("r", "t", "a" * 64, 100), reg)
    assert not rt.admit("w", 0, *policy)
    assert reg.live_count() == 0
    with pytest.raises(RuntimeError):
        rt.allocate("s", 1)
    rt.cleanup(2)
    assert rt.reason == "rejected"


def test_deadline_at_admission_and_allocation():
    reg = r.StateRegistry()
    rt = r.Runtime(r.Request("r", "t", "a" * 64, 1), reg)
    assert not rt.admit("w", 1)
    assert rt.reason == "deadline" and reg.live_count() == 0
    other = r.Runtime(r.Request("r2", "t", "a" * 64, 1), reg)
    other.admit("w", 0)
    assert not other.allocate("s", 1)
    assert reg.live_count() == 0


def test_allocation_conflict_atomic():
    rt = make()
    other = r.Runtime(r.Request("other", "otherTenant", "b" * 64, 100), rt.registry)
    other.admit("w", 0)
    before = list(other.events)
    with pytest.raises(RuntimeError):
        other.allocate("s", 1)
    assert other.phase == r.Phase.ADMITTED and other.lease is None
    assert other.events == before and rt.registry.live_count() == 1
    assert rt.lease.owner[0] == "tenant"


def test_registry_foreign_release_and_generation_aba():
    rt = make()
    old = rt.lease
    foreign = r.Lease(old.state_id, old.generation, ("other", "r", "a" * 64))
    with pytest.raises(RuntimeError):
        rt.registry.release(foreign)
    rt.cancel(1)
    rt.cleanup(2)
    new = rt.registry.claim("s", rt.req)
    assert new.generation == old.generation + 1
    with pytest.raises(RuntimeError):
        rt.registry.release(old)
    rt.registry.release(new)


def test_queue_capacity_not_total_generation_limit():
    rt = make(queue_items=1, max_tokens=3)
    for seq in range(1, 4):
        assert rt.commit(rt.launch(seq), str(seq), seq)
        assert rt.consume(seq) == (seq, str(seq))
    assert rt.reason == "completed" and rt.generated == 3
    rt.cleanup(4)
    check(rt)


def test_byte_capacity_and_utf8_reservation():
    rt = make(queue_items=10, queue_bytes=5, item_bytes=4)
    rt.commit(rt.launch(1), "é", 1)  # two bytes, not one
    before = rt.accounting()
    assert rt.launch(2) is None  # 2+4>5 even though ten item slots exist
    assert rt.accounting() == before
    rt.consume(3)
    assert rt.launch(4) is not None


@pytest.mark.parametrize("item", ["", "abcde", "😀a", "\ud800", 7])
def test_invalid_result_fails_without_output_or_state_commit(item):
    rt = make()
    ticket = rt.launch(1)
    assert not rt.commit(ticket, item, 2)
    assert rt.reason == "failed" and rt.generated == rt.revision == 0
    assert rt.discarded_work == 1 and rt.pending is None
    rt.cleanup(3)
    check(rt)


def test_duplicate_foreign_and_revision_fence():
    rt = make()
    ticket = rt.launch(1)
    foreign = r.Ticket(r.Lease("s", 1, ("other", "r", "a" * 64)), 0, 1)
    with pytest.raises(RuntimeError):
        rt.commit(foreign, "a", 2)
    assert rt.pending == ticket
    rt.commit(ticket, "a", 2)
    with pytest.raises(RuntimeError):
        rt.commit(ticket, "a", 3)
    check(rt)


def test_one_pending_and_backpressure_no_work():
    rt = make()
    t = rt.launch(1)
    with pytest.raises(RuntimeError):
        rt.launch(1)
    rt.commit(t, "a", 2)
    rt.commit(rt.launch(2), "b", 2)
    launched = rt.launched
    assert rt.launch(3) is None
    assert rt.launched == launched and rt.pending is None


def test_cancel_pending_then_physical_ack_then_cleanup():
    rt = make()
    ticket = rt.launch(1)
    rt.cancel(2)
    with pytest.raises(RuntimeError):
        rt.cleanup(2)
    assert rt.registry.live_count() == 1
    assert not rt.commit(ticket, "a", 3)
    assert rt.revision == 0 and rt.reason == "cancelled"
    rt.cleanup(4)
    assert rt.registry.live_count() == 0
    check(rt)


def test_deadline_boundary_blocks_commit_even_when_launch_was_timely():
    rt = make()
    ticket = rt.launch(1)
    assert not rt.commit(ticket, "a", 100)
    assert rt.reason == "deadline"
    check(rt)


@pytest.mark.parametrize(
    "order", list(itertools.permutations(("completed", "cancelled", "failed")))
)
def test_terminal_race_independent_first_winner(order):
    reason, events, live = r.race_trace(order)
    assert reason == order[0]
    assert events.count("terminal") == 1 and events.count("cleaned") == 1 and live == 0


@pytest.mark.parametrize("first", ["completed", "cancelled", "failed", "deadline"])
def test_deadline_priority_at_exact_boundary(first):
    rt = make()
    assert rt.terminate(first, 100)
    assert rt.reason == "deadline"
    assert not rt.terminate("completed", 101)
    rt.cleanup(101)
    assert rt.reason == "deadline"


def test_unarrived_deadline_and_clock_guards():
    rt = make()
    with pytest.raises(ValueError):
        rt.terminate("deadline", 1)
    rt.launch(2)
    with pytest.raises(ValueError):
        rt.consume(1)
    with pytest.raises(ValueError):
        rt.consume(True)


def test_completion_queue_drain_is_not_cleanup():
    rt = make(max_tokens=1)
    rt.commit(rt.launch(1), "a", 1)
    assert rt.reason == "completed" and rt.queue
    with pytest.raises(RuntimeError):
        rt.cleanup(2)
    assert rt.consume(3) == (1, "a")
    rt.cleanup(4)
    assert not rt.cleanup(4)
    check(rt)


def test_explicit_output_discard_and_late_cancel():
    rt = make()
    rt.commit(rt.launch(1), "a", 1)
    rt.cancel(2)
    assert rt.consume(3) == (1, "a")  # chosen policy: committed bytes remain readable
    assert not rt.cancel(4)
    rt.cleanup(5)
    assert rt.reason == "cancelled"
    rt = make(max_tokens=1)
    rt.commit(rt.launch(1), "a", 1)
    rt.cleanup(2, discard_queue=True)
    assert rt.discarded == 1 and rt.delivered == 0
    check(rt)


def test_cleanup_before_terminal_and_unknown_reason():
    rt = make()
    with pytest.raises(RuntimeError):
        rt.cleanup(1)
    with pytest.raises(ValueError):
        rt.terminate("mystery", 1)


def test_trace_metadata_does_not_store_payload():
    rt = make()
    rt.commit(rt.launch(1), "DNA", 1)
    assert "DNA" not in repr(rt.events)


def test_release_failure_retains_handles_for_diagnosis():
    rt = make()
    rt.cancel(1)
    lease = rt.lease
    original = rt.registry.release

    def broken_release(_):
        raise RuntimeError("forced release failure")

    rt.registry.release = broken_release
    with pytest.raises(RuntimeError):
        rt.cleanup(2)
    assert rt.lease == lease and not rt.cleaned
    rt.registry.release = original
    assert rt.cleanup(3)
    check(rt)


def independent_machine(word):
    # Separate small specification; does not call Runtime or its helpers.
    active = True
    pending = False
    cleaned = False
    reason = None
    generated = queued = dequeued = discarded_work = launched = settled = 0
    accepted = []
    for op in word:
        ok = False
        if op == "launch" and active and not pending and queued < 2:
            pending = True
            launched += 1
            ok = True
        elif op == "commit" and pending:
            pending = False
            settled += 1
            ok = True
            if active:
                generated += 1
                queued += 1
                if generated == 3:
                    active = False
                    reason = "completed"
            else:
                discarded_work += 1
        elif op == "consume" and not cleaned:
            if queued:
                queued -= 1
                dequeued += 1
            ok = True
        elif op == "cancel":
            if active:
                active = False
                reason = "cancelled"
            ok = True  # late cancel is an accepted no-op
        elif op == "complete":
            if not active:
                ok = True
            elif not pending:
                active = False
                reason = "completed"
                ok = True
        elif op == "cleanup" and not active and not pending and queued == 0:
            cleaned = True
            ok = True
        accepted.append(ok)
    return accepted, (
        reason,
        pending,
        cleaned,
        generated,
        queued,
        dequeued,
        discarded_work,
        launched,
        settled,
    )


def test_all_7776_length_five_interleavings_against_independent_machine():
    alphabet = ("launch", "commit", "consume", "cancel", "complete", "cleanup")
    for word in itertools.product(alphabet, repeat=5):
        rt = make()
        accepted = []
        for op in word:
            try:
                if op == "launch":
                    ticket = rt.launch(1)
                    ok = ticket is not None
                elif op == "commit":
                    rt.commit(rt.pending, "a", 1)
                    ok = True
                elif op == "consume":
                    rt.consume(1)
                    ok = True
                elif op == "cancel":
                    rt.cancel(1)
                    ok = True
                elif op == "complete":
                    rt.terminate("completed", 1)
                    ok = True
                else:
                    rt.cleanup(1)
                    ok = True
            except RuntimeError:
                ok = False
            accepted.append(ok)
            check(rt)
        oracle, expected = independent_machine(word)
        actual = (
            rt.reason,
            rt.pending is not None,
            rt.cleaned,
            rt.generated,
            len(rt.queue),
            rt.delivered,
            rt.discarded_work,
            rt.launched,
            rt.settled,
        )
        assert accepted == oracle and actual == expected, word


def test_lock_serialized_terminal_threads_only_not_production_runtime():
    rt = make()
    lock = threading.Lock()
    barrier = threading.Barrier(12)
    won = []

    def worker(i):
        barrier.wait()
        with lock:
            won.append(rt.terminate(("completed", "cancelled", "failed")[i % 3], 1))

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(12)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert sum(won) == 1
    rt.cleanup(2)
    check(rt)
