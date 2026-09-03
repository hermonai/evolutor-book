import pytest

from minievolutor.evolution import replace_gene, verify_local_replacement
from minievolutor.gene import Gene
from minievolutor.genome import Genome


def test_verified_local_replacement_preserves_interfaces() -> None:
    original_gene = Gene("copy", ("x",), "y", lambda x: x["x"], int)
    original = Genome((original_gene,), ("x",), ("y",))
    replacement = Gene("copy", ("x",), "y", lambda x: x["x"] + 1, int)
    candidate = replace_gene(original, "copy", replacement)
    verify_local_replacement(original, candidate)


def test_replacement_cannot_change_gene_name() -> None:
    original = Genome(
        (Gene("copy", ("x",), "y", lambda x: x["x"], int),),
        ("x",),
        ("y",),
    )
    with pytest.raises(ValueError, match="preserve"):
        replace_gene(original, "copy", Gene("other", ("x",), "y", lambda x: 1, int))

