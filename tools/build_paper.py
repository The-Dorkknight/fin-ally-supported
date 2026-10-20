# Copyright Matthew Armstrong (https://github.com/The-Dorkknight). Code: PolyForm Noncommercial 1.0.0.
"""Build paper/paper.html, docs/index.html (GitHub Pages) and the PDF from paper/paper.md.

python3 tools/build_paper.py
Needs pandoc and a Chromium or Chrome (set CHROME=/path/to/chrome if it is not found).
"""
import os
import re
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, "paper")
PDF = os.path.join(P, "fin-ally-supported-v1.0.pdf")
REPO = "https://github.com/The-Dorkknight/fin-ally-supported/blob/main/"
DESC = ("Shark-fin supports for long, flat, tilted overhangs in FDM printing: a hobbyist's field guide and a "
        "defensive publication. Matthew Armstrong, 19 October 2026.")


def pandoc(src_md, out_html, title):
    subprocess.run(["pandoc", src_md, "-f", "markdown-implicit_figures", "-s", "--css", "paper.css",
                    "--embed-resources", "--metadata", "lang=en-GB", "--metadata", "pagetitle=" + title,
                    "-o", out_html], cwd=P, check=True)
    t = open(out_html, encoding="utf-8").read()
    t = t.replace("<head>", '<head>\n<meta name="description" content="%s">' % DESC, 1)
    open(out_html, "w", encoding="utf-8").write(t)


def main():
    html = os.path.join(P, "paper.html")
    pandoc("paper.md", html, "Fin-ally Supported")
    # the Pages copy: relative links to repo files point at GitHub instead
    md = open(os.path.join(P, "paper.md"), encoding="utf-8").read()
    md = md.replace("](LICENSE.md)", "](" + REPO + "paper/LICENSE.md)").replace("](../LICENSE-CODE.md)", "](" + REPO + "LICENSE-CODE.md)")
    tmp = os.path.join(P, ".pages.md")
    open(tmp, "w", encoding="utf-8").write(md)
    os.makedirs(os.path.join(ROOT, "docs"), exist_ok=True)
    pandoc(".pages.md", os.path.join(ROOT, "docs", "index.html"), "Fin-ally Supported")
    os.remove(tmp)
    open(os.path.join(ROOT, "docs", ".nojekyll"), "w").close()
    chrome = os.environ.get("CHROME") or next((c for c in ("chromium", "chromium-browser", "google-chrome",
                                                           "/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
                                               if shutil.which(c) or os.path.exists(c)), None)
    if not chrome:
        sys.exit("No Chromium found: paper.html is built; print it to PDF from a browser.")
    subprocess.run([chrome, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                    "--force-color-profile=srgb", "--blink-settings=preferredColorScheme=1",
                    "--print-to-pdf=" + PDF, "file://" + html], check=True, stderr=subprocess.DEVNULL)
    print("built", html, PDF)


if __name__ == "__main__":
    main()
