import pytest
from minievolutor.dispatch_reference import ArithmeticLibrary, chapter_example


def test_equivalence_over_all_declared_operations_and_signed_inputs():
    library = ArithmeticLibrary(12)
    requests = ["double", "square", "absolute", "identity"] + [f"unused-{i}" for i in range(8)]
    for request in requests:
        for value in range(-20, 21):
            assert library.indexed(request, value).value == library.full_scan(request, value).value


def test_oracles_independent_of_selectors():
    library = ArithmeticLibrary()
    for value in (-100, -3, 0, 4, 10**40):
        expected = {"double": value + value, "square": value**2,
                    "absolute": -value if value < 0 else value, "identity": value}
        for request, answer in expected.items():
            assert library.indexed(request, value).value == answer
            assert library.full_scan(request, value).value == answer


def test_counts_expose_unexpressed_routing_work():
    for size, method, result in chapter_example():
        assert result.stored == size and result.value == -6 and result.firings == 1
        assert result.gate_tests == (size if method == "full_scan" else 0)
        assert result.lookups == (1 if method == "indexed" else 0)


def test_invalid_requests_and_values():
    for method in (ArithmeticLibrary().indexed, ArithmeticLibrary().full_scan):
        with pytest.raises(KeyError):
            method("not-in-library", 3)
        with pytest.raises(TypeError):
            method("double", True)
    with pytest.raises(ValueError):
        ArithmeticLibrary(3)
