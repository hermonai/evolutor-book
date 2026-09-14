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
NAME = ("dna-computing" if DNA else "evolutor") + "-ch04-review"
BUILD = ROOT / "build/ch04"


def derived():
    spec = importlib.util.spec_from_file_location(
        "chapter4_reference", HERE / "reference.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if not DNA:
        module.torch.set_num_threads(1)
    r = module.results()
    files = {HERE / "results.json": json.dumps(r, indent=2) + "\n"}
    if DNA:
        table = [
            r"\begin{tabular}{rrrr}",
            r"\toprule",
            r"$n$ & $(n-2)!$ orders & Copies, 99\% & Volume at 1 nM (L)\\",
            r"\midrule",
        ]
        for row in r["resource_table"]:
            table.append(
                f"{row['vertices']} & {row['candidate_orders']:.3e} & {row['copies_99pct_one_witness']:.3e} & {row['litres']:.3e}"
                + r"\\"
            )
        table += [r"\bottomrule", r"\end{tabular}"]
        files[BUILD / "resources.tex"] = "\n".join(table) + "\n"
        plot = []
        for key, style in [
            ("independent", "blue,mark=*"),
            ("shared_failure_10pct", "red,dashed,mark=square*"),
        ]:
            pts = " ".join(
                f"({row['copies']},{row[key]:.12g})"
                for row in r["miss_curves"]
            )
            plot.append(
                r"\addplot[" + style + "] coordinates {" + pts + "};"
            )
        files[BUILD / "miss-plot.tex"] = "\n".join(plot) + "\n"
        selected = ["required_copies", "finite_pool_miss", "inventory"]
    else:
        table = [
            r"\begin{tabular}{rrrr}",
            r"\toprule",
            r"Update & Epoch & Targets & Training loss\\",
            r"\midrule",
        ]
        for row in r["training"]:
            table.append(
                f"{row['update']} & {row['epoch']} & {row['scored_targets']} & {row['loss']:.6f}"
                + r"\\"
            )
        table += [r"\bottomrule", r"\end{tabular}"]
        files[BUILD / "training.tex"] = "\n".join(table) + "\n"
        table = [
            r"\begin{tabular}{lrrr}",
            r"\toprule",
            r"Restored state & Max.\ error & Same rows? & Same losses?\\",
            r"\midrule",
        ]
        for key, row in r["restart"].items():
            table.append(
                key.replace("_", r"\_")
                + f" & {row['max_parameter_error']:.6f} & "
                + ("yes" if row["same_batch_trace"] else "no")
                + " & "
                + ("yes" if row["same_loss_trace"] else "no")
                + r"\\"
            )
        table += [r"\bottomrule", r"\end{tabular}"]
        files[BUILD / "restart.tex"] = "\n".join(table) + "\n"
        coordinates = " ".join(
            f"({row['max_parameter_error']:.15g},{i}) [{row['max_parameter_error']:.6f}]"
            for i, row in enumerate(r["restart"].values())
        )
        files[BUILD / "restart-plot.tex"] = (
            r"\addplot[fill=Blue!35,draw=Blue] coordinates {"
            + coordinates
            + "};\n"
        )
        selected = [
            "collate",
            "masked_loss",
            "Run.step",
            "Run.checkpoint",
            "Run.restore",
        ]
    source = (HERE / "reference.py").read_text()
    tree = ast.parse(source)
    for name in selected:
        nodes = tree.body
        for part in name.split("."):
            node = next(
                n for n in nodes if getattr(n, "name", None) == part
            )
            nodes = getattr(node, "body", [])
        import textwrap

        segment = textwrap.dedent(
            ast.get_source_segment(source, node, padded=True)
        )
        # ast excludes a method's decorator; the printed restore listing declares it.
        if name == "Run.restore":
            segment = "@classmethod\n" + segment
        files[BUILD / (name.replace(".", "-") + ".py")] = segment + "\n"
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
            "Chapter 4 computed artifacts verified"
            if a.check
            else "Chapter 4 computed artifacts generated"
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

        out = ROOT / "tmp/pdfs/ch04-review"
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
