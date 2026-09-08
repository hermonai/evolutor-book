"""Render all deep pages and original SVG keyframes for documented visual review."""
import argparse
import json
from pathlib import Path
import subprocess
from PIL import Image, ImageOps, ImageDraw
ROOT=Path(__file__).resolve().parents[1]
name="deep-dna-computing" if ROOT.name=="dna-computing-book" else "deep-evolutor"
p=argparse.ArgumentParser()
p.add_argument("--preview",action="store_true")
p.add_argument("--chapter-one",action="store_true",help="Inspect the preserved Chapter 1 PDF")
args=p.parse_args()
if not args.chapter_one: name += "-ch01-02"
pdf=ROOT/("build" if args.preview else "output/pdf")/(name+".pdf")
out=ROOT/"tmp/pdfs"/name
out.mkdir(parents=True,exist_ok=True)
subprocess.run(["pdftoppm","-r","110","-png",str(pdf),str(out/"page")],check=True)
info=subprocess.check_output(["pdfinfo",str(pdf)],text=True)
count=int(next(l.split(":")[1] for l in info.splitlines() if l.startswith("Pages:")))
pages=[out/f"page-{i:0{len(str(count))}d}.png" for i in range(1,count+1)]
assert all(p.exists() for p in pages)
for start in range(0,len(pages),4):
    sheet=Image.new("RGB",(1280,1870),"#D7DFE5")
    draw=ImageDraw.Draw(sheet)
    for i,path in enumerate(pages[start:start+4]):
        thumb=ImageOps.contain(Image.open(path).convert("RGB"),(620,890))
        x=10+(i%2)*640;y=30+(i//2)*935
        sheet.paste(thumb,(x,y))
        draw.text((x,y-20),f"PDF page {start+i+1}",fill="black")
    sheet.save(out/f"contact-{start//4+1}.png")
    ImageOps.grayscale(sheet).save(out/f"grayscale-{start//4+1}.png")
frames=sorted((ROOT/"animation").glob("*/frame-*.svg")) if args.chapter_one else sorted((ROOT/"animation").glob("*-02/*.svg"))
for i,path in enumerate(frames):
    subprocess.run(["rsvg-convert","-o",str(out/f"frame-{i+1:02}.png"),str(path)],check=True)
if frames:
    sheet=Image.new("RGB",(1200,360*((len(frames)+1)//2)),"#D7DFE5")
    draw=ImageDraw.Draw(sheet)
    for i,path in enumerate(frames):
        thumb=ImageOps.contain(Image.open(out/f"frame-{i+1:02}.png").convert("RGB"),(580,320))
        x=10+(i%2)*600;y=25+(i//2)*360
        sheet.paste(thumb,(x,y));draw.text((x,y-18),path.name,fill="black")
    sheet.save(out/"frames-contact.png")
print(json.dumps({"pdf":str(pdf),"pages":count,"pageRenders":len(pages),"keyframes":len(frames),"directory":str(out)}))
