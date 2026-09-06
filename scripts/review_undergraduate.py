"""Render every undergraduate PDF page and build numbered contact sheets for human/agent review."""
from pathlib import Path
import subprocess
from PIL import Image, ImageOps, ImageDraw
ROOT=Path(__file__).resolve().parents[1]
name="undergraduate-dna-computing" if ROOT.name=="dna-computing-book" else "undergraduate-evolutor"
out=ROOT/"tmp/pdfs"/name
out.mkdir(parents=True,exist_ok=True)
subprocess.run(["pdftoppm","-r","110","-png",str(ROOT/"output/pdf"/(name+".pdf")),str(out/"page")],check=True)
pages=sorted(out.glob("page-*.png"))
for start in range(0,len(pages),4):
    sheet=Image.new("RGB",(1280,1870),"#D7DFE5")
    draw=ImageDraw.Draw(sheet)
    for i,p in enumerate(pages[start:start+4]):
        thumb=ImageOps.contain(Image.open(p).convert("RGB"),(620,890))
        x=10+(i%2)*640
        y=30+(i//2)*935
        sheet.paste(thumb,(x,y))
        draw.text((x,y-20),f"PDF page {start+i+1}",fill="black")
    sheet.save(out/f"contact-{start//4+1}.png")
    ImageOps.grayscale(sheet).save(out/f"contact-gray-{start//4+1}.png")
print(f"Rendered {len(pages)} pages: {out}")
