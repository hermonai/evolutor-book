"""The reboot contract checks real links, graph structure and archive fidelity."""
from pathlib import Path
import importlib.util
import re
import subprocess
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("render_graphs", ROOT / "scripts/render_graphs.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_reset_deliverables_and_reviewed_chapter_manifest():
    for path in ["ASTRA_REDESIGN.md", "BOOK_PLAN.md", "PUBLICATION_PLAN.md",
                 "REFERENCE_IMPLEMENTATION.md", "RESET_REPORT.md",
                 "research/reset-audit.md", "research/primary-sources.md",
                 "research/claims-ledger.md", "book/NOTATION.md",
                 "book/TERMINOLOGY.md", "book/GRAPH_STANDARD.md"]:
        assert (ROOT / path).is_file(), path
    manifest = (ROOT / "tex/chapters/manifest.tex").read_text()
    book = json.loads((ROOT / "book/book.json").read_text())
    if book.get("edition") == "4-deep":
        # Check the canonical source independently; the old manifest remains frozen.
        assert len(book["chapters"]) == 2
        assert book["chapters"][0]["source"] == "tex/deep/ch01.tex"
        assert r"\input{deep/ch01}" in (ROOT/book["main"]).read_text()
        assert book["status"] == "chapter-two-production"
        anchor = book["preservedUndergraduateEdition"]["commit"]
        book = json.loads(subprocess.check_output(
            ["git", "show", anchor+":book/book.json"], cwd=ROOT, text=True))
    includes = re.findall(r"\\input\{([^}]+)\}", manifest)
    expected = [str(Path(chapter["source"]).relative_to("tex").with_suffix(""))
                for chapter in book["chapters"]]
    assert includes == expected
    for chapter in book["chapters"]:
        assert chapter["status"] == "internally-reviewed-draft"
        assert (ROOT / chapter["source"]).is_file()


def test_chapter_example_artifacts_are_current():
    subprocess.run([sys.executable, "scripts/chapter01_artifacts.py", "--check"],
                   cwd=ROOT, check=True)
    subprocess.run([sys.executable, "scripts/chapter02_artifacts.py", "--check"],
                   cwd=ROOT, check=True)


def test_scientific_figure_matches_canonical_source():
    sys.path.insert(0, str(ROOT / "scripts"))
    from render_chapter02 import svg
    source = ROOT / "book/diagrams/evo-g07.txt"
    expected = svg(*MODULE.parse_graph(source))
    assert (ROOT / "book/figures" / (source.stem + ".svg")).read_text() == expected


def test_scientific_figure_rejects_unrepresented_relation():
    sys.path.insert(0, str(ROOT / "scripts"))
    from render_chapter02 import svg
    import pytest
    meta, nodes, edges = MODULE.parse_graph(ROOT / "book/diagrams/evo-g07.txt")
    with pytest.raises(ValueError, match="unsupported"):
        svg(meta, nodes, edges + [("n3", "n1", "CONTROL", "unrepresented feedback")])


def test_every_graph_is_complete_and_has_generated_svg():
    sources = sorted((ROOT / "book/diagrams").glob("*.txt"))
    assert sources
    ids = []
    for source in sources:
        meta, nodes, edges = MODULE.parse_graph(source)
        ids.append(meta["ID"])
        if meta.get("LAYOUT") == "chapter02":
            assert len(nodes) >= 3 and len(edges) >= 2
        else:
            assert len(nodes) == 6 and len(edges) >= 7
        assert meta["EVIDENCE"] and meta["FAILURE"] and meta["READING"]
        assert "→" in source.read_text()
        svg = ROOT / "book/figures" / (source.stem + ".svg")
        assert svg.is_file()
        assert 'aria-labelledby="title desc"' in svg.read_text()
    assert len(ids) == len(set(ids))


def test_graph_parser_rejects_dangling_edges(tmp_path):
    source = next((ROOT / "book/diagrams").glob("*.txt"))
    invalid = tmp_path / "bad.txt"
    invalid.write_text(source.read_text().replace("EDGE n1 → n2", "EDGE n1 → missing"))
    import pytest
    with pytest.raises(ValueError, match="dangling edge"):
        MODULE.parse_graph(invalid)


def test_active_markdown_relative_links_resolve():
    paths = list(ROOT.glob("*.md"))
    for folder in ["research", "book"]:
        paths.extend((ROOT / folder).rglob("*.md"))
    for path in paths:
        for target in re.findall(r"\]\(([^)]+)\)", path.read_text()):
            if "://" in target or target.startswith("#"):
                continue
            local = target.split("#")[0]
            assert (path.parent / local).exists(), (str(path.relative_to(ROOT)), target)


def test_old_book_and_research_are_byte_preserved():
    snapshot = "9df0d006e10e56cd836a4b84400009dab3cbf4f2"
    listing = subprocess.check_output(
        ["git", "ls-tree", "-r", "--name-only", snapshot, "book", "research"],
        cwd=ROOT, text=True).splitlines()
    assert listing
    for path in listing:
        expected = subprocess.check_output(["git", "show", f"{snapshot}:{path}"], cwd=ROOT)
        assert (ROOT / "historical/pre-reboot" / path).read_bytes() == expected, path
