#!/usr/bin/env python3
"""Build the GitHub Pages site with the interactive quizzes into build/site/.

    python3 scripts/build_site.py

Every course or module with "quiz: true" in study-plan.yaml must have a quiz/ folder
(index.html and its files): it is copied as is, keeping its path, and listed in the home page.
"""
import html
import shutil
import sys

from build_index import ROOT, load_plan, quizzes

OUT = ROOT / "build" / "site"


def main():
    plan = load_plan()
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    (OUT / ".nojekyll").touch()

    items = []
    for c in plan["courses"]:
        for label, path in quizzes(c):
            src = ROOT / path
            if not (src / "index.html").exists():
                sys.exit("{}: 'quiz: true' but {}index.html does not exist".format(c["slug"], path))
            shutil.copytree(src, OUT / path)
            title = c["name"] if label == "Quiz" else label[len("Quiz ("):-1]
            items.append('<li><a href="{}">{}</a></li>'.format(path, html.escape(title)))

    repo = "https://github.com/{}".format(plan["repository"])
    (OUT / "index.html").write_text("""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{name} quizzes</title>
<style>
:root {{ --bg: #f5f7fa; --fg: #17202b; --muted: #5d6877; --accent: #2f5bd3; }}
@media (prefers-color-scheme: dark) {{ :root {{ --bg: #0f1318; --fg: #e7ebf1; --muted: #9ba6b5; --accent: #86a6ff; }} }}
body {{ margin: 0; background: var(--bg); color: var(--fg); font: 17px/1.5 system-ui, sans-serif; }}
main {{ max-width: 700px; margin: 0 auto; padding: 40px 16px; }}
a {{ color: var(--accent); }}
p {{ color: var(--muted); }}
li {{ margin: 8px 0; font-weight: 600; }}
</style>
</head>
<body>
<main>
<h1>Interactive quizzes</h1>
<p>Exam simulators of the <a href="{repo}">{name}</a> notes. Summaries and PDFs are in the repository.</p>
<ul>
{items}
</ul>
</main>
</body>
</html>
""".format(name=html.escape(plan["degree"]["name"]), repo=repo, items="\n".join(items) or "<li>No quiz yet.</li>"),
        encoding="utf-8")
    print("{} quiz(zes) -> {}".format(len(items), OUT.relative_to(ROOT)))


if __name__ == "__main__":
    main()
