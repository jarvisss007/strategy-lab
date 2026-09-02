#!/usr/bin/env python3
"""Rebuild honest_evaluation_survey.pdf from the markdown source.

    python3 make_pdf.py

Requires: python `markdown`, and LibreOffice (`soffice`) for HTML -> PDF.
Keeps the paper reproducible from source, like every other number in this repo.
"""
import markdown, subprocess, pathlib, sys

HERE = pathlib.Path(__file__).parent
SRC  = HERE / "honest_evaluation_survey.md"

CSS = """
@page { size: A4; margin: 22mm 20mm 22mm 20mm; }
body { font-family: 'Georgia','Times New Roman',serif; font-size: 10.5pt; line-height: 1.42; color:#111; }
h1.doctitle { font-size: 17pt; text-align:center; margin:0 0 6pt 0; line-height:1.25; }
h2 { font-size: 12pt; margin: 16pt 0 5pt 0; border-bottom:0.6pt solid #999; padding-bottom:2pt; }
h3 { font-size: 10.8pt; margin: 12pt 0 4pt 0; }
p { margin: 0 0 7pt 0; text-align: justify; }
table { border-collapse: collapse; width:100%; margin: 8pt 0 10pt 0; font-size: 8.8pt; }
th, td { border: 0.5pt solid #888; padding: 2.5pt 4pt; text-align:left; }
th { background:#eeeeee; font-weight:bold; }
ol, ul { margin: 0 0 7pt 0; padding-left: 16pt; }
li { margin-bottom: 3pt; text-align: justify; }
hr { border:none; border-top:0.6pt solid #bbb; margin:10pt 0; }
code { font-family:'Menlo',monospace; font-size:9pt; }
"""

def main():
    lines = SRC.read_text().split("\n")
    title, rest = lines[0].lstrip("# ").strip(), "\n".join(lines[1:])
    body = markdown.markdown(rest, extensions=["tables", "fenced_code", "footnotes", "attr_list"])
    html = (HERE / "honest_evaluation_survey.html")
    html.write_text(f'<html><head><meta charset="utf-8"><style>{CSS}</style></head>'
                    f'<body><h1 class="doctitle">{title}</h1>{body}</body></html>')
    for soffice in ("/opt/homebrew/bin/soffice", "soffice"):
        try:
            subprocess.run([soffice, "--headless", "--convert-to", "pdf",
                            str(html), "--outdir", str(HERE)], check=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            break
        except (FileNotFoundError, subprocess.CalledProcessError):
            continue
    else:
        sys.exit("soffice not found - install LibreOffice to build the PDF")
    print("built", HERE / "honest_evaluation_survey.pdf")

if __name__ == "__main__":
    main()
