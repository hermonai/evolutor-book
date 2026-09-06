"""Render typed biological relations without implying a universal feedback loop."""
from pathlib import Path
from svg_primitives import Canvas, BLUE

ROOT = Path(__file__).resolve().parents[1]


def svg(meta, nodes, edges):
    if set(nodes) != {"n1", "n2", "n3", "n4"} or [(a, b, k) for a, b, k, _ in edges] != [
            ("n1", "n2", "DATA"), ("n2", "n3", "DATA"), ("n4", "n1", "CONTROL")]:
        raise ValueError("unsupported sequence/control graph contract")
    c = Canvas(meta, height=840)
    c.text(30, 35, meta["ID"] + " / BIOLOGICAL RELATIONS", 15, True, color=BLUE)
    c.text(30, 78, meta["TITLE"], 29, True)
    c.text(30, 111, meta["SUBTITLE"], 19)
    for node, x in (("n1", 35), ("n2", 380), ("n3", 725)):
        c.box(x, 160, 240, 190, "#f2f7fb")
        c.text(x+120, 195, nodes[node][0], 21, True, "middle")
    # Schematic sequence rails: symbolic architecture, not atom or protein structure.
    c.path("M65,245 H245", width=4)
    c.path("M65,280 H245", width=4)
    for x, y, label in ((48, 249, "5′"), (250, 249, "3′"), (48, 284, "3′"), (250, 284, "5′")):
        c.text(x, y, label, 12)
    for x in (85, 115, 145, 175, 205, 235):
        c.path(f"M{x},248 V277", dashed=True, width=1.4)
    c.text(155, 320, "paired sequence", 18, anchor="middle")
    c.path("M410,260 Q430,225 450,260 T490,260 T530,260 T560,260", width=4)
    c.text(500, 320, "coding transcript", 18, anchor="middle")
    c.path("M765,265 L800,240 L835,270 L870,235 L910,263", width=3)
    for x, y in ((765, 265), (800, 240), (835, 270), (870, 235), (910, 263)):
        c.circle(x, y, 11, "#c8dccd")
    c.text(845, 320, "amino-acid chain", 18, anchor="middle")
    for start, end, label in ((275, 380, "transcription"), (620, 725, "translation")):
        c.path(f"M{start},265 H{end}", marker="arrow")
        c.text((start+end)/2, 236, label, 14, anchor="middle")
    c.box(35, 460, 285, 145, "#f3f6ed")
    c.text(55, 495, nodes["n4"][0], 21, True)
    c.lines(55, 528, "Separate factor; origin not shown. Acts at a DNA control site.", width=26, size=18, step=23)
    c.path("M155,460 V362", dashed=True, marker="bar")
    c.text(180, 395, "repression", 18, True)
    c.text(180, 421, "control, not sequence copying", 17)
    c.box(440, 460, 525, 145, "#fff9ee")
    c.text(460, 495, "What the diagram does not assert", 21, True)
    c.lines(460, 531, "No reverse translation. No universal feedback loop. No claim that all RNA is translated.", width=46, size=18, step=25)
    c.text(35, 654, "Solid arrow: sequence transfer   |   dashed T-ended line: inhibitory control", 18, True)
    c.lines(35, 697, "READING: " + meta["READING"], width=97, size=16, step=22)
    c.lines(35, 775, "BOUNDARY: " + meta["FAILURE"], width=97, size=16, step=22)
    return c.finish()


def render_chapter02(path, meta, nodes, edges):
    target = ROOT / "book/figures" / (path.stem + ".svg")
    target.write_text(svg(meta, nodes, edges))
    return target
