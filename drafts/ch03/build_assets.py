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
sys.path.insert(0, str(HERE))
from finish_figures import render_extra, semantic_lines
from completion_diagnostics import results as completion_results


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



def marker(x, y, color, shape="circle"):
    if shape == "square":
        return f'<rect x="{x-4:.4f}" y="{y-4:.4f}" width="8" height="8" fill="{color}"/>'
    return f'<circle cx="{x:.4f}" cy="{y:.4f}" r="4.5" fill="{color}"/>'


def dna_next_figure(kind, result):
    if kind == "size":
        s = txt(450,35,"Choose the unit before counting the cost",26,"bold","middle")
        s += txt(25,90,"A  GRAPH REPRESENTATION",21,"bold")
        edges = set(map(tuple, result["instance"]["edges"]))
        for v in range(4):
            s += txt(45,139+v*38,str(v),18)
            for w in range(4):
                if v == 0: s += txt(93+w*38,110,str(w),18,anchor="middle")
                s += rect(77+w*38,116+v*38,32,32,"#DDECF8" if (v,w) in edges else "#F3F5F7")
                s += txt(93+w*38,139+v*38,str(int((v,w) in edges)),18,anchor="middle")
        s += line(255,195,310,195)
        s += txt(335,156,["4 × 4 adjacency matrix: 16 edge bits",
                           "plus vertex count and endpoint metadata",
                           "General matrix payload: n² bits"],22)
        s += txt(25,325,"B  NUMERIC VALUE IS NOT BIT LENGTH",21,"bold")
        for i, bit in enumerate("10000000000"):
            s += rect(25+i*32,350,28,38,"#E7F2EA")
            s += txt(39+i*32,377,bit,20,anchor="middle")
        s += txt(200,424,"11 binary digits encode N = 1024",20,anchor="middle")
        s += line(390,370,450,370)
        s += txt(475,367,["A loop to N uses 1024 iterations.",
                          "For N = 2^k, length is k + 1 bits."],21)
        s += txt(25,495,"C  MATERIAL IS A SEPARATE INVENTORY",21,"bold")
        for row in range(2):
            for col in range(3):
                x,y = 45+col*92,545+row*45
                s += line(x,y,x+62,y,arrow=False)
                for j in range(5):
                    s += line(x+8+j*11,y,x+8+j*11,y+12,arrow=False,width=2)
        s += txt(340,550,["Six copies of one schematic strand ≠ six sequences.",
                         "Record distinct designs and physical copy counts.",
                         "Backbone marks are schematic, not bond geometry."],21)
        s += txt(450,675,"Bits, operation counts and molecular copies are different resource coordinates.",20,anchor="middle")
        return s,705
    if kind == "search":
        s = txt(450,35,"Delete an edge only while a witness survives",26,"bold","middle")
        s += txt(25,83,"Query 1: the original six-edge graph is YES.",22)
        for x,label in [(25,"QUERY"),(140,"TRIAL DELETION"),(380,"ORACLE"),(545,"ACTION"),(705,"EDGES LEFT")]:
            s += txt(x,132,label,18,"bold")
        for i,row in enumerate(result["self_reduction"]["trace"]):
            y = 157+i*57
            s += rect(20,y,860,48,"#EAF4ED" if row["trial_has_path"] else "#F3F5F7")
            u,v = row["edge"]
            for x,label in [(40,str(row["query"])),(160,f"{u} → {v}"),
                            (395,"YES" if row["trial_has_path"] else "NO"),
                            (555,row["action"].upper()),(765,str(len(row["kept_edges"])))]:
                s += txt(x,y+31,label,21)
        s += txt(25,545,"The final graph exposes the witness:",22,"bold")
        route = result["self_reduction"]["route"]
        for i,label in enumerate(route):
            x=130+i*215
            if i: s += line(x-184,603,x-32,603)
            s += circle(x,603,str(label))
        s += txt(450,680,"Invariant: the retained graph is YES after every trial, including a NO trial answer.",20,anchor="middle")
        s += txt(450,719,"Seven oracle calls here; each call runs exponential subset search, not a free test.",20,anchor="middle")
        return s,749
    if kind == "np":
        s = txt(450,35,"Negate the existence claim, not one verifier result",25,"bold","middle")
        for x,title,label,flags in [(20,"YES: at least one witness","∃P R(G,s,t,P)",[0,1,0,0]),
                                    (470,"NO: every candidate fails","∀P ¬R(G,s,t,P)",[0,0,0,0])]:
            s += rect(x,85,410,300)
            s += txt(x+15,123,title,21,"bold")
            for i,accepted in enumerate(flags):
                xx=x+55+i*97
                s += circle(xx,202,"P"+str(i+1),r=27)
                s += line(xx,230,xx,273)
                s += txt(xx,311,"YES" if accepted else "NO",19,"bold","middle",
                         color=GREEN if accepted else GRAY)
            s += txt(x+205,360,label,22,anchor="middle")
        s += txt(450,422,"Four candidate slots illustrate quantifiers; they are not the toy graph's full search.",19,anchor="middle")
        s += rect(20,461,860,180)
        s += txt(40,500,"CLASS DEFINITIONS, NOT A SEPARATION DIAGRAM",22,"bold")
        s += txt(40,540,["P: decide membership in polynomial time.",
                         "NP: a polynomial-length YES certificate can be checked in polynomial time.",
                         "coNP: the complement language belongs to NP."],21)
        s += txt(450,691,"P ⊆ NP ∩ coNP. No strict inclusion or class separation is asserted.",22,anchor="middle")
        return s,725
    if kind == "cost":
        s = txt(450,35,"Count candidates, states and transitions separately",25,"bold","middle")
        s += txt(450,76,"Complete directed graphs; endpoints fixed; early arrival at t forbidden",20,anchor="middle")
        x0,y0,w,h=110,125,655,300
        s += line(x0,y0+h,x0+w+20,y0+h)+line(x0,y0+h,x0,y0-10)
        for exponent in range(5):
            yy=y0+h-exponent*h/4
            s += line(x0,yy,x0+w,yy,color="#CCD6DF",width=1,arrow=False)
            s += txt(95,yy+5,"10^"+str(exponent),17,anchor="end")
        rows=result["dense_graph_counts"]
        for row in rows: s += txt(x0+(row["n"]-2)*w/6,y0+h+28,str(row["n"]),19,anchor="middle")
        series=[("all interior orders",BLUE,"square",lambda r:math.factorial(r["n"]-2)),
                ("reachable DP states",GREEN,"circle",lambda r:r["reachable_states"]),
                ("outgoing-neighbor scans",RED,"square",lambda r:r["neighbor_scans"])]
        for i,(label,color,shape,value) in enumerate(series):
            points=[(x0+(r["n"]-2)*w/6,y0+h-math.log10(value(r))*h/4) for r in rows]
            for (a,b),(c,d) in zip(points,points[1:]):
                s += line(a,b,c,d,color=color,arrow=False,width=2)
            for a,b in points: s += marker(a,b,color,shape)
            s += marker(60,521+i*36,color,shape)+txt(80,528+i*36,label,21,color=color)
            s += txt(775,528+i*36,str(value(rows[-1])),21,anchor="end")
        s += txt(450,480,"n vertices (vertical axis: logarithmic algorithmic count)",20,anchor="middle")
        s += txt(775,495,"at n = 8",18,anchor="end")
        s += txt(25,658,["Enumeration count assumes every interior order is examined, not early stopping.",
                        "A stored state is not a whole route; a neighbor scan is not a full verification.",
                        "The plot compares accounting categories, not runtime or molecular efficiency."],20)
        return s,757
    raise ValueError(kind)


def evo_next_figure(kind, result):
    purple="#7147A8"
    def reverse_arrow(x1,y1,x2,y2):
        return (f'<path d="M{x1},{y1} L{x2},{y2}" fill="none" stroke="{purple}" '
                'stroke-width="3" marker-end="url(#shared-adjoint)"/>')
    if kind == "shared":
        s = ('<defs><marker id="shared-adjoint" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto">'
             f'<path d="M0,0 L0,6 L7,3 z" fill="{purple}"/></marker></defs>')
        s += txt(450,35,"One shared bias; three reverse contributions",26,"bold","middle")
        s += txt(450,77,"Projection coordinate j = 1 in the fixed three-row network",21,anchor="middle")
        s += circle(130,253,"c₁",r=38,fill="#E5EFF8")
        for i,y in enumerate([150,253,356]):
            s += line(171,253,314,y)
            s += rect(320,y-35,220,70)
            s += txt(430,y+7,f"z[{i},1] = h[{i}]·u₁ + c₁",17,anchor="middle")
            s += reverse_arrow(595,y,547,y)
            e=result["accumulation"]["mean_loss_logit_adjoints"][i][1]
            s += txt(612,y+7,f"E[{i},1] = {e:+.6f}",21,color=purple)
        s += txt(130,422,"Forward: reuse c₁",20,anchor="middle")
        s += txt(660,422,"Reverse: contributions already include /3",19,anchor="middle")
        s += reverse_arrow(695,443,695,487)
        s += rect(20,500,860,143,fill="#F3EFF9")
        total=result["accumulation"]["bias_gradient"][1]
        s += txt(40,540,"∂L / ∂c₁ = E[0,1] + E[1,1] + E[2,1]",25,"bold",color=purple)
        s += txt(40,582,f"Sum, then display rounding: {total:+.10f}",23)
        s += txt(40,620,"Each use has local derivative 1; the chain rule adds every route to the loss.",20)
        s += txt(450,694,"Dividing this sum by 3 again would silently change the gradient scale.",21,anchor="middle")
        return s,727
    if kind == "loss":
        s = txt(450,35,"Subtract the maximum before exponentiating",26,"bold","middle")
        s += txt(450,77,"Target class y = 1; finite CPU float64 example",21,anchor="middle")
        rows=[("logits z",[1000,1001,999]),("shifted z − m",[-1,0,-2]),
              ("exp(z − m)",[math.exp(-1),1.,math.exp(-2)])]
        for i,(label,values) in enumerate(rows):
            y=120+i*120
            s += txt(30,y+39,label,22,"bold")
            for j,value in enumerate(values):
                x=295+j*190
                s += rect(x,y,160,65,"#E5F2E9" if j==1 else "#F3F5F7")
                show=f"{value:.6f}" if i==2 else str(value)
                s += txt(x+80,y+41,show,23,anchor="middle")
                if i<2: s += line(x+80,y+65,x+80,y+109)
            if i==0: s += txt(450,y+95,"m = 1001",18,anchor="middle")
        s += rect(20,493,860,140)
        loss=result["extreme_logits"]["stable_nll"]
        s += txt(40,535,"L = log Σ exp(zⱼ − m) − (zᵧ − m)",26,"bold")
        s += txt(40,581,f"    = log(1 + exp(−1) + exp(−2)) − 0 = {loss:.10f}",22)
        s += txt(450,679,"Naive exp(z) overflows; these equivalent shifted operations remain finite here.",20,anchor="middle")
        s += txt(450,716,"Green shading marks the target column; the maximum shift does not change it.",20,anchor="middle")
        return s,749
    if kind == "accumulation":
        s = txt(450,35,"The denominator belongs to the objective",26,"bold","middle")
        s += txt(450,77,"All three scored targets have equal weight in the full-batch mean",21,anchor="middle")
        for x,width,label,count in [(20,270,"MICROBATCH A",1),(365,515,"MICROBATCH B",2)]:
            s += rect(x,115,width,135)
            s += txt(x+18,152,label,22,"bold")
            for i in range(count):
                xx=x+30+i*230
                s += rect(xx,179,195,45,"#E5EFF8")
                s += txt(xx+97,210,"one scored target",19,anchor="middle")
        s += line(155,250,155,295)+line(620,250,620,295)
        s += txt(155,331,"mean gradient g_A",23,anchor="middle")
        s += txt(620,331,"mean gradient g_B",23,anchor="middle")
        s += line(155,350,330,397)+line(620,350,560,397)
        s += rect(230,410,460,75,fill="#E5F2E9")
        s += txt(460,457,"g = (1·g_A + 2·g_B) / 3",26,"bold","middle")
        a=result["accumulation"]
        s += txt(450,531,f'Weighted max error: {a["weighted_max_abs_error"]:.2e}; equal means: {a["unweighted_max_abs_error"]:.2e}',21,anchor="middle")
        s += txt(25,587,"BUFFER LIFECYCLE (sum-loss convention)",21,"bold")
        stages=[("clear",90),("+ 1·g_A",310),("+ 2·g_B",540),("divide by 3",780)]
        for i,(label,x) in enumerate(stages):
            if i: s += line(stages[i-1][1]+80,632,x-85,632)
            s += rect(x-75,604,150,60)+txt(x,642,label,21,anchor="middle")
        s += txt(450,708,"Accumulate at unchanged parameters, normalize once, then take one optimizer step.",20,anchor="middle")
        s += txt(450,745,"Equivalence here uses independent rows; batch-dependent or stateful layers need care.",19,anchor="middle")
        return s,779
    if kind == "precision":
        s = txt(450,35,"A smaller perturbation is not always a better check",25,"bold","middle")
        s += txt(450,77,"Maximum absolute gradient discrepancy over the fixed float64 network",20,anchor="middle")
        x0,y0,w,h=120,130,650,330
        s += line(x0,y0+h,x0+w+20,y0+h)+line(x0,y0+h,x0,y0-10)
        for exponent in range(-12,-2,2):
            yy=y0+h-(exponent+12)*h/10
            s += line(x0,yy,x0+w,yy,color="#CCD6DF",width=1,arrow=False)
            s += txt(100,yy+5,"10^"+str(exponent),18,anchor="end")
        points=[]
        for r in sorted(result["step_size_scan"],key=lambda r:r["h"]):
            xx=x0+(math.log10(r["h"])+9)*w/8
            yy=y0+h-(math.log10(r["max_abs_error"])+12)*h/10
            points.append((xx,yy))
            s += txt(xx,y0+h+30,f'10^{round(math.log10(r["h"]))}',18,anchor="middle")
        for (a,b),(c,d) in zip(points,points[1:]): s += line(a,b,c,d,arrow=False)
        for xx,yy in points: s += marker(xx,yy,BLUE)
        s += txt(450,539,"h increases → (both axes logarithmic)",21,anchor="middle")
        s += txt(135,185,["Small h:", "roundoff can dominate"],19)
        s += txt(525,405,["Large h:", "truncation can dominate"],19)
        s += txt(450,594,"Observed low point: h = 10^−5 among these five tested values",22,anchor="middle")
        s += txt(450,644,"Schematic error balance: C₁h² + C₂ε/h",25,"bold","middle")
        s += txt(450,688,"Connected points guide the eye; no fitted curve or universal optimal h is claimed.",20,anchor="middle")
        return s,721
    raise ValueError(kind)


def numerical_observations(kind, result):
    """Carry chart and state-trace values into the accessible text companion."""
    if kind == "search":
        return ["Query 1: original graph YES."] + [
            f'Query {r["query"]}: try removing {r["edge"][0]} → {r["edge"][1]}; '
            f'oracle {"YES" if r["trial_has_path"] else "NO"}; {r["action"]}; '
            f'retained edges = {r["kept_edges"]}.'
            for r in result["self_reduction"]["trace"]]
    if kind == "cost":
        return [f'n={r["n"]}: interior orders={math.factorial(r["n"]-2)}; '
                f'reachable states={r["reachable_states"]}; neighbor scans={r["neighbor_scans"]}.'
                for r in result["dense_graph_counts"]]
    if kind == "shared":
        return [f'Row {i}, coordinate 1: E={r[1]:+.10f}.'
                for i,r in enumerate(result["accumulation"]["mean_loss_logit_adjoints"])] + [
                    f'Summed bias gradient, coordinate 1: {result["accumulation"]["bias_gradient"][1]:+.10f}.']
    if kind == "loss":
        return ["Logits: [1000,1001,999]. Target index: 1. Maximum: 1001.",
                "Shifted logits: [-1,0,-2].",
                f'Stable cross entropy: {result["extreme_logits"]["stable_nll"]:.10f}.']
    if kind == "accumulation":
        a = result["accumulation"]
        return ["Target counts: [1,2]. Full gradient: (g_A + 2g_B)/3.",
                f'Weighted maximum absolute error: {a["weighted_max_abs_error"]:.6e}.',
                f'Equal-mean maximum absolute error: {a["unweighted_max_abs_error"]:.6e}.']
    if kind == "precision":
        return [f'h={r["h"]:.1e}: maximum absolute gradient error={r["max_abs_error"]:.6e}.'
                for r in sorted(result["step_size_scan"], key=lambda r:r["h"])]
    return []


def outputs():
    storyboard = json.loads((HERE / "storyboard.json").read_text())
    model = load_reference()
    result = model.results()
    emitted = {"results.json": json.dumps(result, indent=2, allow_nan=False) + "\n"}
    completion = completion_results(ROOT.name == "dna-computing-book")
    emitted["completion-results.json"] = json.dumps(completion, indent=2, allow_nan=False) + "\n"
    for index, figure in enumerate(storyboard["figures"]):
        if index < 4:
            draw = dna_figure if ROOT.name == "dna-computing-book" else evo_figure
        else:
            draw = dna_next_figure if ROOT.name == "dna-computing-book" else evo_next_figure
        body, height = (draw(figure["kind"], result) if index < 8
                        else render_extra(figure["kind"], completion))
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
        observed = numerical_observations(figure["kind"], result)
        if index >= 8:
            companion += "\nSEMANTIC TXT GRAPH\n" + "\n".join(semantic_lines(figure["kind"])) + "\n"
        if observed:
            companion += "\nNUMERICAL OBSERVATIONS\n" + "\n".join(observed) + "\n"
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
