# Contributing

Thanks for helping out! Every contribution goes through a pull request (PR).

## How to open a PR

1. **Fork** the repository and create a branch, for example `deep-learning/summary-cnn`.
2. Add or edit files **inside the folder of one course** (`courses/<course>/`).
3. Open a PR and fill in the template.

By opening a PR you agree to release your contribution under the repository's
[CC BY-SA 4.0 license](LICENSE).

After the review, the maintainer merges the PR and adds you to the course's contributors in the index.
**Don't edit `study-plan.yaml`, the index in the README or the `curricula/` pages:
the maintainer updates them.**

## Where things go

| What | Where | File name |
|---|---|---|
| Course summary | `courses/<course>/summary.md` | already there, fill it in |
| Exercises and past exams | `courses/<course>/exercises/` | `topic.md` or `YYYY-MM-DD-exam.md` |
| Images and diagrams | `courses/<course>/assets/` | short descriptive name, e.g. `cnn-architecture.png` |
| Course info (lecturer, exam, syllabus) | `courses/<course>/README.md` | already there, fill in the _TBD_ fields |

For courses split into modules (e.g. Intelligent Systems), each module has its own summary:
`courses/intelligent-systems/automated-planning/summary.md`.

## How to write

- **Markdown**, in the course's `summary.md`. Things said in class that are not in the lecturer's material
  (an example on the blackboard, a clarification) go in the matching section of the summary.
- **English** for everything, so that all students can use the material.
- **Math in LaTeX**, which GitHub renders: `$O(n \log n)$` inline, `$$ ... $$` on its own line.
- **Diagrams**: Mermaid code blocks (GitHub renders them) or images in `assets/`.
- **Summaries** should be self-contained: someone who missed the lectures should be able to follow them.
- **Fixes to someone else's work are welcome.** Explain what you changed in the PR.

## Course status

Each course in the index has a status. The maintainer sets it, following these rules:

| Status | Meaning |
|---|---|
| ⬜ To do | Nothing yet, only the empty structure. |
| 🟡 Draft | Some material exists (a partial summary, some exercises), but it is not enough to prepare the exam. |
| ✅ Done | All of the conditions below are met. |

A course is **done** when:

1. `summary.md` covers **every topic of the official syllabus**. For courses split into modules, this applies to the summary of each module.
2. The course `README.md` is filled in: lecturer, exam format and syllabus.
3. The summary has been **reviewed by someone other than its author**, ideally someone who has already passed the exam.

"Done" is not final: if the syllabus changes or someone finds mistakes, the course goes back to draft until it is fixed.

## What not to upload

- Lecturers' slides, handouts or PDFs, and scans of textbooks. Link to the official page instead.
- Exam papers the lecturer has not made public. Rewrite the exercise in your own words.
- Personal data of anyone (emails, phone numbers, grades).

## Maintainer checklist

After merging a PR:

1. In `study-plan.yaml`, add the author to the course's `contributors` (`"@github-username"`)
   and update `status` (`todo`, `draft` or `done`) following the [course status](#course-status) rules.
2. Run `python3 scripts/build_index.py` (needs `pip install -r scripts/requirements.txt`).
3. Commit the updated `study-plan.yaml`, `README.md` and `curricula/`.

The PDFs don't need any action: on every push to `main`, the **PDF** workflow rebuilds the PDF of every course
whose status is not `todo` and publishes it in the [`pdf` release](https://github.com/salvo27/artificial-intelligence-and-computer-science/releases/tag/pdf).
To preview a PDF locally: `python3 scripts/build_pdfs.py <course-slug>` (needs pandoc 3.1.10 or later and Google Chrome);
the file is written to `build/pdf/`.

To add a free-choice course: add it to `study-plan.yaml` with `curricula: []`,
then run `python3 scripts/build_index.py --scaffold` to create its folder.
