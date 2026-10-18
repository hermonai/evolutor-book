"""Assemble the active authored sources into one continuous review candidate.

Frozen editions and chapter sources are not edited. Derived TeX only rewrites
citation keys to an explicit bibliography map; label namespaces are scoped in
the wrapper. A successful build is not visual/scientific acceptance.
"""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
BOOK = "evolutor"
BUILD = ROOT / "build/convergence"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def bib_items(text):
    """Read the book's simple authored bibitem environments; reject ambiguity."""
    blocks = re.findall(
        r"\\begin\{thebibliography\}\{[^}]*\}(.*?)\\end\{thebibliography\}",
        text,
        flags=re.S,
    )
    items = []
    for block in blocks:
        matches = list(re.finditer(r"\\bibitem\{([^}]+)\}", block))
        for i, match in enumerate(matches):
            end = matches[i + 1].start() if i + 1 < len(matches) else len(block)
            items.append((match[1], block[match.end() : end].strip()))
    if len({k for k, _ in items}) != len(items):
        raise ValueError("Duplicate bibitem key within one source")
    return items


def strip_bib(text):
    return re.sub(
        r"\\begin\{thebibliography\}\{[^}]*\}.*?\\end\{thebibliography\}",
        "",
        text,
        flags=re.S,
    )


def identity(body):
    """Conservative exact primary identifier matching, not fuzzy title guessing."""
    dois = re.findall(r"https?://doi\.org/([^}\s]+)", body)
    if dois:
        return "doi:" + dois[0].rstrip(".").lower()
    # One arXiv identifier names one work across abs/html/pdf views and
    # versions; per-version access notes stay in the bibliography map.
    arxiv = re.search(
        r"arxiv\.org/(?:abs|html|pdf)/(\d{4}\.\d{4,5})(?:v\d+)?", body
    )
    if arxiv:
        return "arxiv:" + arxiv[1]
    urls = re.findall(r"\\(?:url|href)\{(https?://[^}]+)\}", body)
    if urls:
        # URL paths can be case-sensitive; never merge distinct paths by case.
        return "url:" + urls[0].rstrip("/")
    return "text:" + re.sub(r"\s+", " ", body)


def remap_cites(text, mapping):
    def rewrite(match):
        keys = [k.strip() for k in match[1].split(",")]
        missing = set(keys) - mapping.keys()
        if missing:
            raise ValueError(f"Unresolved citation keys: {sorted(missing)}")
        return r"\cite{" + ",".join(mapping[k] for k in keys) + "}"

    return re.sub(r"\\cite\{([^}]+)\}", rewrite, text)


def safe_figure_loop_variable(text):
    """Alpha-rename a reserved TikZ loop variable in derived figures only.

    Some legacy plates use the LaTeX cross-reference command as a loop variable.
    Its redefinition conflicts with scoped book labels on current PGF/Hyperref.
    Do not change the artwork, its geometry or historical reviewed source bytes.
    Reject mixed uses rather than accidentally renaming a real reference label.
    """
    if not re.search(r"\\foreach\s+[^{}]*?/\\label\b", text):
        return text
    if re.search(r"\\label\s*\{", text) or r"\EvolutorLoopText" in text:
        raise ValueError("Ambiguous figure label/loop-variable use")
    return re.sub(r"\\label\b", lambda _: r"\EvolutorLoopText", text)


def cumulative_layout(number, text):
    """A reviewed local pagination adjustment, without changing chapter sources."""
    if number == 37:
        # In the continuous geometry the opening definition otherwise leaves
        # its final word alone above the display on the next physical page.
        heading = r"\section{Construct the next mixed iteration}"
        text = text.replace(heading, r"\Needspace{8\baselineskip}" + "\n" + heading)
    return text


EVIDENCE_CHAPTER_HEAD = re.compile(
    r"\A(\s*)\\chapter\*\{([^{}]*)\}(?:(\s*)\\addcontentsline\{toc\}\{chapter\}\{\2\})?"
)


def evidence_heading(text):
    """Typeset a chapter's source note as a section of that chapter.

    Standalone review PDFs open the note as an unnumbered chapter; in the
    continuous book that would start a page and add a chapter-level contents
    entry. Only the derived copy changes.
    """
    def section(match):
        lead, title, gap = match[1], match[2], match[3]
        head = lead + rf"\section*{{{title}}}"
        if gap is not None:
            head += gap + rf"\addcontentsline{{toc}}{{section}}{{{title}}}"
        return head

    return EVIDENCE_CHAPTER_HEAD.sub(section, text, count=1)


def chapter_dir(number):
    name = f"ch{number:02d}"
    if BOOK == "dna-computing" and number == 17:
        name += "-theory"
    return ROOT / "drafts" / name


GUIDES = ROOT / "tex/convergence/chapter-guides.json"
CHAPTER_HEAD = re.compile(
    r"\\chapter\{(?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*\}(?:[ \t]*\\label\{[^}]*\})?"
)
EXERCISES_HEAD = re.compile(
    r"\\section\*?\{(?:Exercises|Twenty worked|Twelve worked|Worked|Final exercises)"
)


def chapter_guides():
    """Reader-facing goals and key ideas: book apparatus, not chapter sources."""
    data = json.loads(GUIDES.read_text())
    guides = {}
    for entry in data["chapters"]:
        number = entry["chapter"]
        goals, ideas = entry["goals"], entry["key_ideas"]
        if number in guides:
            raise ValueError(f"Duplicate chapter guide: {number}")
        if not (3 <= len(goals) <= 5 and 3 <= len(ideas) <= 5):
            raise ValueError(f"Chapter {number} guide needs 3-5 goals and ideas")
        guides[number] = entry
    if sorted(guides) != list(range(1, len(guides) + 1)):
        raise ValueError("Chapter guides must cover a contiguous chapter range")
    return guides


def guide_files(number, guide):
    """Render one chapter's opening goals and closing key ideas."""
    out = BUILD / "guides"
    out.mkdir(parents=True, exist_ok=True)
    items = lambda xs: "\n".join(rf"\item {x}" for x in xs)
    (out / f"ch{number:02d}-goals.tex").write_text(
        "\\begin{ChapterGoals}\n" + items(guide["goals"]) + "\n\\end{ChapterGoals}\n"
    )
    (out / f"ch{number:02d}-ideas.tex").write_text(
        "\\begin{KeyIdeas}\n" + items(guide["key_ideas"]) + "\n\\end{KeyIdeas}\n"
    )


def inject_guide(number, text):
    """Place goals after the chapter heading and key ideas before exercises.

    Only derived copies change. The chapter-level label is unscoped so the
    contents-at-a-glance page can reference every chapter uniformly.
    """
    head = CHAPTER_HEAD.search(text)
    exercises = EXERCISES_HEAD.search(text)
    if head is None or exercises is None or exercises.start() < head.end():
        raise ValueError(f"Chapter {number}: guide anchors not found")
    goals = (
        "\n" + rf"\OriginalBookLabel{{book:ch{number:02d}}}"
        + rf"\input{{../build/convergence/guides/ch{number:02d}-goals}}" + "\n"
    )
    ideas = rf"\input{{../build/convergence/guides/ch{number:02d}-ideas}}" + "\n"
    return (
        text[: head.end()]
        + goals
        + text[head.end() : exercises.start()]
        + ideas
        + text[exercises.start() :]
    )


def structure():
    return json.loads((ROOT / "chapter-structure.json").read_text())


def part_opener(part, chapters):
    """Part page body: orientation file plus the generated chapter list."""
    source = ROOT / f"tex/convergence/parts/part{part['number']:02d}.tex"
    if not source.is_file():
        raise ValueError(f"Missing part opener: {source.name}")
    rows = [
        rf"\PartChapter{{{c['number']}}}{{{c['title']}}}{{{c['purpose']}}}"
        for c in chapters
        if part["start"] <= c["number"] <= part["end"]
    ]
    out = BUILD / "parts"
    out.mkdir(parents=True, exist_ok=True)
    body = (
        source.read_text().rstrip()
        + "\n\\begin{PartChapters}\n"
        + "\n".join(rows)
        + "\n\\end{PartChapters}\n"
    )
    (out / f"part{part['number']:02d}.tex").write_text(body)
    return (
        rf"\EvolutorPart{{{part['number']}}}{{{part['title']}}}"
        + rf"{{../build/convergence/parts/part{part['number']:02d}}}"
    )


def contents_at_a_glance(data):
    lines = [r"\begin{GlanceTable}"]
    for part in data["parts"]:
        lines.append(rf"\GlancePart{{{part['number']}}}{{{part['title']}}}")
        for c in data["chapters"]:
            if part["start"] <= c["number"] <= part["end"]:
                lines.append(
                    rf"\GlanceChapter{{{c['number']}}}{{{c['title']}}}"
                    + rf"{{book:ch{c['number']:02d}}}"
                )
    lines.append(r"\end{GlanceTable}")
    (BUILD / "glance.tex").write_text("\n".join(lines) + "\n")


def part_starts():
    """The same twelve-part navigation drives the source map and printed book."""
    data = json.loads((ROOT / "chapter-structure.json").read_text())
    parts = data["parts"]
    coverage = [n for p in parts for n in range(p["start"], p["end"] + 1)]
    if coverage != list(range(1, data["planned_chapters"] + 1)):
        raise ValueError("Part ranges must cover the planned spine exactly once")
    return {p["start"]: p["title"] for p in parts}


def run(command, cwd=ROOT):
    subprocess.run(
        command,
        cwd=cwd,
        check=True,
        env=dict(
            os.environ,
            OMP_NUM_THREADS="1",
            PATH="/Library/TeX/texbin:" + os.environ["PATH"],
        ),
    )


def prepare(through, refresh):
    BUILD.mkdir(parents=True, exist_ok=True)
    deep = ROOT / "build/deep-figures"
    deep.mkdir(parents=True, exist_ok=True)
    svgs = sorted((ROOT / "book/figures/deep").glob("*.svg"))
    svgs += sorted((ROOT / "drafts/ch03/figures").glob("*.svg"))
    for source in svgs:
        output = deep / (source.stem + ".pdf")
        if (
            refresh
            or not output.exists()
            or source.stat().st_mtime > output.stat().st_mtime
        ):
            run(["rsvg-convert", "-f", "pdf", "-o", str(output), str(source)])
    for number in range(4, through + 1):
        directory = chapter_dir(number)
        if not (directory / "manuscript.tex").is_file():
            raise ValueError(f"Active manuscript missing: chapter {number}")
        generated = ROOT / "build" / directory.name
        if refresh or not generated.exists():
            run([sys.executable, str(directory / "build.py"), "--assets-only"])
    return svgs


def assemble(through):
    opening = ROOT / "tex/deep/references-ch01-02.tex"
    opening_items = bib_items(opening.read_text())
    entries = {}
    seen = {}
    provenance = []
    for key, body in opening_items:
        entries[key] = body
        # Preserve the frozen opening's key references even if identifiers repeat.
        seen.setdefault(identity(body), key)
        provenance.append(
            {
                "source": str(opening.relative_to(ROOT)),
                "original_key": key,
                "book_key": key,
            }
        )
    parts = part_starts()
    data = structure()
    guides = chapter_guides()
    openers = {
        p["start"]: part_opener(p, data["chapters"]) for p in data["parts"]
    }
    contents_at_a_glance(data)
    opening = BUILD / "opening"
    opening.mkdir(parents=True, exist_ok=True)
    wrappers = []
    # Opening chapters keep their preserved sources; only derived copies gain
    # the book-level guide boxes. Their \input paths resolve from tex/.
    for number, source in (
        (1, ROOT / "tex/deep/ch01.tex"),
        (2, ROOT / "tex/deep/ch02.tex"),
        (3, ROOT / "tex/textbook/ch03.tex"),
    ):
        if number in openers:
            wrappers.append(openers[number])
        guide_files(number, guides[number])
        (opening / f"ch{number:02d}.tex").write_text(
            inject_guide(number, source.read_text())
        )
        wrappers.append(rf"\input{{../build/convergence/opening/ch{number:02d}}}")
    for number in range(4, through + 1):
        if number in parts:
            wrappers.append(openers[number])
        guide_files(number, guides[number])
        directory = chapter_dir(number)
        source_file = directory / "sources.tex"
        source = source_file.read_text()
        items = bib_items(source)
        mapping = {}
        for key, body in items:
            ident = identity(body)
            book_key = seen.get(ident, f"ch{number:02d}:{key}")
            seen[ident] = book_key
            # Current later record supersedes earlier display metadata for the
            # same exact identifier, retaining all contributing source records.
            entries[book_key] = body
            mapping[key] = book_key
            provenance.append(
                {
                    "source": str(source_file.relative_to(ROOT)),
                    "original_key": key,
                    "book_key": book_key,
                    "matched_identifier": ident,
                }
            )
        out = BUILD / f"ch{number:02d}"
        out.mkdir(parents=True, exist_ok=True)

        def rewrite_local_inputs(text):
            def replace(match):
                target = match[1]
                if (directory / target).is_file():
                    return rf"\input{{../build/convergence/ch{number:02d}/{target}}}"
                return match[0]

            return re.sub(r"\\input\{([^}]+)\}", replace, text)

        for authored in directory.glob("*.tex"):
            if authored.name in ("review.tex", "sources.tex"):
                continue
            text = cumulative_layout(number, authored.read_text())
            if authored.name == "manuscript.tex":
                text = inject_guide(number, text)
            (out / authored.name).write_text(
                rewrite_local_inputs(remap_cites(text, mapping))
            )
        (out / "evidence.tex").write_text(
            remap_cites(evidence_heading(strip_bib(source)), mapping)
        )
        figures = out / "figures"
        figures.mkdir(exist_ok=True)
        for figure in sorted((directory / "figures").glob("*.tex")):
            (figures / figure.name).write_text(
                remap_cites(safe_figure_loop_variable(figure.read_text()), mapping)
            )
        wrappers.extend(
            [
                r"\clearpage\begingroup",
                rf"\def\ChapterNamespace{{ch{number:02d}:}}",
                rf"\def\Generated{{../build/{directory.name}}}",
                rf"\def\PlateDirectory{{../build/convergence/ch{number:02d}/figures}}",
                r"\ScopedChapterLabels",
                rf"\input{{../build/convergence/ch{number:02d}/manuscript.tex}}",
                rf"\input{{../build/convergence/ch{number:02d}/evidence.tex}}",
                r"\clearpage\endgroup",
            ]
        )
    (BUILD / "chapters.tex").write_text("\n".join(wrappers) + "\n")
    # Front/back matter written for the continuous book. Its own references
    # join the single bibliography through the same exact-identifier rule.
    matter = ROOT / "tex/convergence/matter"
    matter_sources = matter / "sources.tex"
    mapping = {}
    for key, body in bib_items(matter_sources.read_text()):
        ident = identity(body)
        book_key = seen.get(ident, f"matter:{key}")
        seen[ident] = book_key
        entries.setdefault(book_key, body)
        mapping[key] = book_key
        provenance.append(
            {
                "source": str(matter_sources.relative_to(ROOT)),
                "original_key": key,
                "book_key": book_key,
                "matched_identifier": ident,
            }
        )
    derived = BUILD / "matter"
    derived.mkdir(parents=True, exist_ok=True)
    for authored in sorted(matter.glob("*.tex")):
        if authored.name != "sources.tex":
            (derived / authored.name).write_text(
                remap_cites(authored.read_text(), mapping)
            )
    bibliography = [
        r"\begin{thebibliography}{999}",
        r"\addcontentsline{toc}{chapter}{Bibliography}",
    ]
    bibliography += [rf"\bibitem{{{k}}} {v}" for k, v in entries.items()]
    bibliography.append(r"\end{thebibliography}")
    (BUILD / "bibliography.tex").write_text("\n\n".join(bibliography) + "\n")
    (BUILD / "bibliography-map.json").write_text(
        json.dumps(provenance, indent=2) + "\n"
    )
    (BUILD / "scope.tex").write_text(rf"\def\IncludedThrough{{{through}}}" + "\n")
    return provenance


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--through", type=int, required=True)
    parser.add_argument("--refresh-assets", action="store_true")
    parser.add_argument("--prepare-only", action="store_true")
    args = parser.parse_args()
    maximum = 32 if BOOK == "dna-computing" else 52
    if not 4 <= args.through <= maximum:
        parser.error(f"--through must be between 4 and {maximum}")
    svgs = prepare(args.through, args.refresh_assets)
    provenance = assemble(args.through)
    if args.prepare_only:
        print("Derived chapter wrappers and consolidated bibliography prepared.")
        return
    name = BOOK + "-convergence"
    command = [
        "latexmk",
        "-xelatex",
        "-interaction=nonstopmode",
        "-halt-on-error",
        "-outdir=../build/convergence",
        "convergence/book.tex",
        "-jobname=" + name,
    ]
    result = subprocess.run(
        command,
        cwd=ROOT / "tex",
        capture_output=True,
        text=True,
        env=dict(os.environ, PATH="/Library/TeX/texbin:" + os.environ["PATH"]),
    )
    (BUILD / "console.log").write_text(result.stdout + result.stderr)
    if result.returncode:
        raise RuntimeError((result.stdout + result.stderr)[-6000:])
    # Regenerate explicitly: a stale .ind can survive host latexmk defaults.
    index = subprocess.run(
        ["makeindex", "-o", name + ".ind", name + ".idx"],
        cwd=BUILD,
        env=dict(os.environ, PATH="/Library/TeX/texbin:" + os.environ["PATH"]),
        capture_output=True,
        text=True,
        check=True,
    )
    rerun = subprocess.run(
        result.args,
        cwd=ROOT / "tex",
        env=dict(os.environ, PATH="/Library/TeX/texbin:" + os.environ["PATH"]),
        capture_output=True,
        text=True,
    )
    with (BUILD / "console.log").open("a") as stream:
        stream.write(index.stdout + index.stderr + rerun.stdout + rerun.stderr)
    if rerun.returncode:
        raise RuntimeError((rerun.stdout + rerun.stderr)[-6000:])
    log = (BUILD / (name + ".log")).read_text()
    failures = [
        line
        for line in log.splitlines()
        if any(
            s in line
            for s in (
                "Overfull",
                "Missing character:",
                "undefined references",
                "multiply defined",
                "LaTeX Warning: Reference",
                "LaTeX Warning: Citation",
            )
        )
    ]
    (BUILD / "warning-audit.json").write_text(
        json.dumps({"release_blocking_warnings": failures}, indent=2) + "\n"
    )
    if failures:
        raise RuntimeError("\n".join(failures))
    output = ROOT / "output/pdf" / (name + ".pdf")
    output.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(BUILD / (name + ".pdf"), output)
    info = subprocess.check_output(["pdfinfo", str(output)], text=True)
    paths = (
        list((ROOT / "tex").rglob("*.tex"))
        + svgs
        + [
            Path(__file__),
            ROOT / "chapter-structure.json",
            GUIDES,
        ]
        + sorted((ROOT / "tex/convergence/figures").glob("*.txt"))
    )
    for number in range(4, args.through + 1):
        paths.extend(
            p
            for p in chapter_dir(number).rglob("*")
            if p.is_file() and "__pycache__" not in p.parts
        )
    record = {
        "book": BOOK,
        "through": args.through,
        "status": "continuous authored-source build; visual/editorial acceptance pending",
        "complete_planned_range": args.through == maximum,
        "pdf": str(output.relative_to(ROOT)),
        "pages": int(re.search(r"Pages:\s+(\d+)", info)[1]),
        "pdf_sha256": sha(output),
        "bibliography_contributions": len(provenance),
        "source_hashes": {str(p.relative_to(ROOT)): sha(p) for p in sorted(set(paths))},
    }
    (BUILD / "build-record.json").write_text(json.dumps(record, indent=2) + "\n")
    print(
        json.dumps({k: v for k, v in record.items() if k != "source_hashes"}, indent=2)
    )


if __name__ == "__main__":
    main()
