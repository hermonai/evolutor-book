"""Render canonical TXT graph records to accessible, deterministic SVGs."""
from pathlib import Path
from html import escape
import textwrap

ROOT = Path(__file__).resolve().parents[1]


def parse_graph(path):
    meta, nodes, edges = {}, {}, []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("NODE "):
            key, title, body = line[5:].split(" | ", 2)
            if key in nodes:
                raise ValueError(f"duplicate node {key}")
            nodes[key] = (title, body)
        elif line.startswith("EDGE "):
            pair, kind, label = line[5:].split(" | ", 2)
            start, end = pair.split(" → ")
            if kind not in {"DATA", "CONTROL", "HYPOTHESIS"}:
                raise ValueError(f"unknown edge type {kind}")
            edges.append((start, end, kind, label))
        elif ": " in line:
            key, value = line.split(": ", 1)
            meta[key] = value
    required = {"ID", "TITLE", "SUBTITLE", "EVIDENCE", "LEGEND", "READING", "FAILURE"}
    if required - meta.keys() or set(nodes) != {f"n{i}" for i in range(1, 7)}:
        raise ValueError(f"incomplete graph {path}")
    if any(a not in nodes or b not in nodes for a, b, _, _ in edges):
        raise ValueError("dangling edge")
    return meta, nodes, edges


def render(path):
    meta, nodes, edges = parse_graph(path)
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="920" viewBox="0 0 1000 920" role="img" aria-labelledby="title desc">',
           f'<title id="title">{escape(meta["ID"] + ": " + meta["TITLE"])}</title>',
           f'<desc id="desc">{escape(meta["EVIDENCE"] + " " + meta["READING"] + " Failure: " + meta["FAILURE"])}</desc>',
           '<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#245579"/></marker></defs>',
           '<rect width="1000" height="920" fill="white"/>']

    def text(x, y, value, size=18, color="#20334a", weight="normal", anchor="start"):
        out.append(f'<text x="{x}" y="{y}" font-family="DejaVu Sans, sans-serif" font-size="{size}" fill="{color}" font-weight="{weight}" text-anchor="{anchor}">{escape(value)}</text>')

    text(30, 36, meta["ID"] + "  /  EDITION 2 RESEARCH MAP", 15, "#245579", "bold")
    text(30, 77, meta["TITLE"], 28, weight="bold")
    text(30, 110, meta["SUBTITLE"], 18)
    pos = {f"n{i+1}": (30 if i < 3 else 600, 155 + (i % 3) * 185) for i in range(6)}
    for a, b, kind, label in edges:
        ax, ay = pos[a]; bx, by = pos[b]
        dash = '' if kind == "DATA" else ' stroke-dasharray="7 5"'
        if a == "n6" and b == "n2":
            route = 'M785,640 V682 H10 V395 H30'
            lx, ly, anchor = 500, 708, "middle"
        elif ax == bx and by > ay:
            route = f'M{ax+185},{ay+115} V{by}'
            lx, ly, anchor = ax+202, ay+151, "start"
        elif ay == by and bx > ax:
            route = f'M{ax+370},{ay+58} H{bx}'
            lx, ly, anchor = 500, ay+25, "middle"
        else:
            raise ValueError(f"layout not defined for {a} → {b}")
        out.append(f'<path d="{route}" fill="none" stroke="#245579" stroke-width="2"{dash} marker-end="url(#arrow)"/>')
        for j, line in enumerate(textwrap.wrap(label, 20)):
            text(lx, ly+j*18, line, 15, anchor=anchor)
    for key, (title, body) in nodes.items():
        x, y = pos[key]
        fill = "#eef5fb" if x == 30 else "#f2f7f2"
        out.append(f'<rect x="{x}" y="{y}" width="370" height="115" rx="9" fill="{fill}" stroke="#afc4d5"/>')
        text(x+15, y+28, title, 19, weight="bold")
        for j, line in enumerate(textwrap.wrap(body, 37)):
            text(x+15, y+55+j*22, line, 17)
    text(30, 744, "Solid: data / dependency     Dashed: control / review", 16, "#245579", "bold")
    y = 772
    for prefix, value in [("READING", meta["READING"]), ("BOUNDARY", meta["FAILURE"])]:
        for line in textwrap.wrap(prefix + ": " + value, 101):
            text(30, y, line, 16)
            y += 23
    text(30, 898, "Conceptual map. No measured superiority or physical validation is implied by an arrow.", 14)
    out.append('</svg>')
    target = ROOT / "book" / "figures" / (path.stem + ".svg")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("\n".join(out) + "\n", encoding="utf-8")
    return target


if __name__ == "__main__":
    for graph in sorted((ROOT / "book" / "diagrams").glob("*.txt")):
        print(render(graph).relative_to(ROOT))
