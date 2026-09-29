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

## 8. The car dealer

*From the lectures "Code constructs promoting security", "Domain primitives", "Ensuring integrity of state" and "Reducing complexity of state".*

The same scenario comes back in four lectures, each time with a new step. The lecturer's Python solution is shown in
[section 3.3](../summary.md#33-advanced-tests-for-python).

**Readings first** (lecture "Code constructs promoting security"):

- immutability: [Baeldung, *Immutable Objects in Java*](https://www.baeldung.com/java-immutable-object) and
  [Reading 8: Mutability & Immutability](http://web.mit.edu/6.031/www/fa18/classes/08-immutability/) of MIT 6.031;
- specifications and exceptions: [Reading 6: Specifications](http://web.mit.edu/6.031/www/fa18/classes/06-specifications/) of MIT 6.031.

**Step 1: do it the way you usually do it** (homework of "Code constructs promoting security").
Implement a class `Vehicle` with `String plate`, `String producer`, `String name`, `Double price`, with constructors, get/set and `toString`.
Implement `Car` and `Motorbike`, both extending `Vehicle` and redefining `getPrice()`:

- cars with price less than 10000 euro: price reduced by 5%;
- cars with price less than 20000 euro: price reduced by 10%;
- motorbikes with price less than 7000 euro: price reduced by 3%;
- motorbikes with price less than 15000 euro: price reduced by 7.5%;
- in all other cases, the price is not reduced.

Implement a class `Dealer` owning an `ArrayList<Vehicle>` with `addVehicle`, `removeVehicle`, `printVehicles`, `sortVehiclesByAscendingPrice`,
`sortVehiclesByAscendingName`, `sumOfPrices`, `saveToFile(String filename)` (one vehicle per line, format `plate;producer;name;price`) and
`readFromFile(String filename)`. Finally, write a `main` to test `Dealer`.

**Step 2: with domain primitives** (lecture "Domain primitives"). The lecture comments a naive solution of step 1 (any problem in the code?
even before, any problem in the specification? what is an entity, a value object, an aggregate?), then asks for the same application with
domain primitives: cars and motorbikes with plate, producer, model name and price before discount; a dealer that adds and removes them, accesses them
(e.g. by index), sorts them by ascending final price or by ascending model, computes the sum of prices before discount, and loads and saves data
to file automatically. *Time to implement a few domain primitives, and write secure code!*

**Step 3: a text user interface** (homework of "Domain primitives", discussed in "Ensuring integrity of state"). Implement a TUI with this menu:

1. Add car (read data from STDIN)
2. Add motorbike (read data from STDIN)
3. Remove car (by index)
4. Remove motorbike (by index)
5. Set order by ascending name
6. Set order by ascending final price
7. Print sum of prices before discount
8. Exit

Always show the list of cars and motorbikes before the menu, in the order set by the user (default: ascending name). Load and save data automatically.
In "Ensuring integrity of state" the lecture asks whether menus should be considered a domain, and then: *time to write domain primitives and entities for menus!*

**Step 4: vehicles as entities** (lecture "Reducing complexity of state"). Handle cars and motorbikes as entities, so that their fields can be changed.
How do we identify cars and motorbikes? Add these operations to the menu:

- modify car; modify motorbike;
- print the list of car producers; print the list of motorbike producers;
- print the list of cars of a producer (given by the user); print the list of motorbikes of a producer (given by the user).

> [!TIP]
> **Not in the slides: some hints.** The specification of step 1 has overlapping rules (a car of 8000 euro is below both 10000 and 20000): decide which
> one applies, as in the lecturer's solution (the first matching one). Money should not be a `Double` ([section 1.2](../summary.md#deves-mistakes)).
> For step 4, the plate looks like a natural identity, but can a plate be mistyped and corrected? Remember the fiscal code discussion in
> [section 2.1](../summary.md#entity).

## 9. The restaurant

*From the lecture "Handling failures securely", repeated at the end of "Advanced tests for Python".*

Write an application with a textual menu for a (very simple) restaurant, which wants to manage the list of orders to be served.

For an order we want the customer, a textual description and the price. From the discussion with the domain expert: the customer is a string of letters,
numbers and spaces (punctuation and special characters too, if you think it makes sense, but it is not required), at most 100 characters long. The same
applies to the description. The price is in euro, with two decimal digits, and cannot be negative.

The application must:

- show all orders;
- add and remove orders;
- show the list of customers;
- restrict the view to the orders of a given customer;
- sort orders by ascending price.

Data are saved automatically to `default.csv` and loaded when the application starts. In the Python version (after section 3.3): *we expect tests, too...
should I still say it?!?*

The lecturer's Java skeleton (package `net.alviano`) gives a head start. It already contains:

- a generic **menu** built with the builder pattern of [section 2.4](../summary.md#the-builder-pattern) (`Menu.Builder`, `withEntry`, `build` that empties the builder);
- **domain primitives** for the menu: `MenuKey` (1 to 10 characters, `[0-9A-Za-z_-]`) and `MenuDescription` (1 to 1000 characters, `[0-9A-Za-z ;.,_-]`);
- `Prezzo` (price), stored as a `long` number of cents, with `parse("12.50")`, `add` and `compareTo`;
- an `App` with commented-out hints (`Ristorante`, `Cliente`, `Ordine`, a `leggiCliente()` loop that keeps asking until the input is valid,
  a global `catch` that prints only "Panic error!").

> [!TIP]
> **Not in the slides: what is left to do.** Write `Cliente` and `Descrizione` as domain primitives (length and characters from the expert's rules),
> `Ordine` as a value object or an entity (can an order change after it is taken?), and `Ristorante` as the entity holding the list. Look at how `App`
> handles failures: invalid input is rejected and asked again, never "repaired" ([section 3.1](../summary.md#handling-bad-data)), and the global handler
> does not print the exception.

## 10. TUI exercises with tests

*From the lecture "Advanced tests for Python".*

Besides the restaurant (exercise 9), two more exercises in the style of the car dealer. For both, data are saved automatically to `default.csv` in the root
of the project and loaded at start, and tests are expected.

**Music archive.** Manage a list of songs, each with author, title, genre and duration. Author, title and genre are strings of letters, numbers and spaces,
at most 100 characters. The duration is shown in minutes and seconds (e.g. `3:25`); choose the internal representation. The application must show all songs,
add and remove songs, show the list of authors, restrict the view to the songs of a given author, and sort songs by several criteria of your choice.

**Medical office.** Manage a list of reservations, each with the patient's name, the scheduled time, the type of visit and the cost. Name and type of visit are
strings of letters, numbers and spaces, at most 100 characters. The time is shown in hours and minutes (e.g. `15:20`); choose the internal representation.
The cost is in euro with two decimal digits (and definitely not negative). The application must show all reservations, always sorted by ascending scheduled time;
add and remove reservations; and restrict the view to reservations scheduled after a given time.

> [!TIP]
> **Not in the slides: choosing the internal representation.** Like `Price` in cents, store a duration as a number of seconds and a time as minutes since
> midnight: comparisons and sorting become integer comparisons, and `3:25` or `15:20` is only the string representation (`__str__` and `parse`).
> Then test the boundaries: `0:00`, `59:59` or `23:59`, and invalid inputs like `3:60`, `24:00`, `-1:00`, `3:5`.

## 11. More quizzes

Google Forms from the lectures:

- "Domain primitives": https://forms.gle/Zv6VQZRoNCMzeKQM7
- "Ensuring integrity of state": https://forms.gle/tWyjnj4Cz1pyE25T8
- "Reducing complexity of state": https://forms.gle/TfoNLvUQ7QzTYPhq5
- "Handling failures securely": https://forms.gle/VHn7SuPw5J8W6ryT8
