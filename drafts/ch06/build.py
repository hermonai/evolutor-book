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
NAME = ("dna-computing" if DNA else "evolutor") + "-ch06-review"
BUILD = ROOT / "build/ch06"


def derived():
    spec = importlib.util.spec_from_file_location(
        "chapter6_reference", HERE / "reference.py"
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    if not DNA:
        module.torch.set_num_threads(1)
    r = module.results()
    files = {HERE / "results.json": json.dumps(r, indent=2) + "\n"}
    if DNA:
        rows = [
            r"\begin{tabular}{lrrrr}",
            r"\toprule",
            r"Sequence & $\Delta H^\circ$ & $\Delta S^\circ$ & $K_d$ (nM) & $T_m$ ($^\circ$C)\\",
            r"\midrule",
        ]
        for v in r["sequence_comparison"]:
            rows.append(
                f"{v['sequence']} & {v['dh_kcal']:.1f} & {v['ds_cal']:.1f} & {v['kd_37_m'] * 1e9:.3f} & {v['tm_100nm_c']:.2f}"
                + r"\\"
            )
        selected = [
            "duplex_molar",
            "kd_from_thermo",
            "nn_parameters",
            "melting_kelvin",
        ]
        nn = [
            r"\begin{tabular}{lrr}",
            r"\toprule",
            r"Upper step & $\Delta H^\circ$ (kcal/mol) & $\Delta S^\circ$ (cal/mol/K)\\",
            r"\midrule",
        ]
        for key, (h, s) in r["nn_table"].items():
            nn.append(f"{key} & {h:.1f} & {s:.1f}" + r"\\")
        nn += [r"\bottomrule", r"\end{tabular}"]
        files[BUILD / "parameters.tex"] = "\n".join(nn) + "\n"
        for name, data, x, keys in [
            (
                "binding",
                r["concentration_curve"],
                "b_nm",
                ["exact_fraction", "excess_approximation"],
            ),
            (
                "melting",
                r["melting_curve"],
                "celsius",
                ["10", "100", "1000"],
            ),
        ]:
            lines = []
            for key, style in zip(
                keys,
                [
                    "Blue,thick",
                    "Red,dashed,thick",
                    "Green,dashdotted,thick",
                ],
            ):
                points = " ".join(f"({v[x]},{v[key]:.10g})" for v in data)
                lines.append(
                    r"\addplot[" + style + "] coordinates {" + points + "};"
                )
            files[BUILD / (name + "-plot.tex")] = "\n".join(lines) + "\n"
    else:
        rows = [
            r"\begin{tabular}{lrrl}",
            r"\toprule",
            r"Boundary policy & Final state & $\partial h_4/\partial a$ & $\partial h_4/\partial x$\\",
            r"\midrule",
        ]
        for name, v in r["chunks"].items():
            grad = ", ".join(f"{a:g}" for a in v["input_gradient"])
            rows.append(
                f"{name} & {v['final']:.3f} & {v['parameter_gradient']:.3f} & [{grad}]"
                + r"\\"
            )
        selected = ["gru_step", "lstm_step", "scan_gru", "chunk_experiment"]
        lines = []
        for z, style in zip(
            [0.5, 0.9, 0.99],
            ["Blue,thick", "Red,dashed,thick", "Green,dashdotted,thick"],
        ):
            points = " ".join(
                f"({n},{z**n:.10g})" for n in range(0, 101, 2)
            )
            lines.append(
                r"\addplot[" + style + "] coordinates {" + points + "};"
            )
        files[BUILD / "retention-plot.tex"] = "\n".join(lines) + "\n"
    rows += [r"\bottomrule", r"\end{tabular}"]
    files[BUILD / "results-table.tex"] = "\n".join(rows) + "\n"
    source = (HERE / "reference.py").read_text()
    tree = ast.parse(source)
    for name in selected:
        node = next(
            n for n in tree.body if getattr(n, "name", None) == name
        )
        files[BUILD / (name + ".py")] = (
            ast.get_source_segment(source, node) + "\n"
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
            "Chapter 6 computed artifacts verified"
            if a.check
            else "Chapter 6 computed artifacts generated"
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

        out = ROOT / "tmp/pdfs/ch06-review"
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
