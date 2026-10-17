"""Render explicit current-PDF pages and color/grayscale contact sheets.

This creates inspectable images, not an automatic acceptance declaration.
"""

import argparse
import os
from pathlib import Path
import re
import subprocess

from PIL import Image, ImageDraw, ImageOps

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "output/pdf/evolutor-convergence.pdf"
OUT = ROOT / "tmp/pdfs/convergence-review"
ENV = dict(os.environ, PATH="/opt/homebrew/bin:/usr/local/bin:" + os.environ["PATH"])


def selected_pages(expression, total):
    if expression == "all":
        return list(range(1, total + 1))
    pages = set()
    for part in expression.split(","):
        bounds = [int(n) for n in part.split("-")]
        if len(bounds) == 1:
            pages.add(bounds[0])
        elif len(bounds) == 2 and bounds[0] <= bounds[1]:
            pages.update(range(bounds[0], bounds[1] + 1))
        else:
            raise ValueError("Expected comma-separated pages and inclusive ranges")
    if not pages or min(pages) < 1 or max(pages) > total:
        raise ValueError("Page selection is outside this PDF")
    return sorted(pages)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pages", default="all")
    args = parser.parse_args()
    info = subprocess.check_output(["pdfinfo", str(PDF)], env=ENV, text=True)
    total = int(re.search(r"Pages:\s+(\d+)", info)[1])
    pages = selected_pages(args.pages, total)
    OUT.mkdir(parents=True, exist_ok=True)
    for n in pages:
        subprocess.run(
            [
                "pdftoppm",
                "-f",
                str(n),
                "-l",
                str(n),
                "-r",
                "90",
                "-png",
                str(PDF),
                str(OUT / "page"),
            ],
            check=True,
            env=ENV,
        )
    for start in range(0, len(pages), 4):
        sheet = Image.new("RGB", (1280, 1870), "#D7DFE5")
        draw = ImageDraw.Draw(sheet)
        for k, n in enumerate(pages[start : start + 4]):
            source = OUT / ("page-" + str(n).zfill(len(str(total))) + ".png")
            thumb = ImageOps.contain(Image.open(source).convert("RGB"), (620, 890))
            x, y = 10 + (k % 2) * 640, 30 + (k // 2) * 935
            sheet.paste(thumb, (x, y))
            draw.text((x, y - 20), f"PDF page {n}", fill="black")
        name = f"contact-{start // 4 + 1}"
        sheet.save(OUT / (name + ".png"))
        ImageOps.grayscale(sheet).save(OUT / (name + "-gray.png"))
    print(
        {
            "pdf_pages": total,
            "rendered_pages": pages,
            "contact_sheets": (len(pages) + 3) // 4,
        }
    )


if __name__ == "__main__":
    main()
