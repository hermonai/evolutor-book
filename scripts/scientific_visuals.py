"""Original molecular and research-map vectors; no raster or copied textbook art."""
import argparse
from pathlib import Path
from build_deep_chapter import txt, rect, line, circle, envelope, BLUE, GREEN, RED, GRAY
ROOT=Path(__file__).resolve().parents[1]

def strand(x,y,width=220,paired=True,nick=False):
    out=""
    for yy,color in [(y,BLUE)]+([(y+72,GREEN)] if paired else []):
        if nick and yy==y:
            out+=line(x,yy,x+width/2-8,yy,color=color,width=5,arrow=False)
            out+=line(x+width/2+8,yy,x+width,yy,color=color,width=5,arrow=False)
        else: out+=line(x,yy,x+width,yy,color=color,width=5,arrow=False)
    for i,(a,b) in enumerate(zip("ACGT","TGCA")):
        xx=x+width*(i+.5)/4
        out+=line(xx,y,xx,y+13,color=BLUE,width=2,arrow=False)
        out+=rect(xx-16,y+9,32,25,"#DDEFFC",BLUE)+txt(xx,y+29,a,17,"bold","middle")
        if paired:
            out+=rect(xx-16,y+37,32,25,"#E0F1E4",GREEN)+txt(xx,y+56,b,17,"bold","middle")
            out+=line(xx,y+34,xx,y+37,color=GRAY,width=2,dash=True,arrow=False)
            out+=line(xx,y+62,xx,y+72,color=GREEN,width=2,arrow=False)
    out+=txt(x-24,y+5,"5′",17)+txt(x+width+9,y+5,"3′",17)
    if paired: out+=txt(x-24,y+77,"3′",17)+txt(x+width+9,y+77,"5′",17)
    return out

def protein(x,y,label,color="#F8E5AE"):
    path=f'M{x-45},{y} C{x-58},{y-31} {x-18},{y-43} {x},{y-28} C{x+31},{y-49} {x+60},{y-13} {x+39},{y+10} C{x+48},{y+43} {x+7},{y+47} {x-7},{y+28} C{x-32},{y+49} {x-61},{y+22} {x-45},{y} Z'
    return '<path d="'+path+'" fill="'+color+'" stroke="#967229" stroke-width="2"/>'+txt(x,y+5,label,17,"bold","middle")

def master(dna):
    if dna:
        title="From molecular recognition to a computational claim"
        body=txt(450,38,title,25,"bold","middle")
        body+=txt(450,73,"Mechanistic schematic: four bases illustrate orientation, not an oligo design.",18,anchor="middle")
        for x,lab in [(55,"RECOGNITION"),(350,"NICKED DUPLEX"),(645,"SEALED BACKBONE")]:
            body+=txt(x+105,118,lab,19,"bold","middle")
        body+=strand(55,165,200,paired=False)
        body+=strand(350,165,200,nick=True)
        body+=strand(645,165,200)
        body+=line(285,190,315,190)+line(580,190,610,190)
        body+=protein(450,286,"ligase")
        body+=line(450,248,450,184,dash=True)
        body+=txt(65,277,["Pairing is selective,","not perfectly specific."],18)
        body+=txt(636,277,["A suitable nick can","be covalently sealed."],18)
        body+=txt(450,348,"Conditions, substrate chemistry and enzymes constrain which transitions occur.",20,anchor="middle")
        labels=[("MOLECULAR OPERATOR",["Association / ligation","yield, mismatch, kinetics"]),
                ("FORMAL PRIMITIVE",["Match / concatenate","specified symbolic rule"]),
                ("ALGORITHM + EVIDENCE",["Generate / filter / verify","sample, measure, interpret"])]
        for i,(head,lines) in enumerate(labels):
            x=20+i*300
            body+=rect(x,392,260,135)+txt(x+15,427,head,18,"bold")+txt(x+15,466,lines,18)
            if i<2: body+=line(x+264,457,x+294,457,dash=True)
        body+=txt(450,569,"Dashed bridge = abstraction, not biochemical identity or guaranteed execution.",19,anchor="middle")
        text="5′ ACGT 3′ pairs with aligned 3′ TGCA 5′; suitable nick → ligase-dependent seal.\nPhysical association / ligation ⇢ symbolic matching / concatenation ⇢ algorithm.\nThe abstraction omits concentration, kinetics, mismatch, yield and readout limits."
    else:
        title="Biological regulation motivates a research question"
        body=txt(450,38,title,25,"bold","middle")
        body+=txt(450,77,"Simplified bacterial transcription control; not a universal gene-regulation circuit.",18,anchor="middle")
        for y,label,blocked in [(151,"A  Promoter occupied: initiation inhibited",True),(307,"B  Promoter accessible: initiation may occur",False)]:
            body+=txt(30,y-30,label,21,"bold")
            body+=line(75,y+25,820,y+25,width=5,arrow=False)
            body+=line(75,y+47,820,y+47,color=GREEN,width=5,arrow=False)
            for x in range(85,820,25): body+=line(x,y+27,x,y+45,color=GRAY,width=1,arrow=False)
            body+=rect(240,y+16,155,42,"#FFF0D5")+txt(315,y+44,"promoter",19,anchor="middle")
            body+=txt(42,y+29,"5′",17)+txt(833,y+29,"3′",17)
            body+=txt(42,y+62,"3′",17)+txt(833,y+62,"5′",17)
            if blocked:
                body+=protein(319,y-1,"repressor")
                body+=txt(495,y-4,"RNAP recruitment inhibited",18)
            else:
                body+=protein(612,y+26,"RNAP")
                body+='<path d="M603,353 C580,388 555,347 532,384 S487,362 460,392" fill="none" stroke="#AD3346" stroke-width="4"/>'
                body+=txt(417,405,"5′ RNA",17,color=RED)+txt(654,y+68,"extension →",17,color=RED)
        body+=txt(450,447,"Biology does not supply a gradient rule for a hard software selector.",21,"bold","middle")
        for x,name,family in [(30,"DOGMA","non-Transformer DNA-native"),(470,"HERMON DNA","Transformer-based genomic")]:
            body+=rect(x,482,400,128)+txt(x+20,515,name,23,"bold")+txt(x+20,550,[family,"architecture → training → reference inference"],17)
        body+=line(230,610,450,642,dash=True)+line(670,610,450,642,dash=True)
        body+=txt(450,680,"EVOLUTOR: evidence, comparison and eventual orchestration",21,"bold","middle")
        body+=txt(450,723,"Lower branches are research tracks, not validated implementations or novelty claims.",18,anchor="middle")
        text="Promoter occupancy can inhibit initiation; accessible promoter can permit RNAP initiation.\nBiological regulation ⇢ conditional execution hypothesis; hard routing needs separate mathematics.\nDOGMA (non-Transformer) and Hermon DNA (Transformer) each require training and inference proof.\nBoth ⇢ Evolutor evidence and prospective orchestration; proposed, not validated engines."
    figure={"id":"DNA-MASTER" if dna else "EVO-MASTER","title":title,
            "teachingPurpose":text,"limit":"Original schematic; not to scale; research branches are proposed."}
    return envelope(figure,body,610 if dna else 755),text+"\n"

if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--check",action="store_true");a=p.parse_args()
    svg,text=master(ROOT.name=="dna-computing-book")
    for ext,data in [("svg",svg),("txt",text)]:
        path=ROOT/"research/figures"/("scientific-master."+ext)
        if a.check: assert path.read_text()==data
        else: path.parent.mkdir(parents=True,exist_ok=True);path.write_text(data)
