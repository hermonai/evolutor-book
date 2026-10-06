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


def chapter_dir(number):
    name = f"ch{number:02d}"
    if BOOK == "dna-computing" and number == 17:
        name += "-theory"
    return ROOT / "drafts" / name


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
    wrappers = [r"\input{deep/ch01}", r"\input{deep/ch02}", r"\input{textbook/ch03}"]
    for number in range(4, through + 1):
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
            (out / authored.name).write_text(
                rewrite_local_inputs(remap_cites(authored.read_text(), mapping))
            )
        (out / "evidence.tex").write_text(remap_cites(strip_bib(source), mapping))
        figures = out / "figures"
        figures.mkdir(exist_ok=True)
        for figure in sorted((directory / "figures").glob("*.tex")):
            (figures / figure.name).write_text(remap_cites(figure.read_text(), mapping))
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
    paths = list((ROOT / "tex").rglob("*.tex")) + svgs + [Path(__file__)]
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
