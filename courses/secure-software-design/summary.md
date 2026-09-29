# Secure Software Design: summary

Based on the slides by Mario Alviano. Parts 1-3 draw on the book *Secure by Design* (Johnsson, Deogun, Sawano),
the TDD lectures on *Crafting Test-Driven Software with Python* (Molina), and the Django lectures on
*Django for APIs* (Vincent). The sections follow the order of the slides. Code examples are in Java up to section 3.1
and in Python from section 3.2, as in the slides.

Some explanations are not in the slides: they are marked **Not in the slides**, so you can tell them
apart from the lecturer's material.

**Progress:** all the lectures published so far are covered, from "Why design matters for security" to
"Django REST Framework, part 2". The lecture on the student project is summarized in the [README](README.md#student-project).

## Contents

1. Introduction to secure software design
   - [1.1 Why design matters for security](#11-why-design-matters-for-security)
   - [1.2 Deep modeling](#12-deep-modeling)
2. Domain-Driven Design
   - [2.1 Domain-Driven Design: models and constructs](#21-domain-driven-design-models-and-constructs)
   - [2.2 Code constructs promoting security](#22-code-constructs-promoting-security)
   - [2.3 Domain primitives](#23-domain-primitives)
   - [2.4 Ensuring integrity of state](#24-ensuring-integrity-of-state)
   - [2.5 Reducing complexity of state](#25-reducing-complexity-of-state)
3. Failures and Test-Driven Development
   - [3.1 Handling failures securely](#31-handling-failures-securely)
   - [3.2 Introduction to Test-Driven Development](#32-introduction-to-test-driven-development)
   - [3.3 Advanced tests for Python](#33-advanced-tests-for-python)
4. Django REST Framework
   - [4.1 Django REST Framework, part 1: a first REST API](#41-django-rest-framework-part-1-a-first-rest-api)
   - [4.2 Django REST Framework, part 2: authentication, authorization, tests](#42-django-rest-framework-part-2-authentication-authorization-tests)
5. [Cheat sheet](#cheat-sheet)

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

![A PIN keypad next to a door](assets/why-design-matters/pin-keypad.jpg)
*From the slides.*

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

![The login page protects the listing, but the download link can be reached without logging in](assets/why-design-matters/login-bypass.png)
*From the slides.*

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

![The normal flow of an online order](assets/deep-modeling/normal-order-flow.png)
*From the slides: the normal flow of an online order.*

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

![An order of -1 book: billing sees nothing to collect, the ledger pays Joe back](assets/deep-modeling/minus-one-book.png)
*From the slides.*

**Why it is hard to discover.** Nobody orders only -1 book. But you can add it to a normal order as a "discount":
with $246 of books in the cart, adding -1 *Hamlet* at $39 brings the total down to **$207**.
In the case study this was happening frequently.

![Adding -1 book as a discount](assets/deep-modeling/discount-trick.png)
*From the slides.*

**It affects other systems too.** Further investigation showed the damage extends beyond the economy system:

- **inventory**: buying -1 book *increases* the stock (from 15 to 16), so the computer representation of the inventory no longer matches the books on the shelves;
- **shipping**: it receives an order to ship -1 book, ignores it, and nobody checks the logs.

These inconsistencies can **compensate each other and stay unnoticed**, causing steady losses for the company.

![The abnormal flow: inventory grows, shipping ignores the order, payment gets nothing](assets/deep-modeling/abnormal-order-flow.png)
*From the slides: the abnormal flow of an "antibook" order.*

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

![A model train](assets/domain-driven-design/train-model.png)
*From the slides.*

The same model can be written in several ways: a diagram ("a Person, with name, age and shoe size, may have a Pet"),
a database schema, a textual description, pseudo-code. In the slides, the model describes two concrete people:
Joe, 34, shoe size 9, with his dog Zarphac, and Jane, 28, shoe size 6, with no pet.
Height, gender and everything else are left out, because they do not matter for this model. The rule is **KISS: Keep It Simple and Stupid**.

![The same model as a diagram and as a database schema, and the people it describes](assets/domain-driven-design/person-pet-models.png)
*From the slides.*

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

![Two models of a person, each good for a different purpose](assets/domain-driven-design/choosing-a-model.png)
*From the slides.*

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

![Aggregate root, entities and value objects inside the aggregate boundary](assets/domain-driven-design/model-constructs.png)
*From the slides.*

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

![The company aggregate](assets/domain-driven-design/company-aggregate.png)
*From the slides.*

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

![How Finance, Shipping and the Account communicate](assets/domain-driven-design/department-flow.png)
*From the slides.*

In the **context map**, the shipping context is **downstream** from the finance context (finance is **upstream**):
an order of the finance department is **converted** into an order of the shipping department. The two `Order`s are the same concept in different contexts.

![Context map: the shipping context is downstream (D) of the finance context (U)](assets/domain-driven-design/context-map.png)
*From the slides.*

> [!TIP]
> **Not in the slides: upstream and downstream.** As in a river, what happens upstream flows downstream. The upstream context (Finance) produces the data;
> the downstream one (Shipping) receives it and depends on it. The conversion at the boundary is the right place to check the incoming data,
> as the slides say: pay attention to what crosses the boundary.

---

## 2.2 Code constructs promoting security

The lecture turns the ideas of part 1 into three strategies to use in code, and teaches to recognize the problems they solve in legacy code:

- **immutability**, against integrity and availability issues;
- **fail fast**, against irregular input and state;
- **validation**, to make sure input conforms to a specification.

### Immutability

An object is **mutable** if it allows state changes, **immutable** if it does not. Immutable objects:

- can be **safely shared among threads**;
- give **high data availability**, which helps prevent DoS attacks.

**Unless required, do not make an object mutable**: mutability is dangerous and expensive.

> [!TIP]
> **Not in the slides: DoS.** A Denial of Service attack makes a system unavailable, for example by flooding it with requests
> or by making it block. If every read of an object must wait for a lock, a burst of requests is enough to create long queues:
> that is exactly the "availability" problem of the example below.

**Example: an online shop.** Each customer has a score based on previous purchases; customers with a high score can pay later
(delayed payment) instead of immediately. Scores are computed while orders are added. During an advertising campaign, problems appear:
long waiting lines, many orders time out, and the finance department reports **delayed payments for many customers with a low score**.

The `Customer` class of the slides:

```java
public class Customer {
    private static final int MIN_INVOICE_SCORE = 500;
    private Id id;
    private Name name;
    private Order order;
    private CreditScore creditScore;

    public synchronized Id getId() { return id; }
    public synchronized void setId(final Id id) { this.id = id; }
    public synchronized Name getName() { return name; }
    public synchronized void setName(Name name) { this.name = name; }

    public synchronized Order getOrder() {
        this.order = OrderService.fetchLatestOrder(id);
        return order;
    }
    public synchronized void setOrder(Order order) { this.order = order; }

    public synchronized CreditScore getCreditScore() { return creditScore; }
    public synchronized void setCreditScore(CreditScore creditScore) {
        this.creditScore = creditScore;
    }

    public synchronized boolean isAcceptedForInvoicePayment() {
        return creditScore.compute() > MIN_INVOICE_SCORE;
    }
}
```

Several problems: attributes must be initialized with setters, so the state can change and it is not clear when the object is actually
initialized; and **all methods are `synchronized`**, so threads compete for the object and get stuck. Categorizing the observed issues
shows how they depend on the implementation:

| Observed issue | Category | Probable cause |
|---|---|---|
| Long waiting lines and poor efficiency | Availability | The system cannot reliably access customer data, and times out |
| Orders time out at checkout | Availability | The system cannot obtain in time the data needed to process orders |
| Inconsistent payment methods | Integrity | Customer scores are changed irregularly |

**Availability issues** come from synchronization. The app does many reads and few writes. Removing `synchronized` is fine for reads,
but not for writes. A nontrivial solution is a `ReadWriteLock`; the simple solution is to **make the object immutable**:
attributes are initialized on construction and cannot change, so the object can be shared among threads.

```java
public final class Customer {
    private final Id id;
    private final Name name;
    private final CreditScore creditScore;

    public Customer(final Id id, final Name name, final CreditScore creditScore) {
        this.id = notNull(id);
        this.name = notNull(name);
        this.creditScore = notNull(creditScore);
    }

    public Id id() { return id; }
    public Name name() { return name; }
    public Order order() { return OrderService.fetchLatestOrder(id); }

    public boolean isAcceptedForInvoicePayment() {
        return creditScore.isAcceptedForInvoicePayment();
    }
}
```

Writes are still an issue: they need **entity snapshots**, a concept of section 2.5.

**Integrity issues.** Look again at the credit score in the old class:

1. `CreditScore` is initialized by a setter, so **changes cannot be controlled**;
2. `setCreditScore()` **does not copy its argument**: the object may be shared with someone else and modified from outside;
3. `getCreditScore()` **releases a reference** to the internal `CreditScore`: its value can be modified from outside.

**`synchronized` is useless if the object can be modified from outside.** Moreover, `CreditScore` computes the score and needs the
customer's data, so the logic of `Customer` and `CreditScore` is mutually dependent: very bad. The fix is to make `CreditScore`
immutable and let `Customer` (or another, higher entity) do the calculation:

```java
public class CreditScore {
    private static final int MIN_INVOICE_SCORE = 500;
    private final int score;

    public CreditScore(final int computedCreditScore) {
        isTrue(computedCreditScore > -1, "Credit score must be > -1");
        this.score = computedCreditScore;
    }

    public boolean isAcceptedForInvoicePayment() {
        return score > MIN_INVOICE_SCORE;
    }
}
```

An immutable `CreditScore` can be shared among threads. The method that assigns a new `CreditScore` to a `Customer` must still be
synchronized (or use another mechanism, such as entity snapshots).

> [!TIP]
> **Not in the slides: why problems 2 and 3 break integrity.**
>
> ```java
> CreditScore score = customer.getCreditScore(); // reference to the internal object
> score.setValue(900);                           // if CreditScore were mutable...
> // ...the customer's score is now 900, and no synchronized method of Customer was called
> ```
>
> The lock protects the methods of `Customer`, not the objects it hands out. With an immutable `CreditScore` there is no `setValue`,
> so handing out the reference is harmless.

### Fail fast by contracts

Invalid data are **blocked before they can create an invalid object**. The idea is that every class defines a **contract**:
it guarantees some invariants, and other classes can assume that all invariants hold.

**Contract example: the plumber.** You call a plumber to fix a sink. The plumber asks you not to lock the bathroom door and to close
the water stop valve: these are the **preconditions** of the job; if they are not satisfied, better not to do the job at all (fail fast).
The plumber guarantees that after the job the sink will work: this is the **postcondition**. Classes should define similar contracts.

**Example: a class for cat breeders.** Cat names are put in a queue as soon as they come to mind; when a cat is born, a name is taken
from the queue.

```java
public class CatNameList {
    private final List<String> catNames = new ArrayList<String>();

    public void queueCatName(String name) { catNames.add(name); }
    public String nextCatName() { return catNames.get(0); }
    public void dequeueCatName() { catNames.remove(0); }
    public int size() { return catNames.size(); }
}
```

Its contract:

| Method | Required preconditions | Guaranteed postconditions |
|---|---|---|
| `nextCatName` | list is nonempty | size doesn't change; the returned name contains 's' |
| `dequeueCatName` | list is nonempty | size decreases by 1 |
| `queueCatName` | name is not null and contains at least an 's'; name is not already in the list | size increases by 1 |

The contract clarifies, for example, that **the caller** must provide a name not already in the list.
The contract is represented in code: **methods start with validity checks**, and if the preconditions are not satisfied they fail fast
by raising exceptions. Use `NullPointerException` if `null` is used where it is not expected, and `IllegalArgumentException` for the
other checks (unless there is a more specific Java exception):

```java
public void queueCatName(String name) {
    if (name == null)
        throw new NullPointerException();
    if (!name.matches(".*s.*"))
        throw new IllegalArgumentException("Must contain s");
    if (catNames.contains(name))
        throw new IllegalArgumentException("Already queued");
    catNames.add(name);
}
```

The same with `Validate` of Apache Commons Lang, which has `notNull`, `isTrue`, `matchesPattern`, `exclusiveBetween`,
`inclusiveBetween` and more. Use `import static` to call its methods directly (the book has a few typos here: it misses `static`).

```java
import static org.apache.commons.lang3.Validate.*;

public void queueCatName(String name) {
    notNull(name);
    matchesPattern(name, ".*s.*", "Cat name must contain s");
    isTrue(!catNames.contains(name), "Cat name already queued");
    catNames.add(name);
}
```

> [!WARNING]
> **Do not put invalid data in exception messages.** It opens the door to security issues: injections and sensitive data leakage, to start.
> For example, write `"Cat name already queued"`, not `"Cat name " + name + " already queued"`.

**When to use contracts.**

- Define contracts and verify the preconditions of **public** methods.
- For methods with **package** visibility it depends: yes if the package is big and the methods are widely used, no if they are part of a small utility class.
- **Private** methods do not need contracts (they usually use assertions).
- **Protected** methods: well, you should not use them.

**Invariants in the constructor.** Avoid empty constructors, unless there are clear default values. Name and sex of a cat are required,
so they are given to the constructor, which checks that they are not null. `notNull` returns its argument (if it does not throw),
while `matchesPattern` is void.

```java
enum Sex { MALE, FEMALE; }

public class Cat {
    private String name;
    private final Sex sex;

    public Cat(String name, Sex sex) {
        this.name = notNull(name);
        this.sex = notNull(sex);
        matchesPattern(name, ".*s.*", "Cat name must contain s");
    }
}
```

The same validation of the name appears in `Cat` and in `CatNameList`: it would be better to define a `CatName` class
(a domain primitive, as in section 2.3).

**Fail on invalid state.** `validState()` throws an `IllegalStateException` if the expression is false. `isTrue()` is not used here
because it is meant for arguments: it throws `IllegalArgumentException`. The full class:

```java
public class CatNameList {
    private final List<String> catNames = new ArrayList<String>();

    public void queueCatName(String name) {
        notNull(name);
        matchesPattern(name, ".*s.*", "Cat name must contain s");
        isTrue(!catNames.contains(name), "Cat name already queued");
        catNames.add(name);
    }

    public String nextCatName() {
        validState(!catNames.isEmpty());
        return catNames.get(0);
    }

    public void dequeueCatName() {
        validState(!catNames.isEmpty());
        catNames.remove(0);
    }

    public int size() { return catNames.size(); }
}
```

A few more lines of code, but a clear contract: the code is safer, invalid data are stopped immediately, and the list cannot be in an invalid state.

> [!TIP]
> **Not in the slides: fail fast vs fail late.** Without the check, `nextCatName()` on an empty list throws `IndexOutOfBoundsException`
> from deep inside `ArrayList`, and a `null` name would be accepted and only cause a `NullPointerException` much later, when someone
> reads it. Failing at the boundary gives a clear reason and a stack trace that points to the real culprit, and no invalid object ever exists.

### Validation

OWASP stresses the importance of input validation. But **validation is contextual**:

- for the quantity of books in an order, 42 is valid and -1 is not; for a temperature, -1 is valid;
- `<script>alert(42)</script>` is usually invalid, but it is valid for a website that reports security issues.

"Validate your input" is as helpful as "when driving, avoid accidents". We must clarify the kinds of validation and the **order**
in which they are done: from the cheapest check, such as the length, to the most expensive, such as those involving the database.

**Types of validation, in this order:**

1. **Origin**: do the data come from a legitimate sender?
2. **Size**: is the size reasonable?
3. **Lexical content**: does it contain only admissible characters?
4. **Syntax**: is the format correct?
5. **Semantics**: do the data make sense?

An input that is invalid because of its length is detected with few resources. Do not delegate simple and cheap checks to the database.

**Origin.** It is the first thing to check. Many attacks are asymmetric in favor of the attacker: sending malicious data costs little.
To prevent DoS and DDoS:

- check IP addresses: for internal services, limit access to a few known IPs, and be aware of spoofing;
- ask for an **access key** to your API: assign unique keys to legitimate users, and ask them to send back some token.

**Size.** Understand what a reasonable size is: it depends on the context. Avoid processing huge data.
An ISBN is 10 characters: discard any other length, and do not rely only on the regular expression that comes next.
What happens if you receive one billion characters?

```java
public class ISBN {
    private final String isbn;

    public ISBN(final String isbn) {
        notNull(isbn);
        inclusiveBetween(10, 10, isbn.length());
        this.isbn = isbn;
    }
}
```

**Lexical content.** Check that the received characters are the permitted ones, and that the encoding is correct.
An ISBN-10 contains only digits and the letter X (dashes and spaces are usually accepted too, but let's simplify).
More complex input requires a **lexical analyzer** (lexer).

```java
isTrue(isbn.matches("[0-9X]*"));
```

**Syntax.** Check that the characters are in the correct places, usually with a regex; if the regex is unreadable, prefer code.
In an ISBN-10 the letter X is allowed only in the last position. Lexical content and syntax are often checked together.

```java
isTrue(isbn.matches("[0-9]{9}[0-9X]"));
isTrue(checksumValid(isbn));
```

**Semantics.** Check that the data are consistent with the state of the system: does the product in the basket exist?
Is the payment method allowed? These checks are part of the model; if the data are invalid, throw an `IllegalStateException`.

> [!TIP]
> **Not in the slides: why the order matters.** The regex `[0-9]{9}[0-9X]` alone would reject a string of one billion characters too,
> but only after reading it all. Checking the length first costs one comparison. In the same way, a database lookup
> ("does this ISBN exist in the catalog?") is thousands of times more expensive than a regex: do it last, and only on data that
> already passed the cheap checks. The ISBN-10 checksum: $\sum_{i=1}^{10} (11-i)\,d_i \equiv 0 \pmod{11}$, where X stands for 10.
> For `0306406152`: $10\cdot0 + 9\cdot3 + 8\cdot0 + 7\cdot6 + 6\cdot4 + 5\cdot0 + 4\cdot6 + 3\cdot1 + 2\cdot5 + 1\cdot2 = 132 = 12 \cdot 11$, so it is valid.

### Secure by design

Putting everything together gives an **immutable `ISBN` class that validates on construction**:

```java
public final class ISBN {
    private final String isbn;

    public ISBN(final String isbn) {
        notNull(isbn);
        inclusiveBetween(10, 10, isbn.length());
        isTrue(isbn.matches("[0-9]{9}[0-9X]"));
        isTrue(checksumValid(isbn));
        this.isbn = isbn;
    }

    private boolean checksumValid(String isbn) { /* ... */ }
}
```

We can use this class without further worries about the validity of the ISBN code. Such small bricks promote security:
they are called **domain primitives**.

The lecture ends with readings on immutability, specifications and exceptions, and a homework (the car dealer) that is picked up
again in the next lectures: see the [exercises](exercises/README.md#8-the-car-dealer).

---

## 2.3 Domain primitives

### The naive dealer

The lecture opens by commenting a naive solution of the homework (classes `Vehicle`, `Car`, `Motorbike` with `String` and `Double` fields,
and a `Dealer` that keeps an `ArrayList<Vehicle>`). The questions: any problem in the code? Even before, **any problem in the specification**?
What is an entity, a value object, an aggregate here?

> [!TIP]
> **Not in the slides: some problems of the specification.** "Cars with price less than 10000 euro get 5%" and "cars with price less than 20000
> get 10%" overlap: a car of 8000 euro satisfies both. Which discount applies? "Price" is a `Double` (see "never use float or double for money"
> in section 1.2). `sumOfPrices()` returns `void`. And `plate`, `producer` and `name` are all `String`, so they can be swapped without the compiler noticing.
> The solution of the lecturer (section 3.3) applies the first matching rule: 5% up to 10000, 10% up to 20000.

### What domain primitives are

- **Value objects of the domain**.
- **Invariants are checked on creation**: an object **exists if and only if it is valid**.
- They do not use generic types and values, like `null`.
- Every concept of the domain must be well represented and encapsulated.

```java
public final class Quantity {
    private final int value;

    public Quantity(final int value) {
        inclusiveBetween(1, 200, value);
        this.value = value;
    }

    public int value() { return value; }

    public Quantity add(final Quantity addend) {
        notNull(addend);
        return new Quantity(value + addend.value);
    }

    // equals() hashCode() etc...
}
```

A quantity is defined as an integer between 1 and 200, not simply an integer. If an instance of `Quantity` exists, it satisfies the
required conditions. Note that `add` returns a **new** `Quantity`, built by the constructor, so the sum is checked too.

### The meaning depends on the context

The meaning of a domain primitive is **limited by a given context**. An ISBN may have the same meaning in an external context and in yours;
an email address may be defined by an RFC outside, and **by you** in your context. It may make sense to **redefine** a concept to better
adapt it to your goals, usually by **restricting** its definition.

![The same term in an external context and in yours](assets/domain-primitives/context-meaning.png)
*From the slides.*

**Making a definition more permissive is not recommended**: it creates confusion. Better to introduce a **new term** and use inheritance.
In the slides, your context needs to identify books that have no ISBN yet: instead of stretching "ISBN", it introduces a `Book Id`,
which can be an ISBN or an unpublished book number.

![Book Id: a new term that is either an ISBN or an unpublished book number](assets/domain-primitives/new-term.png)
*From the slides.*

> [!TIP]
> **Not in the slides: restricting a definition.** The RFC allows email addresses such as `"john doe"@[192.168.0.1]`. Your application
> probably does not need them, and accepting them makes parsing and displaying harder. Defining your `Email` as "letters, digits, dots,
> at most 254 characters, one `@`" is a restriction: every value you accept is still a valid email for the rest of the world.

### Define your own library of domain primitives

- Define domain primitives for all terms **from the beginning**.
- A method whose arguments and return value are domain primitives is safer: the arguments are valid, and the returned value is valid.
- At the end of the day **you write less code**: validation is done once, in the correct place.

**Use case: hardening an API.** Logs go to a repository on an internal server:

```java
void sendAuditLogsToServerAt(java.net.InetAddress serverAddress);
```

A method like this does not prevent the logs from being sent to an external IP. Define a new type that represents **internal addresses**:

```java
void sendAuditLogsToServerAt(InternalAddress serverAddress) {
    notNull(serverAddress);
    // Retrieve logs and send them to server
}
```

It is no longer possible to send logs outside by mistake: an `InternalAddress` can only be built from an internal address.

### Avoid exposing the domain publicly

If you define a REST API, **avoid exposing your internal model**: future changes would be expensive, because every API user would have to follow them.
Define ad-hoc objects for transmission, **Data Transfer Objects (DTOs)**. They have their own invariants, and the internal model can change
more or less independently.

> [!TIP]
> **Not in the slides: a DTO in practice.** The internal `Customer` may have an id, a `CreditScore` and a list of orders. The API returns a
> `CustomerDto` with only `id` and `name`. If tomorrow `Name` is split into first and last name, only the conversion from `Customer` to
> `CustomerDto` changes, and clients see the same JSON. It also avoids leaking fields (like the credit score) that clients should never see.

### Read-once objects

Objects designed to be **read only once**:

- they detect unexpected usage;
- they are often domain primitives (but can also be entities or aggregates);
- they prevent the serialization of sensitive data;
- they prevent subclassing and extension.

```java
public final class SensitiveValue implements Externalizable {         // (1) (2)
    private final transient AtomicReference<String> value;            // (3)

    public SensitiveValue(final String value) {
        validate(value);                                              // (4)
        this.value = new AtomicReference<>(value);
    }

    public String value() {
        return notNull(value.getAndSet(null),
                       "Sensitive value has already been consumed");  // (5)
    }

    @Override
    public String toString() { return "SensitiveValue{value=*****}"; } // (6)

    @Override
    public void writeExternal(final ObjectOutput out) { deny(); }     // (7)
    @Override
    public void readExternal(final ObjectInput in) { deny(); }        // (7)

    private static String validate(final String value) {
        // Check domain-specific invariants
        return notBlank(value).trim();
    }

    private static void deny() {
        throw new UnsupportedOperationException("Not allowed on sensitive value");
    }
}
```

1. `final`: no subclassing or extension.
2. `Externalizable`: only the identity of the class is serialized (and anyway serialization is blocked by 7).
3. The value is `transient`, so it is not serialized. `AtomicReference` guarantees an atomic assignment of the reference, for multiple threads.
5. The value is read and forgotten: a second read fails.
6. `toString()` is redefined, so the value cannot leak into some log file.
7. Serialization and deserialization are denied.

**Example: a password.** The password (or its hash) traverses several modules of the system: web modules, domain logic, infrastructure,
and finally the authentication system. It is only used once. With a read-once object, the authentication system can detect unauthorized
reads in the preceding modules: if someone read it before, `value()` fails.

![The password travels through the system but is used only once](assets/domain-primitives/read-once-password.png)
*From the slides.*

```java
public final class Password implements Externalizable {
    private final char[] value;
    private boolean consumed = false;

    public Password(final char[] value) {
        this.value = validate(value).clone();                           // (1)
    }

    public synchronized char[] value() {                                // (2)
        validState(!consumed, "Password value has already been consumed");
        final char[] returnValue = value.clone();                       // (3)
        Arrays.fill(value, '0');                                        // (4)
        consumed = true;                                                // (5)
        return returnValue;
    }

    @Override
    public String toString() { return "Password{value=*****}"; }

    @Override
    public void writeExternal(final ObjectOutput out) { deny(); }
    @Override
    public void readExternal(final ObjectInput in) { deny(); }

    private static void deny() {
        throw new UnsupportedOperationException("Serialization of passwords is not allowed");
    }

    private static char[] validate(final char[] value) {
        // Validate length, characters and so forth
        return value;
    }
}
```

The password is **actually deleted** after the read (4): this guarantees that it is no longer in memory. Removing the reference is not enough.
The caller of `value()` must erase the returned array in a similar way.

> [!TIP]
> **Not in the slides: why `char[]` and not `String`.** A Java `String` is immutable: you cannot overwrite it, and it stays in memory until
> the garbage collector removes it, which may be much later. A memory dump (or a heap dump attached to a bug report) would contain it.
> A `char[]` can be filled with zeros as soon as it has been used.

**Example: the SSN.** A `User` with name, nickname and age contains no sensitive data. After a remodeling, `User` also contains the
**SSN** (social security number): now it contains sensitive data, so the SSN is modeled as a read-once object. Tests pass and the system
goes to production. After some time, error messages "Not allowed on sensitive value" appear **when Tomcat is terminated**: Tomcat
serializes the session to disk before shutting down. What would have happened if the SSN were not a read-once object?

![User before and after the SSN is added](assets/domain-primitives/user-ssn.png)
*From the slides.*

> [!TIP]
> **Not in the slides: the answer.** Without the read-once object, Tomcat would have silently written every SSN of every active session to a file on disk,
> in clear text, where anyone with access to the server (or to its backups) could read it. The error message is annoying, but it is the design
> **telling you** that sensitive data was about to leak.

### Domain primitives are the bricks of your system

**Entities** represent long-living objects (the rooms of a hotel, the basket of an online shop), and the functions of the system change their
state (rooms are booked, products are added to and removed from the basket). **If everything is `int` or `String`, validation must be done
in the entities**: entity code grows in uncontrollable ways, with many `for` and `if`, and some path will be missed.

```java
class Order {
    private BookRepository bookCatalog;
    private ArrayList<Object> items;
    private boolean paid = false;
    Inventory inventory;

    public void addItem(String isbn, int qty) {
        if (this.paid == false) {
            notNull(isbn);
            isTrue(isbn.length() == 10);
            isTrue(isbn.matches("[0-9X]*"));
            isTrue(isbn.matches("[0-9]{9}[0-9X]"));
            Book book = bookCatalog.findByISBN(isbn);
            if (inventory.availableBooks(isbn) >= qty) {
                items.add(new OrderLine(book, qty));
            }
        }
    }
}

class ShoppingFlow {
    void handleOrderAdd() {
        String isbnText = ...
        int qty = Integer.parseInt(qtyText);
        order.addItem(isbnText, qty);
    }
}
```

The ISBN is validated in `addItem()`; every other method that uses an ISBN must do the same, without missing any check.
And did we just forget to validate the quantity? Oops!

**Remember the types of validation.** Entities should validate the **semantics** of the data, which depends on the context they know.
All the other kinds (origin, size, lexical content, syntax) should be done by domain primitives. With `ISBN` and `Quantity` as domain primitives,
the `Order` entity only asks semantic questions: does the catalog contain a book with this ISBN? Is the quantity in the warehouse sufficient?

```java
class Order {
    public void addItem(ISBN isbn, Quantity qty) {
        notNull(isbn);
        notNull(qty);
        if (this.paid == false) {
            Book book = bookCatalogue.findByISBN(isbn);
            if (inventory.availableBooks(isbn).greaterOrEqualTo(qty)) {
                addToItems(new OrderLine(book, qty));
            }
        }
    }
}

class ShoppingFlow {
    void handleOrderAdd() {
        String isbn = ...
        int qty = ...
        order.addItem(new ISBN(isbn), new Quantity(qty));
    }
}
```

### Summing up

Use domain primitives for method arguments, constructor arguments, return types and attributes of entities:

- input is always valid;
- validation is consistent;
- entity code is shorter (it does not care about limit cases, formats, etc.);
- entity code is more readable (it speaks the language of the domain).

The overhead is irrelevant compared to the other operations of the system: evaluating a regex costs nothing compared to a database access.

---

## 2.4 Ensuring integrity of state

The lecture opens by commenting a naive solution of the TUI homework (see [exercises](exercises/README.md#8-the-car-dealer)),
with a question: **should we consider menus as a domain?** The answer comes at the end of the lecture: yes, menus get their own
domain primitives and entities, as in the lecturer's [skeleton](exercises/README.md#9-the-restaurant).

### Not everything is immutable

The state of the system is mutable: items are added to the basket, orders are paid, items are shipped. In DDD **the mutable state is
represented by entities**. Two questions follow: how to **create** consistent entities (entities are more complex than domain primitives:
the builder pattern helps), and how to **keep** them consistent.

There are several ways to handle mutable state: in a browser cookie that is sent to the server when the work is finished, in the database
through stored procedures, or as **entities** that represent the state changes reported by the UI through an API and are then stored.
The last is the preferred way. **Mixing different approaches makes the state hard to manage and exposes it to vulnerabilities**:
mutable state must be understood and modeled with entities.

![Three ways of handling mutable state](assets/integrity-of-state/mutable-state.png)
*From the slides.*

### Consistency on creation

An entity that is inconsistent with the business rules is dangerous for the safety of the system, so **consistency must be there already when
the entity is created**, and we need a way to guarantee it. Do not underestimate the problem: how do I create a new `BankAccount`? When do I
specify the owner? A bank account with no owner may cost the bank its license. What about a **no-arguments constructor**?

```java
public class Account {
    private AccountNumber number;          // (1) mandatory
    private LegalPerson owner;             // (1) mandatory
    private Percentage interest;           // (1) mandatory
    private Money creditLimit;             // (2) optional
    private AccountNumber fallbackAccount; // (2) optional

    public Account() {}                    // (3)

    public AccountNumber getNumber() { return number; }
    public void setNumber(AccountNumber number) { this.number = number; }
    public LegalPerson getOwner() { return owner; }
    public void setOwner(LegalPerson owner) { this.owner = owner; }
    // ...
}

class AccountService {
    void openAccount() {
        Account account = new Account();   // (5) the entity is inconsistent
        account.setNumber(number);         // (6)
        account.setOwner(accountowner);    // (6)
        account.setInterest(interest);     // (6) consistent only after 3 setters
        account.setCreditLimit(limit);     // (7)
        // ...
    }
}
```

Several issues: entities are inconsistent, with the *promise* to become consistent later (after three setters: be careful not to forget any!).
And if a mandatory field is added, every use of the constructor must be checked by hand: **the compiler cannot report any problem**.

**ORM and no-arg constructors.** ORM frameworks need no-arg constructors. How to use an ORM safely?

1. conceptually **separate the persistent model from the domain model**;
2. directly map domain objects to the persistence framework.

The first approach is safer; the second is common, but then: use **private** no-arg constructors, and **annotate fields** instead of
providing getters and setters. ORM frameworks usually use reflection, so they can still reach private members.

> [!TIP]
> **Not in the slides: ORM and reflection.** An ORM (Object-Relational Mapping, such as Hibernate) turns database rows into objects. To do so
> it creates an empty object and then fills its fields. **Reflection** lets code inspect and call private members at run time, which is how the
> ORM can use a private constructor that the rest of your code cannot call.

**The constructor must specify all mandatory fields.** The slides compare two ways of getting a car: saying "I want a car", then
"with four doors", then "winter tires", then "and it should be gray" (the car is not ready to be used until the end: is it really worth calling it a "car"?),
or saying everything at once and getting a car immediately ready. **Prefer the second.**

![Building a car step by step vs in one go](assets/integrity-of-state/car-constructor.png)
*From the slides.*

```java
public class Account {
    private AccountNumber number;
    private LegalPerson owner;
    private Percentage interest;
    private Money creditLimit;
    private AccountNumber fallbackAccount;

    public Account(AccountNumber number, LegalPerson owner, Percentage interest) {  // (1)
        this.number = notNull(number);                                               // (2)
        this.owner = notNull(owner);
        this.interest = notNull(interest);
    }

    protected Account() {}                                   // (3) only if an ORM needs it

    public AccountNumber number() { ... }                    // (4)
    public LegalPerson owner() { ... }

    public void changeInterest(Percentage interest) {        // (5)
        notNull(interest);                                   // (6)
        this.interest = interest;
    }

    public Money creditLimit() { ... }
    public void changeCreditLimit(Money creditLimit) {       // (7)
        notNull(creditLimit);
        this.creditLimit = creditLimit;
    }

    public void changeFallbackAccount(AccountNumber fallbackAccount) {
        this.fallbackAccount = notNull(fallbackAccount);
    }
    public void clearFallbackAccount() { this.fallbackAccount = null; }
}

class AccountService {
    void openAccount() {
        AccountNumber number = ...
        LegalPerson accountowner = ...
        Percentage interest = ...
        Money limit = ...                                    // (8)
        Account account = new Account(number, accountowner, interest);   // (9)
        account.changeCreditLimit(limit);                    // (10)
        accountRepository.registerNew(account);
    }
}
```

1-2. The constructor takes all mandatory fields and validates them. 3. A private (or protected) no-arg constructor only if an ORM needs it.
4. Access methods are domain-friendly (`number()`, not `getNumber()`). 5-7. Mandatory and optional fields can be changed, with checks.
9. The entity is consistent on creation. 10. Optional fields are added later.

### Many fields: fluent interfaces

Avoid constructors with 20 arguments: probably some arguments can be grouped into a domain primitive or an entity. Pay attention also to
constructors with `null` arguments, or entities with many combinations of arguments. Before the builder pattern, the slides introduce the
**fluent interface** pattern: code that reads like fluent text in natural language, useful to set optional fields. The trick is to
**return a reference to the entity**:

```java
public class Account {
    // ...
    public Account withCreditLimit(Money creditLimit) {
        this.creditLimit = creditLimit;
        return this;
    }

    public Account withFallbackAccount(AccountNumber fallbackAccount) {
        this.fallbackAccount = fallbackAccount;
        return this;
    }
}

Account account = new Account(number, accountowner, interest)
    .withCreditLimit(limit)
    .withFallbackAccount(fallbackAccount);
```

> [!WARNING]
> **We lose command-query separation.** Commands should change the state and return nothing; queries should return an answer without
> changing anything. A `with*` method does both.

**Nonfluent fluent interfaces.** Do not return `this` from a setter: a fluent interface must produce code that *reads* fluently. What about this?

```java
Person p = new Person()
    .setFirstName("Deve")
    .setLastName("Loper")
    .setProfession("Developer");
```

> [!TIP]
> **Not in the slides: what is wrong with it.** It is still a no-arg constructor followed by setters: the `Person` exists without a name
> while the chain runs, and forgetting `.setLastName(...)` compiles fine. The chain only hides the problem of the previous section, and
> "set first name Deve set last name Loper" does not read like a sentence either.

### Advanced constraints

Some constraints involve **several fields at once**. Example: a bank account must have **either an overdraft (a credit limit) or a fallback
account**, but not both. With a credit limit, the balance can go below zero to a limited degree; with a fallback account, the missing money
is taken from another account.

![An account must have either an overdraft or a fallback account, but not both](assets/integrity-of-state/overdraft-or-fallback.png)
*From the slides.*

```java
private void checkInvariants() throws IllegalStateException {
    validState(fallbackAccount != null
               ^ creditLimit != null);
}

public void changeToFallbackAccount(AccountNumber fallbackAccount) {
    this.creditLimit = null;                      // (1)
    this.fallbackAccount = fallbackAccount;       // (2)
    checkInvariants();                            // (3)
}
```

The invariant can be violated **while the method runs** (1): after the first line the account has neither. It is important to
**restore consistency before returning control** (2), and better to **verify complex invariants before returning** (3): fail fast.

> [!TIP]
> **Not in the slides: the `^` operator.** In Java, `a ^ b` on booleans is the exclusive or: true when exactly one of the two is true.
> So `(fallbackAccount != null) ^ (creditLimit != null)` is exactly "either one or the other, not both, not neither".

### The builder pattern

The idea is to obtain a **complete object, satisfying all constraints, before other parts of the code can access it**. The complexity of
building the entity is hidden by another object, the **builder**, and whoever uses the builder does not need to see (and cannot see)
the partially built object.

![The basic idea of the builder pattern](assets/integrity-of-state/builder-idea.png)
*From the slides.*

The builder's constructor takes all mandatory fields; optional fields are added with other methods; `build()` returns the object,
and **all constraints are checked in `build()`**. Builders are well suited to a fluent interface:

```java
Account account = new AccountBuilder(number, accountOwner, interest)
    .withCreditLimit(limit)
    .build();
```

The implementation:

```java
public class Account {
    private final AccountNumber number;
    private final LegalPerson owner;
    private Percentage interest;
    private Money creditLimit;
    private AccountNumber fallbackAccount;

    private Account(AccountNumber number, LegalPerson owner, Percentage interest) {  // (1)
        this.number = notNull(number);
        this.owner = notNull(owner);
        this.interest = notNull(interest);
    }

    private void checkInvariants() throws IllegalStateException {
        validState(fallbackAccount != null ^ creditLimit != null);                    // (2)
    }

    public static class Builder {                                                     // (3)
        private Account product;

        public Builder(AccountNumber number, LegalPerson owner, Percentage interest) {  // (4)
            product = new Account(number, owner, interest);
        }

        public Builder withCreditLimit(Money creditLimit) {
            validState(product != null);                                              // (5)
            product.creditLimit = creditLimit;
            return this;                                                              // (6)
        }

        public Builder withFallbackAccount(AccountNumber fallbackAccount) {
            validState(product != null);
            product.fallbackAccount = fallbackAccount;
            return this;
        }

        public Account build() {
            validState(product != null);
            product.checkInvariants();                                                // (7)
            Account result = product;
            product = null;                                                           // (8)
            return result;                                                            // (9)
        }
    }
}
```

The entity's constructor is private (1). The builder is a **static inner class** of the entity (3), so it can access the entity's private members.
`build()` checks the invariants (7) before returning the entity (9), and **destroys itself** (8) to avoid a second use: after `build()`,
the builder has no product, so nobody can keep modifying the account through it.

### Preserving the integrity of entities

Now we know how to create valid entities. How do we keep them valid? It is impossible if the entity **releases a mutable field**,
or if it provides **setters without controls**. Changes must be controlled.

```java
class Order {
    private CustomerID custid;
    private List<OrderLine> orderitems;
    private Addr billingaddr;
    private Addr shippingaddr;
    private boolean paid;                          // (1)
    private boolean shipped;

    public void setPaid(boolean paid) {            // (2)
        this.paid = paid;
    }
    public boolean getPaid() { return paid; }
}

Order order = ...
order.paid = true;                                 // (3) does not compile
order.setPaid(true);                               // (4) allowed
```

The field `paid` is private (1), but the setter (2) exposes it to arbitrary changes: the compiler blocks (3), but (4) is allowed, and so is
`order.setPaid(false)` on a paid order.

**Encode only business rules.** An unpaid order can become paid, but not the other way around. A method `markPaid()` implements this rule:

```java
class Order {
    private boolean paid = false;
    private boolean shipped;

    public void markPaid() { this.paid = true; }
    public boolean isPaid() { return paid; }
}
```

### Do not share mutable objects

Entities need to share their data. The safest way is to share **domain primitives, which are immutable**. Sharing mutable objects allows
changes outside the control of the entity: goodbye encapsulation.

```java
class Person {
    private String name;
    private StringBuffer title;

    String name() { return name; }                 // (1)
    StringBuffer title() { return title; }         // (2)
}

String personalizedLetter(Person p) {
    String greeting = p.name()
        .concat(", we'd like to make you an offer");        // (3)
    String salute = p.title()
        .append(", we'd like to make you an offer")
        .toString();                                        // (4)
    // ...
}
```

(3) does not change the entity: `String` is immutable, and `concat` returns a new string. (4) **does** change the entity: `StringBuffer` is mutable,
and `append` modifies the very object inside `Person`. The class `java.util.Date` is deprecated precisely because it is mutable.

If you really need to return a mutable object, **return a copy**: later changes affect the copy, not the entity.

```java
class Person {
    private Date birthdate;

    Date birthdate() {
        return birthdate.clone();
    }
}
```

### Caution with collections

Consider `private List<OrderLine> orderItems;`.

- `public void setOrderItems(List<OrderLine> orderItems)`: the argument is mutable, so do not keep a reference to it in the entity.
  Make a copy of the list (expensive), or better, **encode only business logic**, for example `public void addOrderItem(OrderLine orderItem)`
  and `public int numberOfItems()`.
- `public List<OrderLine> orderItems()`: do not return a reference to a mutable field. Return a copy (expensive, and it may mislead the caller
  into thinking they can change the entity's list), or return a **read-only proxy** (but pay attention to the objects inside the list: are they mutable?).

```java
void addFreeShipping(Order order) {
    if (order.value().greaterThan(FREE_SHIPPING_LIMIT)) {
        List<OrderLine> orderlines = order.orderItems();
        orderlines.add(new OrderLine(SHIPPING_VOUCHER, 1));   // modifies the order!
    }
}

class Order {
    private List<OrderLine> orderitems;
    public List<OrderLine> orderItems() {
        return new ArrayList(orderitems);                   // a copy, with the copy constructor
    }
}

class Order {
    private List<OrderLine> orderitems;
    public List<OrderLine> orderItems() {
        return Collections.unmodifiableList(orderitems);    // better: a read-only proxy
    }
}

List<OrderItem> items = order.orderItems();
items.add(new OrderItem(SHIPPING_VOUCHER, 1));              // throws UnsupportedOperationException
```

**They are not immutable.** Even if the list is a copy or a read-only proxy, the entity may still be changed from outside **if the list contains
mutable objects**. The solution is lists of immutable objects (domain primitives). If you really need to return a mutable list, you must make a
**deep copy** (very expensive).

> [!TIP]
> **Not in the slides: shallow vs deep copy.** `new ArrayList(orderitems)` creates a new list containing **the same** `OrderLine` objects.
> If `OrderLine` had a `setQuantity`, then `order.orderItems().get(0).setQuantity(...)` would change the order even through the copy.
> A deep copy also copies each element; if the elements are immutable, a shallow copy (or a read-only proxy) is enough.

---

## 2.5 Reducing complexity of state

Managing the mutable state of entities is difficult, and state transitions can be complex. We need secure patterns for state changes:

- **partially immutable entities**;
- **entity state objects** (single-thread);
- **entity snapshots** (multi-thread);
- **entity relay** (decomposition).

**Why it matters.** This `withdraw` is fine with a single thread:

```java
void withdraw(Money amount) {
    if (this.balance.moreThan(amount)) {                     // (1)
        Money newBalance = this.balance.subtract(amount);    // (2)
        this.balance = newBalance;                           // (3)
    } else {
        throw new InsufficientFundsException();
    }
}
```

With several threads there is a **race condition**, and the balance can go below 0 through a **TOCTOU** vulnerability. The balance is $100:

1. ATM withdrawal checks the balance ($100 > $75): OK, proceed.
2. Automatic transfer checks the balance ($100 > $50): OK, proceed.
3. ATM withdrawal computes the new balance: $100 - $75 = $25.
4. ATM withdrawal updates the balance: $25.
5. Automatic transfer computes the new balance: $25 - $50 = -$25.
6. Automatic transfer updates the balance: -$25.

It can be even worse: the order 1, 2, 3, 5, 4, 6 gives a **wrong final balance**. Goodbye bank license.

> [!TIP]
> **Not in the slides: TOCTOU and the worse ordering.** TOCTOU means *Time Of Check to Time Of Use*: the check (step 1) and the use (step 3)
> are separate moments, and the world can change in between. In the order 1, 2, 3, 5, 4, 6 both threads compute their new balance from $100:
> the ATM computes $25 (step 3), the transfer computes $100 - $50 = $50 (step 5), then the ATM writes $25 (step 4) and the transfer overwrites it
> with $50 (step 6). $125 left the account, but the balance says only $50 did.

### Partially immutable entities

Anything that is not expected to change should be immutable. In class `Order`, the field `custid` must not change: does it make sense to transfer
a customer's basket to another customer? If not, why leave that possibility open? Security by design: make the entity **partially immutable**.

```java
class Order {
    private final CustomerID custid;
    Order(CustomerID custid) {
        Validate.notNull(custid);
        this.custid = custid;
    }
    public CustomerID getCustid() {
        return custid;
    }
}

class SomeOtherPartOfFlow {
    void processPayment(Order order) {
        registerDebt(order.getCustid(), order.value());
    }
}
```

`custid` is `final`, so it cannot change (as long as `CustomerID` is immutable). In this case we could also remove the getter and make `custid`
public. The code `order.custid = new CustomerID(...);` does not compile.

### Entity state objects

A person can be unmarried or married: from *Unmarried*, *Marry* leads to *Married*, and *Divorce* leads back. *Dating* is allowed when unmarried,
but **not allowed in the married status**. How to represent such state changes? The naive solution is many `if` statements.

![The marital status of a person as a state diagram](assets/complexity-of-state/marital-status.png)
*From the slides.*

**Incorrect encoding 1: the state is not checked in the entity.**

```java
public class Person {
    private final boolean married;
    public Person(boolean married) { this.married = married; }
    public boolean isMarried() { return married; }
    public void date(Person datee) {}
}

public class Work {
    private Person boss;
    private Person employee;

    void afterwork() {
        // boss attempts to date
        if (!boss.isMarried()) {
            boss.date(employee);
        } else {
            logger.warn("bad egg");
        }
    }
}
```

Very likely, some check will be forgotten in some use of the entity.

**Incorrect encoding 2: the state is implicit.**

```java
public class Person {
    private boolean married;
    public Person(boolean married) { this.married = married; }
    public boolean isMarried() { return married; }

    public void date(Person datee) {
        if (!isMarried()) {
            dinnerAndDrinks();
        } else {
            logger.warn("bad egg");
        }
    }
    private void dinnerAndDrinks() {}
}
```

Probably the `if` statements were added case by case. The state of the entity is very important: it must be carefully designed. In code,
this means an **ad-hoc class devoted to the state of the entity**:

```java
public class MaritalStatus {
    private boolean married = false;

    public void date() {
        validState(!married, "Not appropriate to date when married");
    }
    public void marry() {
        validState(!married);
        married = true;
    }
    public void divorce() {
        validState(married);
        married = false;
    }
}

public class Person {
    private MaritalStatus maritalStatus = new MaritalStatus();

    public void date(Person datee) {
        maritalStatus.date();
        buydrinks();
        offerCompliments();
    }
    public void divorce() {
        maritalStatus.divorce();
        // ...
    }
}
```

The state is explicitly represented, so we can also write **unit tests for the state** of the entity. The entity calls methods of the
state class, and **illegal calls are detected** (and logged).

### Entity snapshots

Multi-thread environments are quite common (for example, web services). Sharing immutable objects (domain primitives) is fine; sharing mutable
objects is subtler: several methods must be synchronized, and deadlocks can appear. With **entity snapshots**, the entity is not represented
by mutable classes: we use **immutable snapshots** of it.

**The idea.** A friend you have not seen for a long time: you see their pictures on Facebook. Your friend is an entity; each picture represents
your friend at a given instant. You only see photos (value objects), but you still think of them as a person (an entity).

![The entity snapshot idea](assets/complexity-of-state/snapshot-idea.png)
*From the slides.*

```java
public class OrderSnapshot {                                        // (1)
    public final OrderID orderid;
    public final CustomerID custid;
    private final List<OrderItem> orderItemList;

    public OrderSnapshot(OrderID orderid, CustomerID custid, List<OrderItem> orderItemList) {
        this.orderid = notNull(orderid);
        this.custid = notNull(custid);
        this.orderItemList = Collections.unmodifiableList(notNull(orderItemList));   // (2)
        checkBusinessRuleInvariants();
    }

    public List<OrderItem> orderItems() { return orderItemList; }   // (2)

    public int nrItems() { ... }                                    // (3)

    private void checkBusinessRuleInvariants() {
        validState(nrItems() <= 38, "Too large for ordinary shipping");
    }
}                                                                   // (4)

public class OrderService {
    public OrderSnapshot findOrder(OrderID orderid) ...
    public List<OrderSnapshot> findOrdersByCustomer(CustomerID custid) ...
}
```

- An entity snapshot is an **immutable object**, usually built from data stored in a database.
- Much of the business logic is in the snapshot (like `nrItems()` and the invariant).
- State changes must be handled by **another class** (`OrderService`): this violates encapsulation.
- Synchronization is needed only to "take" the snapshot.

### Entity relay

A pattern for entities with **many states**. The idea is to identify the **life phases** of the domain entity; each phase is represented in code by
a new entity, and a phase change means a change of entity. An entity with few states is directly manageable; with many states, it is better
to group the states into phases.

![A handful of states vs many states](assets/complexity-of-state/few-vs-many-states.png)
*From the slides.*

A person can be seen as one entity with many states from birth to death, or as a **chain of entities**, one per life phase, each with its own states:
when a phase is over, a new entity of the next phase arises like a phoenix.

![One entity through many phases vs a chain of entities](assets/complexity-of-state/person-phases.png)
*From the slides.*

**If there are points of no return, there is likely a life phase.** An order is **preliminary** until it is paid; at that point it is **definitive**.
If the shipment is rejected by the customer, the order enters a third phase, **rejected**. So the order is represented with 3 entities:

- each entity has a manageable number of states;
- the 3 phases are ordered;
- there is only one transition point from one phase to the next (2 or 3 transition points are also OK).

![The order as three entities: preliminary, definitive, rejected](assets/complexity-of-state/order-phases.png)
*From the slides.*

> [!TIP]
> **Not in the slides: the relay in code.** A sketch of the idea:
>
> ```java
> public class PreliminaryOrder {                   // states: under configuration, complete but not paid, payment rejected
>     public void addItem(ISBN isbn, Quantity qty) { ... }
>     public DefinitiveOrder pay(Payment payment) { // the only transition point
>         validState(isComplete());
>         return new DefinitiveOrder(id, items, payment);
>     }
> }
>
> public class DefinitiveOrder {                    // states: paid, shipped, delivered, misplaced, lost
>     // no addItem here: a paid order cannot change its items, and the compiler enforces it
>     public RejectedOrder reject() { ... }
> }
> ```
>
> The rule "items cannot be added to a paid order" is no longer an `if` that someone might forget: `DefinitiveOrder` simply has no such method.

The lecture ends with an exercise on the car dealer: handle cars and motorbikes as entities that can be modified (how do we identify them?), see
[exercises](exercises/README.md#8-the-car-dealer).

---

# 3. Failures and Test-Driven Development

## 3.1 Handling failures securely

### Consider failures, or fail

The real world is not perfect: nothing really goes as expected, and people may deviate from ordinary paths. Please, **consider failure when designing a system**.

### Failures represented by exceptions

Stack traces are often shown to the end user. Very bad! Why does this happen? Exceptions are often used to represent failures: they interrupt
the normal flow of a program and carry information on **why** (the message) and **where** (the stack trace) the flow was interrupted.

```
java.sql.SQLException: Closed Connection
    at oracle.jdbc.driver.DatabaseError...
    at oracle.jdbc.driver.DatabaseError.throwSqlException(...
    at oracle.jdbc.driver.PhysicalConnection.rollback(...
    at org.apache.tomcat.dbcp.dbcp.DelegatingConnection...
    at org.apache.tomcat.dbcp.dbcp.PoolingDataSource$PoolGuardConnectionWrapper.rollback(...
    at net.sf.hibernate.transaction.JDBCTransaction...
```

This trace leaks a lot: Java is used (let's look for Java vulnerabilities), SQL is used and data are stored in a relational database (let's try SQL injection),
Tomcat is used, Hibernate is used.

### Reasons to raise exceptions

- **Business exceptions** prevent actions that are illegal from the domain's point of view: withdrawing money from an account with insufficient funds,
  adding items to a paid order.
- **Technical exceptions** are not concerned with domain rules: adding items to an order without enough memory.

It is better to **separate business and technical exceptions**: business exceptions are part of the domain.

![Business exceptions come from domain rule violations, technical ones from framework and technical violations](assets/handling-failures/exception-kinds.png)
*From the slides.*

**Mixing them is bad.**

```java
public Account fetchAccountFor(final Customer customer, final AccountNumber accountNumber) {
    notNull(customer);
    notNull(accountNumber);

    try {
        return accountDatabase
            .selectAccountsFor(customer)
            .stream()
            .filter(account -> account.number().equals(accountNumber))
            .findFirst()
            .orElseThrow(
                () -> new IllegalStateException(
                    format("No account matching %s for %s", accountNumber.value(), customer)));
    } catch (SQLException e) {
        throw new IllegalStateException(
            format("Unable to retrieve account %s for %s", accountNumber.value(), customer), e);
    }
}
```

An exception is thrown if no matching account is found (business) or if a database error occurs (technical). Note that `findFirst()` is also
a not-very-good choice here. How does the caller distinguish the two cases, if both are `IllegalStateException`? **It can only rely on the message**:

```java
public Balance accountBalance(final Customer customer, final AccountNumber accountNumber) {
    notNull(customer);
    notNull(accountNumber);
    try {
        return repository.fetchAccountFor(customer, accountNumber).balance();
    } catch (IllegalStateException e) {
        if (e.getMessage().contains("No account matching")) {
            return Balance.unknown(accountNumber);
        }
        throw e;
    }
}
```

A very fragile design: the message can change, and a new `IllegalStateException` may be added and escape the `catch` block.

> [!TIP]
> **Not in the slides: why `findFirst()` is not a good choice.** A customer should have at most one account with a given number. If there are two,
> the data is inconsistent, and `findFirst()` silently picks one of them, hiding the problem. Failing if the filter finds more than one account would be safer.

### Separate business and technical exceptions

All business exceptions extend `AccountException`; catch **specific** exceptions; handle any other `AccountException` by raising a technical
exception, left to a global exception handler.

```java
public abstract class AccountException extends RuntimeException {}

public class AccountNotFound extends AccountException {
    private final AccountNumber accountNumber;
    private final Customer customer;

    public AccountNotFound(final AccountNumber accountNumber, final Customer customer) {
        this.accountNumber = notNull(accountNumber);
        this.customer = notNull(customer);
    }
    // ...
}

public Account fetchAccountFor(final Customer customer, final AccountNumber accountNumber) {
    notNull(customer);
    notNull(accountNumber);
    try {
        return accountDatabase
            .selectAccountsFor(customer).stream()
            .filter(account -> account.number().equals(accountNumber))
            .findFirst()
            .orElseThrow(() -> new AccountNotFound(accountNumber, customer));
    } catch (SQLException e) {
        throw new IllegalStateException(
            format("Unable to retrieve account %s for %s", accountNumber.value(), customer), e);
    }
}
```

The **type** of the exception already says why it failed: no need for a message. Technical exceptions stay separate from business exceptions.

```java
public Balance accountBalance(final Customer customer, final AccountNumber accountNumber) {
    notNull(customer);
    notNull(accountNumber);
    try {
        return repository.fetchAccountFor(customer, accountNumber).balance();
    } catch (AccountNotFound e) {
        return Balance.unknown(accountNumber);
    } catch (AccountException e) {
        throw new IllegalStateException(
            format("Unhandled domain exception: %s", e.getClass().getSimpleName()));
    }
}
```

Known business exceptions are handled; unknown business exceptions should not exist, but just in case they become a technical exception.

**Be aware that the application may still leak sensitive data.** Look at the message of the technical exception above:
`format("Unable to retrieve account %s for %s", accountNumber.value(), customer)`. Is the customer's name sensitive? Is it sensitive in another context?
At that point you really do not know which contexts this information will traverse. You may end up logging private data that should not be
accessed by developers, who usually have access to log files. **Never include sensitive data in exceptions!**

### Failure is not exceptional

Failures are a natural and expected outcome of anything we do. Does it make sense to model them as exceptions? A method usually has several
outcomes: it can succeed, and it can fail. If failures are designed as **unexceptional outcomes**, many problems are solved: there is no ambiguity
between domain and technical exceptions, and it is impossible to leak sensitive information by accident.

**Example: a money transfer between bank accounts.** Initiate the transfer; if there are sufficient funds, execute it, otherwise reject it.

![The execution flow of a money transfer](assets/handling-failures/money-transfer.png)
*From the slides.*

```java
public final class Account {
    public void transfer(final Amount amount, final Account toAccount)
            throws InsufficientFundsException {
        notNull(amount);
        notNull(toAccount);
        if (balance().isLessThan(amount)) {
            throw new InsufficientFundsException();
        }
        executeTransfer(amount, toAccount);
    }
    // ...
}
```

Using exceptions to control the flow of a program is odd: **an insufficient balance is not exceptional**. Define **Result objects** for your methods;
their design is part of the business model:

```java
public final class Account {
    public Result transfer(final Amount amount, final Account toAccount) {
        notNull(amount);
        notNull(toAccount);
        if (balance().isLessThan(amount)) {
            return INSUFFICIENT_FUNDS.failure();
        }
        return executeTransfer(amount, toAccount);
    }
    // ...
}

public final class Result {
    public enum Failure {
        INSUFFICIENT_FUNDS,
        SERVICE_NOT_AVAILABLE;

        public Result failure() { return new Result(this); }
    }

    public static Result success() { return new Result(null); }

    private final Failure failure;
    private Result(final Failure failure) { this.failure = failure; }

    public boolean isFailure() { return failure != null; }
    public boolean isSuccess() { return !isFailure(); }
    public Optional<Failure> failure() { return Optional.ofNullable(failure); }
}
```

Some advantages of designing failures as expected, unexceptional outcomes:

| Security issue | Solved through |
|---|---|
| Ambiguity between domain and technical exceptions | Domain exceptions are completely removed. |
| Exception payload leaking into logs | Failures are not handled by generic error-handling code, so their data do not slip into error logs by accident. |
| Accidentally leaking sensitive information | Failures are handled in a context that knows what is sensitive and what is not, and how to handle sensitive data properly. |

> [!TIP]
> **Not in the slides: using the result.**
>
> ```java
> Result result = from.transfer(amount, to);
> if (result.isFailure()) {
>     switch (result.failure().get()) {
>         case INSUFFICIENT_FUNDS    -> showMessage("Not enough money on the account");
>         case SERVICE_NOT_AVAILABLE -> showMessage("Try again later");
>     }
> }
> ```
>
> The caller cannot forget that a transfer may fail: the return type says it. With an unchecked exception, forgetting the `catch` compiles fine.

### Designing for availability

You do not want your application to be unavailable, yet you cannot pretend to serve every request: there is always a physical limit.
It is better to tell the user that the system is busy than to let them wait forever. **Implement queues.**

**Circuit breakers.**

- Start with a **closed** circuit: all requests are processed, and failures are counted.
- When there are too many failures, **open** the circuit: requests are discarded.
- After some time, **half-open** the circuit: process some requests; if they succeed, close the circuit, otherwise open it again.

![The states of a circuit breaker](assets/handling-failures/circuit-breaker.png)
*From the slides.*

> [!TIP]
> **Not in the slides: why it helps.** Suppose the payment service is down and each call waits 30 seconds before timing out. Without a breaker,
> every checkout blocks a thread for 30 seconds, threads run out, and the whole shop goes down with the payment service. With the breaker open,
> calls fail immediately ("payments are temporarily unavailable"), the rest of the shop keeps working, and the payment service gets time to recover
> instead of being hammered with requests.

### Handling bad data

Data is often dirty: spaces here and there, missing characters, special characters. **Do not try to repair the input.** Repairing opens the way to
injection flaws and to **second-order attacks**, where the vulnerability shows up in another system, such as the log viewer.

![A repair filter turns the input into D', which ends up in the browser and in the logs](assets/handling-failures/repair-filter.png)
*From the slides.*

In the slides the input `%3<Cscript%3>Ealert("XSS")%3<C/script%3>E` goes through a filter that "repairs" it by removing `<` and `>`.
The result is `%3Cscript%3Ealert("XSS")%3C/script%3E`: the URL encoding of `<script>alert("XSS")</script>`. The name validation then fails with
an exception that contains the repaired data in its payload; the data is rendered in the browser and written to the log files, where a
browser-based log analysis tool decodes it and runs the script.

**Do not echo input verbatim, never, not even in log files!**

> [!TIP]
> **Not in the slides: reading the example.** `%3C` and `%3E` are the URL encodings of `<` and `>`. The attacker hid a `<` and a `>` *inside*
> the encodings (`%3<C`, `%3>E`), knowing that the filter would remove them and thus build the encoded payload by itself. The original input was
> harmless for the validator; the "repaired" one is an attack. Rejecting the input instead of repairing it would have stopped it at the start.

---

## 3.2 Introduction to Test-Driven Development

Main reference: *Crafting Test-Driven Software with Python*, chapters 5 and 6.

### Introduction

**Test-Driven Development (TDD)** is a methodology. It helps to write better code, but it will not solve all your problems.
It is **not a religion**: do not commit to it blindly; understand it, don't let it dominate you.

**A real-life example.**

> Boss: I just met with the rest of the board. Our clients are not happy, we didn't fix enough bugs in the last two months.
> Programmer: I see. How many bugs did we fix?
> Boss: Well, not enough!
> Programmer: OK, so how many bugs do we have to fix every month?
> Boss: More!

How do we know if we improved "enough"? What are we going to measure? **Avoid working with foggy concepts**: we want precise concepts, and we must
**measure** something to know if we improved.

### The idea of TDD

You write a function and expect it "to work". How do you test that it works? What do you mean by "works"? **TDD forces you to state your goal clearly
before writing the code.** Not only for software: apply it everywhere.

> **TDD mantra: test first, code later.** Whatever you are going to do, first define your goals clearly, and a reproducible procedure to measure what you achieved.

**Example of test:** `sum(4, 5) == 9`. It says that there will be a `sum` function in the system, that it accepts two integers, and that for 4 and 5 it
returns 9. If we test first and code later, the test will fail. True, and expected: the test is **evidence that a feature is missing**.

### A simple TDD project: a calculator

The final result is in the repository [pycabook/calc](https://github.com/pycabook/calc). The slides show how to set up the project in PyCharm:
create a virtual environment (usually in `.venv`), activate it, install the requirements, and run the tests with pytest (either with a pytest run
configuration, or by right-clicking the `tests` directory).

**Requirements.** Write a class `Calc` that performs addition, subtraction, multiplication and division.

- Addition and multiplication accept multiple arguments.
- Division returns a float, and division by zero returns the string `"inf"`.
- Multiplication by zero raises a `ValueError`.
- A function computes the average of an iterable such as a list. It takes optional upper and lower thresholds and removes from the computation the
  values outside them. For an empty sequence the average is undefined and the function returns `None`.

The requirements on multiplication and division are strange: it's just an example.

### The first test

`tests/test_calc.py`:

```python
from calc.calc import Calc

def test_add_two_numbers():
    c = Calc()
    res = c.add(4, 5)
    assert res == 9
```

pytest discovers the tests: every `test_*` function is a test, and **a test fails if it raises an exception**. Running it now gives errors: they are
expected, and now we fix them. **The requirements are used to write the tests, and the tests are used to write the code.**

The fix goes in small steps, each one the minimum that changes the error:

```python
class Calc:                      # step 1: TypeError: add() takes 1 positional argument but 3 were given
    def add(self):
        pass

class Calc:                      # step 2: AssertionError: assert None == 9
    def add(self, a, b):
        pass

class Calc:                      # step 3: 1 passed
    def add(self, a, b):
        return 9
```

**Stop here! All tests are satisfied.** Do you want more? Give me more tests! (Obviously we are exaggerating, but it is to give the idea.)

### More tests

The requirement says addition accepts multiple arguments, not only two. Add a test:

```python
def test_add_three_numbers():
    c = Calc()
    res = c.add(4, 5, 6)
    assert res == 15
```

It fails (`add() takes 3 positional arguments but 4 were given`). The minimum fix is a third argument, `def add(self, a, b, c): return 9`, and now
**test 1 breaks**: `add() missing 1 required positional argument: 'c'`. That's good! It is a **regression test failure**: we know the problem was
introduced by the last change. What if test 1 had not been there to help?

Actually, test 2 is failing too. **Focus on one failing test at a time.** Tests that were passing before get priority: they are easier to fix,
just undo the last change. A third argument with a default value, `def add(self, a, b, c=0): return 9`, makes test 1 pass. Test 2 still fails:
fix it with `return 15`? That would break test 1, so no: `return a + b + c`, and both pass.

### TDD is slow

Yes, it is. You would be much faster without tests, **until something breaks**: then you spend time searching for the bug. How long was the bug there?
How do you find it? You have to write examples. **Those examples are tests!** Wasn't it better to write them once and for all?

### We are not done

"Addition and multiplication accept multiple arguments": not only two, possibly three, four and so on. We cannot test infinitely many cases, but we
should test at least the **boundary cases**: what are the corner cases of our algorithm? If the input goes from 1 to 100, you may not need to test 42,
but you should test 1 and 100, and also the errors for 0 and 101.

In TDD a solution is not correct because it is beautiful, smart, or uses the latest feature of the language: **TDD wants your code to pass the tests**.
TDD does not cover all the needs of a software project: your code might be ugly, convoluted and slow.

```python
def test_add_many_numbers():
    assert Calc().add(*range(100)) == 4950

class Calc:
    def add(self, *args):
        return sum(args)
```

> [!TIP]
> **Not in the slides: `*args`.** `def add(self, *args)` collects all positional arguments into a tuple, so `add(4, 5)` gives `args = (4, 5)`.
> In the call `add(*range(100))`, the star does the opposite: it unpacks the range into 100 separate arguments, 0 to 99, whose sum is $\frac{99 \cdot 100}{2} = 4950$.

### Subtraction, multiplication, refactoring

**Subtraction.** Multiple arguments are not mentioned, so it takes two operands. A test from the requirement, and the fix is simple:
we don't need all the steps we did for addition, which were only to understand the approach.

```python
def test_subtract_two_numbers():
    assert Calc().sub(10, 3) == 7
```

**Multiplication** is similar to addition. After writing it for two numbers, a new test for many numbers does **not** fail: should we keep it?
It checks multiple arguments, so in this case yes. **Usually new tests must fail. If not, ask yourself whether the new test makes sense.**

**Refactoring.** If all tests pass, we can refactor. Do not refactor without tests: how can you be confident that you are not breaking something?
Better to write tests before refactoring; better still with TDD: no tests, no code. Always test boundary cases: for multiplication with no numbers the
result is 1.

```python
def test_multiply_two_numbers():
    assert Calc().mul(6, 4) == 24

def test_multiply_many_numbers():
    assert Calc().mul(*range(1, 10)) == 362880

def test_multiply_no_numbers():
    assert Calc().mul() == 1
```

### Division and exceptions

Division returns a float, and by requirement division by zero returns the string `"inf"` (very strange, but it's just an example).
Multiplication by zero must raise a `ValueError`: use `pytest.raises` to check that an exception is raised.

```python
def test_division_two_numbers():
    assert Calc().div(13, 2) == 6.5

def test_division_by_zero_returns_inf():
    assert Calc().div(5, 0) == "inf"

def test_multiplication_by_zero_raises_exception():
    with pytest.raises(ValueError):
        Calc().mul(3, 0)
```

### A more complex set of requirements: the average

A function computes the average of an iterable, with two optional thresholds to remove outliers. Break it into simple tests:

- it computes the average: `avg([2, 5, 12, 98]) == 29.25`;
- optional upper threshold: `avg([2, 5, 12, 98], ut=90) == avg([2, 5, 12])`;
- optional lower threshold: `avg([2, 5, 12, 98], lt=10) == avg([12, 98])`;
- the upper threshold stays in: `avg([2, 5, 12, 98], ut=98) == avg([2, 5, 12, 98])`;
- the lower threshold stays in: `avg([2, 5, 12, 98], lt=5) == avg([5, 12, 98])`;
- it works with an empty list: `avg([]) == None`;
- it works if the list is empty after removing outliers: `avg([12, 98], lt=15, ut=90) == None`;
- outlier removal works on an empty list: `avg([], lt=15, ut=90) == None`.

Following the tests one by one gives this code, where all tests pass:

```python
def avg(self, it, lt=None, ut=None):
    if not it:
        return None
    if not lt:
        lt = min(it)
    if not ut:
        ut = max(it)
    _ = [x for x in it if lt <= x <= ut]
    if not _:
        return None
    return sum(_) / len(_)
```

All tests pass: **refactoring time!**

```python
def avg(self, it, lt=None, ut=None):
    if lt:
        it = [x for x in it if x >= lt]
    if ut:
        it = [x for x in it if x <= ut]
    if not it:
        return None
    return sum(it) / len(it)
```

### Tests from bug reports

**A bug is an example of a missing test in your suite.** What if `lt` is 0? `if lt:` is false for 0, so the threshold is ignored:

```python
def test_avg_manages_zero_value_lower_outlier():
    assert Calc().avg([-1, 0, 1], lt=0) == 0.5    # fails: assert 0.0 == 0.5
```

The fix is `if lt is not None:`, and the same problem exists for `ut`:

```python
def test_avg_manages_zero_value_upper_outlier():
    assert Calc().avg([-1, 0, 1], ut=0) == -0.5

def avg(self, it, lt=None, ut=None):
    if lt is not None:
        it = [x for x in it if x >= lt]
    if ut is not None:
        it = [x for x in it if x <= ut]
    if not it:
        return None
    return sum(it) / len(it)
```

Note that we are refactoring: luckily we have regression tests! Last but not least, run the tests with **coverage analysis**: lines not covered by tests
are either unreachable or a sign of missing tests.

> [!TIP]
> **Not in the slides: truthiness.** In Python, `if x:` is false not only for `None` but also for `0`, `0.0`, `""`, `[]` and `{}`. That is why `if not lt:`
> treated a threshold of 0 as "no threshold". When you mean "was this argument given?", write `is None` / `is not None`.
> Note also that in the first version `if not ut: ut = max(it)` would have the same bug.

### Summing up

1. Test first, code later.
2. Add the bare minimum of code you need to pass the tests.
3. You shouldn't have more than one failing test at a time.
4. Write code that passes the tests. Then refactor it.
5. A test should fail the first time you run it. If it doesn't, ask yourself why you are adding it.
6. Never refactor without tests.

---

## 3.3 Advanced tests for Python

Main reference: *Crafting Test-Driven Software with Python*, chapters 7 and 8. The lecture covers type hints, dataclasses, type and value validation,
fixtures, mocks and patches. The examples were updated to use **poetry**.

### Running example: the car dealer

A TUI to store cars and motorbikes (plate, producer, model, price), with a discount applied as in the Java homework. It is limited to add and remove,
and to sorting by producer and by price.

### Third-party modules

A simple way to validate types and values is `if` statements that raise exceptions. It is better to reuse third-party modules and new features of Python:

- **type hints** can be used by a static analyzer, but also for **dynamic validation** with [typeguard](https://typeguard.readthedocs.io/en/latest/userguide.html);
- **dataclasses** are convenient to define classes from annotations; typeguard does not validate the generated `__init__`, but validation can be enforced
  in `__post_init__`;
- for further validation, [valid8](https://smarie.github.io/python-valid8/).

```python
@dataclass(frozen=True, order=True)
class Plate:
    value: str

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value, min_len=5, max_len=10, custom=pattern(r'[0-9A-Z]*'))

    def __str__(self):
        return self.value
```

- `@dataclass` generates `__init__`, `__eq__` and other methods; `frozen=True` prevents changes; `order=True` generates `__lt__` and the other comparisons.
- The annotation says that `Plate` has a field `value` of type `str`.
- `__post_init__` is called after `__init__` to add further validation: `validate_dataclass` checks the type of all fields, and `validate()` from valid8
  checks the value, with a custom validator that enforces a regex.
- `__str__` is customized.

The two helpers live in a small `validation` package (it could be a third-party module):

```python
def validate_dataclass(dataclass_instance):
    for field in dataclasses.fields(dataclass_instance):
        check_type(value=getattr(dataclass_instance, field.name), expected_type=field.type, ...)

@typechecked
def pattern(regex: str) -> Callable[[str], bool]:
    r = re.compile(regex)
    def res(value):
        return bool(r.fullmatch(value))
    res.__name__ = f'pattern({regex})'
    return res
```

> [!TIP]
> **Not in the slides: Python has no compiler to check types.** `Plate(42)` runs without complaint in plain Python: type hints are only annotations.
> `validate_dataclass` turns them into run-time checks, so `Plate(42)` raises `TypeCheckError`, giving back part of the safety that Java's compiler
> gives for free. `pattern` returns a function (a closure) that valid8 calls on the value.

### Project structure

- `dealer/`: the project modules: domain classes, generic menu classes (they could be a third-party module), and the I/O classes of the app.
- `validation/`: utilities to ease validation.
- `tests/`: the tests; the folder **mirrors the structure** of the other folders and modules, with **one `test_*` file for every module**.
- `default.csv`: data are loaded from and saved to this file automatically.

Tests check **wrong values** (we expect exceptions) and **correct values** (we expect to read them back). Try to cover all lines of code with your tests.

```python
def test_plate_format():
    wrong_values = ['', 'abcde', 'AA000bb', 'A'*11]
    for value in wrong_values:
        with pytest.raises(ValidationError):
            Plate(value)

    correct_values = ['CA220NE', 'ABCDE', 'A'*10]
    for value in correct_values:
        assert Plate(value).value == value
```

**A note on `@typechecked`.** It is a no-op in production (when Python runs in optimized mode). It is used to introduce dynamic type checking
gradually in an existing project with broken types. We can instead install the **import hook** (before loading anything else), and typeguard will
check (almost) everything; `@typechecked` can then be removed. By default only the first element of a collection is checked, so the strategy is set to
check all items:

```python
# dealer/__init__.py
typeguard.config.collection_check_strategy = CollectionCheckStrategy.ALL_ITEMS
install_import_hook('dealer')
```

### Discount and Price

The discount is expressed **in thousands** (so 7.5% is 75). Test boundaries, the string representation, and any non-trivial computation the class performs.
Use type hints as much as possible: PyCharm uses them to help you code, and if we have to fail, better to fail soon; typeguard lets us fail.

```python
@dataclass(frozen=True, order=True)
class Discount:
    value_in_thousands: int

    def __post_init__(self):
        validate_dataclass(self)
        validate('value_in_thousands', self.value_in_thousands, min_value=0, max_value=1000)

    def __str__(self):
        return f'{self.value_in_thousands // 10}.{self.value_in_thousands % 10}%'

    def apply(self, value: int) -> int:
        return value * (1000 - self.value_in_thousands) // 1000
```

**Price, never simple.** The price is stored **in cents**, to be precise. It is created from euro and possibly cents, so the plain constructor should be
disabled to avoid confusion. How? A constructor cannot be private in Python. Non-string domain primitives also get a `parse` method.

```python
@dataclass(frozen=True, order=True)
class Price:
    value_in_cents: int
    create_key: InitVar[Any] = field(default=None)

    __create_key = object()
    __max_value = 100000000000 - 1
    __parse_pattern = re.compile(r'(?P<euro>\d{0,11})(?:\.(?P<cents>\d{2}))?')

    def __post_init__(self, create_key):
        validate('create_key', create_key, equals=self.__create_key)
        validate_dataclass(self)
        validate('value_in_cents', self.value_in_cents, min_value=0, max_value=self.__max_value)

    @staticmethod
    def create(euro: int, cents: int = 0) -> 'Price':
        validate('euro', euro, min_value=0, max_value=Price.__max_value // 100)
        validate('cents', cents, min_value=0, max_value=99)
        return Price(euro * 100 + cents, Price.__create_key)

    @staticmethod
    def parse(value: str) -> 'Price':
        m = Price.__parse_pattern.fullmatch(value)
        validate('value', m)
        euro = m.group('euro')
        cents = m.group('cents') if m.group('cents') else 0
        return Price.create(int(euro), int(cents))

    @property
    def cents(self) -> int:
        return self.value_in_cents % 100

    @property
    def euro(self) -> int:
        return self.value_in_cents // 100

    def add(self, other: 'Price') -> 'Price':
        return Price(self.value_in_cents + other.value_in_cents, self.__create_key)

    def apply_discount(self, discount: Discount) -> 'Price':
        return Price(discount.apply(self.value_in_cents), self.__create_key)
```

**The create key: a private constructor in Python.** `create_key` is an extra argument of `__init__` (and `__post_init__`), declared as `InitVar`.
`__create_key` is a private class variable (its name is actually mangled), and `__post_init__` requires `create_key == __create_key`. Since
`__create_key` is not reachable from outside `Price`, **the constructor can be called only inside `Price`**: `Price(1)` raises a `ValidationError`.

Other notes from the slides:

- Use a **string as type hint** (`'Price'`) when the type is not fully defined yet. Do it for methods that return instances of the class;
  if you need it anywhere else, you probably have circular dependencies.
- A **property** is a method taking only `self` that we want to read without parentheses (`price.euro`). A property can also have a setter,
  but not in a frozen dataclass.
- `Price` knows `Discount`, but `Discount` does not know `Price`. Unless there is a valid reason, **avoid circular dependencies**.
- Non-trivial calculations always come with tests.

```python
def test_price_no_init():
    with pytest.raises(ValidationError):
        Price(1)

def test_price_parse():
    assert Price.parse('10.20') == Price.create(10, 20)

def test_price_add():
    assert Price.create(9, 99).add(Price.create(0, 1)) == Price.create(10)

def test_price_apply_discount():
    assert Price.create(100).apply_discount(Discount(100)) == Price.create(90)
```

> [!TIP]
> **Not in the slides: name mangling.** Inside a class, an attribute named `__create_key` becomes `_Price__create_key`. It is not truly secret
> (a determined programmer can still type `Price._Price__create_key`), but nobody can use it **by mistake**, which is the point: the design makes the
> wrong usage hard and visible.

### Cars and motos: should we bind them?

`Car` and `Moto` have the same fields and most of the logic in common. We could use a hierarchy, but it would be justified more technically than by the
domain. **KISS**: as we will see, it is not a lot of code. Python also has **duck typing**: if it walks like a duck and quacks like a duck, then it must be a duck.

```python
@dataclass(frozen=True, order=True)
class Car:
    plate: Plate
    producer: Producer
    model: Model
    price: Price

    @property
    def type(self) -> str:
        return 'Car'

    @property
    def final_price(self) -> Price:
        if self.price <= Price.create(10000):
            return self.price.apply_discount(Discount(50))
        if self.price <= Price.create(20000):
            return self.price.apply_discount(Discount(100))
        return self.price
```

- `type` returns the kind of vehicle, useful to save to file (it could be derived from the class name, but... KISS).
- The price with discount is a **different** property, `final_price`: avoid ambiguities.
- Arithmetic comparisons work because `Price` is `@dataclass(order=True)`.

`Moto` is essentially the same, at least for now: **don't bind concepts that can stay separate**.

**Fixtures.** Objects used by many tests can be defined as fixtures: pass the name of the fixture as an argument to get the object it returns,
as many times as you like.

```python
@pytest.fixture
def cars():
    return [
        Car(Plate('AB123CD'), Producer('Car Producer'), Model('Model'), Price.create(100)),
        Car(Plate('AB123CE'), Producer('Car Producer'), Model('Model'), Price.create(11000)),
        Car(Plate('AB123CF'), Producer('Car Producer'), Model('Model'), Price.create(21000)),
    ]

def test_car_final_price(cars):
    assert cars[0].final_price == cars[0].price.apply_discount(Discount(50))
    assert cars[1].final_price == cars[1].price.apply_discount(Discount(100))
    assert cars[2].final_price == cars[2].price
```

### The Dealer

The `Dealer` must provide all the functionality, but **must not care about I/O**. Test all the functionality. TDD: test first, code later
(not a religion: it is also OK to test and code in parallel).

```python
@dataclass(frozen=True)
class Dealer:
    __vehicles: List[Union[Car, Moto]] = field(default_factory=list, init=False)

    def vehicles(self) -> int:
        return len(self.__vehicles)

    def vehicle(self, index: int) -> Union[Car, Moto]:
        validate('index', index, min_value=0, max_value=self.vehicles() - 1)
        return self.__vehicles[index]

    def add_car(self, car: Car) -> None:
        self.__vehicles.append(car)

    def add_moto(self, moto: Moto) -> None:
        self.__vehicles.append(moto)

    def remove_vehicle(self, index: int) -> None:
        validate('index', index, min_value=0, max_value=self.vehicles() - 1)
        del self.__vehicles[index]

    def sort_by_producer(self) -> None:
        self.__vehicles.sort(key=lambda x: x.producer)

    def sort_by_price(self) -> None:
        self.__vehicles.sort(key=lambda x: x.price)
```

`Union[Car, Moto]` means either a `Car` or a `Moto`; `default_factory` is a function called to create the default value; `init=False` excludes the field
from `__init__`. Nothing special in the rest.

### The menu, mocks and patches

The menu has its own domain primitives, `Description` and `Key` (built like `Plate`), and an `Entry`:

```python
@dataclass(frozen=True)
class Entry:
    key: Key
    description: Description
    on_selected: Callable[[], None] = field(default=lambda: None)
    is_exit: bool = field(default=False)

    def __post_init__(self):
        validate_dataclass(self)

    @staticmethod
    def create(key: str, description: str, on_selected: Callable[[], None] = lambda: None,
               is_exit: bool = False) -> 'Entry':
        return Entry(Key(key), Description(description), on_selected, is_exit)
```

**How can we check that `on_selected` works?** We have to simulate a call and check that the call actually happened. In Python this is usually done with a
**Mock**: an object on which essentially any method can be called; calls are recorded and can be checked later.

```python
def test_entry_on_selected():
    mocked_on_selected = Mock()
    entry = Entry(Key('1'), Description('Say hi'), on_selected=lambda: mocked_on_selected())
    entry.on_selected()                        # simulate a call to entry.on_selected
    mocked_on_selected.assert_called_once()    # check that the mocked method was called
```

The lambda uses the `__call__` dunder method of the mock (we could also use `mocked_on_selected.foo()`). We can also check the call arguments.

We can also mock **global objects**, declared somewhere else: for this we use **patches**. Here we want to print something when the entry is selected,
and verify that `print` was indeed called with the argument `'hi'`:

```python
@patch('builtins.print')                      # the name of the patched object
def test_entry_on_selected_print_something(mocked_print):
    entry = Entry(Key('1'), Description('Say hi'), on_selected=lambda: print('hi'))
    entry.on_selected()
    assert mocked_print.mock_calls == [call('hi')]
```

**The menu itself** uses the create-key pattern to have a private constructor, so that it can only be built by its builder:

```python
@dataclass(frozen=True)
class Menu:
    description: Description
    auto_select: Callable[[], None] = field(default=lambda: None)
    __entries: List[Entry] = field(default_factory=list, repr=False, init=False)
    __key2entry: Dict[Key, Entry] = field(default_factory=dict, repr=False, init=False)
    create_key: InitVar[Any] = field(default=None)

    def __post_init__(self, create_key: Any):
        validate('create_key', create_key, custom=Menu.Builder.is_valid_key)
        validate_dataclass(self)

    def _add_entry(self, value: Entry, create_key: Any) -> None:
        validate('create_key', create_key, custom=Menu.Builder.is_valid_key)
        validate('value.key', value.key, custom=lambda v: v not in self.__key2entry)
        self.__entries.append(value)
        self.__key2entry[value.key] = value

    def __select_from_input(self) -> bool:
        while True:
            try:
                line = input("? ")
                key = Key(line.strip())
                entry = self.__key2entry[key]
                entry.on_selected()
                return entry.is_exit
            except (KeyError, TypeError, ValueError):
                print('Invalid selection. Please, try again...')

    def run(self) -> None:
        while True:
            self.__print()                     # description, auto_select(), then all entries
            is_exit = self.__select_from_input()
            if is_exit:
                return

    @dataclass()
    class Builder:
        __menu: Optional['Menu']
        __create_key = object()

        def __init__(self, description: Description, auto_select: Callable[[], None] = lambda: None):
            self.__menu = Menu(description, auto_select, self.__create_key)

        @staticmethod
        def is_valid_key(key: Any) -> bool:
            return key == Menu.Builder.__create_key

        def with_entry(self, value: Entry) -> 'Menu.Builder':
            validate('menu', self.__menu)
            self.__menu._add_entry(value, self.__create_key)
            return self

        def build(self) -> 'Menu':
            validate('menu', self.__menu)
            validate('menu.entries', self.__menu._has_exit(), equals=True)
            res, self.__menu = self.__menu, None
            return res
```

- `auto_select` is a function called after printing the description (the app uses it to print the list of vehicles).
- `__entries` and `__key2entry` are excluded from `__init__`: their values are implicit.
- **The builder holds the key** and never releases it; it adds entries through a protected method (`_add_entry`) that only accepts the key.
- Fluent interface: `with_entry` returns the builder.
- `build` **cannot be called twice**, and the menu **must have an exit entry**.
- `__select_from_input` keeps asking until a valid choice is given.

**`side_effect`** lists the return values of a patched object, one per call. Here the user types `1`, then `0`:

```python
@patch('builtins.input', side_effect=['1', '0'])
@patch('builtins.print')
def test_menu_selection_call_on_selected(mocked_print, mocked_input):
    menu = Menu.Builder(Description('a description'))\
        .with_entry(Entry.create('1', 'first entry', on_selected=lambda: print('first entry selected')))\
        .with_entry(Entry.create('0', 'exit', is_exit=True))\
        .build()
    menu.run()
    mocked_print.assert_any_call('first entry selected')   # the first entry was selected
    mocked_input.assert_called()

@patch('builtins.input', side_effect=['-1', '0'])
@patch('builtins.print')
def test_menu_selection_on_wrong_key(mocked_print, mocked_input):
    # same menu...
    menu.run()
    mocked_print.assert_any_call('Invalid selection. Please, try again...')
```

Check for mistakes too: users will make many!

> [!TIP]
> **Not in the slides: the order of patch arguments.** Decorators are applied bottom-up, so the **innermost** `@patch` (the one closest to `def`) gives the
> **first** argument. Above, `@patch('builtins.print')` is closest, so the first argument is `mocked_print`, then `mocked_input`.

### The App

The app fixes the menu on construction and calls methods to handle events:

```python
class App:
    __filename = Path(__file__).parent.parent / 'default.csv'
    __delimiter = '\t'

    def __init__(self):
        self.__menu = Menu.Builder(Description('LaRusso Auto Group'),
                                   auto_select=lambda: self.__print_vehicles())\
            .with_entry(Entry.create('1', 'Add car', on_selected=lambda: self.__add_car()))\
            .with_entry(Entry.create('2', 'Add moto', on_selected=lambda: self.__add_moto()))\
            .with_entry(Entry.create('3', 'Remove vehicle', on_selected=lambda: self.__remove_vehicle()))\
            .with_entry(Entry.create('4', 'Sort by producer', on_selected=lambda: self.__sort_by_producer()))\
            .with_entry(Entry.create('5', 'Sort by price', on_selected=lambda: self.__sort_by_price()))\
            .with_entry(Entry.create('0', 'Exit', on_selected=lambda: print('Bye!'), is_exit=True))\
            .build()
        self.__dealer = Dealer()

    def __add_car(self) -> None:
        car = Car(*self.__read_vehicle())
        self.__dealer.add_car(car)
        self.__save()
        print('Car added!')

    @staticmethod
    def __read(prompt: str, builder: Callable) -> Any:
        while True:
            try:
                line = input(f'{prompt}: ')
                res = builder(line.strip())
                return res
            except (TypeError, ValueError, ValidationError) as e:
                print(e)

    def __read_vehicle(self) -> Tuple[Plate, Producer, Model, Price]:
        plate = self.__read('Plate', Plate)
        producer = self.__read('Producer', Producer)
        model = self.__read('Model', Model)
        price = self.__read('Price', Price.parse)
        return plate, producer, model, price

    def __run(self) -> None:
        try:
            self.__load()
        except ValueError as e:
            print(e)
            print('Continuing with an empty list of vehicles...')
        self.__menu.run()

    def run(self) -> None:
        try:
            self.__run()
        except:
            print('Panic error!', file=sys.stderr)
```

`__load` reads `default.csv` row by row, rebuilding every field through its domain primitive (`Plate(row[1])`, `Price.parse(row[4])`, ...),
so a corrupted file cannot put invalid data in the dealer; `__save` writes every vehicle after each change. `run` is the **global exception handler**:
it avoids leaking sensitive data by printing only "Panic error!". The ignition, `__main__.py`, uses a small trick to reach 100% coverage:

```python
def main(name: str):
    if name == '__main__':
        App().run()

main(__name__)
```

**Two lessons about testability:**

- private methods are good to make sure a class is not misused, but they can make testing harder: reaching all paths may be challenging;
- relying on global objects like `input()` and `print()` simplifies the code, but makes testing harder, with heavy use of mocks and patches.
  As a general rule, **avoid hardcoding global objects**: better to have a way to set them, with the global objects as default values.

**Testing the app.** We often need to bypass the check on the existence of `default.csv`, and to simulate reading it, so we define two fixtures.
A patch can also be applied as a context manager, and for `open()` there is `mock_open()` in `unittest.mock`:

```python
@pytest.fixture
def mock_path():
    Path.exists = Mock()
    Path.exists.return_value = True
    return Path

@pytest.fixture
def data():
    data = [
        ['Car', 'CA220NE', 'Fiat', 'Punto', '199.99'],
        ['Moto', 'CA220NI', 'Kawasaki', 'Ninja', '99.99'],
    ]
    return '\n'.join(['\t'.join(d) for d in data])

@patch('builtins.input', side_effect=['0'])
@patch('builtins.print')
def test_app_main(mocked_print, mocked_input):
    with patch.object(Path, 'exists') as mocked_path_exists:
        mocked_path_exists.return_value = False
        with patch('builtins.open', mock_open()):
            main('__main__')                                      # simulate the main execution
            mocked_print.assert_any_call('*** LaRusso Auto Group ***')
            mocked_print.assert_any_call('0:\tExit')
            mocked_print.assert_any_call('Bye!')

@patch('builtins.input', side_effect=['0'])
@patch('builtins.print')
def test_app_handles_corrupted_datafile(mocked_print, mocked_input, mock_path):
    with patch('builtins.open', mock_open(read_data='xyz')):
        App().run()
    mocked_print.assert_any_call('Continuing with an empty list of vehicles...')

@patch('builtins.input', side_effect=['1', 'ca220ne', 'CA220NE', 'Fiat', 'Punto', '199.99', '0'])
@patch('builtins.print')
def test_app_add_car_resists_to_wrong_plate(mocked_print, mocked_input, mock_path):
    with patch('builtins.open', mock_open()) as mocked_open:
        App().run()
    handle = mocked_open()
    handle.write.assert_called_once_with('Car\tCA220NE\tFiat\tPunto\t199.99\n')

@patch('builtins.input', side_effect=['0'])
@patch('builtins.print')
def test_app_global_exception_handler(mocked_print, mocked_input):
    with patch.object(Path, 'exists') as mocked_path_exists:
        mocked_path_exists.side_effect = Mock(side_effect=Exception('Test'))
        App().run()
    assert mocked_input.mock_calls == []
    assert list(filter(lambda x: 'Panic error!' in str(x), mocked_print.mock_calls))
```

Test the reading of the file, but also **stability on corrupted files**; test correct usage, but also **stability on mistakes** (a lowercase plate is
rejected and asked again); test the global handler by introducing an unexpected exception.

### Coverage and code inspection

**Coverage: the higher the better.** Every metric can be tricked: don't trick yourself. Use coverage analysis to find missing tests and unreachable code.
PyCharm also offers *Code | Inspect Code*, *Code | Code Cleanup* and *Code | Optimize Imports*: use them, and check every warning.

The lecture ends with three exercises in the same style (restaurant, music archive, medical office), in the [exercises](exercises/README.md#10-tui-exercises-with-tests).

---

# 4. Django REST Framework

## 4.1 Django REST Framework, part 1: a first REST API

These lectures are based on the online documentation and on *Django for APIs* by William S. Vincent (mainly chapters 5-9).
**Django** is a mature web framework (since 2005), written in Python, and proven to be solid (many tools and libraries, including a REST framework).
The lectures introduce the minimum needed to start, focusing on REST APIs (the back-end).

### Why REST APIs

Monolithic websites should stay in the past: why mix back-end (database models, URLs and views) and front-end (HTML templates, CSS, JavaScript)?
Modern websites **separate back-end and front-end**: Django for the back-end, only for data operations, and whatever front-end you like, even more
than one (browser, Android, iOS).

**HTTP** is a request-response protocol, often used for CRUD operations:

| CRUD | HTTP verb |
|---|---|
| Create | POST |
| Read | GET |
| Update | PUT / PATCH |
| Delete | DELETE |

**Endpoints** are URLs that expose and receive data (in JSON or XML):

```
https://www.mysite.com/api/users        # GET returns all users
https://www.mysite.com/api/users/<id>   # GET returns a single user
```

**REST** (REpresentational State Transfer) is an architecture for building APIs on top of HTTP. It is **stateless** (every request is independent of the
previous ones), relies on the HTTP verbs, and represents data in JSON or XML.

> [!TIP]
> **Not in the slides: a request and its response.**
>
> ```
> GET /api/v1/posts/1/ HTTP/1.1
> Host: 127.0.0.1:8000
>
> HTTP/1.1 200 OK
> Content-Type: application/json
>
> {"id": 1, "author": 1, "title": "First post", "body": "A test here", "created_at": "..."}
> ```
>
> Stateless means that this request carries everything the server needs (including, later, the authentication token): the server does not remember
> what you asked before.

### A Django project

The book creates a virtual environment, installs Django and runs `django-admin startproject blog_api`; PyCharm does all of it (the lecture uses pip).
The anatomy of the project:

- `settings.py`: the configuration of the project. It is a file of variable declarations, all UPPERCASE and considered constants.
  **Before deploying to production, something here must change.**
- `urls.py`: all the routes of the project.
- `templates/`: the HTML pages. For REST APIs they are not really needed (remove them if you want), but keep the static files for the admin site.
- `manage.py`: a script to run Django commands during development; we use it but usually don't modify it.
- `wsgi.py` and `asgi.py`: WSGI is the standard for Python web servers, ASGI for asynchronous servers.

> [!TIP]
> **Not in the slides: what must change before production.** In the example `settings.py`, `SECRET_KEY` is written in the file (and ends up in git),
> `DEBUG = True` shows detailed error pages with stack traces and settings to anyone (section 3.1!), and `ALLOWED_HOSTS` is empty. In production the
> secret key comes from an environment variable, `DEBUG` is `False`, and `ALLOWED_HOSTS` lists the real domain names.

**Start the project**: first migrate the database (`./manage.py migrate` creates or upgrades it), then start the server on localhost
(`./manage.py runserver`) and visit `http://127.0.0.1:8000/`. Logs and debug information go to STDERR.

**Create a superuser** from the command line (`./manage.py createsuperuser`). **Always avoid the username `admin`**, and generate passwords with a password
generator. **Change the default URL of the admin site**: in the example it becomes `admin-IMinewINTANG/` instead of `admin/`. Then log in with the
superuser credentials.

> [!TIP]
> **Not in the slides: why.** Bots scan the internet for `/admin/` pages and try `admin` with common passwords. An unusual URL and an unusual username
> do not make the site secure by themselves, but they remove it from the cheapest, most automated attacks (the "origin" check of section 2.2 is about
> the same asymmetry).

### Install Django REST Framework

Add the packages `djangorestframework` and `django-cors-headers` (the Pipfile is updated). The front-end will be on a different server, so requests must
be limited to known domains (CORS). In `settings.py`:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    # ... the other django.contrib apps
    'rest_framework',
    'corsheaders',
]

MIDDLEWARE = [
    # ...
    'corsheaders.middleware.CorsMiddleware',      # before CommonMiddleware
    'django.middleware.common.CommonMiddleware',
    # ...
]

CORS_ALLOWED_ORIGINS = [                          # whitelist of allowed origins
    'http://localhost:8000',
]
```

Permissions are set later (section 4.2).

> [!TIP]
> **Not in the slides: CORS.** Browsers apply the *same-origin policy*: JavaScript loaded from `http://localhost:8001` cannot read responses from
> `http://localhost:8000` (a different port is a different origin) unless the server says it is allowed, with CORS headers. The whitelist is what
> tells the browser which front-ends may call your API.

**Documentation** with `drf-yasg`: add it to the installed apps and set the schema class in `settings.py`:

```python
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.openapi.AutoSchema',
}
```

In `urls.py`, `get_schema_view(openapi.Info(...))` creates a schema view that provides human-readable documentation (shown as **Swagger** and **ReDoc**)
and machine-readable documentation (JSON). Details in the [drf-yasg repository](https://github.com/axnsan12/drf-yasg/).

### Apps and models

Apps are **isolated components**. `./manage.py startapp posts` (or, in PyCharm, *Tools | Run manage.py Task* and `startapp posts`) adds a new module:
`migrations/` stores the migration files that upgrade the database, `admin.py` adds content to the admin site, `apps.py` has app-specific configuration,
and `models.py`, `tests.py`, `views.py` hold the database model, tests and views. Install the app by adding `'posts.apps.PostsConfig'` to `INSTALLED_APPS`.

**The model.** A `Post` table with five fields: author, title, body, created_at, updated_at. Django provides a `User` model (a table): use
`get_user_model()` to avoid problems.

```python
from django.contrib.auth import get_user_model
from django.db import models

class Post(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)   # join to other tables
    title = models.CharField(max_length=50)                                  # small strings
    body = models.TextField()                                                # large amounts of text
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):                                                       # used by the admin site
        return self.title
```

Add `Post` to the admin site in `admin.py` with `admin.site.register(Post)`. Then `./manage.py makemigrations` makes the migration files (you may want
to put them in git) and `./manage.py migrate` upgrades the database. In the admin site, the app POSTS now has the object Posts: add a couple of posts,
try to make mistakes, and so on.

### Define the REST API

Three steps: `serializers.py` produces JSON, `views.py` applies logic to each endpoint, `urls.py` defines the routes.

```python
# posts/serializers.py
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'author', 'title', 'body', 'created_at')
        model = Post

# posts/views.py
class PostList(generics.ListCreateAPIView):              # list all posts
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostDetail(generics.RetrieveUpdateDestroyAPIView): # all operations on a single post
    queryset = Post.objects.all()
    serializer_class = PostSerializer

# posts/urls.py
urlpatterns = [
    path('<int:pk>/', PostDetail.as_view()),             # primary key to operate on a post
    path('', PostList.as_view()),                        # empty path to list all posts
]

# blog_api/urls.py
urlpatterns = [
    path('admin-IMinewINTANG/', admin.site.urls),
    # ... documentation
    path('api/v1/', include('posts.urls')),              # version number in the URL
]
```

With `ModelSerializer` it is enough to specify the model and the fields to expose.

> [!TIP]
> **Not in the slides: the serializer is a DTO.** The `fields` tuple is the "avoid exposing the domain" advice of section 2.3 in practice: `updated_at`
> exists in the model but is not part of the API. A serializer also validates incoming data before it reaches the model.

**The browsable API.** Visit `http://127.0.0.1:8000/api/v1/` for the list of posts and a form to add a new one, and `http://127.0.0.1:8000/api/v1/1/`
for the details of a post and a form to update it. The documentation is at `/swagger/`, `/redoc` and `/schema/`.

**Refactor with viewsets and routers.** A **viewset** can replace multiple views, and a **router** generates the URLs for a viewset:

```python
# posts/views.py
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

# posts/urls.py
router = SimpleRouter()
router.register('', PostViewSet, basename='posts')
urlpatterns = router.urls
```

---

## 4.2 Django REST Framework, part 2: authentication, authorization, tests

### Consuming the API

**A JavaScript example.** Create `index.html` in an empty directory; it fetches the posts and shows their titles in a list:

```html
<script>
  fetch('http://localhost:8000/api/v1/')
    .then(response => response.json())
    .then(data => {
      let ul = document.createElement('ul');
      data.forEach(record => {
        let li = document.createElement('li');
        li.innerHTML = record.title;
        ul.appendChild(li);
      });
      let content = document.getElementById('content');
      content.innerHTML = '';
      content.appendChild(ul);
    });
</script>
<h1>Posts</h1>
<div id='content'>Loading content...</div>
```

Add `http://localhost:8001` to the CORS whitelist, start the front-end server with `python3 -m http.server 8001`, and visit `http://localhost:8001`:
"Loading content..." becomes the list of posts. If it doesn't work, use a private tab or clear the browser cache. **Plain JavaScript is likely the worst option**:
prefer a library or framework (Svelte, Vue.js, jQuery, React, Angular), or make the requests from Python or Java and consume the API in a TUI or GUI.

> [!WARNING]
> **Not in the slides: look at `li.innerHTML = record.title`.** The slides mark this line with a warning sign. `innerHTML` interprets the string as HTML,
> so a post titled `<img src=x onerror=alert(1)>` runs JavaScript in every visitor's browser: the XSS of section 1.1. Use `li.textContent = record.title`,
> which treats it as plain text. The validators added at the end of this lecture reduce the risk on the server side too.

**A Python example**, a small TUI:

```python
import requests

api_server = 'http://localhost:8000/api/v1'

def fetch_posts():
    res = requests.get(url=f'{api_server}/')
    if res.status_code != 200:
        return None
    return res.json()

def show_posts(posts):
    def sep():
        print('-' * 60)
    fmt = '{:4}\t{:50}'
    print()
    sep()
    print('ALL POSTS FROM THE BLOG')
    sep()
    print(fmt.format('ID', 'TITLE'))
    sep()
    for post in posts:
        print(fmt.format(post['id'], post['title']))
    sep()
    print()

def main():
    welcome()
    posts = fetch_posts()
    if posts is None:
        error_message()
    show_posts(posts)
    goodbye()
```

### Authentication

**Session-based authentication.** The client sends the initial credentials; the server stores in the session object that the user is authenticated;
the client stores the **session ID** (usually in a cookie flagged `HttpOnly`) and sends it with every request. After logout, the session is destroyed on
both sides. It is kept for the browsable API, and because it's simple.

**Token-based authentication.** The client sends the initial credentials; the server generates a unique **token**; the client stores it (for example in an
environment variable of the front-end, if it is used as an API key, like those of the Google Maps API) and sends it with each request.
By default, Django generates a token for each user and stores it in the database. More sophisticated approaches, based on **JWT** and **OAuth2**, don't need to store anything.

> [!TIP]
> **Not in the slides: `HttpOnly`, and the token in practice.** A cookie flagged `HttpOnly` cannot be read by JavaScript, so even an XSS cannot steal the session ID.
> With DRF's token authentication, the client adds a header to each request: `Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b`.
> A JWT instead contains the user's identity and an expiry date, signed by the server: the server only checks the signature, without a database lookup.

**What we need:**

- URLs for session-based authentication;
- token-based authentication: `rest_framework.authtoken`;
- login, logout and password reset endpoints: `dj-rest-auth` (must be installed);
- registration endpoints: `django-allauth` (must be installed) and `requests`; `django.contrib.sites`, needed by allauth, handles multiple sites in the same project.

```python
INSTALLED_APPS = [
    # ...
    'django.contrib.sites',
    'rest_framework',
    'rest_framework.authtoken',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'dj_rest_auth',
    'dj_rest_auth.registration',
    'corsheaders',
    'drf_yasg',
    'posts.apps.PostsConfig',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [              # support session and token authentication
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    # ...
}

ACCOUNT_EMAIL_VERIFICATION = 'none'                  # disabled for simplicity
SITE_ID = 1                                          # only one site

# blog_api/urls.py
urlpatterns = [
    path('admin-IMinewINTANG/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),                           # session auth for the browsable API
    # ... documentation
    path('api/v1/posts/', include('posts.urls')),                                # prefix to avoid ambiguities
    path('api/v1/auth/', include('dj_rest_auth.urls')),                          # token auth, part of the REST API
    path('api/v1/auth/registration/', include('dj_rest_auth.registration.urls')),
]
```

Migrate the database and start the project: the browsable API now supports login and logout. The token-based endpoints are
`/api/v1/auth/login/`, `/logout/`, `/password/reset/`, `/password/reset/confirm/` and `/password/change/`.

### Authorization

**Authentication** deals with **who you are**; **authorization** with **what you can do**. The plan: restrict the default permission to admin only,
authorize with a per-view or per-object policy, and take advantage of Django's permissions and groups.

```python
REST_FRAMEWORK = {
    # ...
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAdminUser',
    ],
}
```

Only the admin is authorized: **the default policy must be restrictive**, so that no unauthorized usage of the API is left open by accident.

**Different permissions on views.** With `permission_classes = [permissions.IsAuthenticatedOrReadOnly]` on the viewset, everyone can read posts but only
authenticated users can change them: in the browsable API, an anonymous user sees no delete button and no form.

**Restrict changes to authors, and reads to authenticated users**, with a permission class written by us in `posts/permissions.py`:

```python
class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):          # permission on the view?
        return True                                   # the default implementation, can be omitted

    def has_object_permission(self, request, view, obj):   # permission on this object?
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user

class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthorOrReadOnly, IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
```

**Be aware of what we are doing: we are just experimenting.** In a real setting, the author of a post would be fixed to `request.user`, and the POST view
would use a different serializer, without the `author` field.

> [!TIP]
> **Not in the slides: `SAFE_METHODS`, and why the author field is a problem.** `SAFE_METHODS` is `('GET', 'HEAD', 'OPTIONS')`: the methods that only read.
> As written, the serializer accepts `author` from the client, so an authenticated user can create a post **in someone else's name** by sending
> `{"author": 2, ...}`. `IsAuthorOrReadOnly` only protects existing objects. The fix is to make `author` read-only in the serializer and set it in the view
> (`serializer.save(author=self.request.user)`).

**Users can only read their own posts?** Yes: the view must **filter the objects in the queryset**, by defining `get_queryset`. Add a new view (or, in a real
setting, modify the existing one), and URLs for it:

```python
class PostByAuthorViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

router.register('by-author', PostByAuthorViewSet, basename='posts-by-author')
router.register('', PostViewSet, basename='posts')
```

**Role-based authorization.** Django provides a rich set of permissions for users and groups. In the admin site, create a `post_editors` group with all the
permissions on posts, and add a user to it; add another user with only the permission *posts | post | Can view post*. Then authorize views to members
of specific groups: **the group represents a role**.

```python
class IsPostEditor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='post_editors').exists()

class PostEditorViewSet(viewsets.ModelViewSet):
    permission_classes = [IsPostEditor]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

router.register('editor', PostEditorViewSet, basename='post-editors')
```

**Permission-based authorization.** Authorize views to users with specific permissions (users inherit the permissions of their groups):

```python
method2perm = {
    'POST': 'add', 'PUT': 'change', 'PATCH': 'change', 'DELETE': 'delete',
    'GET': 'view', 'HEAD': 'view', 'OPTIONS': 'view',
}

class IsPermittedOnPost(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method not in method2perm:
            return False
        return request.user.has_perm(f'posts.{method2perm[request.method]}_post')
```

In the final example code the main viewset combines permissions with `|` and `&`:
`permission_classes = [IsAdminUser | (IsAuthorOrReadOnly & IsAuthenticated)]`.

> [!TIP]
> **Not in the slides: roles vs permissions.** Checking the group name (`post_editors`) ties the code to a role: if tomorrow "moderators" must edit posts too,
> the code changes. Checking the permission (`posts.change_post`) ties the code to an action; who holds that permission is decided in the admin site,
> by giving it to groups or users, without touching the code.

### Tests

Test first, code later: we have a lot of code and no tests, only because we were learning Django. Time to fix it; from now on, prefer a TDD approach.

**Setup.** Install `pytest-django` and `mixer`, set pytest as the test tool with a run configuration on the path `tests`, and create test files for `models.py`
and `urls.py` (testing `views.py` is possible but more tedious, and somehow implicit in `test_urls.py`). Since tests live in `tests/`, `tests.py` in the app
can be removed. Add `pytest.ini` in the root of the project, pointing to the settings:

```ini
[pytest]
DJANGO_SETTINGS_MODULE = blog_api.settings
```

**The first test.** `db` is a fixture that gives access to the temporary database used by the tests; `mixer` creates objects from our models with random values
for the fields not provided; `full_clean()` validates an object of the model.

```python
def test_post_title_of_length_51_raises_exception(db):
    post = mixer.blend('posts.post', title='A'*51)
    with pytest.raises(ValidationError) as err:
        post.full_clean()
    assert 'at most 50 characters' in '\n'.join(err.value.messages)
```

We can also check the message of the exception, but the lecturer would not encourage it. This test passes: it should have been written before the code!

**A failing test, then the fix.** A title must be capitalized; the test fails because currently any text of at most 50 characters is allowed.

```python
def test_post_title_not_capitalized_raises_exception(db):
    post = mixer.blend('posts.post', title='my wrong title')
    with pytest.raises(ValidationError):
        post.full_clean()
```

Validators can be defined as functions, in `posts/validators.py`, and each field of the model takes a list of validators; Django also provides many common ones:

```python
# posts/validators.py
def validate_title(value: str) -> None:
    if len(value) == 0:
        raise ValidationError('Title must not be empty')
    if not value[0].isupper():
        raise ValidationError('Title must be capitalized')

# posts/models.py
class Post(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=50, validators=[validate_title])
    body = models.TextField(validators=[RegexValidator(r'^[\w\s.:;,\'"]*$')])
    # ...
```

> [!TIP]
> **Not in the slides: the model validators are Django's domain primitives.** `max_length=50`, `validate_title` and the regex on `body` are the size, lexical
> and syntax checks of section 2.2, in the place where Django applies them for every serializer and form. Note that `mixer.blend` saves the object without
> validating it: that is why the tests call `full_clean()` explicitly.

**Test the URLs, mainly for permissions.** Our own fixtures can populate the database; `APIClient` simulates an API consumer; `get()` performs a GET request;
the arguments for the URL go in a dictionary.

```python
@pytest.fixture()
def posts(db):
    return [mixer.blend('posts.post') for _ in range(3)]

def get_client(user=None):
    res = APIClient()
    if user is not None:
        res.force_login(user)
    return res

def test_post_anon_user_get_nothing():
    path = reverse('posts-list')
    client = get_client()
    response = client.get(path)
    assert response.status_code == HTTP_403_FORBIDDEN

def test_post_retrieve_a_single_post(posts):
    path = reverse('posts-detail', kwargs={'pk': posts[0].pk})
    client = get_client(posts[0].author)
    response = client.get(path)
    assert response.status_code == HTTP_200_OK
    obj = parse(response)
    assert obj['title'] == posts[0].title

def test_post_add_a_new_post(posts, admin_user):
    path = reverse('posts-list')
    client = get_client(admin_user)
    response = client.post(path, data={'author': posts[0].author.pk, 'title': 'Foo', 'body': 'bar'})
    assert response.status_code == HTTP_201_CREATED
```

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
- **Immutability** fixes availability (no locks needed to share) and integrity (nobody can change what you handed out). `synchronized` is useless if the object can be modified from outside.
- **Fail fast by contracts**: check preconditions at the start of public methods; `NullPointerException` for unexpected `null`, `IllegalArgumentException` for bad arguments (`notNull`, `isTrue`, `matchesPattern`, `inclusiveBetween`), `IllegalStateException` for bad state (`validState`). No invalid data in exception messages.
- **Validation order**: origin, size, lexical content, syntax, semantics (cheapest first). Semantics belongs to entities, everything else to domain primitives.
- **Domain primitive**: an immutable value object that exists only if valid; use them for arguments, return values and fields. Restrict definitions, never widen them (introduce a new term). Don't expose the domain in APIs: use DTOs.
- **Read-once objects** for sensitive data: `final`, not serializable, value forgotten after the first read, masked `toString()`.
- **Entities**: consistent on creation (constructor with all mandatory fields, private no-arg constructor only for the ORM); **builder** for complex creation (checks invariants in `build()`, usable once); no setters, only business methods (`markPaid()`); never share mutable fields (return copies or read-only views, prefer lists of immutable objects).
- **Complex state**: partially immutable entities (`final` fields), **state objects** (explicit, testable state), **snapshots** (immutable views for multi-thread), **entity relay** (one entity per life phase, at points of no return).
- **Failures**: separate business and technical exceptions (typed business exceptions, a global handler for technical ones), never sensitive data in exceptions, prefer **Result objects** for expected failures, **circuit breakers** and queues for availability, never repair bad input and never echo it.
- **TDD**: test first, code later; minimum code to pass; one failing test at a time; refactor only with tests; a new test should fail; a bug is a missing test; test boundaries; use coverage to find missing tests.
- **Python tests**: dataclasses (`frozen=True`) + typeguard + valid8 for domain primitives; the create-key trick for private constructors; fixtures for shared objects; `Mock` records calls; `@patch` replaces globals like `input` and `print` (`side_effect` for successive inputs); `mock_open` for files.
- **DRF**: models + serializers (DTOs) + viewsets + routers; CORS whitelist; documentation with drf-yasg; no `admin` username, a custom admin URL, `DEBUG = False` in production.
- **Auth**: session (cookie `HttpOnly`) or token authentication; default permission **restrictive** (`IsAdminUser`), then per-view, per-object (`has_object_permission`), per-queryset (`get_queryset`), role-based (groups) or permission-based (`has_perm`).
- **Django tests**: `pytest-django` with the `db` fixture, `mixer` for random objects, `full_clean()` to run validators, `APIClient` to test URLs and permissions.
