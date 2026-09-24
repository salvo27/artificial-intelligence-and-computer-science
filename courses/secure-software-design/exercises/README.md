# Exercises

Exercises and readings assigned in the slides, in the order they appear. Back to the [summary](../summary.md).

## 1. The theater

*From the lecture "Why design matters for security".*

Develop a booking system for a theater with 1000 seats grouped in 25 rows of 40 armchairs each.
Every armchair is identified by a letter and a number. For a person, we are interested in the fiscal code and the name.

- **In class:** think about how you usually approach coding. Can you implement such a system?
  The lecturer also used a Google Form on this scenario: https://forms.gle/JYBYJsSEpusV1X5h7
- **Homework:** write the application. A terminal application is preferred; there is no need for a complex framework.

> [!TIP]
> **Not in the slides: how to approach it with deep modeling.** Before writing code, apply the method of
> [section 1.2](../summary.md#12-deep-modeling): list the domain concepts and, for each one, ask what its values can be.
> Some questions to start from (the answers are for you, or the "domain expert", to decide):
>
> - **Row.** 25 rows, identified by a letter: which letters exactly? A to Y? Is it case-sensitive?
> - **Seat number.** From 1 to 40, or from 0 to 39? Is it the same for every row?
> - **Seat.** A row plus a number: are there exactly 1000 valid seats?
> - **Fiscal code.** What format does it have? What about people without an Italian fiscal code?
> - **Name.** How long can it be? Which characters are allowed?
> - **Booking.** Can the same seat be booked twice? Can one person book more than one seat? Can a booking be cancelled?
>
> Each concept with rules is a candidate for its own class that validates itself on creation, like `Username` and `Quantity`.
> Then check: can your code represent a seat "Z99", a negative seat number, or a booking with an empty name?

## 2. CIA quiz

*From the lecture "Why design matters for security".*

Google Form about confidentiality, integrity and availability: https://forms.gle/ePz4eAsDgu8EQeqw9

## 3. Homework: static checking

*From the lecture "Why design matters for security".*

Understand the concept of static code checking by reading
[Reading 1: Static Checking](http://web.mit.edu/6.031/www/fa18/classes/01-static-checking/) of MIT course 6.031.
The sections to read, including their reading exercises, are:

- Static Typing
- Static Checking, Dynamic Checking, No Checking
- Surprise: Primitive Types Are Not True Numbers

The link with the course: specific types such as `Username` or `Quantity` let the compiler catch mistakes
before the program runs (see "Deve's mistakes" in [section 1.2](../summary.md#deves-mistakes)).

## 4. Reading: good coding principles

*From the lecture "Deep modeling".*

Some general principles of good coding:
[Reading 4: Code Review](http://web.mit.edu/6.031/www/fa18/classes/04-code-review/) of MIT course 6.031.

## 5. Discussion: the Person class

*From the lecture "Domain-Driven Design".*

The slides show this class and say it has many design problems, to be discussed in class. Which ones do you see?

```java
class Person {
    private String name;
    private int age;
    private int shoeSize;
    private Animal pet;

    void growOlder() {
        this.age++;
    }

    void swapPetWith(Person other) { ... }
}
```

<details>
<summary>Some possible answers (not in the slides)</summary>

These are not the lecturer's answers: they apply the ideas of the course so far.

- **`name` is a `String`**: it can be empty, huge, or contain anything (see `Username` in section 1.1).
- **`age` is an `int`**: it can be negative or two billion. `growOlder()` increments it with no upper bound, so it can pass 150
  (the invariant of the `Age` value object in section 2.1) or even overflow.
- **`shoeSize` is an `int`**: any value is accepted, and it does not say which sizing system is used.
- **`pet` is a single `Animal`**: this hard-codes the "only one pet" decision. It must be an explicit business decision
  (section 2.1, "Models are strict"), and `swapPetWith` depends on it. "No pet" is probably represented by `null`, which every method must remember to handle.
- **No constructor and no validation**: a `Person` can exist in an invalid state, for example with `name` null and `age` 0.
- **No identity**: `Person` looks like an entity, but it has no identifier. How do we tell apart two people with the same name and age?
- **`swapPetWith` changes another object's state**: who guarantees the invariants of both persons? What happens with `swapPetWith(this)` or `swapPetWith(null)`?

</details>

## 6. DDD quizzes

*From the lecture "Domain-Driven Design".*

Google Forms on DDD:

- https://forms.gle/eyMP4MzPxg8GE7yp8
- https://forms.gle/RzJmuMSLTaWgx1sc8

## 7. Reading: snapshot diagrams

*From the lecture "Domain-Driven Design".*

Section **Snapshot diagrams** of [Reading 2: Basic Java](http://web.mit.edu/6.031/www/fa18/classes/02-basic-java/) of MIT course 6.031.
*Not in the slides:* snapshot diagrams draw objects and references at a given moment, which is useful to see what "immutable" means for value objects
and why a stored reference to an inner entity of an aggregate is risky.
