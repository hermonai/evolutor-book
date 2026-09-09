"""Build only working-draft assets; never update the accepted PDF or review."""
import argparse
import importlib.util
import json
import math
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_deep_chapter import txt, rect, line, circle, panel, envelope, BLUE, GREEN, RED, GRAY


def load_reference():
    spec = importlib.util.spec_from_file_location("draft_reference", HERE / "reference.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def dna_figure(kind, result):
    if kind == "certificate":
        s = panel(20, 20, 370, 110, "INSTANCE", ["Directed graph G", "Fixed endpoints s and t"])
        s += panel(510, 20, 370, 110, "CERTIFICATE", ["One proposed vertex order", "Length n; labels are explicit"])
        s += line(210, 130, 340, 190) + line(695, 130, 560, 190)
        s += panel(205, 190, 490, 140, "DETERMINISTIC VERIFIER",
                   ["Endpoints + every vertex exactly once", "Every consecutive pair is a graph edge"])
        s += line(330, 330, 210, 385) + line(570, 330, 690, 385)
        s += panel(20, 385, 405, 145, "ACCEPT", ["This order is a witness.", "Therefore this instance is YES."])
        s += panel(470, 385, 410, 145, "REJECT", ["This order fails.", "Another order may still succeed."])
        s += txt(450, 575, "A rejected certificate is not a proof that no witness exists.", 22, anchor="middle")
        return s, 610
    if kind == "states":
        s = txt(450, 35, "Different histories; the same remaining search", 26, "bold", "middle")
        for y, name, route in [(140, "PREFIX A", [0,1,2,3]), (330, "PREFIX B", [0,2,1,3])]:
            s += txt(30, y-60, name, 21, "bold")
            for i, vertex in enumerate(route):
                x = 65 + i*95
                if i: s += line(x-67, y, x-29, y)
                s += circle(x, y, str(vertex), fill="#E5F2E9" if i==3 else "#FFFFFF")
            s += txt(30, y+60, "Used vertices: {0, 1, 2, 3}", 20)
        s += line(380,140,485,215) + line(380,330,485,255)
        s += panel(485,165,395,150,"MERGED STATE",["S = {0, 1, 2, 3}", "last vertex = 3", "One Boolean reachability entry"])
        s += line(680,315,680,380)
        s += circle(680,412,"4",r=31)
        s += txt(680,475,"Remaining vertex",21,anchor="middle")
        s += txt(680,510,"Can edge 3 → 4 complete the path?",19,anchor="middle")
        s += rect(20,550,860,95)
        s += txt(35,582,["What is kept: used set + current endpoint + one witness predecessor.",
                         "What is forgotten: previous order, alternate-path counts, physical copies."],20)
        s += txt(450,685,"Illustrative five-vertex instance. Both drawn prefixes use legal directed edges.",20,anchor="middle")
        return s,715
    if kind == "reduction":
        s = txt(450, 35, "Split the pivot: incoming arcs end; outgoing arcs begin", 24, "bold", "middle")
        s += txt(25, 85, "Example cycle", 23, "bold")
        points = [(140, 180, "0"), (450, 180, "1"), (760, 180, "2")]
        s += line(169, 180, 418, 180) + line(479, 180, 728, 180)
        s += line(760, 209, 760, 265, arrow=False) + line(760, 265, 140, 265, arrow=False) + line(140, 265, 140, 212)
        for x, y, label in points: s += circle(x, y, label)
        s += txt(140, 135, "pivot", 21, anchor="middle")
        s += txt(25, 335, "Fixed-endpoint path after splitting vertex 0", 23, "bold")
        for i, label in enumerate(["s", "1", "2", "t"]):
            x = 120 + i * 220
            if i: s += line(x - 189, 405, x - 32, 405)
            s += circle(x, 405, label)
        s += txt(120, 460, "no incoming arcs", 20, anchor="middle")
        s += txt(780, 460, "no outgoing arcs", 20, anchor="middle")
        s += panel(20, 505, 860, 120, "BOTH DIRECTIONS MATTER",
                   ["Open a Hamiltonian cycle at the pivot to obtain an s–t path.",
                    "Identify s and t to close a Hamiltonian path into a cycle."])
        s += txt(450, 665, "The reduction transforms an instance; it does not find the cycle.", 21, anchor="middle")
        return s, 695
    if kind == "sat":
        s = txt(450, 35, "x[v,p] = true exactly when vertex v occupies position p", 24, "bold", "middle")
        s += txt(330, 88, "position p", 21)
        for p in range(4): s += txt(245 + p * 100, 120, str(p), 21, anchor="middle")
        for v in range(4):
            s += txt(130, 175 + v * 65, "v = " + str(v), 21)
            for p in range(4):
                s += rect(215 + p * 100, 140 + v * 65, 65, 50, "#E2F2E7" if p == v else "#F3F5F7")
                s += txt(247 + p * 100, 174 + v * 65, "1" if p == v else "0", 23, anchor="middle")
        s += txt(650, 190, ["Example order", "0 → 1 → 2 → 3"], 22)
        s += panel(20, 435, 410, 145, "ASSIGNMENT CONSTRAINTS",
                   ["Exactly one true value per row.", "Exactly one true value per column.", "Pin the start and finish positions."])
        s += panel(460, 435, 420, 145, "TRANSITION CONSTRAINTS",
                   ["For every forbidden edge u → v:", "¬x[u,p] ∨ ¬x[v,p+1]", "for each consecutive position pair."])
        c = result["cnf"]
        s += txt(450, 630, f'Toy instance: {c["variables"]} variables; {c["clauses"]} clauses; {c["literal_occurrences"]} literal occurrences.', 21, anchor="middle")
        return s, 665
    raise ValueError(kind)


def evo_figure(kind, result):
    if kind == "shapes":
        s = txt(450, 35, "One fixed network, explicit dimensions", 25, "bold", "middle")
        rows = [
            ("A = XW + b", "X[3,2] · W[2,2] + b[2]", "A[3,2]; b is shared across rows"),
            ("H = tanh(A)", "elementwise nonlinearity", "H[3,2]; same shape, new values"),
            ("Z = HU + c", "H[3,2] · U[2,3] + c[3]", "Z[3,3]; three class logits per row"),
            ("L = mean cross entropy", "targets y[3] are integer class indices", "L is scalar; normalization divides by 3")]
        for i, row in enumerate(rows):
            y = 65 + i * 155
            s += panel(25, y, 850, 120, row[0], row[1:])
            if i < 3: s += line(450, y + 120, 450, y + 152)
        s += txt(450, 720, "CPU float64 reference. The alphabet/model family is not the learning objective.", 20, anchor="middle")
        return s, 750
    if kind == "reverse":
        purple = "#7147A8"
        def adjoint(x1,y1,x2,y2):
            return (f'<path d="M{x1},{y1} L{x2},{y2}" fill="none" stroke="{purple}" '
                    'stroke-width="3" marker-end="url(#adjoint-arrow)"/>')
        s = ('<defs><marker id="adjoint-arrow" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto">'
             f'<path d="M0,0 L0,6 L7,3 z" fill="{purple}"/></marker></defs>')
        s += txt(450,35,"Forward values; reverse sensitivities",26,"bold","middle")
        for x,title,body in [(20,"A = XW + b","affine input; A[B,H_d]"),
                             (320,"H = tanh(A)","hidden values; H[B,H_d]"),
                             (620,"Z = HU + c","class logits; Z[B,V]")]:
            s += rect(x,80,260,105) + txt(x+15,118,title,22,"bold") + txt(x+15,155,body,18)
        s += line(280,132,316,132) + line(580,132,616,132)
        s += line(750,185,750,235)
        s += panel(620,235,260,105,"SCALAR LOSS",["L = mean CE(Z,y)"])
        s += adjoint(750,340,750,390)
        for x,title,body in [(620,"E = ∂L / ∂Z",["(Q − one_hot(y)) / B","logit sensitivity [B,V]"]),
                             (320,"D_H = EUᵀ",["reverse projection","hidden sensitivity [B,H_d]"]),
                             (20,"D_A = D_H ⊙ (1−H²)",["local tanh derivative","input sensitivity [B,H_d]"])]:
            s += rect(x,390,260,120,fill="#F3EFF9",stroke="#BEADD6")
            s += txt(x+12,423,title,19,"bold",color=purple) + txt(x+12,461,body,18)
        s += adjoint(620,450,584,450) + adjoint(320,450,284,450)
        s += adjoint(150,510,150,560) + adjoint(750,510,750,560)
        s += rect(20,560,395,100,fill="#F3EFF9",stroke="#BEADD6")
        s += txt(35,596,["∇W = XᵀD_A", "∇b = sum_rows(D_A)"],22,color=purple)
        s += rect(485,560,395,100,fill="#F3EFF9",stroke="#BEADD6")
        s += txt(500,596,["∇U = HᵀE", "∇c = sum_rows(E)"],22,color=purple)
        s += txt(25,245,["Blue → forward evaluation", "Purple ← reverse propagation"],21)
        s += txt(25,325,["Backward rules use saved forward values.",
                         "Repeated uses add into shared gradients."],20,color=GRAY)
        s += txt(450,710,"Mean-loss normalization enters once, in E; bias sharing requires row sums.",20,anchor="middle")
        return s,740
    if kind == "checks":
        s = panel(20, 20, 860, 140, "SMOOTH NETWORK: TWO AGREEMENT CHECKS",
                   [f'Hand versus autograd max error: {result["manual_autograd_max_abs"]:.2e}',
                    f'Hand versus central difference: {result["manual_finite_difference_max_abs"]:.2e}',
                    "PyTorch gradcheck also passes on the fixed float64 fixture."])
        s += txt(450, 210, "Known failure: f(x) = x · stop_gradient(x), evaluated at x = 2", 22, "bold", "middle")
        s += panel(20, 245, 410, 160, "FORWARD VALUES", ["Both factors change when x changes.", "f(2) = 4", "Central-difference derivative ≈ 4"])
        s += panel(470, 245, 410, 160, "AUTOGRAD GRAPH", ["Second factor is treated as constant.", "Recorded derivative = 2", "The diagnostic catches the mismatch."])
        s += panel(20, 460, 860, 110, "SCOPE OF THE EVIDENCE", ["Finite smooth checks validate local derivative behavior.",
                       "They do not validate the dataset, objective or generalization."])
        return s, 600
    if kind == "steps":
        s = txt(450, 35, "L(x) = 2x²: exact gradients, different step sizes", 25, "bold", "middle")
        s += txt(450, 74, "x_next = (1 − 4η)x; initial x = 1; six declared updates", 21, anchor="middle")
        # Plot log10 loss, so decrease and explosion remain visible together.
        x0, y0, w, h = 110, 130, 680, 330
        s += line(x0, y0 + h, x0 + w + 15, y0 + h) + line(x0, y0 + h, x0, y0 - 15)
        for exponent in range(-3, 4):
            yy = y0 + h - (exponent + 3) / 6 * h
            s += line(x0, yy, x0 + w, yy, color="#C6D2DC", width=1, arrow=False)
            s += txt(95, yy + 5, "10^" + str(exponent), 17, anchor="end")
        for step in range(7):
            xx = x0 + step * w / 6
            s += txt(xx, y0 + h + 28, str(step), 19, anchor="middle")
        for key, color in [("0.1", GREEN), ("0.5", BLUE), ("0.6", RED)]:
            points = [(x0 + r["step"] * w / 6, y0 + h - (math.log10(r["loss"]) + 3) / 6 * h)
                      for r in result["quadratic"][key]]
            for (a,b),(c,d) in zip(points, points[1:]): s += line(a,b,c,d,color=color,arrow=False)
            for xx,yy in points: s += f'<circle cx="{xx:.5f}" cy="{yy:.5f}" r="4" fill="{color}"/>'
        s += txt(450, 515, "step index (vertical axis: logarithmic loss)", 20, anchor="middle")
        for i, (label, color) in enumerate([("η = 0.1: loss decreases", GREEN), ("η = 0.5: loss stays constant", BLUE), ("η = 0.6: loss increases", RED)]):
            s += txt(130, 558 + i*34, label, 22, color=color)
        s += txt(450, 690, "Stability here requires 0 < η < 0.5. This is not a neural-network convergence theorem.", 19, anchor="middle")
        return s, 720
    raise ValueError(kind)


def outputs():
    storyboard = json.loads((HERE / "storyboard.json").read_text())
    model = load_reference()
    result = model.results()
    emitted = {"results.json": json.dumps(result, indent=2, allow_nan=False) + "\n"}
    for figure in storyboard["figures"][:4]:
        draw = dna_figure if ROOT.name == "dna-computing-book" else evo_figure
        body, height = draw(figure["kind"], result)
        spec = {**figure, "teachingPurpose": figure["captionThesis"],
                "limit": figure["misleadingInterpretation"]}
        emitted["figures/" + figure["id"] + ".svg"] = envelope(spec, body, height)
        companion = "\n\n".join([
            figure["id"] + ": " + figure["title"],
            "QUESTION\n" + figure["readerQuestion"],
            "OBJECTS\n" + "\n".join(figure["objects"]),
            "RELATION / MECHANISM\n" + figure["mechanism"],
            "INFERENCE\n" + figure["captionThesis"],
            "BOUNDARY\n" + figure["misleadingInterpretation"],
            "SOURCE\n" + figure["evidenceSource"],
            "STATUS\nWorking-draft figure; not part of the accepted PDF."]) + "\n"
        emitted["figures/" + figure["id"] + ".txt"] = companion
    return emitted


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    for name, content in outputs().items():
        path = HERE / name
        if args.check:
            if not path.exists() or path.read_text() != content:
                raise SystemExit("Stale working-draft artifact: " + name)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
    print("Chapter 3 working-draft artifacts " + ("fresh" if args.check else "generated"))
