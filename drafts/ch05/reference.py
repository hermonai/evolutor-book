"""Lossless DNA tokenization with explicit offsets and causal target reach."""

from dataclasses import dataclass
import hashlib
import json
import torch
from torch.nn import functional as F

BASES = "ACGT"
SPECIALS = ("<PAD>", "<BOS>", "<EOS>")


def validate(sequence):
    if not isinstance(sequence, str) or set(sequence) - set(BASES):
        raise ValueError(
            "uppercase canonical DNA only; ambiguity is not silently collapsed"
        )
    return sequence


def reverse_complement(sequence):
    return validate(sequence).translate(str.maketrans("ACGT", "TGCA"))[::-1]


def encode_kmer(word):
    validate(word)
    if not word:
        raise ValueError("a k-mer must be nonempty")
    value = 0
    for base in word:
        value = 4 * value + BASES.index(base)
    return value


def decode_kmer(value, k):
    if (
        type(k) is not int
        or k < 1
        or type(value) is not int
        or not 0 <= value < 4**k
    ):
        raise ValueError("integer ID must fit the declared positive k")
    output = []
    for _ in range(k):
        value, digit = divmod(value, 4)
        output.append(BASES[digit])
    return "".join(reversed(output))


@dataclass(frozen=True)
class Token:
    text: str
    start: int
    stop: int


def tokenize(sequence, k, mode="overlap"):
    validate(sequence)
    if type(k) is not int or k < 1 or mode not in ("overlap", "disjoint"):
        raise ValueError("positive k and a declared mode required")
    if mode == "disjoint":
        return [
            Token(sequence[i : i + k], i, min(i + k, len(sequence)))
            for i in range(0, len(sequence), k)
        ]
    if len(sequence) < k:
        return [Token(sequence, 0, len(sequence))] if sequence else []
    return [
        Token(sequence[i : i + k], i, i + k)
        for i in range(len(sequence) - k + 1)
    ]


def reconstruct(tokens):
    """Accept overlaps only when all shared bases agree; reject gaps."""
    output = ""
    for token in tokens:
        validate(token.text)
        if (
            type(token.start) is not int
            or type(token.stop) is not int
            or not token.text
            or not 0 <= token.start <= len(output)
            or token.stop != token.start + len(token.text)
            or token.stop <= len(output)
        ):
            raise ValueError(
                "tokens must extend an ordered gap-free sequence"
            )
        overlap = len(output) - token.start
        if output[token.start :] != token.text[:overlap]:
            raise ValueError("overlap disagrees")
        output += token.text[overlap:]
    return output


def safe_next_base_examples(sequence, k):
    return [
        (t.text, sequence[t.stop], t.stop)
        for t in tokenize(sequence, k)
        if t.stop < len(sequence)
    ]


def vocabulary(k):
    if type(k) is not int or not 1 <= k <= 6:
        raise ValueError("teaching vocabulary budget requires 1 <= k <= 6")
    return SPECIALS + tuple(
        decode_kmer(i, width)
        for width in range(1, k + 1)
        for i in range(4**width)
    )


def vocabulary_digest(k):
    payload = {
        "alphabet": BASES,
        "k": k,
        "tail": "retain-short",
        "tokens": vocabulary(k),
    }
    return hashlib.sha256(
        json.dumps(payload, separators=(",", ":")).encode()
    ).hexdigest()


def encode_record(sequence, k, mode="disjoint"):
    table = {word: i for i, word in enumerate(vocabulary(k))}
    return {
        "vocabulary_sha256": vocabulary_digest(k),
        "mode": mode,
        "tokens": [
            {"id": table[t.text], "start": t.start, "stop": t.stop}
            for t in tokenize(sequence, k, mode)
        ],
    }


def decode_record(record, k):
    if record["vocabulary_sha256"] != vocabulary_digest(k):
        raise ValueError("vocabulary identity mismatch")
    words = vocabulary(k)
    tokens = []
    for item in record["tokens"]:
        i = item["id"]
        if type(i) is not int or not len(SPECIALS) <= i < len(words):
            raise ValueError(
                "sequence token ID required, not padding/control"
            )
        tokens.append(Token(words[i], item["start"], item["stop"]))
    sequence = reconstruct(tokens)
    if tokens != tokenize(sequence, k, record["mode"]):
        raise ValueError("offsets disagree with declared segmentation")
    return sequence


def canonicalize(sequence):
    rc = reverse_complement(sequence)
    return (rc, True) if rc < sequence else (sequence, False)


def embedding_example():
    # Deterministic assigned numbers, not learned biochemical coordinates.
    weight = (
        torch.arange(15, dtype=torch.float64)
        .reshape(5, 3)
        .clone()
        .requires_grad_()
    )
    ids = torch.tensor([[0, 2, 0, 4]])
    selected = F.embedding(ids, weight, padding_idx=4)
    one_hot = F.one_hot(ids, 5).to(torch.float64) @ weight
    selected.sum().backward()
    return {
        "ids": ids.tolist(),
        "vectors": selected.detach().tolist(),
        "one_hot_matches": torch.equal(selected, one_hot),
        "gradient": weight.grad.tolist(),
        "padding_value": selected[0, 3].detach().tolist(),
    }


def results():
    s = "ACGTACG"
    return {
        "scope": "deterministic representation examples, no trained genomic model",
        "sequence": s,
        "kmer_ACG": encode_kmer("ACG"),
        "record": encode_record(s, 3),
        "tokens": {
            mode: [vars(t) for t in tokenize(s, 3, mode)]
            for mode in ("overlap", "disjoint")
        },
        "safe_examples": [list(row) for row in safe_next_base_examples(s, 3)],
        "rc": reverse_complement(s),
        "rc_disjoint": [
            vars(t) for t in tokenize(reverse_complement(s), 3, "disjoint")
        ],
        "vocabulary_rows": [
            {
                "k": k,
                "full_kmers": 4**k,
                "with_tails_and_specials": len(vocabulary(k)),
                "disjoint_tokens_1000": (1000 + k - 1) // k,
                "overlap_tokens_1000": 1000 - k + 1,
                "embedding_bytes_d64_float32": len(vocabulary(k)) * 64 * 4,
            }
            for k in (1, 2, 3, 6)
        ],
        "vocabulary_sha256_k3": vocabulary_digest(3),
        "embedding": embedding_example(),
    }


if __name__ == "__main__":
    torch.set_num_threads(1)
    print(json.dumps(results(), indent=2))
