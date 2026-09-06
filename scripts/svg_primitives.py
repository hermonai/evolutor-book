"""Small deterministic SVG primitives for scientific teaching figures."""
from html import escape
import textwrap

BLUE = "#23577d"
INK = "#19324a"

class Canvas:
    def __init__(self, meta, width=1000, height=880):
        desc = " ".join(meta.get(key, "") for key in ("EVIDENCE", "LEGEND", "READING", "FAILURE"))
        self.parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
            f'<title id="title">{escape(meta["ID"] + ": " + meta["TITLE"])}</title>',
            f'<desc id="desc">{escape(desc)}</desc>',
            '<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#23577d"/></marker><marker id="bar" markerWidth="10" markerHeight="16" refX="5" refY="8" orient="auto"><path d="M5,1 V15" stroke="#23577d" stroke-width="2"/></marker></defs>',
            f'<rect width="{width}" height="{height}" fill="white"/>']
    def text(self, x, y, value, size=20, bold=False, anchor="start", color=INK):
        self.parts.append(f'<text x="{x}" y="{y}" font-family="DejaVu Sans, sans-serif" font-size="{size}" font-weight="{"bold" if bold else "normal"}" text-anchor="{anchor}" fill="{color}">{escape(str(value))}</text>')
    def lines(self, x, y, value, width=75, size=18, step=25):
        for i, line in enumerate(textwrap.wrap(value, width)):
            self.text(x, y + i * step, line, size)
    def box(self, x, y, w, h, fill="#eff5fa", radius=12):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="#adbfce" stroke-width="1.4"/>')
    def path(self, d, *, dashed=False, marker=None, width=2.5, color=BLUE):
        dash = ' stroke-dasharray="6 5"' if dashed else ""
        end = f' marker-end="url(#{marker})"' if marker else ""
        self.parts.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}"{dash}{end}/>')
    def circle(self, x, y, radius, fill):
        self.parts.append(f'<circle cx="{x}" cy="{y}" r="{radius}" fill="{fill}" stroke="#7c97aa" stroke-width="1.3"/>')
    def finish(self):
        return "\n".join(self.parts + ["</svg>"]) + "\n"
