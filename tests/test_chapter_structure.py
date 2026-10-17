import importlib.util
from pathlib import Path


def test_current_navigation_matches_authored_sources_and_staged_packages():
    path = Path(__file__).parents[1] / "scripts/check-chapter-structure.py"
    spec = importlib.util.spec_from_file_location("chapter_structure", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.check()
