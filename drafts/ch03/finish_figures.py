"""Remaining Chapter 3 mechanisms, with distinct molecular and software semantics."""
from build_deep_chapter import txt, rect, line, circle, BLUE, GREEN, RED, GRAY
from scientific_visuals import strand, protein

def tube(x,y,label,include=True,lost=False):
    s=f'<path d="M{x},{y} L{x},{y+95} Q{x+70},{y+170} {x+140},{y+95} L{x+140},{y}" fill="#EDF5FA" stroke="#5B6874" stroke-width="3"/>'
    s+=line(x-5,y,x+145,y,arrow=False,color=GRAY)
    if include:
        for i in range(3 if include is True else int(include)):
            xx=x+27+i*28; yy=y+30+(i%2)*27
            style=' stroke-dasharray="4 4" opacity=".45"' if lost and i==1 else ''
            s+=f'<path d="M{xx},{yy} q12,-13 24,0 t24,0" fill="none" stroke="{GREEN if i==1 else BLUE}" stroke-width="3"{style}/>'
    s+=txt(x+70,y+175,label,18,"bold","middle")
    return s

def render_extra(kind,r):
    if kind=="parallel":
        s=txt(450,35,"Four candidate histories; three sequential tests each",25,"bold","middle")
        s+=txt(450,75,"Toy work/depth model: one test is one abstract unit, not one second.",19,anchor="middle")
        for row in range(4):
            y=145+row*87
            s+=txt(40,y+9,"copy "+str(row+1),20)
            for col in range(3):
                x=225+col*225
                if col: s+=line(x-170,y,x-36,y)
                s+=circle(x,y,str(col+1),r=28)
            s+=txt(800,y+8,"result",19)
        s+=line(195,490,705,490)
        s+=txt(450,535,"Critical-path depth = 3     Total work = 4 × 3 = 12",23,"bold","middle")
        s+=txt(450,583,"Parallel execution needs simultaneous capacity; serial reuse needs more time.",19,anchor="middle")
        return s,620
    if kind=="absence":
        s=txt(450,35,"One observation, several possible physical histories",25,"bold","middle")
        for x,head,include in [(60,"NOT GENERATED",False),(375,"LOST IN PROCESSING",True),(690,"NOT DETECTED",True)]:
            s+=txt(x+70,100,head,18,"bold","middle")+tube(x,135,"no recorded signal",include,lost=x==375)
        s+=txt(450,335,"Dashed green target: removed during processing; blue strands are background.",17,anchor="middle")
        s+=txt(450,360,"Panels are alternative causes—not three successive steps of one experiment.",19,anchor="middle")
        s+=rect(35,395,830,130)+txt(55,433,"Independent-copy toy model",23,"bold")
        s+=txt(55,472,["q = p × survival × detection = 0.1 × 0.5 × 0.8 = 0.04",
                      "P(at least one signal in M copies) = 1 − (1 − q)^M"],21)
        s+=txt(450,571,"M = 10: probability ≈ "+format(r["coverage"][2]["signal_probability"],".6f"),23,"bold","middle")
        s+=txt(450,617,"Copy independence and calibrated probabilities are assumptions, not observations.",18,anchor="middle")
        return s,651
    if kind=="audit":
        s=txt(450,35,"Open the cycle, then prove both directions",26,"bold","middle")
        for y,names in [(155,["0","1","2"]),(350,["s","1","2","t"])]:
            for i,name in enumerate(names):
                x=130+i*(300 if len(names)==3 else 210)
                if i: s+=line(x-(244 if len(names)==3 else 154),y,x-32,y)
                s+=circle(x,y,name)
        s+=line(730,181,730,221,arrow=False)+line(730,221,130,221,arrow=False)+line(130,221,130,183)
        s+=line(450,245,450,307)
        s+=txt(465,276,"split pivot 0",19)
        s+=txt(450,411,"Open: cycle ⇒ s–t path       Close: s–t path ⇒ cycle",23,"bold","middle")
        s+=rect(40,452,820,126)+txt(60,490,["Size: n becomes n+1; each original edge is redirected once.",
                 "Forward and backward implications preserve existence.",
                 "Finite tests detect bugs; the argument establishes the general map."],21)
        return s,615
    if kind=="boundary":
        s=txt(450,35,"The same symbolic state need not mean the same physical population",23,"bold","middle")
        s+=txt(450,87,"One Boolean entry: D[S,v] = true",25,"bold","middle")
        s+=line(450,108,250,162,dash=True)+line(450,108,650,162,dash=True)
        s+=tube(180,183,"one surviving copy",1)+tube(580,183,"many copies, same state",True)
        s+=txt(450,395,"The state records existence, not abundance, yield or reaction history.",21,anchor="middle")
        s+=strand(145,447,220,paired=True)
        s+=line(410,487,481,487,dash=True)
        s+=rect(507,435,350,130)+txt(527,471,["Computational abstraction",
               "sequence / visited set / endpoint",
               "physical state is not preserved"],18)
        s+=txt(450,620,"Pairing and backbone are different; this duplex is a schematic, not a designed reagent.",18,anchor="middle")
        return s,651
    if kind=="discrete":
        s=txt(450,35,"A biological motivation does not define the derivative",24,"bold","middle")
        s+=txt(30,86,"BIOLOGY: promoter occupancy can inhibit transcription initiation.",20)
        s+=line(70,168,820,168,width=5,arrow=False)+line(70,192,820,192,color=GREEN,width=5,arrow=False)
        s+=txt(40,172,"5′",17)+txt(834,172,"3′",17)+txt(40,203,"3′",17)+txt(834,203,"5′",17)
        s+=rect(235,157,160,46,"#FFF0D5")+txt(315,189,"promoter",19,anchor="middle")
        s+=protein(315,140,"repressor")
        s+=txt(50,232,"Simplified bacterial mechanism; occupancy is not a literal binary computer switch.",18)
        s+=txt(30,300,"SOFTWARE: choose f(r) = 2 for r ≥ 0, and −1 for r < 0.",22,"bold")
        s+=line(135,478,765,478)+line(450,535,450,344)
        s+=line(165,520,449,520,color=RED,width=4,arrow=False)
        s+=line(451,375,740,375,color=GREEN,width=4,arrow=False)
        s+=circle(450,375,"",r=6,fill=GREEN,color=GREEN)
        s+=circle(450,520,"",r=6,fill="white",color=RED)
        s+=txt(764,485,"r",20)+txt(464,552,"0",20)
        s+=txt(175,563,"Left value −1",19)+txt(568,358,"Right value 2",19)
        s+=txt(450,619,"At r = 0: central difference = 3/(2h); no finite classical derivative.",21,"bold","middle")
        s+=txt(450,665,"Away from the boundary, selection is locally constant; selected parameters can still learn.",18,anchor="middle")
        return s,700
    if kind=="optimizers":
        s=txt(450,35,"Momentum is persistent optimizer state",26,"bold","middle")
        s+=txt(450,77,"L(θ)=θ²/2; learning rate 0.1; momentum 0.9; no decay or dampening.",19,anchor="middle")
        for i,row in enumerate(r["momentum"]):
            y=165+i*200
            s+=txt(30,y-37,"STEP "+str(i+1),21,"bold")
            vals=[("parameter",row["before"]),("gradient",row["gradient"]),("buffer",row["buffer"]),("new parameter",row["after"])]
            for j,(label,value) in enumerate(vals):
                x=25+j*225
                s+=rect(x,y,185,92)+txt(x+92,y+31,label,18,"bold","middle")+txt(x+92,y+69,format(value,".2f"),25,anchor="middle")
                if j<3:s+=line(x+189,y+46,x+220,y+46)
                if label=="buffer":s+=line(x+7,y+8,x+178,y+8,arrow=False)
        s+=line(568,257,568,360,dash=True)+txt(585,309,"retain v",19)
        s+=txt(450,520,"First buffer v₁ = g₁. Then v₂ = 0.9v₁ + g₂ = 1.8.",22,"bold","middle")
        s+=txt(450,565,"Both steps use the same derivative rule; history changes the second update.",20,anchor="middle")
        s+=txt(450,610,"This is the declared PyTorch SGD convention, not an Adam or evolution algorithm.",19,anchor="middle")
        return s,650
    if kind=="state":
        s=txt(450,35,"A finite-difference test must evaluate the same function twice",24,"bold","middle")
        s+=txt(450,81,"L(θ;s) = (θ+s)², θ=2, s=3, h=0.001",23,anchor="middle")
        for x,title,second,value in [(25,"CONTROLLED",3,r["fixed_state_difference"]),(475,"STATE DRIFT",4,r["changed_state_difference"])]:
            s+=rect(x,126,400,353)+txt(x+20,166,title,23,"bold")
            s+=txt(x+20,215,["plus:  θ+h, state 3",f"minus: θ−h, state {second}"],21)
            s+=line(x+200,276,x+200,316)
            s+=txt(x+200,363,"central difference",21,anchor="middle")+txt(x+200,415,format(value,".3f"),29,"bold","middle",GREEN if second==3 else RED)
        s+=txt(450,534,"The derivative at fixed state is 2(θ+s) = 10.",23,"bold","middle")
        s+=txt(450,580,"Changing state adds another difference; dividing by tiny h amplifies the confound.",19,anchor="middle")
        s+=txt(450,626,"Reset state and replay RNG for both evaluations; parameter perturbation is the only change.",18,anchor="middle")
        return s,665
    if kind=="next":
        s=txt(450,35,"Verified local derivatives are one gate in a training lifecycle",24,"bold","middle")
        labels=[("DATA / SPLIT","fixed information access"),("FORWARD + LOSS","declared mask / denominator"),("BACKWARD","derivative contract"),("UPDATE","parameters + optimizer state"),("CHECKPOINT","parameters, state, RNG, cursor")]
        for i,(title,sub) in enumerate(labels):
            y=85+i*112
            s+=rect(120,y,660,82)+txt(145,y+31,title,21,"bold")+txt(145,y+63,sub,19)
            if i<4:s+=line(450,y+82,450,y+108)
        s+=txt(450,707,"Chapter 4 must test restart equivalence and held-out evaluation; this is a plan.",20,anchor="middle")
        return s,745
    raise ValueError(kind)

def semantic_lines(kind):
    return {
    "parallel":["4 candidate histories × 3 tests = 12 work units; critical-path depth 3.","Parallel workers consume capacity; laboratory time is not abstract depth."],
    "absence":["No witness generated ⇢ no signal; witness lost ⇢ no signal; detection failure ⇢ no signal.","For independent copies: q=p·survival·detection; P(signal)=1−(1−q)^M."],
    "audit":["Cycle ⇢ split pivot ⇢ path; path ⇢ identify endpoints ⇢ cycle.","Construction size n+1 and m; both existence implications required."],
    "boundary":["D[S,v]=true ⇢ one or many physical realizations.","Existence does not store copy count, yield or kinetic state; a molecular mapping adds assumptions."],
    "discrete":["Promoter occupancy ⇢ biological initiation control; analogy only.","r<0 ⇒ f=−1; r≥0 ⇒ f=2. At zero central difference is 3/(2h), not a finite derivative."],
    "optimizers":["θ=1 ⇢ g=1 ⇢ v=1 ⇢ θ=0.9; retain v.","θ=0.9 ⇢ g=0.9 ⇢ v=1.8 ⇢ θ=0.72; no decay or dampening."],
    "state":["Hold s=3 in both L(θ+h;s) and L(θ−h;s): derivative ≈10.","Changing the second state to 4 gives ≈−5489; this compares different functions."],
    "next":["dataset / split ⇢ forward / loss ⇢ backward ⇢ update ⇢ checkpoint.","Chapter 4: replay parameters, optimizer, relevant state, RNG and data cursor."]}[kind]
