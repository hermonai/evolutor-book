"""Chapter 1 original vector figures and traces. No raster assets or external packages."""
from pathlib import Path
import argparse
import importlib.util
import json
from html import escape

ROOT = Path(__file__).resolve().parents[1]
NAVY = "#173A55"
BLUE = "#176CA4"
PALE = "#EDF5FA"
GOLD = "#A86613"
INK = "#172F43"

def text(x, y, lines, size=23, weight="normal", anchor="start", color=INK):
    if isinstance(lines, str):
        lines = lines.split("|")
    return "".join(f'<text x="{x}" y="{y+i*(size+8)}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" fill="{color}">{escape(line)}</text>' for i,line in enumerate(lines))

def box(x,y,w,h,fill=PALE):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{fill}" stroke="#9DB6C7" stroke-width="1.5"/>'

def arrow(x1,y1,x2,y2,label="",dashed=False):
    style=' stroke-dasharray="7 5"' if dashed else ""
    return (f'<path d="M{x1},{y1} L{x2},{y2}" fill="none" stroke="{BLUE}" stroke-width="2.5" marker-end="url(#arrow)"{style}/>'
            + (text((x1+x2)/2,(y1+y2)/2-12,label,20,anchor="middle") if label else ""))

def token(x,y,label,waiting=False):
    return (f'<circle cx="{x}" cy="{y}" r="17" fill="{("#FFF3DC" if waiting else "#D5E9F5")}" stroke="{(GOLD if waiting else BLUE)}" stroke-width="2"/>'
            +text(x,y+7,str(label),20,anchor="middle"))

def strand(x,y,width=310):
    # Schematic connected parts, not a chemical bond diagram or strand-polarity convention.
    s=f'<path d="M{x},{y} L{x+width},{y}" stroke="{BLUE}" stroke-width="5" fill="none"/>'
    for i,base in enumerate("ACGT"):
        px=x+20+i*(width-40)/3
        s+=box(px-21,y-20,42,40,"#FFFFFF")+text(px,y+8,base,23,weight="bold",anchor="middle")
    return s

def figure(f, book):
    k=f["kind"]
    s=""
    h=340
    if k=="counters":
        for i,n in enumerate((3,4,5)):
            x=10+300*i
            s+=box(x,18,280,270)+text(x+18,51,[f"{i+1}  "+("Start" if i==0 else "Move one"),f"{n} in the tray"],23,weight="bold")
            s+=box(x+10,106,260,79,"#FFFFFF")
            for j in range(n):
                s+=token(x+30+j*49,145,j+1)
            for j in range(n,5):
                s+=token(x+65+(j-n)*49,217,j+1,True)
            s+=text(x+18,263,"waiting" if n<5 else "none waiting",20)
        s+=text(450,325,"Same five objects throughout; only their location changes.",22,anchor="middle")
    elif k=="ambiguity":
        s+=box(10,15,880,100,"#FFF6E7")+text(35,50,"UNCLEAR: start at 3; add more",24,weight="bold")
        s+=text(35,89,"Add one: 4     or     add two: 5     — both follow the words.",22)
        s+=arrow(450,123,450,171,"make the rule precise")
        s+=box(10,180,880,100)+text(35,216,"EXPLICIT: start at 3; add exactly 2",24,weight="bold")
        s+=text(35,255,"One completed application gives 5, not 4 and not 7.",22)
        s+=text(450,326,"This example specifies one rule and one application.",22,anchor="middle")
    elif k=="representation":
        names=["Count objects","Read a numeral","Read marked cells"]
        conventions=["one object counts as one","decimal numeral convention","one mark counts as one"]
        for i in range(3):
            x=10+300*i
            s+=box(x,20,280,260)+text(x+140,60,names[i],22,weight="bold",anchor="middle")
            if i==0:
                for j in range(3): s+=token(x+70+j*65,133,j+1)
            elif i==1:
                s+=text(x+140,160,"3",76,weight="bold",anchor="middle")
            else:
                for j in range(3):
                    s+=box(x+39+70*j,102,62,62,"#FFFFFF")+text(x+70+70*j,145,"×",34,anchor="middle")
            s+=text(x+140,212,"Means three",23,weight="bold",anchor="middle")
            # Two lines preserve readable type at publication width.
            words=conventions[i].split(" ")
            s+=text(x+140,249," ".join(words[:3])+"|"+" ".join(words[3:]),20,anchor="middle")
        h=335
    elif k=="dna":
        s+=box(10,15,880,135)+text(35,48,"MOLECULAR STRUCTURE — schematic strand segment",22,weight="bold")
        s+=strand(155,105,570)
        s+=arrow(450,165,450,230,"write the displayed order")
        s+=box(170,243,560, 70,"#FFFFFF")+text(450,286,"A C G T",32,weight="bold",anchor="middle")
        s+=text(450,347,"Letters describe parts; they are not letters inside the molecule.",22,anchor="middle")
        s+=text(450,379,"Not a complete chemical drawing; strand direction comes later.",20,anchor="middle")
        h=400
    elif k=="bridge":
        cols=[("WRITE INPUT","What represents the start?"),("PERFORM RULE","Which change is allowed?"),("READ OUTPUT","What counts as an answer?")]
        for i,(heading,q) in enumerate(cols):
            x=10+i*300
            s+=box(x,15,280,300)+text(x+140,52,heading,22,weight="bold",anchor="middle")
            s+=text(x+140,87,q,20,anchor="middle")
            s+=text(x+20,147,["Three in the tray","Move two into the tray","Count five"][i],21,weight="bold")
            s+=text(x+20,217,[["Choose a DNA","representation"],["Specify a controlled","molecular operation"],["Measure and interpret","the resulting material"]][i],21)
        s+=text(450,352,"Top example: counters. Bottom lane: questions for a DNA design.",21,anchor="middle")
        h=375
    elif k=="program":
        for x,title,body in [(10,"1  Input","temperature: 18"),(310,"2  Stored rule","below 20?"),(610,"3  Output","return “on”")]:
            s+=box(x,40,280,205)+text(x+140,83,title,24,weight="bold",anchor="middle")
            s+=text(x+140,147,body,25,anchor="middle")
        s+=arrow(265,190,332,190)+arrow(568,190,635,190)
        s+=text(450,285,"Solid arrows: data used by the next step.",22,anchor="middle")
        s+=text(450,321,"Output is a word, not a command sent to a real heater.",21,anchor="middle")
    elif k=="boundary":
        for j,heads in enumerate(("INPUT","IS IT BELOW 20?","RETURNED WORD")):
            s+=text(90+j*300,48,heads,22,weight="bold")
        for i,(v,test,out) in enumerate([(18,"yes","on"),(20,"no: equal","off"),(22,"no: above","off")]):
            y=72+i*75
            s+=box(15,y,870,65,"#FFF6E7" if v==20 else PALE)
            s+=text(105,y+42,str(v),27,weight="bold")+text(390,y+42,test,24)+text(700,y+42,out,24,weight="bold")
        s+=text(450,329,"The equality case is part of the specification, not an afterthought.",21,anchor="middle")
        h=350
    elif k=="expression":
        for i,level in enumerate(("Lower production","Higher production")):
            x=10+i*455
            s+=box(x,15,435,270)+text(x+217,53,f"Cell context {i+1}",24,weight="bold",anchor="middle")
            s+=strand(x+60,107,310)+text(x+217,155,"same displayed gene region",21,anchor="middle")
            s+=arrow(x+217,171,x+217,219)
            s+=text(x+217,249,level+" of RNA",21,weight="bold",anchor="middle")
        s+=text(450,326,"Arrows: RNA production using cellular machinery, not DNA movement.",21,anchor="middle")
        s+=text(450,358,"Conceptual comparison; not measured rates or a complete cell.",21,anchor="middle")
        h=380
    elif k=="analogy":
        s+=box(10,20,385,225)+box(505,20,385,225,"#F4F7EB")
        s+=text(202,59,"SOFTWARE UNIT",24,weight="bold",anchor="middle")
        s+=text(35,107,["Stored instructions","Executed by a computer","“Computational gene”:","a proposed software label"],22)
        s+=text(697,59,"BIOLOGICAL GENE",24,weight="bold",anchor="middle")
        s+=text(530,107,["DNA region","Used by cellular machinery","RNA or protein production","Physical molecular processes"],22)
        s+=arrow(398,138,499,138,"compare",True)
        s+=text(450,285,"Resemblance: stored possibilities used in a context.",22,anchor="middle")
        s+=text(450,322,"Not identity: names do not transfer biological capabilities.",22,anchor="middle")
        h=345
    elif k=="research":
        # A true research decision flow; the lower branch is visible, not hidden in prose.
        headings=["OBSERVE","PROPOSE","COMPARE","TEST"]
        bodies=[["One biological","feature"],["One explicit","software rule"],["An ordinary","alternative"],["A declared","success check"]]
        for i in range(4):
            x=10+225*i
            s+=box(x,20,205,150)+text(x+102,57,headings[i],22,weight="bold",anchor="middle")
            s+=text(x+102,105,bodies[i],21,anchor="middle")
            if i<3:s+=arrow(x+205,140,x+226,140)
        s+=text(450,212,"Arrows: research steps; no advantage has been measured.",21,anchor="middle")
        s+=arrow(797,175,797,259)
        s+=box(464,270,426,100,"#FFF6E7")+text(677,310,["Does the claim survive the check?","Retain provisionally or revise."],22,anchor="middle")
        s+=text(25,297,["A failed prediction matters.","A resemblance is not a result."],22)
        h=395
    elif k=="roadmap":
        stages=(
            [("1  REPRESENT","Chapters 2–6","Symbols, procedures,","small programs"),
             ("2  UNDERSTAND","Chapters 7–20","Molecules and","controlled operations"),
             ("3  COMBINE & TEST","Chapters 21–36","DNA methods, limits,","and evidence")]
            if book=="DNA Computing" else
            [("1  PROGRAM","Chapters 2–8","Choices and learning","from small examples"),
             ("2  BUILD & COMPARE","Parts III–VI","Sequences, mechanisms","and fair comparisons"),
             ("3  INVESTIGATE","Parts VII–XIV","Training, engines","and measured limits")])
        for i,(heading,chap,a,b) in enumerate(stages):
            x=10+i*300
            s+=box(x,20,280,250)+text(x+140,61,heading,21,weight="bold",anchor="middle")
            s+=text(x+140,106,chap,23,anchor="middle")+text(x+140,170,[a,b],21,anchor="middle")
        for x in (10,310):
            s+=arrow(x+258,235,x+322,235)
        s+=text(450,311,"Arrows: teaching order. These later chapters are still planned.",21,anchor="middle")
        h=335
    else:
        raise ValueError("unsupported figure kind: "+k)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="{h}" viewBox="0 0 900 {h}" role="img" aria-labelledby="title desc">
<title id="title">{escape(f["id"]+": "+f["title"])}</title>
<desc id="desc">{escape(f["caption"]+" "+f["risk"])}</desc>
<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="{BLUE}"/></marker></defs>
<rect width="900" height="{h}" fill="white"/>
<g font-family="DejaVu Sans, sans-serif">{s}</g></svg>
'''

def validate(plan):
    assert plan["status"] == "storyboard-internally-approved-before-prose"
    ids=[]
    for f in plan["figures"]:
        assert all(f.get(k) for k in ("id","question","concept","prerequisites","objects","steps","caption","risk","evidence","review"))
        assert len(f["steps"]) >= 3
        ids.append(f["id"])
    assert len(ids)==len(set(ids))
    return True

def outputs():
    plan=json.loads((ROOT/"pedagogy/ch01-storyboard.json").read_text())
    validate(plan)
    book=json.loads((ROOT/"pedagogy/curriculum.json").read_text())["book"]
    out={}
    for f in plan["figures"]:
        out[f"book/figures/undergraduate/{f['id']}.svg"]=figure(f,book)
        # These are semantic reading graphs, not pretend physical reaction graphs.
        out[f"book/diagrams/undergraduate/{f['id']}.txt"]=(
            f"FIGURE {f['id']}: {f['title']}\nQUESTION: {f['question']}\n"
            f"OBJECTS: {f['objects']}\nRELATION: explanatory reading order, not an unlabelled physical cause\n"
            +"\n".join(f"STEP {i}: {step}" for i,step in enumerate(f["steps"],1))+"\n"
            +" → ".join(f"STEP {i}" for i in range(1,len(f["steps"])+1))+"\n"
            f"CAPTION: {f['caption']}\nLIMIT: {f['risk']}\nEVIDENCE: {f['evidence']}\n")
    spec=importlib.util.spec_from_file_location("chapter_rule",ROOT/"examples/undergraduate/ch01_rule.py")
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    if book=="DNA Computing":
        cases=[{"input":n,"output":mod.add_two(n)} for n in (0,3,4)]
        headings="Starting count & Add exactly two & Output"
        rows=[f"{r['input']} & {r['input']} + 2 & {r['output']}" for r in cases]
    else:
        cases=[{"input":n,"below_twenty":n<20,"output":mod.heater(n)} for n in (18,20,22)]
        headings="Temperature & Below twenty? & Returned word"
        rows=[f"{r['input']} & {'yes' if r['below_twenty'] else 'no'} & {r['output']}" for r in cases]
    out["artifacts/undergraduate/ch01-results.json"]=json.dumps({"kind":"deterministic teaching example; not a scientific benchmark","cases":cases},indent=2)+"\n"
    out["tex/undergraduate/ch01-trace.tex"]=(
        "% Generated from tested examples/undergraduate/ch01_rule.py; do not hand edit.\n"
        "\\begin{center}\\begin{tabular}{lll}\\toprule\n"+headings+" \\\\\\midrule\n"
        +" \\\\\n".join(rows)+" \\\\\\bottomrule\n\\end{tabular}\\end{center}\n")
    return out

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--check",action="store_true")
    args=p.parse_args()
    stale=[]
    for name,content in outputs().items():
        dest=ROOT/name
        if args.check:
            if not dest.exists() or dest.read_text()!=content:stale.append(name)
        else:
            dest.parent.mkdir(parents=True,exist_ok=True)
            dest.write_text(content)
    if stale: raise SystemExit("Stale Chapter 1 outputs: "+", ".join(stale))
    print("Chapter 1: six original SVG/TXT pairs and executable trace "+("fresh" if args.check else "written"))
if __name__=="__main__":
    main()
