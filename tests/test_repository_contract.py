from pathlib import Path


def test_bootstrap_research_contract_exists() -> None:
    root = Path(__file__).resolve().parents[1]
    required = [
        "research/architecture-taxonomy.md",
        "research/architecture-lineage.md",
        "research/name-migration-options.md",
        "research/claims-ledger.md",
        "research/theorem-ledger.md",
        "research/proof-dependency-graph.md",
        "research/proof-obligations.md",
        "research/experimental-controls.md",
        "research/correction-record.md",
        "research/foundation-library-roadmap.md",
        "research/runtime-roadmap.md",
        "book/NOTATION.md",
    ]
    assert all((root / path).is_file() for path in required)

