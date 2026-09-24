#!/usr/bin/env python3
"""Generate one PDF per course (summary + exercises) into build/pdf/.

    python3 scripts/build_pdfs.py                 # every course whose status is not "todo"
    python3 scripts/build_pdfs.py cryptography    # only the given courses

Requires pandoc (3.1.10 or later, for GitHub alerts) and Google Chrome or Chromium.
Set CHROME to the browser executable if it is not found automatically.
"""
import argparse
import datetime
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from build_index import ROOT, load_plan

PDF_DIR = ROOT / "scripts" / "pdf"
OUT_DIR = ROOT / "build" / "pdf"

CHROME_CANDIDATES = [
    "google-chrome",
    "google-chrome-stable",
    "chromium",
    "chromium-browser",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
]


def find_chrome():
    for candidate in [os.environ.get("CHROME")] + CHROME_CANDIDATES:
        if candidate and (shutil.which(candidate) or os.path.exists(candidate)):
            return shutil.which(candidate) or candidate
    sys.exit("Chrome or Chromium not found: set the CHROME environment variable.")


def course_inputs(course):
    """Markdown files of a course, in reading order: summaries first, then exercises."""
    base = ROOT / "courses" / course["slug"]
    if course["modules"]:
        units = [base / m["slug"] for m in course["modules"]]
    else:
        units = [base]
    files = [u / "summary.md" for u in units]
    files += sorted((base / "exercises").glob("*.md"))
    return [f for f in files if f.exists()], [base] + units + [base / "exercises"]


def build(course, plan, chrome, tmp):
    files, resource_dirs = course_inputs(course)
    html = tmp / "{}.html".format(course["slug"])
    pdf = OUT_DIR / "{}.pdf".format(course["slug"])

    header = tmp / "{}-header.html".format(course["slug"])
    header.write_text(
        '<p class="generated">Generated on {} from '
        '<a href="https://github.com/{repo}">github.com/{repo}</a>. '
        "Unofficial, student-made notes: check them against the official material.</p>\n".format(
            datetime.date.today().isoformat(), repo=plan["repository"]),
        encoding="utf-8")

    subprocess.run(
        ["pandoc", "--from", "gfm", "--to", "html5", "--standalone", "--embed-resources", "--math-method=mathml",
         "--css", str(PDF_DIR / "style.css"),
         "--lua-filter", str(PDF_DIR / "details-open.lua"),
         "--resource-path", os.pathsep.join(str(d) for d in resource_dirs),
         "--metadata", "pagetitle={}".format(course["name"]),
         "--include-before-body", str(header),
         "--output", str(html)] + [str(f) for f in files],
        check=True)

    subprocess.run(
        [chrome, "--headless", "--disable-gpu", "--no-sandbox", "--no-pdf-header-footer",
         "--print-to-pdf={}".format(pdf), html.as_uri()],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if not pdf.exists():
        sys.exit("{}: Chrome did not produce the PDF".format(course["slug"]))
    print("{} -> {}".format(course["slug"], pdf.relative_to(ROOT)))


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("courses", nargs="*", help="slugs of the courses to build (default: all but 'todo')")
    args = parser.parse_args()

    plan = load_plan()
    by_slug = {c["slug"]: c for c in plan["courses"]}
    unknown = [s for s in args.courses if s not in by_slug]
    if unknown:
        sys.exit("unknown course: " + ", ".join(unknown))
    selected = [by_slug[s] for s in args.courses] or [c for c in plan["courses"] if c["status"] != "todo"]

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    chrome = find_chrome()
    with tempfile.TemporaryDirectory() as tmp:
        for course in selected:
            build(course, plan, chrome, Path(tmp))


if __name__ == "__main__":
    main()
