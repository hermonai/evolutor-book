"""Build the isolated Chapter 3 review PDF without changing accepted editions."""
import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
DNA = ROOT.name == "dna-computing-book"
NAME = "deep-dna-computing" if DNA else "deep-evolutor"
BOOK = "DNA Computing" if DNA else "Evolutor"

def command(args, **kwargs):
    result = subprocess.run(args, text=True, capture_output=True, **kwargs)
    if result.returncode:
        raise RuntimeError(result.stdout + result.stderr)
    return result

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--render",action="store_true",help="Render every page and four-page contact sheets")
    args=parser.parse_args()
    command([sys.executable, str(HERE/"build_assets.py"), "--check"])
    build=ROOT/"build/ch03-review"
    build.mkdir(parents=True,exist_ok=True)
    output=ROOT/"output/pdf"/(NAME+"-ch03-review.pdf")
    output.parent.mkdir(parents=True,exist_ok=True)
    for source in (HERE/"figures").glob("*.svg"):
        command(["rsvg-convert","-f","pdf","-o",str(build/(source.stem+".pdf")),str(source)])
    manuscript=(HERE/"manuscript.md").read_text()
    title, body=manuscript.split("\n",1)
    title=title.removeprefix("# Chapter 3. ")
    def figure(match):
        path=build/(Path(match["file"]).stem+".pdf")
        caption=command(["pandoc","-f","markdown+tex_math_single_backslash","-t","latex"],
                        input=match["caption"]).stdout.strip()
        return "\n\n"+r"\begin{figure}[H]"+"\n"+r"\centering"+"\n"+ \
            r"\includegraphics[width=\linewidth,height=.64\textheight,keepaspectratio]{"+path.as_posix()+"}\n"+ \
            r"\caption*{"+caption+"}\n"+r"\end{figure}"+"\n\n"
    body,count=re.subn(r"!\[[^\]]*\]\((?P<file>figures/[^)]+\.svg)\)\s*\n\s*(?P<caption>\*\*[^*]+\*\*.*?)(?=\n\n|\Z)",
                       figure,body,flags=re.S)
    if count != 12: raise ValueError(f"Expected 12 captioned figures, found {count}")
    body=body.replace("\n**","\n\n**")
    source=(HERE/"completion_diagnostics.py").read_text()
    selected={"coverage","work_depth"} if DNA else {"momentum_trace","branch_value","state_control"}
    code="\n\n".join(ast.get_source_segment(source,n) for n in ast.parse(source).body
                     if isinstance(n,ast.FunctionDef) and n.name in selected)
    code="import math\n\n"+code
    fence=chr(96)*3
    appendix="\n\n# Appendix A. Executable boundary diagnostics\n\n"
    appendix+="These functions are reproduced from completion_diagnostics.py and exercised by the repository tests. "
    appendix+="The full reference program, exhaustive checks and machine-readable results remain alongside the manuscript in drafts/ch03/. "
    appendix+="These are teaching calculations, not calibrated biological measurements or a trained model.\n\n"
    appendix+=fence+"python\n"+code+"\n"+fence+"\n"
    ledger=(HERE/"sources.md").read_text()
    ledger=re.sub(r"^(#+) ",r"#\1 ",ledger,flags=re.M)
    body+=appendix+"\n\n# Appendix B. Sources and evidence boundaries\n\n"+ledger
    body=re.sub(r"\[([^\]]+)\]\((?!https?://)([^)]+)\)", r"\1 (companion file: \2)", body)
    body=re.sub(r"^(#{1,2} .+)$",lambda m:"\n"+r"\FloatBarrier"+"\n\n"+m[0],body,flags=re.M)
    # Normalize typographic dashes only in prose; mathematical minus and original SVG are retained.
    body=body.replace("\u2011","-").replace("\u2013","-").replace("\u2014"," - ")
    (build/"review.md").write_text(body)
    header=r"""
\usepackage{float}
\usepackage{graphicx}
\usepackage{placeins}
\usepackage{caption}
\usepackage{fancyhdr}
\usepackage{fvextra}
\usepackage{xurl}
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\small BOOKNAME}
\fancyhead[R]{\small Chapter 3 | Review edition}
\fancyfoot[C]{\thepage}
\setlength{\headheight}{15pt}
\captionsetup{font=small,labelformat=empty}
\DefineVerbatimEnvironment{Highlighting}{Verbatim}{commandchars=\\\{\},breaklines,fontsize=\footnotesize}
\setlength{\emergencystretch}{3em}
\widowpenalty=10000
\clubpenalty=10000
\let\originaltableofcontents\tableofcontents
\renewcommand{\tableofcontents}{\originaltableofcontents\clearpage}
""".replace("BOOKNAME",BOOK)
    (build/"header.tex").write_text(header)
    env=dict(os.environ)
    env["PATH"]="/Library/TeX/texbin:"+env["PATH"]
    options=["pandoc",str(build/"review.md"),"--standalone",
        "-f","markdown+tex_math_single_backslash+raw_tex",
        "--pdf-engine=xelatex","--toc","--toc-depth=2",
        "-V","documentclass=article","-V","fontsize=11pt",
        "-V","geometry:margin=22mm","-V","papersize=a4",
        "-V","mainfont=Times New Roman","-V","sansfont=Arial",
        "-V","monofont=Menlo","-V","colorlinks=true",
        "-V","linkcolor=blue","-V","urlcolor=blue",
        "-M","title="+BOOK+" | Chapter 3",
        "-M","subtitle="+title,
        "-M","date=12 September 2026 | Scientific review candidate",
        "--include-in-header",str(build/"header.tex")]
    result=command(options+["-o",str(output)],env=env)
    (build/"build.log").write_text(result.stdout+result.stderr)
    if "Missing character:" in result.stderr: raise RuntimeError(result.stderr)
    info=command(["pdfinfo",str(output)]).stdout
    pages=int(re.search(r"Pages:\s+(\d+)",info)[1])
    record={"pdf":str(output.relative_to(ROOT)),"pages":pages,
            "sha256":hashlib.sha256(output.read_bytes()).hexdigest(),
            "edition":"standalone review candidate; not cumulative acceptance",
            "figures":count,"sources":{}}
    for path in sorted(HERE.rglob("*")):
        if path.is_file() and "__pycache__" not in path.parts and path.suffix in {".md",".py",".json",".svg",".txt"}:
            record["sources"][str(path.relative_to(ROOT))]=hashlib.sha256(path.read_bytes()).hexdigest()
    (build/"build-record.json").write_text(json.dumps(record,indent=2)+"\n")
    if args.render:
        from PIL import Image, ImageOps, ImageDraw
        out=ROOT/"tmp/pdfs/ch03-review"
        out.mkdir(parents=True,exist_ok=True)
        command(["pdftoppm","-r","110","-png",str(output),str(out/"page")])
        images=[out/f"page-{i:0{len(str(pages))}d}.png" for i in range(1,pages+1)]
        for start in range(0,pages,4):
            sheet=Image.new("RGB",(1280,1870),"#D7DFE5")
            draw=ImageDraw.Draw(sheet)
            for i,path in enumerate(images[start:start+4]):
                thumb=ImageOps.contain(Image.open(path).convert("RGB"),(620,890))
                x=10+(i%2)*640; y=30+(i//2)*935
                sheet.paste(thumb,(x,y))
                draw.text((x,y-20),f"PDF page {start+i+1}",fill="black")
            sheet.save(out/f"contact-{start//4+1}.png")
            ImageOps.grayscale(sheet).save(out/f"grayscale-{start//4+1}.png")
        record["rendered_pages"]=len(images)
    print(json.dumps({k:v for k,v in record.items() if k!="sources"},indent=2))

if __name__=="__main__":
    main()
