"""EVOD-24 DNA-aware mechanisms; local mathematical references, not a trained model."""

from dataclasses import dataclass
import json
import math
import torch
from torch import nn

DNA = "ACGT"
COMP = str.maketrans(DNA, "TGCA")


def integer(value, minimum=0):
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise ValueError("integer outside declared domain")


def canonical(sequence):
    if not isinstance(sequence, str) or not sequence or set(sequence) - set(DNA):
        raise ValueError("nonempty canonical uppercase ACGT required")


def rc(sequence):
    canonical(sequence)
    return sequence.translate(COMP)[::-1]


@dataclass(frozen=True)
class Span:
    token: str
    start: int
    end: int


def tokenize(sequence, k=1, stride=1):
    canonical(sequence)
    integer(k, 1)
    integer(stride, 1)
    if k > len(sequence):
        raise ValueError("token width exceeds record")
    return [
        Span(sequence[i : i + k], i, i + k)
        for i in range(0, len(sequence) - k + 1, stride)
    ]


def mutation_footprint(spans, base_position):
    integer(base_position)
    return [i for i, span in enumerate(spans) if span.start <= base_position < span.end]


def reverse_span(span, length):
    integer(length, 1)
    if (
        not 0 <= span.start < span.end <= length
        or len(span.token) != span.end - span.start
    ):
        raise ValueError("span inconsistent with record")
    return Span(rc(span.token), length - span.end, length - span.start)


def causal_span_leaks(spans, prefix_end):
    """Prediction of base prefix_end may use only bases at coordinates < prefix_end."""
    integer(prefix_end)
    return [i for i, span in enumerate(spans) if span.end > prefix_end]


def validate_ids(ids):
    if not isinstance(ids, torch.Tensor) or ids.dtype != torch.long:
        raise ValueError("int64 nucleotide IDs required")
    if ids.ndim != 2 or not ids.shape[0] or not ids.shape[1]:
        raise ValueError("nonempty [B,T] required")
    if bool(((ids < 0) | (ids > 3)).any()):
        raise ValueError("outside four-base vocabulary")


def rc_ids(ids):
    validate_ids(ids)
    complement = torch.tensor([3, 2, 1, 0], device=ids.device)
    return complement[ids.flip(1)]


class StrandEmbedding(nn.Module):
    """Even/odd feature pairs under joint (sequence, orientation) RC action."""

    def __init__(self, width=2):
        super().__init__()
        integer(width, 1)
        self.even = nn.Parameter(torch.randn(2, width))
        self.odd = nn.Parameter(torch.randn(2, width))
        self.strand = nn.Parameter(torch.randn(width))

    def forward(self, ids, orientation):
        validate_ids(ids)
        if ids.device != self.even.device:
            raise ValueError("IDs and parameters must share device")
        if (
            orientation.shape != (ids.shape[0],)
            or orientation.device != ids.device
            or not bool(((orientation == 1) | (orientation == -1)).all())
        ):
            raise ValueError("orientation is +1/-1 for each record")
        # A/T share an even pair, as do C/G; complement flips odd sign.
        group = torch.tensor([0, 1, 1, 0], device=ids.device)[ids]
        sign = torch.tensor([1, 1, -1, -1], device=ids.device)[ids]
        even = self.even[group]
        odd = self.odd[group] * sign[..., None] + (
            orientation[:, None, None] * self.strand
        )
        return torch.stack([even, odd], dim=2)


def rc_feature_action(features):
    if features.ndim != 4 or features.shape[2] != 2:
        raise ValueError("feature shape [B,T,2,D] required")
    parity = features.new_tensor([1, -1])
    return features.flip(1) * parity[None, None, :, None]


def rotary(x, positions, frequencies):
    """Pair rotation for [B,H,T,Dh]; positions are declared base coordinates."""
    if (
        x.ndim != 4
        or any(size == 0 for size in x.shape)
        or x.shape[-1] % 2
        or not x.is_floating_point()
        or not bool(torch.isfinite(x).all())
    ):
        raise ValueError("finite floating [B,H,T,even Dh] required")
    if (
        positions.shape != (x.shape[2],)
        or frequencies.shape != (x.shape[3] // 2,)
        or positions.device != x.device
        or frequencies.device != x.device
        or positions.dtype != x.dtype
        or frequencies.dtype != x.dtype
        or not bool(torch.isfinite(positions).all())
        or not bool(torch.isfinite(frequencies).all())
    ):
        raise ValueError(
            "finite coordinate/frequency vectors matching dtype/device required"
        )
    angle = positions[:, None] * frequencies[None, :]
    a, b = x[..., 0::2], x[..., 1::2]
    rotated = torch.stack(
        [a * angle.cos() - b * angle.sin(), a * angle.sin() + b * angle.cos()], dim=-1
    )
    return rotated.flatten(-2)


def rotary_matrix_oracle(x, positions, frequencies):
    """Independent explicit block-diagonal matrices, not vectorized pair code."""
    matrices = []
    for position in positions:
        blocks = []
        for frequency in frequencies:
            angle = position * frequency
            c, s = angle.cos(), angle.sin()
            blocks.append(torch.stack([torch.stack([c, -s]), torch.stack([s, c])]))
        matrices.append(torch.block_diag(*blocks))
    return torch.stack(
        [x[:, :, i] @ matrix.T for i, matrix in enumerate(matrices)], dim=2
    )


def edge_lists(length, radius, causal=False, globals_=(), valid=None):
    """Local + static global edges; no suffix-dependent selection. Query->key."""
    integer(length, 1)
    integer(radius)
    if not isinstance(causal, bool):
        raise ValueError("causal must be boolean")
    for index in globals_:
        integer(index)
        if index >= length:
            raise ValueError("global index outside record")
    globals_ = set(globals_)
    if valid is None:
        valid = [True] * length
    if len(valid) != length or any(type(v) is not bool for v in valid):
        raise ValueError("one boolean validity per position required")
    rows = []
    for i in range(length):
        if not valid[i]:
            rows.append([])
            continue
        start, stop = max(0, i - radius), min(length, i + radius + 1)
        local = set(range(start, stop))
        if i in globals_:
            local.update(range(length))
        local.update(globals_)
        rows.append(sorted(j for j in local if valid[j] and (not causal or j <= i)))
    return rows


def validate_qkv(q, k, v, edges):
    if (
        q.ndim != 2
        or q.shape != k.shape
        or q.shape[0] != v.shape[0]
        or v.ndim != 2
        or not q.shape[0]
        or not q.shape[1]
        or not v.shape[1]
        or q.dtype != k.dtype
        or q.dtype != v.dtype
        or q.device != k.device
        or q.device != v.device
        or not q.is_floating_point()
        or not all(bool(torch.isfinite(x).all()) for x in (q, k, v))
    ):
        raise ValueError("finite same-dtype/device Q,K:[T,D], V:[T,Dv] required")
    if len(edges) != q.shape[0]:
        raise ValueError("one edge row per query required")
    for row in edges:
        if row != sorted(set(row)) or any(
            type(j) is not int or not 0 <= j < q.shape[0] for j in row
        ):
            raise ValueError("sorted unique in-range key indices required")


def sparse_attention(q, k, v, edges):
    """Single-head ragged-row gather reference; no dense score matrix."""
    validate_qkv(q, k, v, edges)
    output = []
    for i, allowed in enumerate(edges):
        if not allowed:
            output.append(v.new_zeros(v.shape[1]) + q[i].sum() * 0)
            continue
        logits = (k[allowed] @ q[i]) / math.sqrt(q.shape[1])
        output.append(logits.softmax(0) @ v[allowed])
    return torch.stack(output)


def dense_attention_oracle(q, k, v, edges):
    """Dense vectorized oracle used only for small value/gradient verification."""
    validate_qkv(q, k, v, edges)
    allowed = torch.zeros(len(edges), len(edges), dtype=torch.bool, device=q.device)
    for i, row in enumerate(edges):
        allowed[i, row] = True
    active = allowed.any(1)
    scores = q @ k.T / math.sqrt(q.shape[1])
    scores = scores.masked_fill(~allowed, -float("inf"))
    scores = torch.where(active[:, None], scores, torch.zeros_like(scores))
    weights = scores.softmax(1) * active[:, None]
    return weights @ v


def reachable_sources(edges, query, layers):
    """Dependency expansion includes residual self-access at each layer."""
    integer(query)
    integer(layers)
    if query >= len(edges):
        raise ValueError("query outside graph")
    sources = {query}
    for _ in range(layers):
        sources |= {j for i in sources for j in edges[i]}
    return sorted(sources)


def results():
    torch.set_num_threads(1)
    spans = tokenize("ACGTAC", 3)
    ids = torch.tensor([[0, 1, 2, 3]], dtype=torch.long)
    embed = StrandEmbedding(2).double()
    with torch.no_grad():
        embed.even.copy_(torch.tensor([[1.0, 0.0], [0.0, 1.0]]))
        embed.odd.copy_(torch.tensor([[0.5, 0.25], [-0.25, 0.5]]))
        embed.strand.copy_(torch.tensor([0.1, 0.2]))
    orientation = torch.tensor([1.0], dtype=torch.float64)
    features = embed(ids, orientation)
    transformed = embed(rc_ids(ids), -orientation)
    generator = torch.Generator().manual_seed(240)
    q, k, v = [
        torch.randn(8, 4, generator=generator, dtype=torch.float64) for _ in range(3)
    ]
    edges = edge_lists(8, 1, causal=True, globals_=(0,))
    parity = (
        (sparse_attention(q, k, v, edges) - dense_attention_oracle(q, k, v, edges))
        .abs()
        .max()
        .item()
    )
    pos = torch.arange(8, dtype=torch.float64)
    frequencies = torch.tensor([1.0, 0.01], dtype=torch.float64)
    rq = rotary(q[None, None], pos, frequencies)[0, 0]
    rk = rotary(k[None, None], pos, frequencies)[0, 0]
    shifted_q = rotary(q[None, None], pos + 100, frequencies)[0, 0]
    shifted_k = rotary(k[None, None], pos + 100, frequencies)[0, 0]
    cost = []
    for length in (32, 128, 512, 1024):
        sparse_edges = edge_lists(length, 4, globals_=(0, length - 1))
        causal_edges = edge_lists(length, 4, causal=True, globals_=(0, length - 1))
        cost.append(
            {
                "length": length,
                "dense": length * length,
                "offline_edges": sum(map(len, sparse_edges)),
                "causal_edges": sum(map(len, causal_edges)),
            }
        )
    local = edge_lists(12, 1)
    global_graph = edge_lists(12, 1, globals_=(0,))
    return {
        "scope": "Assigned tensors and algebraic tests; no trained model, genomic benchmark or optimized kernel.",
        "spans": [{"token": s.token, "start": s.start, "end": s.end} for s in spans],
        "mutated_base_2_tokens": mutation_footprint(spans, 2),
        "illegal_tokens_for_target_base_2": causal_span_leaks(spans, 2),
        "strand_features": [
            {
                "base": DNA[int(ids[0, i])],
                "even_1": features[0, i, 0, 0].item(),
                "even_2": features[0, i, 0, 1].item(),
                "odd_1": features[0, i, 1, 0].item(),
                "odd_2": features[0, i, 1, 1].item(),
            }
            for i in range(4)
        ],
        "rc_feature_error": (transformed - rc_feature_action(features))
        .abs()
        .max()
        .item(),
        "rotary_shift_score_error": (rq @ rk.T - shifted_q @ shifted_k.T)
        .abs()
        .max()
        .item(),
        "sparse_dense_value_error": parity,
        "cost": cost,
        "reachability": {
            "local_1_layer_query_1": reachable_sources(local, 1, 1),
            "local_2_layers_query_1": reachable_sources(local, 1, 2),
            "global_1_layer_query_1": reachable_sources(global_graph, 1, 1),
            "global_2_layers_query_1": reachable_sources(global_graph, 1, 2),
        },
        "rotary_frequencies": frequencies.tolist(),
    }


TABLES = [
    ("spans", ["Token", "Start", "End"], ["token", "start", "end"], "lrr"),
    (
        "strand_features",
        ["Base", "Even 1", "Even 2", "Odd 1", "Odd 2"],
        ["base", "even_1", "even_2", "odd_1", "odd_2"],
        "lrrrr",
    ),
    (
        "cost",
        ["Length", "Dense edges", "Offline edges", "Causal edges"],
        ["length", "dense", "offline_edges", "causal_edges"],
        "rrrr",
    ),
]
PLOTS = []
LISTINGS = [
    "tokenize",
    "causal_span_leaks",
    "StrandEmbedding.forward",
    "rotary",
    "edge_lists",
    "sparse_attention",
    "reachable_sources",
]

if __name__ == "__main__":
    print(json.dumps(results(), indent=2))
