"""Training semantics and negative controls, independent of model usefulness."""

import importlib.util
import io
import json
from pathlib import Path
import math
import pytest
import torch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "e04", ROOT / "drafts/ch04/reference.py"
)
M = importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)


def test_review_record_binds_authored_sources_without_promotion():
    import hashlib
    import json
    record = json.loads((ROOT / "artifacts/deep/ch04-review.json").read_text())
    assert record["allPagesInspected"] and record["openGates"]
    assert record["figures"] == 5 and record["exercises"] == 12
    assert record["status"].endswith("no acceptance promotion")
    for path, digest in record["sources"].items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest, path
    accepted = json.loads((ROOT / "book/book.json").read_text())
    assert len(accepted["chapters"]) == 2


def test_local_review_pdf_matches_author_review_when_available():
    import hashlib
    import json
    record = json.loads((ROOT / "artifacts/deep/ch04-review.json").read_text())
    path = ROOT / record["pdf"]
    if not path.exists():
        pytest.skip("Review PDF is a generated, gitignored artifact")
    assert hashlib.sha256(path.read_bytes()).hexdigest() == record["sha256"]


def equal_tree(a, b):
    if isinstance(a, torch.Tensor):
        assert torch.equal(a, b)
    elif isinstance(a, dict):
        assert a.keys() == b.keys()
        for k in a:
            equal_tree(a[k], b[k])
    elif isinstance(a, (tuple, list)):
        assert len(a) == len(b)
        for x, y in zip(a, b):
            equal_tree(x, y)
    else:
        assert a == b


def test_shift_mask_and_uniform_loss():
    x, y = M.collate([("a", "ACGT"), ("b", "AN")])
    assert x.tolist() == [[0, 1, 2], [0, 5, 5]]
    assert y.tolist() == [[1, 2, 3], [-100, -100, -100]]
    z = torch.zeros((2, 3, 4), dtype=torch.float64, requires_grad=True)
    total, n = M.masked_loss(z, y)
    assert n == 3 and float(total.detach() / n) == pytest.approx(
        math.log(4)
    )
    (total / n).backward()
    assert torch.equal(z.grad[1], torch.zeros_like(z.grad[1]))
    assert z.grad[0, 0].tolist() == pytest.approx(
        [1 / 12, -1 / 4, 1 / 12, 1 / 12]
    )


def test_padding_invariance():
    run = M.Run()
    run.model.eval()
    x, y = M.collate([M.CORPUS[0]])
    loss, n = M.masked_loss(run.model(x), y)
    xx = torch.nn.functional.pad(x, (0, 9), value=M.PAD)
    yy = torch.nn.functional.pad(y, (0, 9), value=M.IGNORE)
    loss2, n2 = M.masked_loss(run.model(xx), yy)
    assert n == n2 and torch.equal(loss, loss2)


def test_empty_target_set_rejected():
    with pytest.raises(ValueError):
        M.masked_loss(torch.zeros(1, 2, 4), torch.full((1, 2), M.IGNORE))


@pytest.mark.parametrize("rows", [[], [("a", "A")], [("a", "ACX")]])
def test_bad_corpus(rows):
    with pytest.raises(ValueError):
        M.collate(rows)


def test_split_identity_and_reverse_complement_guard():
    M.validate_split()
    with pytest.raises(ValueError):
        M.validate_split([("same", "AC")], [("same", "AA")])
    with pytest.raises(ValueError):
        M.validate_split([("a", "AC")], [("b", "GT")])


@pytest.mark.parametrize("cut", range(1, 8))
def test_restart_at_every_update_boundary(cut):
    r = M.replay(cut=cut)
    assert r["max_parameter_error"] == 0
    assert r["same_loss_trace"] and r["same_batch_trace"]
    equal_tree(r["expected_optimizer"], r["actual_optimizer"])


@pytest.mark.parametrize("omit", ["optimizer", "rng", "cursor"])
def test_missing_state_controls_fail(omit):
    r = M.replay(omit=omit)
    assert r["max_parameter_error"] > 1e-8
    assert not r["same_loss_trace"]
    if omit == "cursor":
        assert not r["same_batch_trace"]


def test_serialized_snapshot_is_not_live_alias():
    run = M.Run()
    run.step()
    blob = run.checkpoint()
    before = M.parameter_vector(run)
    run.step()
    restored = M.Run.restore(blob)
    assert torch.equal(before, M.parameter_vector(restored))
    assert not torch.equal(before, M.parameter_vector(run))


def test_reject_changed_corpus_or_configuration():
    run = M.Run()
    blob = run.checkpoint()
    with pytest.raises(ValueError):
        M.Run.restore(blob, corpus=M.CORPUS[::-1])
    state = torch.load(io.BytesIO(blob), weights_only=True)
    state["config"]["lr"] = 0.3
    stream = io.BytesIO()
    torch.save(state, stream)
    with pytest.raises(ValueError):
        M.Run.restore(stream.getvalue())


def test_evaluation_preserves_rng_parameters_and_mode():
    run = M.Run()
    run.step()
    before = M.parameter_vector(run)
    rng = torch.get_rng_state().clone()
    assert run.model.training
    a = run.evaluate()
    b = run.evaluate()
    assert a == b and run.model.training
    assert torch.equal(before, M.parameter_vector(run))
    assert torch.equal(rng, torch.get_rng_state())
    assert all(p.grad is None for p in run.model.parameters())


def test_future_base_cannot_change_prefix_predictions():
    model = M.Predictor().eval()
    x, y = M.collate([("a", "ACGTAC")])
    altered = x.clone()
    altered[0, 3:] = (altered[0, 3:] + 1) % 4
    assert torch.equal(model(x)[:, :3], model(altered)[:, :3])


def test_count_weighting_matches_full_batch_gradient():
    run = M.Run()
    run.model.eval()  # disable dropout so both programs evaluate the same function
    rows = [M.CORPUS[0], M.CORPUS[1]]
    x, y = M.collate(rows)
    total, n = M.masked_loss(run.model(x), y)
    full = torch.autograd.grad(total / n, tuple(run.model.parameters()))
    totals = []
    counts = []
    for row in rows:
        x1, y1 = M.collate([row])
        s, c = M.masked_loss(run.model(x1), y1)
        totals.append(s)
        counts.append(c)
    weighted = torch.autograd.grad(
        sum(totals) / sum(counts), tuple(run.model.parameters())
    )
    for a, b in zip(full, weighted):
        assert torch.allclose(a, b, atol=1e-15, rtol=1e-14)


def test_generated_results_reproduce():
    actual = M.results()
    expected = json.loads((ROOT / "drafts/ch04/results.json").read_text())
    assert actual == expected
