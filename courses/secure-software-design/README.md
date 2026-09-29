# Secure Software Design

| | |
|---|---|
| **Code** | 27006179 |
| **ECTS** | 6 |
| **Period** | Year 1, semester 1 |
| **Curriculum** | Computer Security |
| **Lecturer** | Mario Alviano |
| **Exam format** | 3-hour session in the lab: quiz, exercises and computer exercises (see below) |
| **Official page** | https://sites.google.com/unical.it/inf-ssd |

## Contents

- [Summary](summary.md)
- [Exercises and past exams](exercises/): [assigned exercises and readings](exercises/README.md), from the theater to the car dealer and the restaurant

## Exam and attendance

From the lecturer's introductory slides. Details may change from year to year: check the official page.

- **Exam:** a 3-hour session in the lab, with a quiz, exercises and computer exercises.
  The points for every question and exercise are declared in advance.
- **Student project:** it replaces part of the first exam, worth 10 points (see [below](#student-project)).
- **Simulation:** there is an exam simulation at the end of the course.
- **Attendance:** mandatory. You must attend at least 70% of the course to take the exams.

## Student project

From the lecture "Student Projects".

- **Teams** of 4-5 students: fill in the spreadsheet on MS Teams. This part of the course is mainly asynchronous:
  work and interact through MS Teams, and ask the lecturer.
- **Topic:** there is no domain expert to provide and discuss requirements, so be your own domain expert and customer.
  Choose something you like: room reservation or anything you would like to have on campus, sport tracking of any kind,
  a shopping list, a poll maker (like Doodle).
- **When:** mainly in the classroom, about 10 hours in 4 lectures plus 3 hours to present the work, and about 13 hours of homework
  (the expected homework for 1 CFU of lab activity). For a team of 5 it is more than 100 person-hours, more than enough.

**The quest for the 10 points:**

| Points | Requirement |
|---|---|
| 1 | Git repositories (e.g. GitHub or GitLab), with a link for each sub-project (back-end and front-ends) sent to the lecturer, and a short oral presentation or video of the final result. If you don't know git: Dropbox, Drive or anything shareable by link |
| 1 | Django REST Framework set up with CORS and documentation |
| 1 | At least one model (don't overdo it) |
| 1 | The models exposed by the API in a proper way (validate incoming data) |
| 1 | Authentication and authorization implemented properly |
| 1 | Back-end tests, with code coverage above 90% |
| 2 | A Python TUI front-end |
| 1 | Tests of the TUI front-end, with code coverage above 90% |
| 1 | A browser, mobile or desktop front-end, in any language or framework you already know |

Everything needed is in the summary: DRF, CORS, documentation, models, validators, authentication, authorization and tests in
[part 4](summary.md#4-django-rest-framework); the TUI, domain primitives, mocks, patches and coverage in [section 3.3](summary.md#33-advanced-tests-for-python).

## Syllabus

From the lecturer's introductory slides. Links point to the matching section of the [summary](summary.md).

**1. Introduction to secure software design**

- Confidentiality, integrity and availability (covered in [1.1](summary.md#security-concerns-cia-t))
- [Why design matters for security](summary.md#11-why-design-matters-for-security)
- [Deep modeling](summary.md#12-deep-modeling)

**2. Domain-Driven Design**

- [Constructs promoting security](summary.md#22-code-constructs-promoting-security) (and the DDD constructs in [2.1](summary.md#21-domain-driven-design-models-and-constructs))
- [Domain primitives](summary.md#23-domain-primitives)
- [Ensuring integrity of state](summary.md#24-ensuring-integrity-of-state)
- [Reducing complexity of state](summary.md#25-reducing-complexity-of-state)

**3. Test-Driven Development**

- Design of tests, mocks and patches: [TDD](summary.md#32-introduction-to-test-driven-development) and [advanced tests](summary.md#33-advanced-tests-for-python)
- [Handling failures securely](summary.md#31-handling-failures-securely)

Not in the introductory syllabus, but covered in the lectures:
[Django REST Framework](summary.md#4-django-rest-framework), used for the [student project](#student-project).

## Resources

- **Slides and other material** on the [course webpage](https://sites.google.com/unical.it/inf-ssd), together with lectures, books and exams.
- **Books:**
  - *Secure by Design*, Dan Bergh Johnsson, Daniel Deogun, Daniel Sawano (Manning)
  - *Architecture Patterns with Python*, Harry Percival, Bob Gregory (O'Reilly)
  - *Crafting Test-Driven Software with Python*, Alessandro Molina (Packt)
