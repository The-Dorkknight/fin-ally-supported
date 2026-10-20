# Copyright Matthew Armstrong (https://github.com/The-Dorkknight). Code: PolyForm Noncommercial 1.0.0.
"""Write README.md: the whole paper, so the repo's front page on GitHub reads like the PDF.

python3 tools/make_readme.py        (run after editing paper/paper.md; standard library only)

GitHub cannot show a PDF inside a README, so the README is the paper itself, generated from
paper/paper.md with its links and figure paths adjusted, plus a contents list and a short
"about this repository" section at the end. Edit paper/paper.md, never README.md.
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "paper", "paper.md")
OUT = os.path.join(ROOT, "README.md")
PDF = "paper/fin-ally-supported-v1.0.pdf"


def slug(heading: str) -> str:
    """GitHub's anchor for a heading."""
    s = heading.strip().lower()
    s = re.sub(r"[^\w\- ]", "", s)
    return s.replace(" ", "-")


def main():
    md = open(SRC, encoding="utf-8").read()
    # paths: the paper lives in paper/, the README at the top
    md = md.replace("](figures/", "](paper/figures/")
    md = md.replace("](LICENSE.md)", "](paper/LICENSE.md)").replace("](../LICENSE-CODE.md)", "](LICENSE-CODE.md)")
    lines = md.split("\n")
    # the subtitle is a line under the title, not a section
    if lines[2].startswith("## "):
        lines[2] = "**" + lines[2][3:].strip() + "**"
    md = "\n".join(lines)

    sections = [h for h in re.findall(r"^## (.+)$", md, flags=re.M)]
    contents = " · ".join("[%s](#%s)" % (h.split(". ", 1)[-1] if h[0].isdigit() else h, slug(h)) for h in sections)
    nav = ("📄 **[PDF](%s)** · 🌐 [Web page](https://The-Dorkknight.github.io/fin-ally-supported/) · "
           "🔧 [The plugin](https://github.com/The-Dorkknight/cura-shark-support) · "
           "[About this repository](#about-this-repository)\n\n"
           "<sub>This page is the full paper (the same text and figures as the PDF).</sub>\n\n"
           "**Contents:** %s\n" % (PDF, contents))
    # put the navigation right after the byline block (before the "Read this first" box)
    i = md.index("\n> **Read this first.**")
    md = md[:i] + "\n" + nav + md[i:]

    about = """
---

## About this repository

| Path | What |
|---|---|
| [`paper/paper.md`](paper/paper.md) | The paper (this page is generated from it) |
| [`%s`](%s) | The paper as a PDF |
| [`paper/figures/`](paper/figures/) | All figures |
| [`code/shark_core.py`](code/shark_core.py) | The fin geometry (Python, numpy only), as used by the plugin 0.2.0 and 0.2.1-wip |
| [`data/`](data/) | The test boxes and their fins as STL |
| [`tools/`](tools/) | Redraw the figures (`make_figures.py`), plot G-code (`gcode_side_view.py`), build the PDF and web page (`build_paper.py`), write this page (`make_readme.py`) |
| [`docs/`](docs/) | The web version for GitHub Pages |

To rebuild everything: `python3 tools/make_figures.py` (numpy, matplotlib, Pillow), then
`python3 tools/build_paper.py` (pandoc, Chromium), then `python3 tools/make_readme.py`.

GitHub's **Cite this repository** button uses [`CITATION.cff`](CITATION.cff).

**Join in:** print the test plan (section 8), post results with photos as an issue or discussion, fork it, port it to
another slicer, or point out prior art I missed. Everyone who contributes gets credited in the next version.

**Licence:** paper text and figures [CC BY-SA 4.0](LICENSE.md); code in `code/` and `tools/`
[PolyForm Noncommercial 1.0.0](LICENSE-CODE.md) (source-available, not open source); the methods described are
dedicated to the public as a defensive publication. Not legal advice.
""" % (PDF, PDF)
    ref = md.find("\n[prusa-support]: ")          # keep link definitions at the very end
    if ref >= 0:
        md = md[:ref] + "\n" + about + md[ref:]
    else:
        md = md + about
    note = ("<!-- GENERATED from paper/paper.md by tools/make_readme.py. Edit the paper, then run the tool. -->\n")
    open(OUT, "w", encoding="utf-8").write(note + md.rstrip() + "\n")
    print("wrote", OUT, len(md.split("\n")), "lines,", len(sections), "sections")


if __name__ == "__main__":
    main()
