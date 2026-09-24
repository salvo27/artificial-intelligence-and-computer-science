# Secure Software Design: summary

Based on the slides by Mario Alviano, which draw on the book *Secure by Design* (Johnsson, Deogun, Sawano).
The sections follow the order of the slides. Code examples are in Java, as in the slides.

Some explanations are not in the slides: they are marked **Not in the slides**, so you can tell them
apart from the lecturer's material.

**Progress:** part 1 (lectures "Why design matters for security" and "Deep modeling") and the lecture
"Domain-Driven Design" of part 2 are covered; the rest is still to do.

## Contents

1. Introduction to secure software design
   - [1.1 Why design matters for security](#11-why-design-matters-for-security)
   - [1.2 Deep modeling](#12-deep-modeling)
2. Domain-Driven Design
   - [2.1 Domain-Driven Design: models and constructs](#21-domain-driven-design-models-and-constructs)
   - Domain primitives _(to do)_
   - Ensuring integrity of state _(to do)_
   - Reducing complexity of state _(to do)_
3. Test-Driven Development _(to do)_
   - Design of tests, mocks and patches
   - Handling failures securely
4. [Cheat sheet](#cheat-sheet)

---

# 1. Introduction to secure software design

## 1.1 Why design matters for security

### Opening exercise: the theater

The lecture opens with a small exercise: design a booking system for a theater with 1000 seats,
arranged in 25 rows of 40 armchairs. Each armchair is identified by a letter and a number; for each person
we store the fiscal code and the name.

The point is to think about **how you would normally start coding it**. The rest of the lecture shows
why the "usual" approach tends to produce insecure software. The full exercise is in [exercises](exercises/README.md#1-the-theater).

### Security is often a design issue

The slides show a photo of a PIN keypad mounted next to a door, with three questions:
*Any issue here? Can the PIN be shielded? Can you guess the PIN?*

> [!NOTE]
> **Not in the slides: one way to read the photo.** The keypad is in a spot where anyone nearby can watch
> the code being typed, and some keys look worn, which hints at which digits are used.
> Nothing is "missing" from the device: it has a keypad and a PIN, as required.
> The weakness comes from **how and where it was designed and installed**. The same happens in software.

### A common scenario

A typical project goes like this:

1. There is a team of developers, testers and domain experts, and the important qualities are agreed with the stakeholders:
   performance, security, maintainability, usability.
2. **Priority goes to business logic**, to cut release time and costs: users start using whatever is released.
3. **Security is postponed.** Nobody thanks you for it, because when it works it is invisible; at most, some security library is added.

When the software is ready to go into production, there are two outcomes, both bad:

- **Security check and penetration testing before release.** Many vulnerabilities are found and the release is delayed.
  In the extreme case, fixing them means rewriting the software.
- **No checks, straight to production.** Users adopt the software, it gets hacked, sensitive data is stolen,
  it ends up in the news: users leave, and European Union lawyers arrive.

> [!TIP]
> **Not in the slides: penetration testing** means attacking your own system on purpose, as a real attacker would,
> to find vulnerabilities before someone else does. **GDPR** is the EU regulation on personal data protection;
> a data breach can lead to heavy fines.

### A concern, not a feature

Security should make us anxious, but it is often described as a **list of features**.
Example: a home alarm has sensors, sirens, calls and SMS. Is that enough to "keep thieves out"?
It depends on things that are not features:

- how is the alarm switched on and off?
- do I always switch it on before leaving?
- do I leave the remote control where thieves can find it?
- is it easy to tamper with sensors and sirens?

**Security is a concern**: a property the whole system must have, not a component you add.

### Security features vs security concerns

Seeing security as features puts the focus on **what the system does**. Example: a website where users store pictures, with this requirement:

> "As a user, I want a login page to access my pictures."

Implementing a login page satisfies the requirement, but not what the user actually cares about.
The slides show the problem: the login page leads to the list of pictures, and each picture has a download link.
Someone who **knows or guesses the link** can download the picture directly, without ever logging in.

The user's real **concern** is that their pictures stay **confidential**. So the login page is useless if the pictures
can be reached through direct links. The requirement should be rewritten to state the concern:

> "As a user, I want all access to my uploaded pictures to be protected by authentication so that my pictures stay confidential."

The difference: protecting **one path** to the pictures (the login page) is not enough; we must protect **all paths** to them.

### Security concerns: CIA-T

| Concern | Meaning | Example from the slides |
|---|---|---|
| **Confidentiality** | Keep secret what must not become public | a healthcare record |
| **Integrity** | Information does not change, or changes only in specific, authorized ways | counting election results |
| **Availability** | Information is accessible when needed | placing a bid in an online auction before it expires |
| **Traceability** | Know who changed or accessed data | required by the GDPR for sensitive data |

### The traditional approach is not enough

The traditional approach to secure software design is a **checklist of threats** treated as top priority:
attack vectors, zero-day exploits, web vulnerabilities, OWASP. According to the slides, this is apparently not sufficient.
The following example shows why.

> [!TIP]
> **Not in the slides.** A **zero-day** is a vulnerability not yet known to the vendor, so no fix exists.
> **OWASP** (Open Worldwide Application Security Project) publishes, among other things, the list of the most common web application vulnerabilities.

### Example: a user with an id and a username

**Step 1: the naive version.**

```java
public class User {
    private final Long id;
    private final String username;

    public User(final Long id, final String username) {
        this.id = id;
        this.username = username;
    }
}
```

`username` is a `String`, which is **too permissive**: it accepts any sequence of characters, for example
`<script>alert(42);</script>`. This opens the door to an **XSS** vulnerability.

> [!TIP]
> **Not in the slides: what XSS is.** Cross-Site Scripting happens when a web page shows data provided by a user
> without treating it as plain text. If the username above is displayed in a page, the browser does not print
> `<script>alert(42);</script>`: it **runs it** as JavaScript. `alert(42)` only opens a popup, but a real attacker
> would run code that, for example, steals the session of whoever views the page.

**Step 2: validation against specific attacks.** The traditional fix is to add checks for the known attacks:

```java
public User(final Long id, final String username) {
    this.id = notNull(id);                        // rejects null
    this.username = validateForXSS(username);     // rejects XSS payloads
}
```

This works for XSS, but the slides point out three problems:

- **not all developers are security experts**: they must know about XSS to remember to write that check;
- **the focus is usually on business logic**, so checks like this are easy to forget;
- **in the future there will be new attacks**, and `validateForXSS` knows nothing about them.

**Step 3: safe design.** Instead of asking "which attacks must I block?", ask **"what is a username in my application?"**.
Talking to the domain experts, suppose the answer is:

- it contains only the characters `[A-Za-z0-9_-]` (letters, digits, underscore, hyphen);
- it is at least 4 characters long;
- it is at most 40 characters long.

Now **XSS is no longer possible**: an XSS payload needs `<` and `>`, which are not allowed.
We never thought about XSS: **we just modeled the domain**, and the attack was blocked as a side effect.

The constructor of `User` now checks these rules. In the slides it uses the helpers of Apache Commons Lang (`Validate`),
each of which throws an exception if the condition fails:

```java
public User(final Long id, final String username) {
    notNull(id);
    notBlank(username);                           // not null, not empty, not only spaces
    final String trimmed = username.trim();       // remove leading and trailing spaces
    inclusiveBetween(4, 40, trimmed.length());    // 4 <= length <= 40
    matchesPattern(trimmed, "[A-Za-z0-9_-]+");    // only allowed characters
    this.id = id;
    this.username = trimmed;
}
```

**Step 4: a `Username` class.** The username is now validated when a `User` is created. But is `User` the only place where
the concept of username appears? Probably not: think of the login form, the search, the password reset. Each of them would need
the same checks, and forgetting one is enough to reopen the hole. So it is better to put **all the knowledge about usernames
in one class**, `Username`. This kind of class is called a **domain primitive** (the topic of part 2).

```java
public class Username {
    private static final int MINIMUM_LENGTH = 4;
    private static final int MAXIMUM_LENGTH = 40;
    private static final String VALID_CHARACTERS = "[A-Za-z0-9_-]+";

    private final String value;

    public Username(final String value) {
        notBlank(value);
        final String trimmed = value.trim();
        inclusiveBetween(MINIMUM_LENGTH, MAXIMUM_LENGTH, trimmed.length());
        matchesPattern(trimmed, VALID_CHARACTERS, "Allowed characters are: %s", VALID_CHARACTERS);
        this.value = trimmed;
    }

    public String value() {
        return value;
    }
}

public class User {
    private final Long id;
    private final Username username;

    public User(final Long id, final Username username) {
        this.id = notNull(id);
        this.username = notNull(username);
    }
}
```

What changed:

- **the only way to get a `Username` is its constructor**, which validates the value. So every `Username` object that exists is valid;
- `User` now takes a `Username`, not a `String`. Passing a raw string such as `"<script>..."` **does not compile**;
- the rules live in one place: if they change (say, the maximum length becomes 30), there is one line to edit.

### Advantages of security by design

- Software gets designed anyway, so developers **do not perceive extra work**.
- **Business logic and security have the same priority**; otherwise, priority always goes to business logic.
- **Even developers who are not security experts write secure code**, as in the `Username` example.
- **Many security problems are fixed implicitly**, like XSS above.

---

## 1.2 Deep modeling

### Case study: "I'll buy -1 book!"

This case study comes from chapter 2 of *Secure by Design*: a security problem found in an online bookshop during a security check.

**The normal flow of an order.** Joe (a tester) buys 2 copies of *Hamlet* at $39 each. The online store splits the order:

- the **economy system** receives $78, sends it to **payment** (the card circuit) and records in the **accounts receivable ledger** that Joe owes $78 until the payment goes through;
- the **inventory** goes from 17 to 15 copies of *Hamlet*;
- **shipping** picks 2 copies.

**The security check.** Several checks had already passed: malicious packets were blocked, no unexpected ports were open,
session ids were protected, the configuration was correct. Then the tester analyzed the **quantity** field of an order:

- entering JavaScript code: it is not executed, so no XSS;
- trying SQL injection: nothing;
- entering **-1**: **the order is accepted**.

> [!TIP]
> **Not in the slides: what SQL injection is.** If a program builds a database query by pasting user input into it,
> an input like `1; DROP TABLE orders` can become part of the query itself and be executed by the database.

The next day, someone from **accounting** asked for clarifications: the system had issued a **credit note of $39**.
For the developers there was nothing strange, but for a member of the security team there was.

**What happened: the problem crosses several modules.** The order of -1 *Hamlet* at $39 gives -$39 to the economy system:

- **billing** sees no payment to collect: "this doesn't look like there's any payment to collect";
- the **accounts receivable ledger** records Joe with a debt of -$39, which means **the shop owes Joe $39**. To settle the debt as soon as possible, it issues a credit invoice of $39 to Joe.

**Why it is hard to discover.** Nobody orders only -1 book. But you can add it to a normal order as a "discount":
with $246 of books in the cart, adding -1 *Hamlet* at $39 brings the total down to **$207**.
In the case study this was happening frequently.

**It affects other systems too.** Further investigation showed the damage extends beyond the economy system:

- **inventory**: buying -1 book *increases* the stock (from 15 to 16), so the computer representation of the inventory no longer matches the books on the shelves;
- **shipping**: it receives an order to ship -1 book, ignores it, and nobody checks the logs.

These inconsistencies can **compensate each other and stay unnoticed**, causing steady losses for the company.

### Shallow modeling

How could such a bug be introduced? Buying a negative quantity makes no sense, yet the system allowed it.
The developer did not pay attention and used a **simple solution** ("I can use an `int` for this. Problem solved.")
that **does not properly model the domain**.

### The shallow model: Sal and Deve

The book shows how this happens through a conversation between **Sal**, the seller (the domain expert),
and **Deve**, the developer. In summary:

1. Sal explains that books can be added to an order and that a book is shown with a title and a price.
2. Deve asks whether the price is always a whole number. Sal answers no: a book can cost $19.50, tax excluded.
   Deve concludes: the title is a string, and the price is not an `int`, it's a `float`.
3. Deve asks if there is anything else to a book. Sal adds the **ISBN**, which distinguishes hardback and paperback editions.
4. Deve asks if an order is a list like "Moby Dick, Pride and Prejudice, Hamlet, Moby Dick again, …". Sal answers they would rather say
   "three Moby Dick books", because the order in which you buy them does not matter.
   Deve concludes: it isn't a float, it's an integer.

The resulting code:

```java
class Book {
    String title;
    String isbn;
    double price;
}

class Order {
    void addOrderLine(Book book, int quantity) { ... }
}
```

The slides flag three warnings.

**Warning 1: never use `float` or `double` for money** or other values that must be exact.

> [!TIP]
> **Not in the slides: why.** `float` and `double` store numbers in binary, and many decimal values such as 0.10 have no
> exact binary representation, just as 1/3 has no exact decimal one. So in Java `0.1 + 0.2` gives `0.30000000000000004`.
> On a single sum the error is tiny, but on thousands of prices, taxes and discounts it adds up, and comparisons like `total == 0.30` fail.
> For money, use an integer number of cents or `BigDecimal`, wrapped in a `Money` type.

**Warning 2: never stop the modeling at "it's an integer!".** Deve had the right intuition when asking whether the price is always
a whole number, but he did not realize that price is a **complex concept**: Sal said "tax excluded", which hints at rules
that deserve their own analysis. The key question is not *"can I represent it in code?"* but *"did I understand how it works?"*.

**Warning 3: title and ISBN were not examined at all**; Deve just used `String` for both.

### Deve's mistakes

- **`int` for quantity.** An `int` goes from about -2 billion to +2 billion (exactly from -2,147,483,648 to 2,147,483,647).
  Is that a good representation of a quantity of books? Negative values and two billion books are both accepted.
  And is it a good representation of anything else?
- **Can a title really be any string?** Empty, 10,000 characters long, full of control characters?
- **Can an ISBN really be any string?** An ISBN has a precise format.
- **He missed the chance of static checking.** `title` and `isbn` have the same type, `String`, so the compiler cannot tell them apart.

The slides show an extreme example of the last point:

```java
void addCust(String name, String phone, String fax, int creditStatus,
             int vipLevel, String contact, String contactPhone, boolean partner)
```

> [!TIP]
> **Not in the slides: why this is dangerous.** Five parameters are `String` and two are `int`. If someone swaps `phone` and `fax`,
> or `creditStatus` and `vipLevel`, the code still compiles and the bug only shows up at run time, maybe much later.
> If each concept had its own type (`PhoneNumber`, `FaxNumber`, `CreditStatus`, …), a swap would be a **compile error**.
> This is what "static checking" means: finding errors by analyzing the code, before running it
> (see the reading in the [exercises](exercises/README.md#3-homework-static-checking)).

### A deeper model

The same conversation, done well. The book shows how Deve should have proceeded; the slides extract the method.

1. **Identify complex concepts, take note, and deepen them before coding.** When Sal mentions "tax excluded", Deve realizes that
   price is a complicated matter and notes that he must go back to it later.
2. **Use the terms of the domain to deepen the analysis.** Sal speaks of a *quantity* of three Moby Dick books.
   Deve asks whether you can buy half a book: of course not. So **books come in whole numbers**.
3. **Look for the bounds.**
   - *Lower bound.* Deve asks: with three books and then all removed, is it a quantity of zero? Sal: no, a quantity of zero is not a quantity,
     it is "no quantity". So **the minimum is 1**.
   - *Upper bound.* Two billion books? Certainly not: the orders are limited by the **through-store flow**, which cannot handle
     orders bigger than a total quantity of 240.
4. **When the expert uses a new term, ask for clarification: it may be a new domain concept.** Deve asks what the through-store flow is.
   It is how online orders are handled at the warehouse (box sizes, packing stations); bigger orders must go to the *bulk flow*,
   which the online store cannot use. And the **total quantity** of an order is the sum of the quantities of all its books:
   3 *Hamlet* + 4 *Pride and Prejudice* + 1 *Moby Dick* = 8.

Result: a single quantity is between 1 and 240, and so is the total quantity of the order.

### Define specific types

The new model uses a **specific type for each concept**:

```java
class Book {
    BookTitle title;
    ISBN isbn;
    Money price;
}

class Quantity {
    Quantity(int quantityOfBooks) {
        isTrue(0 < quantityOfBooks, "Quantity must be positive");
        isTrue(quantityOfBooks <= 240, "Quantity must fit in through-store flow, which is limited to 240");
        ...
    }
}

class Order {
    void addOrderLine(Book book, Quantity quantity) { ... }
    Quantity totalQuantity() { ... }
}
```

- **Each type is validated when it is created**, and whenever it changes, if changes are allowed.
  `new Quantity(-1)` throws an exception: the invalid value never gets inside the system.
- **The compiler guarantees that only valid data circulates.** `addOrderLine` accepts a `Quantity`, not an `int`, so `addOrderLine(book, -1)`
  does not compile, and the only way to build a `Quantity` goes through the checks above. **It is no longer possible to order -1 book.**
- `totalQuantity()` also returns a `Quantity`. So the rule on the total (at most 240) is checked in the same way:
  if a new line would bring the total above 240, building the total `Quantity` fails.

### Too many classes?

A model like this has many small classes. The slides argue that this is the point:

- **every concept of the domain should be represented by a class**;
- the class is **responsible for validating** its data;
- it **encodes the knowledge** associated with the concept;
- without the class, the same validation code must be **repeated** wherever the concept is used, and each copy is a chance for a bug:
  bugs everywhere.

---

# 2. Domain-Driven Design

## 2.1 Domain-Driven Design: models and constructs

### What DDD is

**Domain-Driven Design (DDD)** is a methodology for developing complex software. It:

- **focuses on the core domain**, the part of the business the software is really about;
- **explores the domain through collaboration** between domain experts and developers;
- uses a **ubiquitous language** (a language shared by everybody) **inside an explicitly bounded context**.

The attitude, in the words of the slides: we are not satisfied with a system that works;
**we want to really understand what we are building**.

### Domain models

Domain models are the foundation of DDD.

- They define **unambiguously and rigorously what the system must do**.
- **The system must not allow any other usage.** This is where security comes in: in the bookshop of section 1.2,
  "buying -1 book" was a usage the model should never have allowed.
- They are made of **value objects** and **entities**; larger structures are represented by **aggregates**.

When several systems (or modules) must work together, each one gets its own **bounded context**, and **context mappings**
describe how data is exchanged between them. According to the slides, this division makes it easier to develop the software securely.
All these constructs are explained below.

### Models are simplifications

A model is an **abstraction of reality**: everything irrelevant **in the context** is removed.
Example: for luggage check-in at an airport, the **weight** of a bag is relevant, the **number of shoes** inside it is not.

A model of a train is a good picture of this. We expect it to share some features with real trains (color, relative size, shape,
moving on rails), while many others are different (material, absolute size, weight, propulsion, how it takes curves).
**A model is a simplification of reality that is still good enough to represent something real correctly.**

The same model can be written in several ways: a diagram ("a Person, with name, age and shoe size, may have a Pet"),
a database schema, a textual description, pseudo-code. In the slides, the model describes two concrete people:
Joe, 34, shoe size 9, with his dog Zarphac, and Jane, 28, shoe size 6, with no pet.
Height, gender and everything else are left out, because they do not matter for this model. The rule is **KISS: Keep It Simple and Stupid**.

> [!TIP]
> **Not in the slides: reading the database schema.** In the slides' diagram, `PK` (primary key) marks the column that identifies
> each row of a table (`Person ID`), and `FK` (foreign key) marks a column that points to a row of another table
> (`Owner ID` in `Pet` holds the `Person ID` of the owner).

### Models are strict

Simplifying lets us be **precise and formal**. Two common mistakes break this.

**Mistake 1: several terms for the same concept.** Bad modeling of airport luggage:

- the check-in system talks about "number of bags";
- the gate talks about "baggage count";
- the staff tablet talks about "luggage".

Are these the same thing? The numbers may not even match: are the bags already on the belt counted or not?
**Always take into account the source of the data you process.**

**Mistake 2: oversimplifying.** If everything is represented with generic types (`String`, `int`), sooner or later there will be
security problems, as seen with `Username` and `Quantity`. If the domain is not clear, **ask the domain experts**;
otherwise, be prepared to face problems.

**Example: how many pets?** The requirement says: "Many persons have only one pet." This is not formal enough.
Ask: "Is it possible to have more than one pet?" The answer: "Oh, it's very unlikely." Now there are two tempting shortcuts, both wrong:

1. **use a list of pets anyway**: the code becomes more complex, possibly for nothing;
2. **allow only one pet**: sooner or later a person with two pets will show up.

The right move is to **keep asking until the requirement is formal**: "Should we allow more pets, or do we add a restriction to only one pet?"
This is a **business decision, not a technical one**: it belongs to the domain expert, not to the developer.

The agreed model then shapes the code. In the slides:

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

The `swapPetWith` method **depends heavily on the pet requirement**: it only makes sense as written if each person has one pet.
The slides also say that this class has **many design problems** and leave them for discussion in class:
see [the exercise](exercises/README.md#5-discussion-the-person-class) for some possible answers.

### Making a model means choosing one

There is no single "right" model of a person. A Person with name, age and shoe size, who may have one Pet, is a good model
for a **dog owners' club**. A Person with date and place of birth, linked to a father and a mother, is a good model
for **family migration studies**. Each model answers the needs of its context and ignores the rest.

### A ubiquitous language

Business people speak business jargon among themselves; technical people speak technical jargon among themselves.
To build a model together, **they must agree on the terms to use**.

Once agreed, **the terms of the model must be used consistently in every artifact of the project**: specifications, diagrams, code,
manuals, databases, log files. In the slides' example, the requirements say "the quantity of goods", the order form has a
field "Quantity", the class `Order` has a `Quantity` attribute, and the `order` table has a quantity column:
it is "quantity" everywhere, it is **ubiquitous**.

### The constructs of the model

DDD models are built from four constructs: **entities**, **value objects**, **aggregates** and **bounded contexts**.
The slides show them in one picture: a `Store` (the aggregate root) has a `Name` (a value object) and zero or more `Customer`s (entities),
and each customer has an `Age` and an `Address` (value objects). A dashed line, the aggregate boundary, surrounds all of them.

### Entity

An **entity**:

- has an **identity** (usually an identifier) that defines it and distinguishes it from all other entities;
- keeps **the same identity for its whole life**;
- may contain other objects, entities or value objects;
- is **responsible for coordinating the operations** on the objects it owns.

**Two entities are equal if they have the same identity, even if their other attributes differ.**
Comparing entities uses only their identities.

*Example: a car.* Over time many parts may be replaced, but it is still the same car. We identify it by its frame number or its plate.

The identifier may be unique only in some contexts: it can be **global or local**, and it can be a progressive number
or a **UUID** (universally unique identifier).

*Example: a customer.* Sam Eperson registers at 31, living at 2 Domain Drive. Then he moves house and has a birthday:
now he is 32 and lives at 3 Dans Road. **The attributes changed, but the identity remained**: it is the same customer.
Could the fiscal code be the identifier? The slides raise two problems:

- **what if the fiscal code was entered wrong?** The identity must never change, but a mistake must be correctable;
- **what if we must register a foreigner without a fiscal code?** Then some customers would have no identity at all.

> [!TIP]
> **Not in the slides: a UUID** is a 128-bit identifier, usually written like `550e8400-e29b-41d4-a716-446655440000`, generated so that
> two systems creating one independently will practically never produce the same value. Unlike a progressive number
> (1, 2, 3, …), it does not reveal how many objects exist and cannot be guessed by adding 1.

*Example: an airplane.* An `Airplane` owns its `Passenger`s, and passengers **can only be added through the method `board(BoardingPass)`**;
direct access to the list of passengers is prevented. The airplane entity is responsible for adding passengers, and
**this is the only way to enforce invariants**.

> [!TIP]
> **Not in the slides: what an invariant is, and why this matters.** An **invariant** is a rule that must always be true,
> for example "the number of passengers does not exceed the number of seats", or "every passenger has a valid boarding pass".
> If `Airplane` exposed its list, any code could call `getPassengers().add(...)` and put someone on board skipping all checks.
> If the only way in is `board(BoardingPass)`, the checks are written in one place and cannot be bypassed.

### Value object

A **value object**:

- **has no identity: it is defined by its value**;
- is **immutable**;
- should form a **conceptual whole**;
- can **refer to** entities, but does not own them;
- **defines and imposes important constraints**;
- can be used as an attribute of entities and of other value objects;
- can have a **short life**.

**Defined by its value.** For me, a 5 euro banknote is equal to any other 5 euro banknote. I don't even distinguish
two 5 euro banknotes from one 10 euro banknote: they are 10 euro. For the European Central Bank, instead, every banknote
is different, because it has a serial number. So the same thing can be a value object in one context (my wallet)
and an entity in another (the central bank).

**Immutable.** The identifier of an entity never changes, and a value object *is* its value: so its value cannot change.
If you need a different value, you create a new value object.

**A conceptual whole, not just a group of attributes.** Compare two models of a customer:

- a single `CustomerInfo` holding age, phone number, email, street, zip code and city;
- separate value objects: `Age`; `ContactInfo` (phone number, email); `Address` (street, zip code, city).

The second **should be preferred**: each value object groups attributes that belong together. Note that `Age` has a single attribute:
**value objects with only one attribute are not so uncommon**.

**Imposes constraints.** If a person's age is an `int`, it can be anything from $-2^{31}$ to $2^{31} - 1$: the primitive type is missing
the invariants. If age is a value object `Age` with $0 \le$ value $\le 150$, **the invariants are enforced by the value object**,
so it guarantees the invariants of the domain.

> [!TIP]
> **Not in the slides: entities and value objects in code.** A sketch in the style of the previous examples.
>
> ```java
> public final class Age {                          // value object
>     private final int value;                      // final: immutable
>
>     public Age(final int value) {
>         inclusiveBetween(0, 150, value);          // the invariant, checked once
>         this.value = value;
>     }
>
>     @Override public boolean equals(Object o) {   // equal if same value
>         return o instanceof Age && ((Age) o).value == value;
>     }
>     @Override public int hashCode() { return Integer.hashCode(value); }
> }
>
> public class Customer {                           // entity
>     private final CustomerId id;                  // identity: never changes
>     private Age age;                              // attributes: may change
>     private Address address;
>
>     @Override public boolean equals(Object o) {   // equal if same identity
>         return o instanceof Customer && ((Customer) o).id.equals(id);
>     }
>     @Override public int hashCode() { return id.hashCode(); }
> }
> ```
>
> To "change" Sam's age we assign a new `Age` object (`age = new Age(32)`): the old `Age(31)` is not modified.

### Aggregate

An **aggregate** is a **conceptual boundary that groups parts of a model**. It is treated **as a unit** when the state of the system changes.
It is not chosen at random or for technical reasons: it is **carefully designed after deeply understanding the model**.

**Rules.**

- It has a **boundary** and a **root**; the root is a specific entity inside the aggregate.
- **Only the root can be referred to persistently from outside the aggregate.**
  - The root has a **global** identity; the other entities inside have a **local** identity.
  - The root **controls all access** to the objects inside the boundary.
- The root may hand out references to **inner entities**, but external objects **should not store** them.
- The root may hand out references to **inner value objects** with no restriction.
- **Invariants among the members of the aggregate are enforced on every transaction.**
- **Invariants involving several aggregates cannot always be consistent**, but they must become consistent at some point: they are **eventually consistent**.
- Objects of an aggregate may refer to other aggregates, that is, to their roots.

> [!TIP]
> **Not in the slides: two terms.**
> A **transaction** is a group of changes applied as a single step: either all of them happen, or none does.
> **Eventually consistent** means that for a while the data may disagree, but the system guarantees it will line up.
> For example, right after an order is placed, the order may already exist while the warehouse stock is not yet updated;
> a moment later, both agree.
>
> Why value objects can be handed out freely and inner entities cannot: value objects are immutable, so nobody can use them to
> change the aggregate. An inner entity can be modified, and a stored reference to it would allow changes that skip the root's checks.

**Example: a company and its employees** (from the book, summarized).

1. **The company is an entity**: it has a clear identity and, since the system handles many companies, it must be **globally identifiable**.
2. **The company's name is a value object**: it is just a value.
3. **An employee is an entity**: it definitely has an identity. Since an employee always belongs to a company, it is a **child entity** of the company.
4. **An employee's role is a value object.**
5. Talking with the domain experts, two facts emerge. An employee **does not need to be identifiable outside the company**, so it can have
   a **local** identity. And **some roles can be held by only one person at a time**: for example, there can only be one CTO.
6. To uphold this invariant, **the company must control the assignment of roles**. So the company, with its child objects, is modeled as an
   **aggregate**, and **the company is its root**.

*Why the root must control the roles:* if an employee could set its own role, two employees could both become CTO, each without knowing
about the other. Only the company sees all its employees at once, so only the company can check "is there already a CTO?".

### Bounded contexts

The ubiquitous language is present everywhere, all the time: the experts and the team speak it, it is expressed in the requirements,
and it is used in discussions, the model, the code and the tests. But **the same term may mean different things in different contexts**:
a "package" for the shipping department is a box; for developers it is a group of classes.
**Where a term changes its meaning, there is the boundary between two contexts.**

The slides follow a conversation from the book between a developer and a domain expert about orders. In summary:

**Step 1: confusion.** The expert says an order contains sellable and nonsellable products. Nonsellable products are items shipped
bundled with sellable ones, and they are not products without a price: all products have a value, but bundled ones have a price of zero,
so they are included for free. The resulting model mixes *things*, *items*, *sellable* and *nonsellable products*, *price*, *value* and *free*:
it is unclear what a product actually is. A model can be drawn, but **the discussion must go deeper**.

**Step 2: agree on unique terms.** The developer proposes to call all of them **product**, and the expert agrees.
"Included" and "bundled" mean the same thing: keep **bundled**. "Price" and "value" mean the same thing: keep **price**.
And whether a product is free does not matter at all: drop **free**. Now the model is simpler and more precise:
an order is shipped to a destination and contains products, which may be bundled and have a price.
Next question: **how many products are in an order?**

**Step 3: new terms appear.** An order has one or more products; the expert adds that an order without products "isn't much of a package".
Asked what a *package* is, the expert explains it is the box in which everything is shipped, and that the quantity of each product is
written in the order. So **quantity** and **package** join the ubiquitous language: an order has 1 to N packages, each with 1 to N products,
and each product has a quantity and a price.

What to learn from these steps: the discussion produces new terms; **find an agreement** on how to use them in the model;
once the domain expert and the developer agree, **ask the other departments** too. **The boundary is where the model stops working.**

**Step 4: another department, another model.** The developer shows the model to a **finance** expert, who says it makes sense but misses
important concepts: payment information, the due date, the reserved amount. The two simply have **a different definition of order**.
So there are two contexts, **Shipping** and **Finance**, with the **same concept but different semantics**.
Once the boundary is found, check whether the two contexts communicate, and **pay attention to the data that crosses the boundary**.

**Step 5: don't force a single model.** Suppose we merge everything into one model of an order: due date, destination, packages, products,
quantity, price, total, payment information, account, reserved amount. Finance has an invariant: **reserved amount ≥ sum of all prices**,
which makes sense **only for finance**. Now a new requirement arrives from shipping: to simplify customs declarations for international shipments,
the **actual value** of a package must be listed. Until now, bundled products were made "free" by faking their price as zero, and that is no longer OK.
The developer asks whether it is enough to remove the faked price; the expert confirms, because the sum of all prices is then the actual value of the package,
and nothing needs to be deducted, since the reserved amount is what Finance charges.

> [!WARNING]
> **Don't insist on a unifying model.** In a single model, many concepts would often go unused, and adding new ones would be hard.
> Here the two departments need different things from the same word: for **shipping**, prices must reflect the products' **value**
> (for customs); for **finance**, what matters is the **selling price**.

> [!TIP]
> **Not in the slides: where the single model breaks.** Before, a bundled product had price 0, so the sum of prices was what the customer paid,
> and the invariant *reserved amount ≥ sum of all prices* held. If bundled products now carry their real value, the sum of prices grows beyond
> what the customer pays, while the reserved amount stays the same: in a single model the finance invariant would break.
> With two contexts, the shipping `Order` carries real values and the finance `Order` keeps selling prices, and each keeps its own rules.

**Step 6: map how the contexts communicate.** Try to understand how communication between departments is structured, and reflect it in the contexts of the model.
The flow in the slides:

1. a new order arrives at **Finance**;
2. Finance **reserves the amount** on the customer's **Account**;
3. Finance sends the order to **Shipping** to be processed;
4. Shipping processes the order and ships the package;
5. Shipping **notifies** Finance that the order was shipped;
6. Finance **completes the transaction** on the Account.

In the **context map**, the shipping context is **downstream** from the finance context (finance is **upstream**):
an order of the finance department is **converted** into an order of the shipping department. The two `Order`s are the same concept in different contexts.

> [!TIP]
> **Not in the slides: upstream and downstream.** As in a river, what happens upstream flows downstream. The upstream context (Finance) produces the data;
> the downstream one (Shipping) receives it and depends on it. The conversion at the boundary is the right place to check the incoming data,
> as the slides say: pay attention to what crosses the boundary.

---

# Cheat sheet

- Security is a **concern** (a property of the whole system), not a **feature** (a component). Protect **all paths**, not one.
- Write requirements that state the concern: "…so that my pictures stay confidential".
- **CIA-T**: Confidentiality, Integrity, Availability, Traceability.
- Checklists of attacks are not enough: developers are not all experts, business logic wins, new attacks appear.
- **Model the domain** ("what is a username?") and many attacks are blocked as a side effect.
- Put all the knowledge about a concept in one class (a **domain primitive**) that validates on creation.
- Never use `float`/`double` for money. Never stop at "it's an integer!". Ask "did I understand how it works?", not "can I represent it?".
- Deep modeling: identify complex concepts, use domain terms, find lower and upper bounds, ask about every new term.
- Specific types (`Quantity`, `ISBN`, `Money`) let the **compiler** reject invalid data: no more -1 books.
- **DDD**: understand the domain with the experts; the model says what the system must do, and **must not allow anything else**.
- Models are **simplifications** (drop what is irrelevant in the context) and **strict** (one term per concept, no generic types).
- Unclear requirement? Keep asking: it is a **business decision**, made by the domain expert.
- **Ubiquitous language**: the same terms in specs, code, database, logs.
- **Entity**: has an identity that never changes; equality by identity; coordinates the objects it owns.
- **Value object**: no identity, defined by its value, immutable, a conceptual whole, enforces invariants (`Age` from 0 to 150).
- **Aggregate**: a boundary with a root entity; only the root is referenced from outside; invariants hold on every transaction; across aggregates they are eventually consistent.
- **Bounded context**: where a term changes meaning, a new context starts. Don't force a single model; map how contexts communicate (upstream/downstream) and check the data crossing boundaries.
