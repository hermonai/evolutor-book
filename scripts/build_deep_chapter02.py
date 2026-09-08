"""Chapter 2 original vectors, semantic TXT graphs and executable evidence.

No historical image reproduction; no raster assets; no Chapter 1 file mutation.
"""
import argparse
import importlib.util
import inspect
import json
import math
from pathlib import Path
from build_deep_chapter import txt, rect, line, circle, panel, envelope, BLUE, GREEN, RED, GRAY, PURPLE, PALE

ROOT = Path(__file__).resolve().parents[1]
DNA = ROOT.name == "dna-computing-book"

def module():
    spec = importlib.util.spec_from_file_location("chapter02", ROOT / "examples/deep/ch02.py")
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result

def table(headers, rows, widths, height=62):
    s = ""; x = 12
    for label, w in zip(headers, widths):
        s += txt(x + 10, 32, label, 20, "bold"); x += w
    for i, row in enumerate(rows):
        y = 50 + i * height
        s += rect(10, y, 880, height - 5, PALE if i % 2 == 0 else "#FFFFFF")
        x = 12
        for value, w in zip(row, widths):
            s += txt(x + 10, y + 29, str(value).split("|"), 19); x += w
    return s, 62 + len(rows) * height

def strand(x, y, domains, width=155, color=BLUE, reverse=False, join=True):
    s = txt(x - 38, y + 31, "3′" if reverse else "5′", 21)
    for i, d in enumerate(domains):
        xx = x + i * (width + 15)
        s += rect(xx, y, width, 45, "#FFFFFF", color) + txt(xx + width/2, y+30, d, 20, "bold", "middle", color)
        if i and join: s += line(xx-15,y+22,xx,y+22,color=color,arrow=False)
    return s + txt(x + len(domains)*(width+15)-8,y+31,"5′" if reverse else "3′",21)

def note(s, h, message):
    return s + txt(450,h+25,message,19,anchor="middle",color=GRAY), h+46

def dna_figure(kind, m, r, phase=None):
    s = ""
    if kind == "graph":
        # Vertices around a circle; bidirectional edges use displaced quadratics.
        pos = {v:(450+300*math.cos(-math.pi/2+v*2*math.pi/7),
                  310+230*math.sin(-math.pi/2+v*2*math.pi/7)) for v in m.VERTICES}
        for u,v in sorted(m.EDGES):
            x,y=pos[u]; X,Y=pos[v]; dx=X-x;dy=Y-y;d=math.hypot(dx,dy)
            a,b=x+dx*29/d,y+dy*29/d; c,e=X-dx*34/d,Y-dy*34/d
            if (v,u) in m.EDGES:
                cx,cy=(a+c)/2-dy*25/d,(b+e)/2+dx*25/d
                s+=f'<path d="M{a},{b} Q{cx},{cy} {c},{e}" fill="none" stroke="{BLUE}" stroke-width="2.5" marker-end="url(#arrow)"/>'
            else: s+=line(a,b,c,e,width=2.5)
        for v,(x,y) in pos.items(): s+=circle(x,y,str(v),fill="#EAF4ED" if v in (0,6) else "#FFFFFF")
        return note(s,560,"14 directed edges; fixed endpoints 0 and 6. Geometry carries no extra meaning.")
    if kind == "routes":
        return table(["Route","Edges","Occurrences","Coverage"],[
            ["0 1 2 3 4 5 6","legal","7","all; witness"],
            ["0 1 3 4 5 6","legal","6","2 absent"],
            ["0 3 2 3 4 5 6","legal","7","1 absent; 3 twice"],
            ["0 1 2 4 3 5 6","illegal","7","all; not a witness"]],[345,130,165,235],75)
    if kind == "sequence":
        for i,(v,code) in enumerate(m.PUBLISHED_CODES.items()):
            y=28+i*80
            s+=txt(35,y+29,f"O{v}",24,"bold")+strand(155,y,[code[:10],code[10:]],270)
        s+=txt(40,310,"O23 = R2 L3",24,"bold")+txt(355,310,r["edge_2_3"],22)
        s+=txt(40,360,"O34 = R3 L4",24,"bold")+txt(355,360,r["edge_3_4"],22)
        s+=txt(40,425,"Aligned splint O3*:",22)+txt(315,425,"3′ "+r["splint_3_aligned_3_to_5"]+" 5′",21)
        return note(s,446,"Only the three printed historical codes are shown; all upper codes read 5′→3′.")
    if kind == "assembly":
        states=range(3) if phase is None else [phase]
        for row,p in enumerate(states):
            y=25+row*175
            s+=txt(20,y+20,["1  Separate","2  Annealed; nick remains","3  Ligated; backbone continuous"][p],22,"bold")
            shift=65 if p==0 else 0
            for x,label in [(75,"R2"),(200,"L3"),(325+shift,"R3"),(450+shift,"L4")]:
                s+=rect(x,y+45,110,45,"#FFFFFF",BLUE)+txt(x+55,y+75,label,22,"bold","middle")
            s+=line(185,y+67,200,y+67,arrow=False)
            s+=line(435+shift,y+67,450+shift,y+67,arrow=False)
            s+=txt(30,y+76,"5′",21)+txt(575+shift,y+76,"3′",21)
            if p:
                s+=strand(200,y+110,["L3*","R3*"],110,color=GREEN,reverse=True)
                for x in list(range(210,305,25))+list(range(335,430,25)):
                    s+=line(x,y+95,x,y+105,color=GREEN,dash=True,arrow=False,width=1.5)
                if p==1: s+=txt(655,y+74,"3′ OH / 5′ P nick",20,color=RED)
                else: s+=line(310,y+67,325,y+67,color=RED,width=5,arrow=False)
            else: s+=txt(695,y+74,"free splint",20,color=GREEN)
        return note(s,len(list(states))*175+16,"Dashed contacts = pairing. Red closure = new backbone bond. Domains not to scale.")
    if kind == "population":
        s+=panel(15,20,405,90,"DIGITAL INVENTORY","Each legal bounded walk once")
        s+=panel(465,20,420,90,"PHYSICAL POPULATION","Unequal copies coexist")
        for i,(route,n) in enumerate([("0 1 2 3 4 5 6",0),("0 1 3 4 5 6",4),("0 3 2 3 4 5 6",2)]):
            y=160+i*105
            s+=txt(40,y,route,24)
            s+=txt(480,y-17,route,20)
            for j in range(n): s+=circle(505+j*70,y+23,"",r=13)
            if n==0:s+=txt(490,y+30,"absent in this illustrative tube",20,color=RED)
        return note(s,440,"The tube is hypothetical. Selection cannot recover an absent candidate.")
    if kind == "pcr":
        p=1 if phase is None else phase
        s+=txt(450,32,["Separated template strands","Inward-facing primers","Compatible products enriched"][p],25,"bold","middle")
        s+=strand(115,80,["O0","interior","O6"],190)
        s+=strand(115,260,["O0*","interior*","O6*"],190,reverse=True,color=GREEN)
        if p>=1:
            s+=line(135,235,425,235,color=BLUE,width=5)+txt(130,215,"5′ O0 primer → 3′ growth",21)
            s+=line(710,150,440,150,color=GREEN,width=5)+txt(460,184,"3′ growth ← O6* primer 5′",21)
        if p==2:
            for i in range(3):s+=line(180,325+i*24,740,325+i*24,arrow=False,width=4)
        else:s+=txt(450,355,"Opposite templates; extension points into the selected interval.",21,anchor="middle")
        return note(s,410,"Schematic enrichment, not exact cycle counts or guaranteed endpoint specificity.")
    if kind == "length":
        s+=rect(25,35,280,355,"#F1F5F8")
        s+=txt(165,24,"Synthetic size lane",22,"bold","middle")
        for bp,y in [(160,130),(140,210),(120,290)]:
            s+=line(75,y,210,y,color=GREEN if bp==140 else BLUE,width=7,arrow=False)
            s+=txt(230,y+7,str(bp),21)
        s+=line(45,70,45,340)+txt(105,370,"migration",19)
        s+=panel(340,60,535,125,"140 bp: seven code occurrences","0 1 2 3 4 5 6     all distinct|0 3 2 3 4 5 6     3 repeats")
        s+=panel(340,215,535,145,"Same size ≠ same identity","20 bases/code × 7 codes = 140 bases|Duplex products: 140 bp|Coverage must be checked separately")
        return note(s,405,"Band spacing is conceptual, not calibrated gel mobility or measured intensity.")
    if kind == "beads":
        states=[0,1,2] if phase is None else [phase]
        rows=[
            ("Prepare single strands","bead—biotin—reverse strand","denature → recover free forward strand"),
            ("Recognize required vertex","bead—biotin—complementary probe","target binds probe; wash away unbound"),
            ("Recover retained target","bead keeps its attached probe","denature → target returns to solution")]
        for j,p in enumerate(states):
            y=20+j*140; title,a,b=rows[p]
            s+=circle(55,y+62,"",fill="#DDE5EB",color=GRAY,r=30)
            s+=line(85,y+62,125,y+62,arrow=False,color=PURPLE)
            s+=txt(140,y+27,title,24,"bold")+txt(140,y+67,a,22)+txt(140,y+106,b,21)
        return note(s,len(states)*140+15,"Biotin attaches. Complementarity recognizes. The retained phase changes with the step.")
    if kind == "capture":
        return table(["Stage","Legal inventory","With pseudo-path"],[
            [a["stage"],a["count"],b["count"]] for a,b in zip(r["stages"],r["fault_stages"])],[365,240,270],47)
    if kind == "mapping":
        return table(["Logical condition","Molecular property","Laboratory operation"],[
            ["permitted adjacency","oriented code overlap","anneal + ligate"],
            ["correct endpoints","opposed primer sites","PCR enrichment"],
            ["seven occurrences","140-bp product","gel fraction recovery"],
            ["contains vertex i","probe-complement site","affinity selection"],
            ["valid witness","resolved ordered code","decode + graph check"]],[265,290,320],67)
    if kind == "readout":
        for block,key in enumerate(("readout_individual","readout_mixture")):
            ox=30+block*445
            data=r[key][0] if block==0 else r[key]
            s+=txt(ox+210,30,"Pure witness" if block==0 else "Three-route mixture",24,"bold","middle")
            s+=rect(ox+10,55,405,315,"#F1F5F8")
            for j,v in enumerate(range(1,7)):
                x=ox+50+j*63;s+=txt(x,85,str(v),20,anchor="middle")
                for bp in data[str(v)]:
                    y=350-(bp-40)*2
                    s+=line(x-18,y,x+18,y,arrow=False,width=5)
            s+=txt(ox+210,405,"Lanes 1–6; 40 bp bottom, 140 bp top",18,anchor="middle")
        return note(s,430,"Synthetic possible product lengths only. Mixture bands lose joint route identity.")
    if kind == "errors":
        rows=[[v["stage"],f'{v["true_expected"]:.5g}',f'{v["false_expected"]:.5g}'] for v in r["sensitivity"]["rows"]]
        s,h=table(["Selections","Expected true copies","Expected false copies"],rows,[205,335,335],52)
        return note(s,h,"Three initial true copies; q=0.8. After five stages: P(no true copy) ≈ 0.304.")
    if kind == "resources":
        s+=panel(10,10,880,115,"Historical input inventory","50 pmol/species → about 3.01 × 10¹³ oligos/species|14 edge species + 5 internal splints; not 19 completed routes")
        tail,h=table(["Vertices n","Fixed-endpoint orders","Assumption"],[
            [x["n"],f'{x["orders"]:,}',"complete directed graph"] for x in r["fixed_endpoint_orders"]],[170,360,345],57)
        s+='<g transform="translate(0 145)">'+tail+'</g>'
        return note(s,h+150,"Search-space count ≠ sampled route support ≠ measured reagent concentration.")
    if kind == "aftermath":
        return table(["Tradition","State / operation","Question opened"],[
            ["SAT filtering","assignments / selection","which clauses hold?"],
            ["Formal DNA systems","strings / formal operators","what can be computed?"],
            ["Molecular automata","state + input / transitions","can reactions follow rules?"],
            ["Self-assembly","tiles / local attachment","can shape encode a program?"],
            ["Strand displacement","signals / strand exchange","can chemistry compose gates?"]],[230,340,305],70)
    raise ValueError(kind)

def evo_figure(kind,m,r,phase=None):
    s=""
    if kind == "protocol":
        return table(["Object","Concrete next-base example","Not interchangeable with"],[
            ["Data","sequence records + relationships","task"],
            ["Task","predict next base from prefix","architecture"],
            ["Model","prefix counts or trained fθ","objective"],
            ["Objective","mean negative log probability","success claim"],
            ["Metric + protocol","held-out nats/base + split + mask","training loss alone"]],[175,390,310],70)
    if kind == "tokens":
        return table(["Encoding of A C G T A C","Tokens","What changes"],[
            ["single bases","A / C / G / T / A / C","6 tokens; 4-symbol alphabet"],
            ["overlapping 3-mers","ACG / CGT / GTA / TAC","next token shares 2 bases"],
            ["nonoverlapping 3-mers","ACG / TAC","2 tokens; up to 64 types"],
            ["illustrative segmentation","AC / G / TAC","variable lengths; learned rules"]],[295,315,265],85)
    if kind == "split":
        p=2 if phase is None else phase
        s+=txt(450,30,["Records before grouping","Union conflict relations","Assign whole components"][p],25,"bold","middle")
        names=["a1","a2","b1"];xs=[150,430,710]
        for name,x in zip(names,xs):s+=circle(x,120,name,r=35)
        s+=txt(150,195,"AACG",22,anchor="middle")+txt(430,195,"CGTT",22,anchor="middle")+txt(710,195,"ACGA",22,anchor="middle")
        if p>=1:
            s+=line(190,120,390,120,arrow=False)+txt(290,95,"exact RC",20,anchor="middle")
            s+=line(470,120,670,120,arrow=False)+txt(570,95,"same locus",20,anchor="middle")
            s+=rect(70,230,750,80,"#EAF4ED")+txt(450,278,"Transitivity: a1, a2, b1 must stay together",25,"bold","middle")
        if p==2:
            s+=txt(450,360,"TRAIN: a1 a2 b1 e1     VALID: c1 c2     TEST: d1 f1",21,anchor="middle")
        return note(s,410,"Guarantee covers only detected/declared relations, not unknown homology.")
    if kind == "causal":
        s+=txt(25,32,"Input position j predicts the NEXT base, not the current base.",24,"bold")
        for row,(label,seq) in enumerate([("inputs",["A","C","G","T"]),("targets",["C","G","T","A"])]):
            y=90+row*110;s+=txt(35,y+12,label,23,"bold")
            for j,v in enumerate(seq):s+=circle(250+j*150,y,v)
        for j in range(4):s+=line(250+j*150,120,250+j*150,165)
        s+=txt(450,345,"Allowed for output j: inputs 0…j. Forbidden: inputs j+1…T−1.",23,anchor="middle")
        return note(s,385,"A diagonal-inclusive mask is causal only with this shifted target convention.")
    if kind == "intervention":
        p=2 if phase is None else phase
        s+=txt(450,30,["Original input","Keep prefix; replace suffix","Compare prefix outputs"][p],25,"bold","middle")
        seqs=["A C G T A C G T","A C G A C G T A"]
        for row,seq in enumerate(seqs[:1] if p==0 else seqs):
            y=95+row*95
            for j,v in enumerate(seq.split()):s+=circle(105+j*96,y,v,color=BLUE if j<3 else RED)
        s+=line(344,55,344,235,dash=True,arrow=False,color=GRAY)
        s+=txt(220,270,"fixed prefix",22,anchor="middle")+txt(600,270,"intervened future",22,anchor="middle")
        if p==2:
            s+=panel(15,310,415,100,"PrefixCounts: Δ = 0","passes this finite test")
            s+=panel(465,310,420,100,"FutureCopy: Δ = 8","negative control is detected")
        return note(s,435,"Seven boundaries tested. Passing finite interventions is not a proof for all inputs.")
    if kind == "entropy":
        s+=panel(15,15,870,100,"Independent uniform next base","Expected loss = ln 4 + E[KL(uniform ∥ predicted distribution)]")
        s+=panel(15,145,410,155,"Valid reference","ln 4 = 1.386294 nats/base|PPL = 4|BPB = 2")
        s+=panel(465,145,420,155,"Deliberate future leak","0.001006 nats/base|accuracy = 1|invalid information access")
        return note(s,340,"Entropy constrains expected fresh-target loss, not every finite sample or training set.")
    if kind == "capacity":
        return table(["Matched quantity","Confound controlled","Still uncontrolled"],[
            ["parameters","stored trainable scalars","state, width, data, FLOPs"],
            ["width","representation dimension","depth, parameters, history"],
            ["state / cache bytes","runtime memory budget","precision, access semantics"],
            ["training tokens","data exposure","compute per token"],
            ["training FLOPs","arithmetic budget","hardware utilization"],
            ["wall time","time on specified system","optimization / kernel maturity"]],[265,285,325],63)
    if kind == "seeds":
        vals=r["illustrative_seed_summary_not_training"]
        s+=line(120,305,825,305,arrow=False)
        for v in [0.5,0.6,0.7,0.8,0.9,1.0]:
            x=120+(v-.5)*1400;s+=line(x,299,x,312,arrow=False)+txt(x,342,f"{v:.1f}",20,anchor="middle")
        for i,v in enumerate(vals["individual"]):
            x=120+(v-.5)*1400;y=155+i*48
            s+=circle(x,y,"",r=12)+txt(x,y-25,f"{v:.2f}",22,anchor="middle")
            s+=line(x,y+16,x,298,arrow=False,dash=True)
        mean=120+(vals["mean"]-.5)*1400
        s+=line(mean,85,mean,300,color=RED,dash=True,arrow=False)+txt(mean,55,"mean 0.8233",22,anchor="middle",color=RED)
        return note(s,380,"Supplied illustrative values, not measured runs; three points do not establish bimodality.")
    if kind == "oracle":
        for row,(name,seq) in enumerate([("input",list("ACGTAC")),("delay 2",["—","—","A","C","G","T"])]):
            y=95+row*145;s+=txt(25,y+5,name,22,"bold")
            for j,v in enumerate(seq):s+=circle(230+j*115,y,v)
        for j in range(4):s+=line(230+j*115,128,230+(j+2)*115,206)
        return note(s,335,"Zero-based scored positions 2…5. First two positions are unscored, not default-A targets.")
    if kind == "tasks":
        return table(["Task","Required memory","Shortcut to exclude"],[
            ["exact delay / copy","recover specified past symbol","fixed position / output leak"],
            ["parity / running sum","compressed statistic","class imbalance / length"],
            ["associative retrieval","key-conditioned lookup","key frequency / duplicates"],
            ["pointer chasing","sequential dependent lookup","one-hop proxy"],
            ["motif / conditional routing","pattern and state","future context / motif count"]],[285,280,310],72)
    if kind == "ablation":
        s+=panel(15,25,410,120,"Removal","Full M versus M without X|Replace lost budget if needed")
        s+=panel(465,25,420,120,"Transplant","Baseline B versus B plus X|Retune under declared budget")
        s+=line(220,155,220,210)+line(675,155,675,210)
        s+=panel(15,225,410,145,"Local question","Does X matter inside M?|Retrained versus inference-only|are different interventions")
        s+=panel(465,225,420,145,"Transfer question","Does the effect travel to B?|Failure may reflect interaction,|not universal uselessness")
        return note(s,405,"Use paired seeds and uncertainty for differences; neither contrast alone proves mechanism.")
    if kind == "metrics":
        return table(["Evidence axis","Measure","Required context"],[
            ["predictive quality","NLL, BPB, F1, retrieval accuracy","same task / targets / split"],
            ["confidence quality","calibration, proper log score","population + fitted calibration"],
            ["systems performance","latency, throughput, memory","hardware / batch / precision"],
            ["engine fidelity","reference-output difference","same weights / inputs / dtype"]],[255,355,265],78)
    if kind == "lifecycle":
        p=2 if phase is None else phase
        actors=["Spec","Reference","Evaluator","Artifact"];xs=[110,335,560,785]
        for a,x in zip(actors,xs):
            s+=rect(x-85,15,170,52)+txt(x,49,a,22,"bold","middle")
            s+=line(x,75,x,440,dash=True,arrow=False,color=GRAY,width=1.5)
        messages=[(0,1,120,"frozen question + seed"),(1,2,215,"fixed predictions; no training"),(2,3,310,"metrics + spec hash")]
        for j,(a,b,y,label) in enumerate(messages):
            if j<=p:s+=line(xs[a],y,xs[b],y)+txt((xs[a]+xs[b])/2,y-20,label,18,anchor="middle")
        return note(s,460,"UML-style sequence for EVO-EXP01-CH02-SMOKE. Parent training remains NOT RUN.")
    raise ValueError(kind)

def outputs():
    m=module();r=m.results()
    data=json.loads((ROOT/"pedagogy/deep-ch02-storyboard.json").read_text())
    out={"artifacts/deep/ch02-results.json":json.dumps(r,indent=2)+"\n"}
    old_bib=(ROOT/"tex/deep/references.tex").read_text()
    extra_bib=(ROOT/"tex/deep/ch02-references.tex").read_text()
    out["tex/deep/references-ch01-02.tex"]=old_bib.replace("\\end{thebibliography}",extra_bib+"\n\\end{thebibliography}")
    for f in data["figures"]:
        meta={"id":f["id"],"title":f["title"],"teachingPurpose":f["readerQuestion"],"limit":f["misleadingInterpretation"]}
        body,h=(dna_figure if DNA else evo_figure)(f["kind"],m,r)
        out["book/figures/deep/"+f["id"]+".svg"]=envelope(meta,body,h)
        out["book/diagrams/deep/"+f["id"]+".txt"]=(
            f["id"]+" — "+f["title"]+"\n\nQUESTION\n"+f["readerQuestion"]+
            "\n\nOBJECTS\n"+"\n".join("• "+v for v in f["objects"])+
            "\n\nRELATION / MECHANISM\n"+f["mechanism"]+"\n\nSTATE TRANSITION\n"+
            f["sequence"]+"\n\nINFERENCE\n"+f["captionThesis"]+"\n\nBOUNDARY\n"+
            f["misleadingInterpretation"]+"\n\nSOURCE\n"+f["evidenceSource"]+
            "\n\nEXECUTABLE EVIDENCE\nartifacts/deep/ch02-results.json; examples/deep/ch02.py\n")
    kinds=["assembly","pcr","beads"] if DNA else ["split","intervention","lifecycle"]
    ledger=[]
    for kind in kinds:
        f=next(f for f in data["figures"] if f["kind"]==kind)
        for phase in range(3):
            name=f"{kind}-{phase+1:02}.svg"
            meta={"id":f["id"]+f"-K{phase+1}","title":f["title"],"teachingPurpose":f["sequence"],
                  "limit":"Static state-changing keyframe, not a rendered animation or measured trajectory."}
            body,h=(dna_figure if DNA else evo_figure)(kind,m,r,phase)
            out["animation/"+data["chapter"].lower()+"/"+name]=envelope(meta,body,h)
            ledger.append({"sequence":kind,"phase":phase+1,"source":name,"state":meta["teachingPurpose"],
                           "changed":"Visible molecular associations, input suffix, grouping or messages advance with phase.",
                           "motion":"none; static editable keyframe"})
    out["animation/"+data["chapter"].lower()+"/frames.json"]=json.dumps(ledger,indent=2)+"\n"
    # Source extraction prevents printed snippets from drifting away from tested code.
    funcs=([m.generate_candidates,m.pipeline,m.graduated_bands] if DNA else
           [m.token_metrics,m.intervention_suite,m.delay_oracle,m.seed_summary])
    out["tex/deep/ch02-code.py"]="\n\n".join(inspect.getsource(f).rstrip() for f in funcs)+"\n"
    for f in funcs:
        out["tex/deep/ch02-"+f.__name__+".py"]=inspect.getsource(f).rstrip()+"\n"
    if not DNA:
        rows=[r"\begin{tabular}{rrr}",r"\toprule Seed & Uniform nats/base & PrefixCounts nats/base \\",r"\midrule"]
        rows += [str(x["seed"])+" & "+f'{x["uniform"]["nats_per_base"]:.6f}'+" & "+f'{x["causal"]["nats_per_base"]:.6f}'+r" \\" for x in r["runs"]]
        rows += [r"\bottomrule",r"\end{tabular}"]
        out["tex/deep/ch02-results.tex"]="\n".join(rows)+"\n"
    return out

def main():
    p=argparse.ArgumentParser();p.add_argument("--check",action="store_true");args=p.parse_args()
    for name,content in outputs().items():
        path=ROOT/name
        if args.check:
            if not path.exists() or path.read_text()!=content:raise SystemExit("Stale Chapter 2 artifact: "+name)
        else:
            path.parent.mkdir(parents=True,exist_ok=True);path.write_text(content)
    print("Chapter 2 artifacts "+("fresh" if args.check else "generated"))

if __name__=="__main__":main()
