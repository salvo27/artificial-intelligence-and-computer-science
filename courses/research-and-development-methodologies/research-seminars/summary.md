# Research Seminars in AI&CS: summary

Module of [Research and Development Methodologies](../README.md). Based on the slides by Francesco Ricca and his assistants
(Manuel Alejandro Borroto Santana, Yissel Rodríguez Aldana), and on the two readings shared with them:
*How to write a paper* by Oded Goldreich and *How to write an introduction: some suggestions* by Sandro Etalle.
The sections follow the order of the lectures.

Explanations and examples that are not in the material are marked **Not in the slides**.

**Progress:** all the material shared so far is covered; nothing said in class is included yet.

## Contents

1. [What is research](#1-what-is-research)
2. [Research dissemination: venues, paper types, publication](#2-research-dissemination-venues-paper-types-publication)
3. [Evaluating research](#3-evaluating-research)
4. [Research ethics](#4-research-ethics)
5. [Research grants](#5-research-grants)
6. [How to write a paper](#6-how-to-write-a-paper)
7. [How to write an introduction](#7-how-to-write-an-introduction)
8. [Related works and tools for bibliography](#8-related-works-and-tools-for-bibliography)
9. [LaTeX](#9-latex)
10. [How to structure a presentation](#10-how-to-structure-a-presentation)
11. [Cheat sheet](#cheat-sheet)

---

## 1. What is research

In the broadest sense, **we do research whenever we gather information to answer a question that solves a problem**: we all do some "research" every day.

**Scientific research** is a systematic and methodical process of inquiry that aims to discover, interpret and expand our understanding of the natural and social world.
It pursues knowledge through a **structured approach**, using **empirical evidence** and **logical reasoning**. Its main goals are to answer questions, test hypotheses,
and contribute to the body of knowledge of a field. In the simplest terms: searching for knowledge and for truth.

**Why do research?** It serves intellectual curiosity, technological progress, problem solving and the betterment of human life.
Without trustworthy published research we would all be locked in the opinions of the moment, prisoners of what we alone experience, or dupes of whatever we are told:
mistaken, even dangerous ideas flourish when people accept too many opinions based on too little evidence.

### Who cares about that? From a question to a problem

Researchers are often mocked for studying esoteric topics that matter to no one but themselves. To avoid it, **turn your question into an (interesting) problem**:

- a problem is something we look for **because we have to**;
- ask: *what will be lost if you don't answer your question?* This is the **"So what?"** question.

There are two kinds of problems:

- a **practical problem** is a situation with a **tangible cost** for you or your readers;
- a **conceptual problem** is some version of **not knowing or not understanding** something.

> [!TIP]
> **Not in the slides: an example.** "How do users react to a slow app?" is a *question*. "Slow apps lose customers, and we don't know which delay users start to abandon at,
> so companies can't decide how much to invest in speed" is a *problem*: it says what is lost if nobody answers. The first part is a practical cost, the second a conceptual gap.

### Pure or applied research?

- **Pure research** addresses a conceptual problem that does not bear directly on any practical situation; it improves the understanding of a community of researchers.
- **Applied research** addresses a conceptual problem that **does have practical consequences**.

### Why write it up? Why a formal paper?

- **Write to remember:** without notes, you are likely to forget or, worse, misremember.
- **Write to understand:** arranging and rearranging your results reveals new implications, connections and complications.
- **Write to test your thinking:** writing is thinking with and for your readers. It disentangles your ideas from your memories and wishes, and lets you and others explore,
  expand, combine and understand them.

Why follow the **standard forms** of a formal paper, instead of your own style? Because **you write for others**. Whatever community you join, you are expected to show that you
understand its practices; and writing the way readers expect makes you anticipate their critical questions, so you understand your own work better
(the slides quote *The Craft of Research* on this).

---

## 2. Research dissemination: venues, paper types, publication

### Research venues

**Venues** are the conferences, journals and other platforms where researchers present and publish their work. They spread new knowledge, foster collaboration,
and shape the direction of the field. The main categories:

| Venue | Character |
|---|---|
| **Workshops** | mostly informal, to discuss preliminary results |
| **Conferences** | mostly formal, recent results |
| **Journals** | formal archival of results |
| **Books** | stable knowledge, various goals |
| **Online archives** | a first view of the work, cheap platforms for publishing |

> [!NOTE]
> **Not in the slides: computer science is special.** In most sciences the journal is the most prestigious venue. In computer science, top **conferences**
> are often as prestigious as journals, because the field moves fast and conference reviews are quicker. A typical path: a preliminary idea at a workshop,
> the full result at a conference, an extended version in a journal. A well-known online archive is arXiv, where many papers appear before (or without) peer review.

### Paper types

| Type | What it does |
|---|---|
| **Theoretical** | develops new theories, models or frameworks; may propose algorithms, data structures, computational models; often has mathematical proofs or formal analysis |
| **Empirical** | presents experimental or observational studies to validate or evaluate existing theories, or to gain insight into practical aspects; experiments, simulations, case studies |
| **Survey** | a comprehensive review of existing research in an area: summarizes the state of the art, highlights trends, identifies research gaps |
| **Application / system** | applies existing theories or technologies to real-world problems; designs, implements and evaluates new systems, tools or software |
| **Position** | expresses the authors' viewpoint on an issue, argues for a stance, may propose new research directions |
| **Extended abstract** | a concise summary of a paper, typically for conferences or workshops, with a brief overview plus some details on methodology, results and conclusions |

### Structuring a paper (basic pattern)

Introduction, background (preliminaries), **one section per main issue**, related work, conclusion, references, appendices.
Beyond content, a paper is shaped by **constraints**: the **call for papers**, the **author instructions** (page limits, template), accompanying material, external repositories
(for code and data).

### The publication process

1. Answer your research question.
2. Write a paper describing your findings.
3. Select a venue.
4. Focus the paper on the venue's requirements.
5. Submit it.
6. The paper goes through one or more rounds of review.
7. The paper is accepted or rejected.

**Peer review** is used to maintain quality standards, improve the work and give it credibility. Scholarly peer review determines whether a paper is suitable for publication.

---

## 3. Evaluating research

Can research be evaluated? A formal definition of evaluation (*International Encyclopedia of Education*, 2010): a form of disciplined and systematic inquiry,
carried out to assess an object, program, practice, activity or system, in order to provide information useful for decision making.
**Evaluating scientific research maintains the quality and integrity of scientific knowledge.**

- **Quantitative methods** ask questions with tangible answers, relying on numerical data and statistical analysis.
- **Qualitative methods** explore opinions, attitudes and behaviors.

Both can be used, and a **combination** is often best.

> [!TIP]
> **Not in the slides: the two kinds of evaluation on one project.** For a new tool that helps students find papers: a *quantitative* evaluation measures, on 50 students, the average time to find 5 relevant papers with and without the tool
> (numbers, statistics); a *qualitative* evaluation interviews 8 of them about what was confusing or useful (opinions, attitudes). The numbers say *whether* the tool helps, the interviews explain *why*.

### Bibliometrics

A field that studies publications **quantitatively**: a systematic, statistical approach to evaluate publications, authors, journals and research areas.
Its goal is to measure patterns of publication, citation and collaboration, and to assess the impact and influence of scholarly work.

**Main databases:** Google Scholar, Web of Science, Scopus, DBLP, PubMed, IEEE Xplore, ScienceDirect.

**Some (in)famous metrics and rankings:**

- **Number of citations**, distinguishing **self-citations** from citations by others.
- **h-index:** an author has index $h$ if they have published $h$ papers, each cited at least $h$ times.
- **g-index:** an author has index $g$ if their $g$ most cited papers together received at least $g^2$ citations.
- **Impact factor:** the relative importance of a **journal** in its field, based on the average number of citations received by its articles over a period.
- **Scimago Journal Rank (SJR):** a weighted average of the citations received.
- **CORE Conference Ranking:** assessments of the major computing conferences.

> [!NOTE]
> **Not in the slides: computing h and g.** An author has 5 papers with 10, 8, 5, 4, 3 citations (sorted).
> *h-index:* 4 papers have at least 4 citations each, but there are not 5 papers with at least 5, so $h = 4$.
> *g-index:* the cumulative sums are 10, 18, 23, 27, 30; the top 5 papers have $30 \ge 5^2 = 25$ citations, so $g = 5$.
> The g-index rewards a few highly cited papers more than the h-index does.
>
> Two common pitfalls: the h-index grows with career length (a young researcher has a low one regardless of quality), and citation habits differ a lot between fields,
> so numbers from different fields cannot be compared directly.

The slides close this part with a warning: **"Contraposition is the sound way of inverting implication. Famous is not necessarily high quality."**

> [!TIP]
> **Not in the slides: what the warning means.** Suppose "high-quality work gets cited". The sound way to invert it is the contrapositive:
> "work that is never cited is probably not high quality". Inverting it the wrong way ("cited, so high quality") is the converse, a logical fallacy:
> a paper can be very cited because it is controversial, wrong and often refuted, or just trendy. Metrics are evidence, not proof of quality.

---

## 4. Research ethics

Research ethics is a set of principles and guidelines governing research involving **human participants, animals**, and the general **handling of data**.

**"Thou shalt nots" for ethical researchers** (*The Craft of Research*):

- they do not **plagiarize** or claim credit for others' results;
- they do not misreport sources, **invent data** or fake results;
- they do not submit data whose accuracy they don't trust, unless they say so;
- they do not conceal objections they cannot rebut;
- they do not caricature or distort opposing views;
- they do not destroy data or conceal sources that are important for those who follow.

In short: when you respect sources, preserve and acknowledge the data that go **against** your results, assert claims only as strongly as warranted,
and acknowledge the limits of your certainty, you join a community searching for a common good, and you build a bond with your readers.
Research focused on the best interests of others turns out to be in your own interest too.

---

## 5. Research grants

Research has costs: who pays for it? **Grant calls** (or funding opportunities) are announcements by funding agencies, institutions or organizations
that invite researchers to submit **proposals** for specific projects.

**Submission process:** researchers submit detailed proposals with **objectives, methodology, budget and expected outcomes**.
Projects are evaluated on the **significance** of the research, its **feasibility**, and the **qualifications of the team**.

| Type | Offered by | Examples from the slides |
|---|---|---|
| Government grants | government agencies, for national priorities | NIH, NSF |
| Foundation grants | private foundations | Bill & Melinda Gates Foundation, Wellcome Trust, Ford Foundation |
| Industry grants | companies or industry associations, for research aligned with their interests | common in technology, pharmaceuticals, energy |
| International grants | international organizations, for collaboration and global challenges | European Union, United Nations |
| Academic grants | universities and research institutions, for their own staff | |
| Early career researcher grants | for researchers who recently finished their PhD | |
| Postdoctoral fellowships | for researchers pursuing further research after the PhD | universities, research institutions, agencies |
| Innovation grants | for innovation, technology transfer, new products and processes | |

> [!TIP]
> **Not in the slides: European examples.** In Europe, the main programme is **Horizon Europe**; the **European Research Council (ERC)** funds individual researchers
> (Starting, Consolidator and Advanced grants, by career stage), and the **Marie Skłodowska-Curie Actions** fund postdoctoral fellowships.
> In Italy, the ministry funds national projects such as **PRIN**.

---

## 6. How to write a paper

This part follows Oded Goldreich's essay *How to write a paper* (2004), summarized in the slides and in the note "Basic tips".

### The purpose

Every human activity has a purpose, and understanding it is necessary to do the activity well.
**The purpose of a paper is to communicate an idea, or a set of ideas, to people who can carry it further or make other good use of it.**
(The cynical answer "to advance my career" does not work: what advances a career is serving the scientific process.)
Badly written papers come from a poor understanding of this role, or from failing to put it into practice.

### Three actions before writing

1. **Identify the idea.** Ask what idea the paper is meant to communicate. It can be:
   - a new way of **looking at** objects (a **model**);
   - a new way of **manipulating** objects (a **technique**);
   - **new facts** about objects (**results**).

   If no idea can be identified, reconsider whether to write the paper at all.
2. **Identify your community.** Not only the experts in the area, but also current and future students and researchers without direct access to the experts.
   Write for them: the reader is **intelligent and has basic background in the field, but not more**. A good model is a good student at the start of graduate studies.
3. **Understand the needs of your readers.** They are drowning in information. **Spend much time writing, so that readers can spend much less time reading.**
   This is simple economics: the writer understands the work better, so clarifying costs them less energy, and one writer serves many readers.

### Serving the reader

**Focus on the readers' needs, not on the writer's desires.** Avoid these symptoms:

| Pitfall | What it is |
|---|---|
| **Checklist phenomenon** | putting in everything you know, each insight in the first possible place rather than the most suitable one |
| **Obscure generality** | presenting ideas in the most general form instead of the most natural one; better to show a meaningful special case first |
| **Idiosyncrasies** | terms, phrases and notations that only have personal appeal |
| **Lack of hierarchy** | not distinguishing the important ideas from the secondary ones |
| **Talmudism** | exploring every subtlety, refinement and possible criticism before the basic idea is clear |

**Be aware of what the reader knows.**

- A reader cannot grasp a new concept and all its implications immediately.
- In proofs, **elaborate on the new conceptual steps, not on the standard technical derivations**. Beginners do the opposite: they feel insecure about standard techniques
  and explain them at length, while hiding their own innovative steps. Both are wrong.
- Avoid treating the general case with all its complications in one shot: present a special case first.
- Don't hide a fundamental difficulty behind a definition that ignores it, without first discussing it.
- Minimize the number of new concepts and definitions: the reader's capacity to absorb them is limited.

**Make reading a non-painful experience.** Avoid:

- **a labyrinth of implicit pointers:** "A is interested in doing X. It has property Y but not Z. This property allows it to do this." What is "it", "this"? Name things explicitly;
- **sentences with complex logical structure**, like "if X and Y or Z then P or Q";
- **mixtures of math and text:** "on input $x$ $y$, $A$ runs $B^y$ on $f(x)$" is better as "on input $x$ and $y$, algorithm $A$ runs the oracle machine $B$ on input $f(x)$, with $y$ on $B$'s oracle tape";
- **cumbersome notations and terms**, like an $(a, b, c, d, e, f, g, h, i, j)$-system.

When these suggestions conflict, **use judgment**: there is no canonical structure, fit the structure to the content.

### The parts of the paper

- **Title:** informative, not too long or cumbersome; it should fit into a sequence of past and future works (different from earlier titles, leaving room for later ones).
- **Authors:** in computer science (and in theory especially), usually in **alphabetical order**, but different communities have different habits.
- **Abstract:** short (typically **no more than 200 words**) and informative. Many people read only the title, some only the abstract, more only the introduction:
  serve them all. The abstract should be **self-contained as a high-level description**: it cannot give rigorous definitions and does not need to motivate the model,
  recall prior work, state the results precisely, or list all of them; it must not refer to other parts of the paper (such as the references).
- **Introduction:** a clear description of the contents (main results and a high-level view of the techniques), the new ideas and conceptual observations,
  a clear **motivation**, and the paper's place with respect to **prior work**, stating fairly where it improves and where it is worse. More in the next section.
- **Technical part:**
  - **discuss definitional choices**, saying whether each is **arbitrary** (any reasonable choice gives the same effect), made **for simplicity** (a more natural choice
    would only complicate the discussion) or **essential** (the results are not known to hold with an equally natural alternative);
  - use a **single numbering system** for all technical items (Definition 5.1, Theorem 5.2, …), so that items can be found by binary search;
  - use informative citations (e.g. include the theorem number).
- **Conclusions are not a must.** A conclusion section that repeats the abstract or introduction is useless. It is justified (Goldreich estimates in less than 5% of papers) only for
  material that is better understood **after** the technical part.
- **References and acknowledgments:** governed by **truth** (never mislead the reader with unjustified credits) and, within truth, **kindness**.

> [!TIP]
> **Not in the slides: two examples for the parts above.**
>
> *An abstract of about 80 words, high level and self-contained:* "Students often cannot tell whether answers from university chatbots are correct. We present a chatbot that checks every answer against a formal encoding of the
> regulations and shows the rule it relies on. On 300 real questions, it answers 91% correctly, against 64% of a retrieval-based baseline, and never contradicts the regulations. We also release the encoding of the regulations of
> our department." No definitions, no citations, no reference to sections: just the problem, the idea, the main result.
>
> *Definitional choices:* a paper defines a "short path" as one with at most 10 edges. If 10 could be any reasonable number with the same results, the choice is **arbitrary** (say so, to reassure the reader).
> If the results also hold for weighted paths, but weights would only complicate the proofs, the choice is **for simplicity**. If the theorems are known to hold only with an unweighted graph, the choice is **essential**, and honesty requires saying it.

### Benefiting from readers' comments

Friends and close colleagues rarely point out major problems, and they know the work too well to be typical readers.
Reviewers are critical readers: you don't have to follow their suggestions, but **any reviewer comment indicates a problem in the write-up**,
even when the proposed fix is not the right one. "Reviewers are typically not idiots, and one can learn even from idiots!"

---

## 7. How to write an introduction

Based on Sandro Etalle's short note. The introduction is the **most read** section and largely determines the reviewer's attitude toward the work.
The recipe (which Etalle learned from Krzysztof Apt) has **three main parts**:

1. **Background.** Make clear what the context is and give an idea of the state of the art, but **keep it short**: less than a page, half a page for a normal 15-page article.
2. **The problem.** If there were no problem, there would be no reason to write, or to read. Tell the reviewer why they should keep reading.
   A few lines are often enough: "So far no one has investigated the link…", "The above solutions don't apply to the case…".
3. **The proposed solution.** Now, **and only now**, outline the contribution. Point out the **novel aspects** clearly: the reviewer cannot know all related articles,
   so make the **difference from other methods** explicit. Avoid going into too much detail.

**Optional parts:**

4. **Related work:** better **postponed to the end** of the paper, when the reader already understands the contribution ("Related works are discussed in Section …").
   An exception is a very prominent related work, whose difference from yours should be clear immediately.
5. **An anticipation of the conclusions:** hard to do well; only for papers with a strong position statement. Keep it short, refer to the concluding section, keep it separate.
6. **The outline** (plan of the paper): useful only for long papers.

**Two extra tips:** keep the parts **well separated** (an itemized list helps), and **keep it short**, unless you know you can write well.

> [!TIP]
> **Not in the slides: a skeleton following the recipe.**
> *Background:* "Chatbots are increasingly used to answer questions about university regulations."
> *Problem:* "However, existing chatbots often give answers that contradict the regulations, and students cannot tell when this happens."
> *Solution:* "We propose a chatbot that checks each answer against a formal encoding of the regulations and shows the rule it is based on.
> Unlike previous approaches, which only retrieve similar text, ours guarantees consistency with the rules. Related works are discussed in Section 6."

---

## 8. Related works and tools for bibliography

### Why related works and references

**Related works** help to:

- **avoid duplication:** not repeating what has already been done;
- **identify gaps** in knowledge that need investigation;
- **build on previous research**, using it as a foundation;
- **support methodologies**, justifying the chosen methods;
- **compare results** with other works.

**Referencing** scientific work gives credit for the ideas you used, supports your claims with research, lets readers check the sources, and shows that you know what has already been studied.

### Bibliographic databases

**Bibliographic databases** are organized digital collections of references to published sources (journal articles, conference proceedings), tagged with titles, authors,
affiliations, abstracts and identifiers. They can be multidisciplinary or subject-specific, and they give each document a **stable identifier**.

| Database | Coverage | Discipline | Access | Provider |
|---|---|---|---|---|
| **Scopus** | > 102.6 million items | multidisciplinary | limited free preview, full access by institutional subscription | Elsevier |
| **Web of Science** | > 240 million items | multidisciplinary | institutional subscription only | Clarivate |
| **IEEE Xplore** | > 6 million items | engineering, CS, electronics | institutional subscription and free | IEEE |
| **ScienceDirect** | > 23 million items | multidisciplinary | institutional subscription and free | Elsevier |
| **DOAJ** | > 11 million items | multidisciplinary, open access journals | free | DOAJ |

### Academic search engines

Unlike Scopus or Web of Science, where an editorial team manages the list of sources, **academic search engines** add to their index **anything that looks academic**
(articles, reports, theses, working papers, chapters), chosen by their algorithm. They cover more, with less control.

| Engine | Coverage | Notes |
|---|---|---|
| **Google Scholar** | > 389 million records | the most used; only a snippet of the abstract; related articles, references, cited by, full-text links; exports APA, MLA, Chicago, Harvard, Vancouver, RIS, BibTeX |
| **BASE** (Bielefeld) | > 463 million records | quality over quantity, sources checked by staff; abstracts and full-text links; exports RIS, BibTeX |
| **Semantic Scholar** | > 230 million records | uses AI (NLP, machine learning) to find hidden connections between topics |
| **CORE** | 431 million records | open-access papers, with a link to the full text for every result |
| **dblp** | > 8 million records | computer science journals and proceedings, high-quality metadata; exports BibTeX, RIS, XML, RDF |
| **ResearchGate** | > 160 million publication pages | an academic social network ("a mix of Facebook, LinkedIn and Twitter") |

Others: ERIC, RefSeek, Wolfram Alpha, DataONE Search, LazyScholar.

### Search strategy

**Keywords** are the concepts your research question is about (single words or key phrases). Select words that describe what you are looking for, and add **synonyms**.

*Example from the slides:* an assignment asks to argue for or against letting children play video games, as parents and educators worry about their negative effects.
The keywords are **children**, **video games**, **effects of video games**, which combine into topics such as "video games and children" or "effects of video games in children".

**The 5 W's and the H** generate more keywords or narrow the topic: *What* is the topic? *Who* is concerned (parents, educators)? *When* (now, in the past)?
*Where* (the EU, a country, a city)? *Why* (they fear negative effects)? *How* (psychological or social effects)? The answers suggest new searches:
"video games in the EU", "negative effects of video games", "pros and cons of video games".

**Boolean operators:**

| Operator | Effect | Example |
|---|---|---|
| **AND** (+) | narrows: all terms must appear | logistics AND supply chain |
| **OR** ( \| ) | broadens: either term may appear | logistics OR supply chain |
| **NOT** (−) | narrows: excludes the second term | "logistics innovation" NOT patenting |

**Other strategies:** **exact phrase** in quotation marks (curly brackets in some databases), e.g. "logistics innovation"; **truncation** with `*` for variations of endings,
e.g. `leader*` finds leaders and leadership; truncation at the start, e.g. `*hydrocarbon` finds polyhydrocarbon too.

> [!TIP]
> **Not in the slides: a combined query.** `("video games" OR videogames) AND child* AND effect* NOT advertising` finds papers about effects of video games on children
> (child, children, childhood), in either spelling, excluding those about advertising.

### Identifiers, formats and citation styles

A **DOI** (digital object identifier) uniquely identifies most journal articles, and also proceedings and book chapters; DataCite issues DOIs for datasets.
Example: `https://doi.org/10.1007/978-3-032-04587-4_19`, or its short form `https://doi.org/qc5n`.

**Standard formats for bibliographic data:**

- **BibTeX**, since the mid 1980s, designed for LaTeX (see [section 9](#9-latex));
- **RIS**, a tag format originally by Research Information Systems (now part of Thomson Reuters);
- **EndNote XML** and **Citeproc JSON**, newer and less widely supported, but easier to process automatically.

A **citation style** dictates how to format a citation, what information to include (authors, title, venue, year, issue, pages), in which order,
and how to refer to it in the text. Common styles are APA, MLA, Chicago, Vancouver, IEEE; **there is no single standard**, and with the different practices of each discipline there
probably never will be.

**In-text citations** come in three kinds:

- **parenthetical:** author and date in parentheses, e.g. (Goldreich, 2004), or author and page;
- **numerical:** a number in brackets or superscript, pointing to a numbered reference list, e.g. [3];
- **note:** a full citation in a footnote or endnote, marked by a superscript number.

**APA** (7th edition of the American Psychological Association manual) was designed for psychology and is widely used in the social sciences.
**IEEE** uses numbers in square brackets matching a numbered reference list, and is used in engineering and IT.

> [!NOTE]
> **Not in the slides: the same reference in the two styles.**
> *APA:* in the text "(Goldreich, 2004)"; in the list: Goldreich, O. (2004). *How to write a paper*. Weizmann Institute of Science.
> *IEEE:* in the text "[1]"; in the numbered list: [1] O. Goldreich, "How to write a paper," Weizmann Institute of Science, 2004.
> With BibTeX you don't write either by hand: the same `.bib` entry is formatted in any style by changing `\bibliographystyle`.

### Reference managers

A **reference manager** (or citation manager) is software to collect, organize and use bibliographic references. It supports three research steps: **searching, storing, writing**.
A good one should (Gilmour and Cobus-Kuo, 2011):

1. import citations from databases and websites;
2. gather metadata from PDF files;
3. organize citations;
4. allow annotations;
5. share the database, or parts of it, with colleagues;
6. exchange data with other managers through standard formats (RIS, BibTeX);
7. produce formatted citations in many styles;
8. work with word processors for in-text citations.

| Manager | Type | Advantages | Disadvantages |
|---|---|---|---|
| **EndNote** | commercial; desktop and web (EndNote Online is free); Windows, Mac, iOS | copes with very large libraries, many styles, journal abbreviations, plug-ins for Word, OpenOffice, Pages | cost, complex for new users, compatibility issues; sharing only in the web version |
| **Mendeley** | free; desktop and web; Windows, Mac, Linux | mobile apps, social networking, collaborative PDF annotation, paper catalogue, plug-ins for Word, Google Docs, OpenOffice | limited free storage (2 GB) |
| **Zotero** | open source; desktop, with sync and groups; Windows, Mac, Linux | mobile apps, tools to create references from websites, plug-ins, works with Word, OpenOffice, RStudio | limited free storage (300 MB) |
| **RefWorks** | commercial, web-based | many styles, access from any computer, plug-ins for Word and Google Docs, unlimited storage | very limited offline access, not compatible with Libre/OpenOffice |

---

## 9. LaTeX

**LaTeX** is a document preparation system for high-quality typesetting, used for medium to large technical and scientific documents.
A document is a plain text file (`.tex`) with **commands** describing the desired result; a TeX engine compiles it into a typeset PDF (or DVI, a device-independent binary layout format).
It is **not WYSIWYG** (What You See Is What You Get): you don't see the final document while writing, LaTeX designs it for you, and you guide it with commands.
If the result is not satisfactory, you change the settings and compile again.

- **Why use it:** complex mathematics, tables and technical content; footnotes, cross-references and bibliographies; indexes, glossaries, tables of contents and lists of figures
  produced automatically; highly customizable through thousands of free packages; a small change to the text does not destroy the formatting.
- **Disadvantages:** a fairly steep learning curve; tables can be hard; spell checking needs a separate tool (Overleaf helps); designing a new layout takes a lot of time;
  not suitable for complex animated presentations.

### Structure of a document

A LaTeX document has two parts:

- the **preamble**: the document class, font and size, margins, spacing, and the packages to use;
- the **body**: the text and the commands that format it.

**Document classes:** `article` (journal articles, short reports), `report` (longer reports with chapters, theses), `book`, `letter`, `beamer` (presentations).

**Packages** add functionality: `\usepackage[options]{name}`. Common ones: `amsmath` (advanced math), `amssymb` (extra symbols), `graphicx` (images),
`hyperref` (clickable links, PDF metadata), `xcolor` (colors), `babel` (languages and hyphenation).

**Commands** start with a backslash; **environments** are delimited by `\begin{…}` and `\end{…}`.

| Purpose | Commands |
|---|---|
| Font | `\textbf` bold, `\textit` italic, `\texttt` typewriter, `\textsc` small caps |
| Alignment | `center`, `flushleft`, `flushright` environments |
| Breaks and spaces | `\newline` or `\\` line break, `\quad` space, `\newpage` page break |
| Size | from `\tiny`, `\scriptsize`, `\footnotesize`, `\small`, `\normalsize` up to `\large`, `\Large`, `\LARGE` |
| Sections | `\chapter`, `\section`, `\subsection`, `\subsubsection`, `\paragraph`, `\subparagraph` |
| Custom commands | `\newcommand{\bb}[1]{\mathbb{#1}}`: after this, `\bb{R}` gives $\mathbb{R}$ |

**Math mode:** inline with `$a^2 + b^2 = c^2$`; display with `\[ … \]`; numbered equations with the `equation` environment.

**Bibliography**, two ways:

- **inline**, with a `thebibliography` environment and `\bibitem{key}` entries, cited with `\cite{key}`: simple, but hard to manage in large documents;
- **BibTeX**, with entries in a separate `.bib` file, the style chosen with `\bibliographystyle{…}` and the file included with `\bibliography{references}`:
  ideal for many references.

> [!TIP]
> **Not in the slides: a complete minimal document.** Put this in `main.tex` and `references.bib` side by side, then compile with `pdflatex`, `bibtex`, `pdflatex`, `pdflatex`
> (or just open it in Overleaf, which does it for you). The repeated runs resolve the citations and cross-references.
>
> ```latex
> \documentclass[11pt]{article}        % preamble starts
> \usepackage{amsmath}
> \usepackage{graphicx}
> \usepackage{hyperref}
>
> \title{A Minimal Example}
> \author{Jane Doe}
>
> \begin{document}                      % body starts
> \maketitle
> \section{Introduction}\label{sec:intro}
> As shown by \cite{lamport1994}, typesetting math is easy:
> \begin{equation}
>   E = mc^2
> \end{equation}
> Section~\ref{sec:intro} is this one.
>
> \bibliographystyle{apalike}
> \bibliography{references}              % reads references.bib
> \end{document}
> ```
>
> ```bibtex
> @book{lamport1994,
>   author    = {Leslie Lamport},
>   title     = {LaTeX: A Document Preparation System},
>   year      = {1994},
>   publisher = {Addison-Wesley}
> }
> ```

---

## 10. How to structure a presentation

The slides on presentation skills show, as a worked example, the structure of a research talk on the automatic detection of **nonconvulsive epileptic seizures** from EEG.
The outline of the talk is the recommended structure:

1. **Introduction:** terms and definitions, then the problem statement.
2. **Review of the state of the art.**
3. **Objective.**
4. **Proposal.**
5. **Material and methods.**
6. **Results and discussion.**
7. **Conclusion.**
8. **Future work and challenges.**
9. **Bibliography.**

How the example fills each part:

| Part | In the example |
|---|---|
| Terms and definitions | what epilepsy, an epileptic seizure and *status epilepticus* are; how many people are affected |
| Problem statement | nonconvulsive status epilepticus is frequent in intensive care, has no obvious motor signs, and needs an EEG to be diagnosed; software can detect it objectively and quickly |
| State of the art | one slide per main existing approach (Kollialil et al., Sharma et al., Fatma et al.) |
| Objective | one sentence: develop methods based on scalp EEG to detect the seizures accurately, for early diagnosis |
| Material and methods | the dataset (14 EEG recordings, 139 seizures, electrodes, sampling rate), then each step of the method, then how the classifiers are trained |
| Results and discussion | a table comparing specificity, sensitivity and accuracy with 8 existing methods, then a discussion |
| Conclusion | what was done, the numbers obtained, and the **limits** (less accurate when the EEG changes over time), then an improved version and its results |
| Future work | extend to children, add seizure prediction, combine the EEG with other signals, integrate into monitoring devices |
| Bibliography | the numbered references cited in the talk, e.g. [1] |

> [!TIP]
> **Not in the slides: what to take from the example.**
> - The **problem** comes before the solution, and it is supported by numbers (how often, how many patients): it answers "so what?" (section 1).
> - The **objective** fits in one sentence.
> - Results are shown **against other methods**, not alone, and the comparison is honest: the table also includes a method with higher accuracy.
> - The conclusion states the **limitations** openly, as research ethics requires (section 4).
> - The same order works for a thesis defense, which is where most students will use it first.

---

## Cheat sheet

- Research: a systematic search for knowledge. Turn a question into a **problem** by answering "So what?". Practical problems have a tangible cost; conceptual ones are a gap in understanding.
- Venues: workshops (preliminary), conferences (recent), journals (archival), books, online archives. Paper types: theoretical, empirical, survey, application/system, position, extended abstract.
- Publication: answer the question, write, choose a venue, adapt, submit, review rounds, accept or reject. Peer review ensures quality and credibility.
- Metrics: citations (self vs others), h-index, g-index, impact factor, SJR, CORE. Famous is not necessarily high quality.
- Ethics: no plagiarism, no invented data, don't hide objections or data against you, don't distort opposing views.
- Grants: proposals with objectives, methodology, budget, outcomes; judged on significance, feasibility, team. Government, foundation, industry, international, academic, early career, postdoc, innovation.
- Writing (Goldreich): identify the idea (model, technique, results), the community (a smart beginner), the readers' needs. Avoid checklist, obscure generality, idiosyncrasies, no hierarchy, Talmudism, implicit pointers.
- Abstract: ≤ 200 words, self-contained at high level. Conclusions: rarely needed. One numbering system. Discuss definitional choices (arbitrary, simplifying, essential).
- Introduction (Etalle): background (short), problem, solution with its novelty; related work usually at the end; outline only for long papers.
- Search: databases (Scopus, WoS, IEEE Xplore, ScienceDirect, DOAJ) vs search engines (Google Scholar, BASE, Semantic Scholar, CORE, dblp, ResearchGate). Keywords, 5 W's and H, AND/OR/NOT, quotes, `*`.
- References: DOI, BibTeX, RIS; styles APA (author-date), IEEE (numbers); managers EndNote, Mendeley, Zotero, RefWorks.
- LaTeX: preamble + body, classes, packages, commands and environments, math mode, BibTeX with `\cite`.
- Presentation: definitions, problem, state of the art, objective, proposal, methods, results vs others, conclusion with limits, future work, bibliography.
