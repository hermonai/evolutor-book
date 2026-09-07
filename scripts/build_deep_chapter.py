"""Original deep Chapter 1 vectors, keyframes and source-linked numerical tables."""
import argparse
import importlib.util
import inspect
import json
import math
from html import escape
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DNA=ROOT.name=="dna-computing-book"
INK="#18344A"; BLUE="#176CA4"; GREEN="#28764A"; GOLD="#A56713"; PURPLE="#7147A8"
PALE="#EDF5FA"; RED="#AD3346"; GRAY="#5B6874"

def txt(x,y,lines,size=23,weight="normal",anchor="start",color=INK):
    x,y=round(x,5),round(y,5)
    if isinstance(lines,str): lines=lines.split("|")
    return "".join(f'<text x="{x}" y="{y+i*(size+8)}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" fill="{color}">{escape(line)}</text>' for i,line in enumerate(lines))

def rect(x,y,w,h,fill=PALE,stroke="#ABC1CF"):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>'

def line(x1,y1,x2,y2,color=BLUE,width=3,dash=False,arrow=True):
    x1,y1,x2,y2=(round(v,5) for v in (x1,y1,x2,y2))
    return f'<path d="M{x1},{y1} L{x2},{y2}" fill="none" stroke="{color}" stroke-width="{width}"'+(' stroke-dasharray="8 6"' if dash else "")+(' marker-end="url(#arrow)"' if arrow else "")+'/>'

def circle(x,y,label,fill="#FFFFFF",color=BLUE,r=25):
    x,y=round(x,5),round(y,5)
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{color}" stroke-width="2.5"/>'+txt(x,y+8,label,24,"bold","middle",color)

def panel(x,y,w,h,title,body,fill=PALE):
    return rect(x,y,w,h,fill)+txt(x+16,y+35,title,23,"bold")+txt(x+16,y+75,body,21)

def envelope(f,body,height):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="900" height="{height}" viewBox="0 0 900 {height}" role="img" aria-labelledby="title desc">'
            f'<title id="title">{escape(f["id"]+": "+f["title"])}</title><desc id="desc">{escape(f["teachingPurpose"]+" "+f["limit"])}</desc>'
            '<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L0,6 L7,3 z" fill="#176CA4"/></marker></defs>'
            '<rect width="100%" height="100%" fill="white"/><g font-family="DejaVu Sans, sans-serif">'+body+'</g></svg>\n')

def graph(m):
    pos={"A":(65,200),"B":(250,70),"C":(250,330),"D":(480,200),"E":(665,70),"F":(825,200)}
    s=""
    for a,b in sorted(m.EDGES):
        x1,y1=pos[a];x2,y2=pos[b]
        if {a,b}=={"B","C"}:
            bend=40 if a=="B" else -40
            s+=f'<path d="M{x1+bend/3},{y1+(25 if y2>y1 else -25)} Q{x1+bend},{200} {x2+bend/3},{y2+(-25 if y2>y1 else 25)}" fill="none" stroke="{BLUE}" stroke-width="2.5" marker-end="url(#arrow)"/>'
        else:
            dx=x2-x1;dy=y2-y1;r=math.hypot(dx,dy)
            s+=line(x1+dx*28/r,y1+dy*28/r,x2-dx*31/r,y2-dy*31/r)
    for name,(x,y) in pos.items(): s+=circle(x,y,name)
    s+=txt(450,395,"Start A; finish F. Nine directed edges; arrow direction matters.",22,anchor="middle")
    return s,420

def grid(steps,current=None,cols=3,connect=True):
    rows=math.ceil(len(steps)/cols);w=880/cols-14;h=116;s=""
    for i,(title,body) in enumerate(steps):
        x=10+(i%cols)*(880/cols);y=15+(i//cols)*(h+25)
        fill=("#FFF0D5" if i==current else PALE) if current is not None else PALE
        s+=panel(x,y,w,h,f"{i+1}  {title}",body,fill)
        if connect and i%cols<cols-1 and i+1<len(steps):
            s+=line(x+w+1,y+h/2,x+880/cols-3,y+h/2)
    return s,rows*(h+25)+20

def figure(f,m):
    k=f["kind"];s="";h=420
    if k=="field":
        for i,(a,b,c) in enumerate([
            ("FORMAL","Graph + predicates","A sequence is a witness"),
            ("PHYSICAL","Strands + reactions","A sample yields a signal"),
            ("INTERPRETIVE","Decode + independent check","The signal supports a claim")]):
            y=15+i*127
            s+=panel(15,y,870,108,a,b+"|"+c)
        h=412
    elif k=="graph": return envelope(f,*graph(m))
    elif k=="routes":
        routes=[("ABCDEF","VALID","all six, legal edges"),("ABCBDF","REPEAT","B twice; E absent"),
                ("ABDEF","SHORT","C absent; only five"),("ABECDF","ILLEGAL EDGE","B→E and E→C absent")]
        for i,(route,label,note) in enumerate(routes):
            y=30+i*100
            s+=rect(10,y-15,880,90,"#F0F8F2" if i==0 else PALE)
            s+=txt(28,y+13,label,20,"bold")
            for j,v in enumerate(route):
                x=290+j*68
                if j: s+=line(x-42,y+5,x-28,y+5)
                s+=circle(x,y+5,v,r=24)
            s+=txt(285,y+57,note,20,color=GRAY)
        h=430
    elif k=="encoding":
        s+=txt(450,32,"Two edge fragments meet at vertex B",25,"bold","middle")
        # Domain blocks share B's split vertex code at a nick.
        for x,label,color in [(115,"a_R",BLUE),(290,"b_L",GREEN),(475,"b_R",GREEN),(650,"c_L",PURPLE)]:
            s+=rect(x,85,145,63,"#EFF5FA",color)+txt(x+72,127,label,26,"bold","middle",color)
        s+=line(93,116,110,116,arrow=False)+txt(35,122,"5′",24)
        s+=line(799,116,825,116,arrow=False)+txt(838,122,"3′",24)
        s+=line(260,116,290,116,arrow=False)
        s+=line(620,116,650,116,arrow=False)
        s+=line(435,296,475,296,color=GREEN,arrow=False)
        s+=txt(190,190,"edge A→B",22,anchor="middle")+txt(655,190,"edge B→C",22,anchor="middle")
        s+=txt(453,76,"nick",21,"bold","middle",RED)
        s+=line(442,116,468,116,color=RED,dash=True,arrow=False)
        for x,label in [(290,"b_L*"),(475,"b_R*")]:
            s+=rect(x,265,145,63,"#EAF4ED",GREEN)+txt(x+72,307,label,26,"bold","middle",GREEN)
            for xx in range(x+15,x+140,22): s+=line(xx,155,xx,255,color=GREEN,width=1.5,dash=True,arrow=False)
        s+=txt(238,306,"3′",24)+txt(636,306,"5′",24)
        s+=txt(450,367,"B splint: antiparallel pairing aligns the adjacent ends.",22,anchor="middle")
        s+=txt(450,402,"Dashed vertical marks: pairing. Closing the nick makes a backbone bond.",20,anchor="middle")
        h=430
    elif k=="pool":
        entries=[("ABCDEF",3),("ACBDEF",2),("ABCBDF",2),("ABDEF",4),("ABECDF",1)]
        s+=rect(15,20,870,335)
        for i,(r,n) in enumerate(entries):
            y=62+i*59
            s+=txt(40,y,r,25,"bold")
            for j in range(n): s+=circle(330+j*100,y-8,str(i+1),r=18)
            s+=txt(790,y,f"×{n}",24,"bold")
        s+=txt(450,390,"Illustrative copies only; the last route is an injected pseudo-path.",21,anchor="middle")
        h=415
    elif k=="pipeline":
        s,h=grid([("Graph","constraints"),("Codes","vertex identity"),("Edges","oriented overlaps"),
                  ("Mix","physical preparation"),("Candidates","possible assemblies"),("Endpoints","PCR enrichment"),
                  ("Length","size selection"),("Vertices","affinity retention"),("Read + check","decode; verify graph")])
        s+=txt(450,h+12,"Design → chemistry → evidence. Panels are conceptual stages, not a lab protocol.",20,anchor="middle");h+=36
    elif k=="lab":
        rows=[("Join","Ligase seals a nick","incompatible / unjoined ends"),
              ("Endpoints","Primers + amplification","off-target amplification"),
              ("Length","Gel size fraction","overlapping bands"),
              ("Contains B","Complementary capture","loss / nonspecific retention"),
              ("Witness","Decoded order + verifier","ambiguous mixed signal")]
        for i,(a,b,c) in enumerate(rows):
            y=20+i*77
            s+=rect(10,y,880,65,"#F0F6FA" if i%2==0 else "#FFFFFF")
            s+=txt(26,y+41,a,22,"bold")+txt(190,y+41,b,21)+txt(550,y+41,c,20,color=GRAY)
        s+=txt(450,435,"Predicate     /     intended physical mechanism     /     possible failure",20,anchor="middle");h=455
    elif k=="readout":
        s+=txt(450,29,"Synthetic expected bands for the teaching witness A B C D E F",23,"bold","middle")
        s+=rect(110,65,680,320,"#F2F6F8")
        for j,(v,bp) in enumerate(zip("BCDEF",[40,60,80,100,120])):
            x=200+j*120
            s+=rect(x-23,75,46,15,"#DCE7EF")
            s+=txt(x,56,v,22,"bold","middle")
            y=360-(bp-40)*2.5
            s+=f'<rect x="{x-32}" y="{y}" width="64" height="8" fill="{BLUE}"/>'
        for bp in [40,60,80,100,120]:
            y=360-(bp-40)*2.5
            s+=txt(93,y+9,str(bp),19,anchor="end")
        s+=txt(52,245,"bp",20,"bold")
        s+=txt(450,424,"Assume 20 bases per vertex in this idealized length model.",21,anchor="middle")
        s+=txt(450,457,"A mixture can superpose bands from different molecules.",21,anchor="middle",color=RED);h=480
    elif k=="scaling":
        s+=txt(450,30,"Fixed endpoints: internal vertex orders = (n − 2)!",24,"bold","middle")
        s+=line(100,340,790,340,arrow=False)+line(100,340,100,70,arrow=False)
        for y in (0,5,10,15,20,25):
            py=340-y*10
            s+=line(100,py,790,py,color="#DCE4E9",width=1,arrow=False)+txt(82,py+6,str(y),18,anchor="end")
        points=[]
        for row in m.results()["scaling"]:
            x=100+(row["n"]-6)*34
            y=340-math.log10(row["internal_orders"])*10
            points.append((x,y))
            s+=circle(x,y,"",r=5)+txt(x,371,str(row["n"]),20,anchor="middle")
        for a,b in zip(points,points[1:]): s+=line(*a,*b,arrow=False)
        s+=txt(450,412,"n: number of vertices",22,anchor="middle")+txt(110,62,"log10(candidate count)",20)
        s+=txt(450,452,"M ≥ ln(δ) / ln(1 − p)   under independent draws, 0 < p < 1.",22,anchor="middle")
        s+=txt(450,490,"A count is not a concentration, reaction time or success probability.",20,anchor="middle",color=GRAY);h=510
    elif k=="frontier":
        s,h=grid([("Search","candidate selection"),("Automata","state transitions"),("CRNs","reaction dynamics"),
                  ("Circuits","composed gates"),("Assembly","local geometry"),("Simulation","digital models")],connect=False)
        s+=txt(450,h+10,"Storage and learned DNA representations are related, distinct activities.",21,anchor="middle");h+=35
    elif k=="compare":
        heads=["PROGRAM","NEURAL MODEL","GENOMIC SYSTEM"]
        lines=[["code / configuration","calls and branches","processor + runtime","output and state"],
               ["structure + weights","activations / routing","tensor operations","prediction and state"],
               ["DNA + cellular context","regulated expression","molecular machinery","products / phenotype"]]
        for i in range(3):
            x=10+i*300
            s+=panel(x,20,280,350,heads[i],lines[i][0])
            for j in range(1,4):
                s+=line(x+140,90+j*65-40,x+140,90+j*65-15)
                s+=txt(x+140,90+j*65,lines[i][j],19,anchor="middle")
        s+=txt(450,409,"Aligned questions do not make the three mechanisms identical.",22,anchor="middle");h=435
    elif k=="stored":
        s+=panel(10,15,880,110,"ONE IMMUTABLE CATALOG","clip     center     prefix")
        s+=panel(10,180,425,165,"bounded","clip → prefix|[3, −1, 2] → [3, 3, 5]")
        s+=panel(465,180,425,165,"balanced","center → prefix|output: [5/3, −2/3, 0]")
        s+=line(225,128,225,175)+line(675,128,675,175)
        s+=txt(450,394,"Same catalog and input; context changes the selected plan.",22,anchor="middle");h=425
    elif k=="regulation":
        s+=txt(450,33,"A qualitative transcription-control example",25,"bold","middle")
        s+=line(90,208,810,208,width=5,arrow=False)
        s+=rect(290,170,110,74,"#E7F2EA",GREEN)+txt(345,216,"site",23,"bold","middle")
        s+=rect(470,170,285,74,PALE)+txt(610,216,"transcribed region",22,"bold","middle")
        s+=circle(345,88,"R",r=32,color=GREEN)+txt(400,95,"regulatory molecule",23)
        s+=line(345,122,345,162,color=GREEN)
        s+=txt(90,250,"DNA",22,"bold")
        s+=line(610,250,610,299)+txt(610,336,"RNA synthesis",24,"bold","middle")
        s+=txt(450,390,"Binding can change activity; the DNA sequence need not change.",21,anchor="middle")
        s+=txt(450,424,"Other control points exist; no quantitative rates are shown.",20,anchor="middle",color=GRAY);h=450
    elif k=="expression":
        s+=circle(450,25,"",r=10,fill=INK,color=INK)
        s+=panel(315,62,270,105,"Read context","request argument")
        s+=line(450,38,450,57)
        s+='<path d="M450,195 L535,240 L450,285 L365,240 z" fill="#FFFFFF" stroke="#176CA4" stroke-width="2"/>'
        s+=txt(450,247,"context?",20,anchor="middle")
        s+=line(450,170,450,191)
        s+=panel(20,310,380,110,"clip → prefix","selected plan")
        s+=panel(500,310,380,110,"center → prefix","selected plan")
        s+=txt(185,277,"[bounded]",20)+txt(605,277,"[balanced]",20)
        s+=line(365,240,210,305)+line(535,240,690,305)
        s+='<path d="M450,440 L485,465 L450,490 L415,465 z" fill="white" stroke="#176CA4" stroke-width="2"/>'
        s+=line(210,425,410,462)+line(690,425,490,462)
        s+=panel(285,525,330,100,"Execute / trace","operations in order")
        s+=line(450,493,450,520)
        s+=line(450,630,450,655)
        s+=circle(450,675,"",r=15,fill="white",color=INK)+circle(450,675,"",r=8,fill=INK,color=INK)
        s+=txt(450,725,"UML activity; unknown context raises an error (not shown).",20,anchor="middle");h=750
    elif k=="development":
        s,h=grid([("Description","repeat prefix 2 times"),("Development","construct ordered plan"),("Program","prefix → prefix")])
        s+=panel(15,190,870,155,"Execute on [3, −1, 2]","first prefix: [3, 2, 4]|second prefix: [3, 5, 9]")
        s+=txt(450,390,"Generating a program is already possible in ordinary software.",22,anchor="middle");h=420
    elif k=="timescales":
        rows=[("STATE","one execution","s changes"),("PARAMETERS","optimizer updates","θ changes"),
              ("STRUCTURE","proposal / validation","module graph changes"),("POPULATION","variation / selection","descriptions change")]
        for i,(a,b,c) in enumerate(rows):
            y=20+i*105
            s+=panel(10,y,265,90,a,b)
            s+=line(305,y+45,600,y+45)
            s+=txt(630,y+52,c,20)
        s+=txt(450,465,"Different update rules; no universal ordering of physical durations.",21,anchor="middle");h=490
    elif k=="alternatives":
        rows=[("Dispatch / plugins","select stored routines"),("MoE / conditional networks","route work among experts"),
              ("Attention / retrieval","query accessible representations"),("Recurrence / SSMs","update carried state"),
              ("Synthesis / architecture search","construct or search programs"),
              ("Agent / workflow systems","compose tools and actions")]
        for i,(a,b) in enumerate(rows):
            y=15+i*65;s+=rect(10,y,880,56,PALE if i%2==0 else "#FFFFFF")
            s+=txt(28,y+36,a,21,"bold")+txt(448,y+36,b,21)
        s+=txt(450,442,"A new label must earn a new semantic or empirical contribution.",21,anchor="middle");h=470
    elif k=="taxonomy":
        for x,y,w,heading,body in [
            (225,15,450,"«research» Evolutor","theory / experiments"),
            (15,185,400,"«model» DOGMA","non-Transformer DNA-native"),
            (485,185,400,"«model» Hermon DNA","Transformer-based DNA"),
            (15,350,400,"«engine» DOGMA Engine","state-native execution"),
            (485,350,400,"«engine» Hermon DNA Engine","attention / KV execution"),
            (225,530,450,"«orchestration» Evolutor","compose engines and modules")]:
            s+=panel(x,y,w,110,heading,body)
        s+=line(370,130,215,180,dash=True)+line(530,130,685,180,dash=True)
        s+=line(215,345,215,300,dash=True)+line(685,345,685,300,dash=True)
        s+=txt(232,330,"implements",18)+txt(702,330,"implements",18)
        s+=line(370,525,215,465,dash=True)+line(530,525,685,465,dash=True)
        s+=txt(190,510,"invokes",18)+txt(660,510,"invokes",18)
        s+=txt(450,685,"Dashed arrows: client depends on target; proposed roles only.",20,anchor="middle");h=710
    elif k=="memory":
        s+=panel(10,15,425,365,"DOGMA candidate","carried state per request")
        s+=panel(465,15,425,365,"Hermon DNA","K/V representations by position")
        for i in range(3):
            s+=rect(60,130+i*65,315,45,"#EFEAF8",PURPLE)+txt(217,161+i*65,["state block 1","state block 2","state block L"][i],21,anchor="middle",color=PURPLE)
        for i in range(4):
            s+=rect(505,125+i*48,335,36,PALE)+txt(675,150+i*48,f"position {i+1}: K and V",20,anchor="middle")
        s+=txt(675,350,"append next position",20,anchor="middle")
        s+=panel(10,420,880,100,"BOTH ALSO NEED","weights + temporary buffers + optional history, external memory and traces")
        s+=txt(450,565,"Compression and addressability are strategies, not a universal ranking.",21,anchor="middle");h=590
    elif k=="roadmap":
        s,h=grid([("Semantics","types / transitions"),("Reference","exact runnable model"),("Parity","state / logits / causality"),
                  ("Experiments","baselines / ablations"),("Engine","profile before kernels"),("Capabilities","test transfer and limits")])
        s+=txt(450,h+10,"A failure sends the proposal back for revision; no gate is proof of AGI.",20,anchor="middle");h+=36
    else:
        raise ValueError("unrepresented figure kind: "+k)
    return envelope(f,s,h)

def module():
    spec=importlib.util.spec_from_file_location("deep_example",ROOT/"examples/deep/ch01.py")
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def outputs():
    data=json.loads((ROOT/"pedagogy/deep-ch01-storyboard.json").read_text())
    if data["status"] not in {"storyboard-internally-approved-before-prose","internally-reviewed-produced"}:
        raise ValueError("storyboard approval required")
    if len(data["figures"])!=10 or len({f["id"] for f in data["figures"]})!=10:
        raise ValueError("ten unique production figures required")
    m=module();result={};computed=m.results()
    excerpts=[]
    names=("is_hamiltonian","walks","filter_pool") if DNA else ("select","execute")
    for name in names:
        source,start=inspect.getsourcelines(getattr(m,name))
        end=start+len(source)-1
        excerpts.append(r"\VerbatimInput[fontsize=\footnotesize,numbers=left,numbersep=5pt,firstline="
                        +str(start)+",lastline="+str(end)+r"]{../examples/deep/ch01.py}")
    result["tex/deep/ch01-code.tex"]="\n\n".join(excerpts)+"\n"
    result["artifacts/deep/ch01-results.json"]=json.dumps(computed,indent=2,ensure_ascii=False)+"\n"
    for f in data["figures"]:
        if not f["steps"] or not f["limit"]: raise ValueError("incomplete storyboard")
        result["book/figures/deep/"+f["id"]+".svg"]=figure(f,m)
        records=[f'ID: {f["id"]}',f'TITLE: {f["title"]}',"PURPOSE: "+f["teachingPurpose"]]
        records += [f"STEP {i} → STEP {i+1}: {a} → {b}" for i,(a,b) in enumerate(zip(f["steps"],f["steps"][1:]),1)]
        records += ["LIMIT: "+f["limit"],"EVIDENCE: "+f["evidence"]]
        result["book/diagrams/deep/"+f["id"]+".txt"]="\n".join(records)+"\n"
    if DNA:
        rows=[r"\begin{tabular}{lrr}",r"\toprule Stage & Legal walks & With pseudo-path \\",r"\midrule"]
        for name,count in computed["counts"].items():
            rows.append(f"{name.capitalize()} & {count} & {computed['contaminated_counts'][name]} "+r"\\")
        rows += [r"\bottomrule",r"\end{tabular}"]
        result["tex/deep/ch01-results.tex"]="\n".join(rows)+"\n"
        scale=[r"\begin{tabular}{rr}",r"\toprule Vertices $n$ & Internal orders $(n-2)!$ \\",r"\midrule"]
        scale += [f"{r['n']} & {r['internal_orders']:,} "+r"\\" for r in computed["scaling"]]
        scale += [r"\bottomrule",r"\end{tabular}"]
        result["tex/deep/ch01-scaling.tex"]="\n".join(scale)+"\n"
        steps=[("Graph","six teaching vertices"),("Codes","symbolic domains"),("Edges","directed overlap"),
               ("Mix","molecular components"),("Candidates","possible assemblies"),("Endpoints","amplification"),
               ("Length","size fraction"),("Coverage","sequence retention"),("Verify","check decoded witness")]
    else:
        rows=[r"\begin{tabular}{lll}",r"\toprule Context & Plan & Output \\",r"\midrule"]
        for name,c in computed["contexts"].items():
            rows.append(name+" & "+" / ".join(c["plan"])+" & "+", ".join(c["output"])+r" \\")
        rows += [r"\bottomrule",r"\end{tabular}"]
        result["tex/deep/ch01-results.tex"]="\n".join(rows)+"\n"
        steps=[("Persistent","module catalog"),("Context","request input"),("Regulate","choose plan"),
               ("Express","ordered operations"),("Execute","produce output"),("Trace","record operations"),
               ("Adapt?","future proposal only")]
    prefix="animation/"+data["chapter"].lower()
    states=([
        ("FORMAL INSTANCE","V = {A,B,C,D,E,F}; start A; finish F.|Nine edges constrain consecutive vertices."),
        ("SYMBOLIC CODES","Each O_v = L_v R_v; domain lengths both h.|Codes name vertex identity, not validated sequences."),
        ("EDGE JUNCTION","A→B supplies a_R b_L; B→C supplies b_R c_L.|An antiparallel B splint aligns the nick."),
        ("PREPARATION","Edge fragments + complementary splints + suitable reagents.|Amounts and physical conditions are intentionally unspecified."),
        ("LOGICAL POPULATION","106 legal walks of 1..7 vertices in the executable model.|ABCBDF repeats B; ABDEF omits C."),
        ("ENDPOINT PREDICATE","14 model candidates begin at A and finish at F.|ABCDEF, ABCBDF and ABDEF still survive."),
        ("LENGTH PREDICATE","4 candidates contain six vertex occurrences.|ABDEF is removed; ABCBDF is still retained."),
        ("COVERAGE PREDICATE","2 candidates contain all six required identities.|ABCBDF is removed because E is absent."),
        ("DECODE AND VERIFY","ABCDEF and ACBDEF both pass the independent verifier.|An injected ABECDF would fail adjacency here.")
    ] if DNA else [
        ("PERSISTENT DESCRIPTION","Catalog = {clip, center, prefix}; all map X to X.|The catalog is unchanged throughout this execution."),
        ("REQUEST","Input x = [3, −1, 2]; context = balanced.|No learned regulator or hidden context is assumed."),
        ("REGULATION","balanced selects the ordered plan center → prefix.|bounded would select clip → prefix instead."),
        ("EXPRESSION","The selected names resolve to typed catalog operations.|A plan is ordered; a set of names would lose semantics."),
        ("EXECUTION","center gives [5/3, −7/3, 2/3].|prefix then gives [5/3, −2/3, 0]."),
        ("TRACE","Record each operation, its input and its output.|The persistent catalog still has not changed."),
        ("ADAPTATION BOUNDARY","No G→G′ update is implemented by this example.|A structural proposal needs its own update and validation rules.")
    ])
    ledger=[]
    for i,(title,body) in enumerate(steps):
        frame={"id":data["chapter"]+f"-A1-{i+1:02}","title":title,"teachingPurpose":"Static conceptual keyframe: "+body,
               "limit":"State panel changes; stage identities and layout stay fixed. Conceptual, not a live simulation."}
        svgbody,height=grid(steps,i)
        state_title,state_body=states[i]
        svgbody+=panel(10,height+10,880,160,state_title,state_body)
        height+=195
        result[f"{prefix}/frame-{i+1:02}.svg"]=envelope(frame,svgbody,height)
        ledger.append({"frame":i+1,"focus":title,"before":"entry assumptions" if i==0 else states[i-1][1],
                       "change":state_body,"unchanged":"all stage identities and layout","motion":"none; static keyframe",
                       "creationConsumption":"not asserted at this abstraction level",
                       "source":f"frame-{i+1:02}.svg"})
    result[prefix+"/frames.json"]=json.dumps(ledger,indent=2)+"\n"
    result[prefix+"/storyboard.md"]="# Chapter 1 static keyframes\n\nNine-stage DNA process or seven-stage computational process, as applicable. These are original SVG keyframes, not a rendered animation or a laboratory protocol. Each frame changes the highlighted conceptual stage and its concrete state panel. Later adaptation in Evolutor is a question, not implemented behavior.\n\n"+"\n".join(f"- Frame {x['frame']}: {x['focus']} — {x['change']}." for x in ledger)+"\n"
    return result

def main():
    p=argparse.ArgumentParser();p.add_argument("--check",action="store_true");a=p.parse_args()
    for name,content in outputs().items():
        path=ROOT/name
        if a.check:
            if not path.exists() or path.read_text()!=content: raise SystemExit("Stale deep artifact: "+name)
        else:
            path.parent.mkdir(parents=True,exist_ok=True);path.write_text(content)
    print("Deep Chapter 1 artifacts "+("fresh" if a.check else "generated"))
if __name__=="__main__":main()
