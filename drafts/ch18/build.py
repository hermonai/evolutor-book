"""Build authored LaTeX only; generate data tables and literal tested code."""

import argparse
import ast
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DNA = False  # book identity must survive a checkout directory rename
NAME = ("dna-computing" if DNA else "evolutor") + "-ch18-review"
BUILD = ROOT / "build/ch18"


def derived():
    spec = importlib.util.spec_from_file_location(
        "chapter18_reference", HERE / "reference.py"
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    if hasattr(module, "torch"):
        module.torch.set_num_threads(1)
    r = module.results()
    files = {HERE / "results.json": json.dumps(r, indent=2) + "\n"}

    def table(name, headers, rows, fmt):
        lines = [
            r"\begin{tabular}{" + fmt + "}",
            r"\toprule",
            " & ".join(headers) + r"\\",
            r"\midrule",
        ]
        lines += [" & ".join(map(str, row)) + r"\\" for row in rows]
        lines += [r"\bottomrule", r"\end{tabular}"]
        files[BUILD / (name + ".tex")] = "\n".join(lines) + "\n"

    def plot(name, data, x, keys):
        styles = [
            "Blue,thick",
            "Red,dashed,thick",
            "Green,dashdotted,thick",
        ]
        lines = []
        for key, style in zip(keys, styles):
            points = " ".join(f"({v[x]:.12g},{v[key]:.12g})" for v in data)
            lines.append(
                r"\addplot[" + style + "] coordinates {" + points + "};"
            )
        files[BUILD / (name + ".tex")] = "\n".join(lines) + "\n"

    for name, headers, keys, fmt in module.TABLES:
        table(name, headers, [[v[k] for k in keys] for v in r[name]], fmt)
    for name, key, x, ys in module.PLOTS:
        plot(name, r[key], x, ys)
    selected = module.LISTINGS
    source = (HERE / "reference.py").read_text()
    tree = ast.parse(source)
    for name in selected:
        node = next(
            n for n in tree.body if getattr(n, "name", None) == name
        )
        first = min(
            [node.lineno]
            + [d.lineno for d in getattr(node, "decorator_list", [])]
        )
        files[BUILD / (name + ".py")] = (
            "\n".join(source.splitlines()[first - 1 : node.end_lineno])
            + "\n"
        )
    return files


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--check", action="store_true")
    p.add_argument("--assets-only", action="store_true")
    p.add_argument("--render", action="store_true")
    a = p.parse_args()
    for path, data in derived().items():
        if a.check:
            assert path.exists() and path.read_text() == data, str(path)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(data)
    if a.check or a.assets_only:
        print(
            "Chapter 18 computed artifacts verified"
            if a.check
            else "Chapter 18 computed artifacts generated"
        )
        return
    env = dict(os.environ, PATH="/Library/TeX/texbin:" + os.environ["PATH"])
    result = subprocess.run(
        [
            "latexmk",
            "-xelatex",
            "-interaction=nonstopmode",
            "-halt-on-error",
            "-outdir=" + str(BUILD),
            "review.tex",
        ],
        cwd=HERE,
        env=env,
        capture_output=True,
        text=True,
    )
    (BUILD / "console.log").write_text(result.stdout + result.stderr)
    if result.returncode:
        raise RuntimeError((result.stdout + result.stderr)[-6000:])
    log = (BUILD / "review.log").read_text()
    bad = [
        l
        for l in log.splitlines()
        if any(
            v in l
            for v in (
                "Overfull",
                "Missing character:",
                "undefined references",
                "multiply defined",
                "LaTeX Warning: Reference",
                "LaTeX Warning: Citation",
            )
        )
    ]
    if bad:
        raise RuntimeError("\n".join(bad))
    output = ROOT / "output/pdf" / (NAME + ".pdf")
    output.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(BUILD / "review.pdf", output)
    info = subprocess.check_output(["pdfinfo", str(output)], text=True)
    import re

    pages = int(re.search(r"Pages:\s+(\d+)", info)[1])
    record = {
        "pdf": str(output.relative_to(ROOT)),
        "pages": pages,
        "sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
        "status": "standalone authored-LaTeX review candidate; no acceptance promotion",
        "sources": {
            str(path.relative_to(ROOT)): hashlib.sha256(
                path.read_bytes()
            ).hexdigest()
            for path in sorted(HERE.rglob("*"))
            if path.is_file() and "__pycache__" not in path.parts
        },
    }
    (BUILD / "build-record.json").write_text(
        json.dumps(record, indent=2) + "\n"
    )
    if a.render:
        from PIL import Image, ImageOps, ImageDraw

        out = ROOT / "tmp/pdfs/ch18-review"
        out.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            [
                "pdftoppm",
                "-r",
                "110",
                "-png",
                str(output),
                str(out / "page"),
            ],
            check=True,
        )
        images = [
            out / f"page-{i:0{len(str(pages))}d}.png"
            for i in range(1, pages + 1)
        ]
        for start in range(0, pages, 4):
            sheet = Image.new("RGB", (1280, 1870), "#D7DFE5")
            draw = ImageDraw.Draw(sheet)
            for i, path in enumerate(images[start : start + 4]):
                thumb = ImageOps.contain(
                    Image.open(path).convert("RGB"), (620, 890)
                )
                x = 10 + (i % 2) * 640
                y = 30 + (i // 2) * 935
                sheet.paste(thumb, (x, y))
                draw.text(
                    (x, y - 20), f"Page {start + i + 1}", fill="black"
                )
            sheet.save(out / f"contact-{start // 4 + 1}.png")
            ImageOps.grayscale(sheet).save(
                out / f"grayscale-{start // 4 + 1}.png"
            )
    print(
        json.dumps(
            {k: v for k, v in record.items() if k != "sources"}, indent=2
        )
    )


if __name__ == "__main__":
    main()
