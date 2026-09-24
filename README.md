# Artificial Intelligence and Computer Science: notes and summaries

Collaborative lecture notes and summaries for the Master's degree in
[Artificial Intelligence and Computer Science](https://corsi.unical.it/lm/artificial-intelligence-and-computer-science/)
(LM-18) at the University of Calabria.

The degree has two curricula, **Computer Security** and **Data Science**.
Courses shared by both curricula appear only once.

> [!NOTE]
> This is an unofficial, student-made project. The notes may contain mistakes:
> always check them against the official course material.

## Course index

Legend: 🟢 common to both curricula · 🔒 Computer Security only · 📊 Data Science only. See what each [status](CONTRIBUTING.md#course-status) means.

<!-- INDEX:START -->
**Progress:** ✅ 0 done · 🟡 0 draft · ⬜ 16 to do, out of 16 courses.

**Curricula:** [Computer Security](curricula/computer-security.md) · [Data Science](curricula/data-science.md)

### Year 1

#### Semester 1

| Course | ECTS | Curriculum | Status | Contributors |
|---|---|---|---|---|
| **[Deep Learning](courses/deep-learning/)** | 9 | 🟢 Common | ⬜ To do |  |
| **[Research and Development Methodologies](courses/research-and-development-methodologies/)**<br><sub>Agile Software Development · Research Seminars in AI&CS</sub> | 9 | 🟢 Common | ⬜ To do |  |
| **[Cryptography](courses/cryptography/)** | 6 | 🔒 COS | ⬜ To do |  |
| **[Secure Software Design](courses/secure-software-design/)** | 6 | 🔒 COS | ⬜ To do |  |
| **[Massively Parallel Programming on GPUs](courses/massively-parallel-programming-on-gpus/)** | 6 | 📊 DAS | ⬜ To do |  |
| **[Statistical Methods for Data Science](courses/statistical-methods-for-data-science/)** | 6 | 📊 DAS | ⬜ To do |  |

#### Semester 2

| Course | ECTS | Curriculum | Status | Contributors |
|---|---|---|---|---|
| **[Intelligent Systems](courses/intelligent-systems/)**<br><sub>Automated Planning · Intelligent Agents</sub> | 12 | 🟢 Common | ⬜ To do |  |
| **[Theoretical Computer Science](courses/theoretical-computer-science/)**<br><sub>Decidability and Logics · Computational Complexity</sub> | 12 | 🟢 Common | ⬜ To do |  |
| **[Network Security](courses/network-security/)** | 6 | 🔒 COS | ⬜ To do |  |
| **[Data Warehouse and Visualization](courses/data-warehouse-and-visualization/)** | 6 | 📊 DAS | ⬜ To do |  |

### Year 2

#### Semester 1

| Course | ECTS | Curriculum | Status | Contributors |
|---|---|---|---|---|
| **[Algorithmic Game Theory](courses/algorithmic-game-theory/)** | 6 | 🟢 Common | ⬜ To do |  |
| **[Neurosymbolic AI](courses/neurosymbolic-ai/)**<br><sub>Foundations of Neurosymbolic AI · LLM Lab</sub> | 6 | 🟢 Common | ⬜ To do |  |
| **[Cyber Offense and Defense](courses/cyber-offense-and-defense/)** | 6 | 🔒 COS | ⬜ To do |  |
| **[Big Data Analytics](courses/big-data-analytics/)** | 6 | 📊 DAS | ⬜ To do |  |
| **[Optimization for Machine Learning](courses/optimization-for-machine-learning/)** | 6 | 📊 DAS | ⬜ To do |  |

#### Semester 2

| Course | ECTS | Curriculum | Status | Contributors |
|---|---|---|---|---|
| **[Business Game](courses/business-game/)** | 6 | 🔒 COS | ⬜ To do |  |

### Free-choice courses

_None yet. Add the ones you attend to `study-plan.yaml` with `curricula: []`._

<!-- INDEX:END -->

## Repository structure

```
.
├── study-plan.yaml          # course list: ECTS, semester, curriculum, status, contributors
├── courses/
│   └── <course>/
│       ├── README.md        # course info: lecturer, exam format, syllabus, resources
│       ├── summary.md       # the polished summary, for exam prep
│       ├── notes/           # lecture notes, one file per lecture (01-intro.md, …)
│       ├── exercises/       # exercises and past exams
│       ├── assets/          # images and diagrams
│       └── <module>/        # courses split into modules: summary.md and notes/ per module
├── curricula/               # one page per curriculum (generated)
├── templates/               # templates for lecture notes and new courses
└── scripts/build_index.py   # regenerates the indexes from study-plan.yaml
```

## Contributing

Contributions are welcome through pull requests: new notes, summaries, exercises,
or fixes to existing material. Read the [contributing guide](CONTRIBUTING.md) first.
Everyone who contributes to a course is credited in the index above.

## License

The content of this repository is licensed under
[Creative Commons Attribution-ShareAlike 4.0](LICENSE) (CC BY-SA 4.0):
you can share and adapt it, as long as you credit the authors and release
your changes under the same license.
