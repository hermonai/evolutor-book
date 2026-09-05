"""Pure arithmetic dispatch controls; event counts are not timing measurements."""
from dataclasses import dataclass
from collections.abc import Callable


@dataclass(frozen=True)
class DispatchResult:
    value: int
    selected: str
    stored: int
    gate_tests: int
    lookups: int
    firings: int = 1


class ArithmeticLibrary:
    """Construct once; construction and index storage are O(K) entries.

    This closed teaching library never executes external tools or learned code.
    An invocation count treats an integer operation as one event, not one CPU
    instruction. Python integer work may depend on the value's bit length.
    """
    def __init__(self, size: int = 4):
        if type(size) is not int or size < 4:
            raise ValueError("size must be an integer at least four")
        entries: list[tuple[str, Callable[[int], int]]] = [
            ("double", lambda x: 2 * x), ("square", lambda x: x * x),
            ("absolute", abs), ("identity", lambda x: x)]
        entries.extend((f"unused-{i}", lambda x: x) for i in range(size - 4))
        self._entries = tuple(entries)
        self._index = dict(entries)

    @staticmethod
    def _validate(request: str, value: int):
        if not isinstance(request, str) or type(value) is not int:
            raise TypeError("request must be str and value must be int")

    def indexed(self, request: str, value: int) -> DispatchResult:
        self._validate(request, value)
        operation = self._index[request]
        return DispatchResult(operation(value), request, len(self._entries), 0, 1)

    def full_scan(self, request: str, value: int) -> DispatchResult:
        self._validate(request, value)
        selected = None
        checks = 0
        for name, operation in self._entries:
            checks += 1
            if name == request:
                selected = operation
        if selected is None:
            raise KeyError(request)
        return DispatchResult(selected(value), request, len(self._entries), checks, 0)


def chapter_example():
    return [(size, method, getattr(ArithmeticLibrary(size), method)("double", -3))
            for size in (4, 64) for method in ("indexed", "full_scan")]
