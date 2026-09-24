# Cryptography: summary

Based on the lecture notes by J. van Bon. The numbering follows the notes, so you can
compare the two side by side. Every proof follows the same steps as the notes; where a step
is not obvious, there is an extra explanation or a worked example.

**Progress:** sections 1.1, 1.2 and 1.3 are covered; the rest of the syllabus is still to do.

## Contents

1. Algebra
   - [1.1 Basic notions](#11-basic-notions)
   - [1.2 The ring Z/mZ](#12-the-ring-zmz)
   - [1.3 Direct products and homomorphisms](#13-direct-products-and-homomorphisms)
   - 1.4 Groups _(to do)_
   - 1.5 Polynomial rings _(to do)_
   - 1.6 Finite fields _(to do)_
   - 1.7 Linear algebra revisited _(to do)_
   - 1.8 Prime numbers _(to do)_
2. Cryptography
   - 2.1 Basic notions _(to do)_
   - 2.2 AES _(to do)_
   - 2.3 RSA _(to do)_
   - 2.4 ElGamal _(to do)_
   - 2.5 Elliptic curves _(to do)_
3. [Cheat sheet](#cheat-sheet)

---

# 1. Algebra

The first part builds, one step at a time, the tools needed for the cryptosystems of part 2.
Sections 1.1 to 1.3 lead to one goal: understanding which elements are invertible modulo $n$,
and how many there are. This is exactly what RSA relies on.

## 1.1 Basic notions

### Binary operations

A **binary operation** on a set $X$ is a map $\ast : X \times X \to X$: it takes two elements of $X$ and
returns one element of $X$. We write $a \ast b$ for the result. It is

- **associative** if $a \ast (b \ast c) = (a \ast b) \ast c$ for all $a, b, c \in X$;
- **commutative** if $a \ast b = b \ast a$ for all $a, b \in X$.

Addition and multiplication on $\mathbb{Z}$, $\mathbb{Q}$ and $\mathbb{R}$ are both associative and commutative.
Two examples where commutativity fails:

- **Composition of functions.** On the set of functions $f : A \to A$, $(f \circ g)(a) = f(g(a))$ is associative,
  but in general $f \circ g \neq g \circ f$. For instance, on $\mathbb{R}$ with $f(x) = x + 1$ and $g(x) = 2x$:
  $f(g(x)) = 2x + 1$, while $g(f(x)) = 2x + 2$.
- **Matrix product.** On $M_n(\mathbb{R})$, the $n \times n$ real matrices, the product is associative
  but not commutative when $n \ge 2$. The sum of matrices is both.

### Semigroups and monoids

A **semigroup** $(H, \ast)$ is a set with an *associative* binary operation. It is commutative if $\ast$ is,
and finite if $H$ is finite.

Examples: $(\mathbb{Z}, +)$, $(\mathbb{Z}, \cdot)$, $(M_n(\mathbb{R}), +)$, $(M_n(\mathbb{R}), \cdot)$, and
$(n\mathbb{Z}, +)$, $(n\mathbb{Z}, \cdot)$, where $n\mathbb{Z} = \lbrace na : a \in \mathbb{Z} \rbrace$ are the multiples of $n$.

An element $e \in H$ is **neutral** if $a \ast e = e \ast a = a$ for every $a \in H$.
If $\ast$ is commutative, checking $a \ast e = a$ is enough, because then $e \ast a = a \ast e = a$ too.

| Semigroup | Neutral element |
|---|---|
| $(\mathbb{Z}, +)$ | $0$ |
| $(\mathbb{Z}, \cdot)$ | $1$ |
| $(M_n(\mathbb{R}), +)$ | the zero matrix $0_n$ |
| $(M_n(\mathbb{R}), \cdot)$ | the identity matrix $I_n$ |
| $(n\mathbb{Z}, +)$ | $0$ |
| $(n\mathbb{Z}, \cdot)$ with $n \ge 2$ | none |

*Why does $(n\mathbb{Z}, \cdot)$ have no neutral element?* Take $n = 2$. A neutral $e$ would need $e \cdot 2 = 2$,
so $e = 1$. But $1$ is not even, so $1 \notin 2\mathbb{Z}$.

**Lemma 1.1.1.** A semigroup has at most one neutral element.

*Proof.* Let $e_1$ and $e_2$ both be neutral. Compute $e_1 \ast e_2$ in two ways:
since $e_2$ is neutral, $e_1 \ast e_2 = e_1$; since $e_1$ is neutral, $e_1 \ast e_2 = e_2$. So $e_1 = e_2$. ∎

A **monoid** $(H, \ast, e)$ is a semigroup with neutral element $e$. When there is no ambiguity we just write $H$.
Examples: $(\mathbb{Z}, +, 0)$ and $(\mathbb{Z}, \cdot, 1)$ are commutative monoids;
$(M_n(\mathbb{R}), \cdot, I_n)$ is a non-commutative monoid for $n \ge 2$.

### Invertible elements

In a monoid $(H, \ast, e)$, an element $a$ is **invertible** if there is $b \in H$ with $a \ast b = b \ast a = e$.

| Monoid | Invertible elements |
|---|---|
| $(\mathbb{R}, +, 0)$ | all ($a$ has inverse $-a$) |
| $(\mathbb{R}, \cdot, 1)$ | all except $0$ ($a$ has inverse $1/a$) |
| $(\mathbb{Z}, +, 0)$ | all |
| $(\mathbb{Z}, \cdot, 1)$ | only $1$ and $-1$ (for example $1/2 \notin \mathbb{Z}$) |
| $(M_n(\mathbb{R}), \cdot, I_n)$ | the invertible matrices (determinant $\neq 0$) |

**Lemma 1.1.2 (cancellation law).** Let $a$ be invertible. If $a \ast b = a \ast c$, then $b = c$.

*Proof.* Let $u$ be such that $a \ast u = u \ast a = e$. Then

$$b = e \ast b = (u \ast a) \ast b = u \ast (a \ast b) = u \ast (a \ast c) = (u \ast a) \ast c = e \ast c = c.$$

The idea is to "multiply by $u$ on the left" on both sides; associativity lets us move the brackets. ∎

> [!WARNING]
> The hypothesis "$a$ invertible" is essential. Modulo 30: $5 \cdot 6 = 30 \equiv 0$ and $5 \cdot 12 = 60 \equiv 0$,
> so $5 \cdot 6 \equiv 5 \cdot 12$. Yet $6 \not\equiv 12$: we cannot cancel the 5, because 5 has no inverse modulo 30.

**Lemma 1.1.3.** An invertible element has exactly one inverse.

*Proof.* Let $b_1$ and $b_2$ both be inverses of $a$. Then $a \ast b_1 = e = a \ast b_2$.
Since $a$ is invertible, the cancellation law gives $b_1 = b_2$. ∎

So we can speak of *the* inverse of $a$, written $a^{-1}$.

**Lemma 1.1.4.** In a monoid $(H, \ast, e)$, for $a, b \in H$:

1. $e$ is invertible;
2. if $a$ and $b$ are invertible, then $a \ast b$ is invertible, with inverse $b^{-1} \ast a^{-1}$;
3. if $a$ is invertible, then $a^{-1}$ is invertible, with inverse $a$;
4. the set $H^\ast = \lbrace a \in H : a \text{ invertible} \rbrace$, with the same operation, is a monoid in which every element is invertible.

*Proof.*

1. $e \ast e = e$, so $e$ is its own inverse: $e^{-1} = e$.
2. We check that $b^{-1} \ast a^{-1}$ works as an inverse, on both sides, moving brackets with associativity:

   $$(a \ast b) \ast (b^{-1} \ast a^{-1}) = a \ast (b \ast b^{-1}) \ast a^{-1} = a \ast e \ast a^{-1} = a \ast a^{-1} = e,$$

   $$(b^{-1} \ast a^{-1}) \ast (a \ast b) = b^{-1} \ast (a^{-1} \ast a) \ast b = b^{-1} \ast e \ast b = b^{-1} \ast b = e.$$

   The order is reversed, like putting on socks and then shoes: to undo it, you take off the shoes first.
   With matrices, $(AB)^{-1} = B^{-1}A^{-1}$, and in general $A^{-1}B^{-1}$ would be wrong.
3. The equalities $a \ast a^{-1} = e$ and $a^{-1} \ast a = e$ say that $a$ is an inverse of $a^{-1}$. So $(a^{-1})^{-1} = a$.
4. We need three things.
   - $\ast$ is an operation *on $H^\ast$*: if $u, v \in H^\ast$, then $u \ast v \in H^\ast$ by point 2.
   - The neutral element belongs to $H^\ast$: by point 1.
   - Every $u \in H^\ast$ is invertible *inside* $H^\ast$: its inverse $u^{-1}$ is in $H^\ast$ by point 3. ∎

A **group** is a monoid in which every element is invertible; a commutative group is also called **Abelian**.

- $(\mathbb{Z}, +, 0)$ is an Abelian group; $(\mathbb{Z}, \cdot, 1)$ is not a group (2 has no inverse).
- By point 4 above, **for any monoid $H$, $(H^\ast, \ast, e)$ is a group.**
- $(M_n(\mathbb{R})^\ast, \cdot, I_n)$, the invertible matrices, is a non-Abelian group for $n \ge 2$.
- $\mathbb{Z}^\ast = \lbrace 1, -1 \rbrace$ is an Abelian group with 2 elements. Its multiplication table:

| $\cdot$ | $1$ | $-1$ |
|---|---|---|
| $1$ | $1$ | $-1$ |
| $-1$ | $-1$ | $1$ |

### Rings

A **ring** $(R, +, \cdot)$ is a set with two binary operations such that

- $(R, +)$ is an Abelian group;
- $(R, \cdot)$ is a semigroup;
- **distributivity** holds on both sides: $u(v + w) = uv + uw$ and $(u + v)w = uw + vw$.

The ring is **commutative** if $\cdot$ is commutative, and it is a **ring with identity** if $(R, \cdot)$ has a neutral element.

| Ring | Commutative | Identity |
|---|---|---|
| $\mathbb{Z}$, $\mathbb{R}$ | yes | yes ($1$) |
| $M_n(\mathbb{R})$, $n \ge 2$ | no | yes ($I_n$) |
| $6\mathbb{Z}$ | yes | no (same reason as $2\mathbb{Z}$ above) |

Notation in a ring:

- $0$ is the neutral element of $+$ (the **zero**); $-u$ is the inverse of $u$ for $+$ (the **opposite**);
- $1$ is the neutral element of $\cdot$ (the **identity**), if it exists;
- "invertible" always refers to **multiplication**, and $u^{-1}$ is the multiplicative inverse;
- $R^\ast = \lbrace u \in R : u \text{ invertible} \rbrace$. By Lemma 1.1.4, $(R^\ast, \cdot, 1)$ is a group.

**Lemma 1.1.5.** In a ring with identity, for all $a, b$:

1. $a \cdot 0 = 0 \cdot a = 0$;
2. $a \cdot (-b) = -(a \cdot b) = (-a) \cdot b$;
3. $(-a) \cdot (-b) = a \cdot b$;
4. $(-1) \cdot a = -a$.

These are the familiar rules of arithmetic. The point is that they follow from the axioms alone,
so they hold in *every* ring, including $\mathbb{Z}/m\mathbb{Z}$ and matrix rings.

*Proof.* Remember that $(R, +, 0)$ is a commutative group, so the cancellation law holds for $+$.

1. Since $0 + 0 = 0$, distributivity gives $a \cdot 0 + a \cdot 0 = a \cdot (0 + 0) = a \cdot 0 = a \cdot 0 + 0$.
   Cancelling $a \cdot 0$ on the left of both sides (cancellation law for $+$): $a \cdot 0 = 0$. The same works for $0 \cdot a$.
2. By point 1, $a \cdot (b + (-b)) = a \cdot 0 = 0$. By distributivity the left side is $a \cdot b + a \cdot (-b)$.
   So $a \cdot b + a \cdot (-b) = 0$: this says that $a \cdot (-b)$ is the opposite of $a \cdot b$, that is $a \cdot (-b) = -(a \cdot b)$.
   In the same way, $(-a) \cdot b = -(a \cdot b)$.
3. Apply point 2 twice: $(-a) \cdot (-b) = -((-a) \cdot b) = -(-(a \cdot b))$.
   The opposite of the opposite of $x$ is $x$ itself (Lemma 1.1.4, point 3, applied to $+$). So $(-a) \cdot (-b) = a \cdot b$.
4. $a + (-1) \cdot a = 1 \cdot a + (-1) \cdot a = (1 + (-1)) \cdot a = 0 \cdot a = 0$.
   So $(-1) \cdot a$ is the opposite of $a$. ∎

**Remark (is $1 \neq 0$?).** The axioms do not say so. If $1 = 0$, then for every $u$:
$u = u \cdot 1 = u \cdot 0 = 0$ (using point 1). So $R = \lbrace 0 \rbrace$, the trivial ring with a single element.
This is why the definition of a field explicitly requires $1 \neq 0$.

From now on, the course mainly deals with **commutative rings with identity**.

### Zero divisors

Let $R$ be a commutative ring with identity. An element $a$ is a **zero divisor** if $a \neq 0$ and
there is $b \neq 0$ with $a \cdot b = 0$.

In $\mathbb{R}$ and $\mathbb{Z}$ there are no zero divisors (a product of nonzero numbers is never zero).
In $\mathbb{Z}/12\mathbb{Z}$ there are: $3 \cdot 4 = 12 \equiv 0$, with $3 \not\equiv 0$ and $4 \not\equiv 0$.

**Lemma 1.1.6.** A zero divisor is never invertible.

*Proof.* Let $a$ be a zero divisor, with $b \neq 0$ and $a \cdot b = 0$. Suppose $a$ has an inverse $a^{-1}$. Then

$$0 = a^{-1} \cdot 0 = a^{-1} \cdot (a \cdot b) = (a^{-1} \cdot a) \cdot b = 1 \cdot b = b,$$

which contradicts $b \neq 0$. ∎

The converse is false in $\mathbb{Z}$: $2$ is neither invertible nor a zero divisor.
In a **finite** ring, though, there is no third option:

**Theorem 1.1.7.** Let $R$ be a finite commutative ring with identity, and $a \in R$ with $a \neq 0$.
Then $a$ is invertible or a zero divisor.

*Proof.* Let $n = \lvert R \rvert$, and write $a^s$ for $a \cdot a \cdots a$ ($s$ times), with $a^0 = 1$.

**Step 1: two powers coincide.** The list $1, a, a^2, \dots, a^n$ has $n + 1$ entries, all in $R$, which has only $n$ elements.
By the pigeonhole principle, two of them are equal: $a^i = a^j$ for some $0 \le i < j \le n$.
Let $r$ be the **smallest** exponent for which this happens, so $a^r = a^{r+d}$ for some $d > 0$.

**Step 2: a product equal to zero.** From $a^{r+d} = a^r$ we get $a^{r+d} - a^r = 0$, and factoring out $a^r$:

$$a^r \cdot (a^d - 1) = 0.$$

**Step 3a: if $r = 0$, then $a$ is invertible.** Then $a^r = 1$, and the equation becomes $a^d - 1 = 0$, that is $a^d = 1$.
Since $d > 0$ we can write $a^d = a \cdot a^{d-1}$, so $a \cdot a^{d-1} = 1$: the inverse of $a$ is $a^{d-1}$.

**Step 3b: if $r > 0$, then $a$ is a zero divisor.** Because $r$ is the smallest exponent where a repetition starts,
the powers one step earlier are still different: $a^{r-1} \neq a^{r-1+d}$. So

$$a^{r-1} \cdot (a^d - 1) = a^{r-1+d} - a^{r-1} \neq 0.$$

Multiplying this nonzero element by $a$ gives $a \cdot a^{r-1}(a^d - 1) = a^r(a^d - 1) = 0$ (Step 2).
So $a$ times a nonzero element is $0$: $a$ is a zero divisor, with $b = a^{r-1}(a^d - 1)$. ∎

> [!NOTE]
> **Two examples in $\mathbb{Z}/12\mathbb{Z}$.**
>
> - $a = 5$: the powers are $1, 5, 25 \equiv 1$. The first repetition is $a^0 = a^2$, so $r = 0$ and $d = 2$.
>   By Step 3a, $5^2 = 1$ and the inverse of 5 is $5^{d-1} = 5$. Indeed $5 \cdot 5 = 25 \equiv 1$.
> - $a = 2$: the powers are $1, 2, 4, 8, 16 \equiv 4$. The first repetition is $a^2 = a^4$, so $r = 2$ and $d = 2$.
>   By Step 3b, $b = a^{r-1}(a^d - 1) = 2 \cdot (4 - 1) = 6 \neq 0$, and $a \cdot b = 2 \cdot 6 = 12 \equiv 0$.
>   So 2 is a zero divisor.

### Fields

A **field** is a commutative ring with identity in which $1 \neq 0$ and every element different from $0$ is invertible.
$\mathbb{Q}$, $\mathbb{R}$ and $\mathbb{C}$ are fields; $\mathbb{Z}$ is not (2 is not invertible).
By Lemma 1.1.6, a field has no zero divisors.

---

## 1.2 The ring Z/mZ

### Congruences and residue classes

Fix $m \ge 2$. For $a, b \in \mathbb{Z}$, we say $a$ is **congruent to $b$ modulo $m$**, written $a \equiv b \pmod m$,
if $m$ divides $a - b$. For example $17 \equiv 5 \pmod{12}$, because $17 - 5 = 12$.

Congruence is an equivalence relation. The class of $a$, called its **residue class** modulo $m$, is

$$[a]_m = \lbrace b \in \mathbb{Z} : b \equiv a \pmod m \rbrace = \lbrace a + km : k \in \mathbb{Z} \rbrace.$$

For example $[5]_{12} = \lbrace \dots, -7, 5, 17, 29, \dots \rbrace$. Any element of a class is a
**representative** of it: $[5]_{12} = [17]_{12} = [-7]_{12}$.
The set of all classes is $\mathbb{Z}/m\mathbb{Z} = \lbrace [a]_m : a \in \mathbb{Z} \rbrace$. For example
$\mathbb{Z}/2\mathbb{Z} = \lbrace [0]_2, [1]_2 \rbrace$ and $\mathbb{Z}/3\mathbb{Z} = \lbrace [0]_3, [1]_3, [2]_3 \rbrace$.
In general $\mathbb{Z}/m\mathbb{Z}$ has $m$ elements, $[0]_m, \dots, [m-1]_m$ (the possible remainders of division by $m$).

**Lemma 1.2.1.** If $a \equiv c$ and $b \equiv d \pmod m$, then $ab \equiv cd$ and $a + b \equiv c + d \pmod m$.
The notes leave the proof as an exercise: see [Exercise 1](exercises/algebra.md#exercise-1).

*Why this matters.* We want to define $[a]_m + [b]_m = [a + b]_m$ and $[a]_m \cdot [b]_m = [ab]_m$.
A class has many representatives, so we must be sure the result does not depend on which ones we pick.
Example modulo 12: $[5] = [17]$ and $[3] = [15]$. Using $5$ and $3$: $5 \cdot 3 = 15$, so the product is $[15] = [3]$.
Using $17$ and $15$: $17 \cdot 15 = 255 = 21 \cdot 12 + 3$, so the product is again $[3]$. Lemma 1.2.1 guarantees this always happens:
the operations are **well defined**.

Both operations are associative and commutative, $[0]_m$ is neutral for $+$ and $(\mathbb{Z}/m\mathbb{Z}, +, [0]_m)$ is an Abelian group,
$[1]_m$ is neutral for $\cdot$, and distributivity holds (all of these are inherited from $\mathbb{Z}$). So:

> $(\mathbb{Z}/m\mathbb{Z}, +, \cdot)$ is a **commutative ring with identity**.

### Invertible elements and zero divisors

This is the key result of the section: it tells us, just from a gcd, what kind of element $[a]_m$ is.

**Lemma 1.2.2.** Let $a \in \mathbb{Z}$. In $\mathbb{Z}/m\mathbb{Z}$:

1. $[a]_m = [0]_m$ if and only if $\gcd(a, m) = m$;
2. $[a]_m$ is a zero divisor if and only if $1 < \gcd(a, m) < m$;
3. $[a]_m$ is invertible if and only if $\gcd(a, m) = 1$.

*Proof.* Let $d = \gcd(a, m)$; since $d$ divides $m$, we have $1 \le d \le m$.

**Point 1.** $d = m$ means that $m$ divides $a$, which means $a \equiv 0$, that is $[a]_m = [0]_m$.

**Point 2, "if".** Assume $[a]_m \neq [0]_m$, so $d < m$. Since $d$ divides both $a$ and $m$, write $a = a_1 d$ and $m = m_1 d$. Then

$$[a]_m [m_1]_m = [a m_1]_m = [a_1 d m_1]_m = [a_1 m]_m = [0]_m,$$

because $d m_1 = m$ and $a_1 m$ is a multiple of $m$. If $d > 1$, then $m_1 = m/d$ satisfies $0 < m_1 < m$, so $[m_1]_m \neq [0]_m$.
So $[a]_m$ times a nonzero class gives zero: $[a]_m$ is a zero divisor.

*Example:* $a = 8$, $m = 12$. Then $d = 4$, $a_1 = 2$, $m_1 = 3$, and $[8][3] = [24] = [0]$ in $\mathbb{Z}/12\mathbb{Z}$.

**Point 2, "only if".** Assume $[a]_m$ is a zero divisor: there is $[b]_m \neq [0]_m$ with $[ab]_m = [0]_m$, so $m$ divides $ab$.
If we had $d = 1$, then $a$ and $m$ would be coprime, and $m$ would have to divide $b$:
since $m$ shares no factor with $a$, all of $m$ must be "absorbed" by $b$ (for example, if $12 \mid 5b$, then $12 \mid b$).
That means $[b]_m = [0]_m$, a contradiction. So $d > 1$ (and $d < m$ because $[a]_m \neq [0]_m$).

**Point 3.** $\mathbb{Z}/m\mathbb{Z}$ is a finite ring, so by Theorem 1.1.7 every nonzero element is invertible or a zero divisor,
and never both (Lemma 1.1.6). So $[a]_m$ is **not** invertible exactly when it is $[0]_m$ (point 1: $d = m$) or a zero divisor
(point 2: $1 < d < m$), that is, when $d \neq 1$. Hence $[a]_m$ is invertible if and only if $d = 1$. ∎

**Example: $\mathbb{Z}/5\mathbb{Z}$ and $\mathbb{Z}/12\mathbb{Z}$.**

In $\mathbb{Z}/5\mathbb{Z}$, every $a \in \lbrace 1, 2, 3, 4 \rbrace$ has $\gcd(a, 5) = 1$, so $(\mathbb{Z}/5\mathbb{Z})^\ast = \lbrace 1, 2, 3, 4 \rbrace$
and $\mathbb{Z}/5\mathbb{Z}$ is a field. Multiplication table of $(\mathbb{Z}/5\mathbb{Z})^\ast$:

| $\cdot$ | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| **1** | 1 | 2 | 3 | 4 |
| **2** | 2 | 4 | 1 | 3 |
| **3** | 3 | 1 | 4 | 2 |
| **4** | 4 | 3 | 2 | 1 |

In $\mathbb{Z}/12\mathbb{Z}$, only $1, 5, 7, 11$ are coprime to 12, so $(\mathbb{Z}/12\mathbb{Z})^\ast = \lbrace 1, 5, 7, 11 \rbrace$ and $\mathbb{Z}/12\mathbb{Z}$ is not a field:

| $\cdot$ | 1 | 5 | 7 | 11 |
|---|---|---|---|---|
| **1** | 1 | 5 | 7 | 11 |
| **5** | 5 | 1 | 11 | 7 |
| **7** | 7 | 11 | 1 | 5 |
| **11** | 11 | 7 | 5 | 1 |

Both groups have 4 elements, but they are **really different**: look at the diagonals.
In $(\mathbb{Z}/12\mathbb{Z})^\ast$ every element squares to 1; in $(\mathbb{Z}/5\mathbb{Z})^\ast$ we have $2^2 = 4 \neq 1$.

**Lemma 1.2.3.** $\mathbb{Z}/m\mathbb{Z}$ is a field if and only if $m$ is prime.

*Proof.* If $m$ is prime, every $[a]_m \neq [0]_m$ has $\gcd(a, m) = 1$ (the only divisors of $m$ are 1 and $m$, and $m \nmid a$).
So by Lemma 1.2.2 every nonzero class is invertible, and $\mathbb{Z}/m\mathbb{Z}$ is a field.

If $m$ is not prime, write $m = ab$ with $0 < a, b < m$ (for example $12 = 3 \cdot 4$). Then $[a]_m \neq [0]_m$ and $[b]_m \neq [0]_m$,
but $[a]_m [b]_m = [ab]_m = [m]_m = [0]_m$. So $[a]_m$ is a zero divisor, hence not invertible (Lemma 1.1.6), and $\mathbb{Z}/m\mathbb{Z}$ is not a field. ∎

> [!TIP]
> **Computing inverses in practice.** Lemma 1.2.2 says *when* $[a]_m$ is invertible, not how to find the inverse.
> For the exercises, use the extended Euclidean algorithm to find $x, y$ with $ax + my = 1$; then $[a]_m^{-1} = [x]_m$.
> Worked examples in [Exercise 4](exercises/algebra.md#exercise-4).

### Euler's φ function

We now want to count the invertible elements of $\mathbb{Z}/m\mathbb{Z}$.

**Lemma 1.2.4.** For $m \ge 2$, the number of invertible elements of $\mathbb{Z}/m\mathbb{Z}$ is the number of $a$ with $1 \le a < m$ and $\gcd(a, m) = 1$.

*Proof.* Every nonzero class is $[a]_m$ for exactly one $a$ with $1 \le a < m$ (its remainder),
and by Lemma 1.2.2 it is invertible if and only if $\gcd(a, m) = 1$. ∎

**Definition.** For $n \ge 1$, **Euler's φ function** $\varphi(n)$ is the number of elements of $\lbrace 1, 2, \dots, n \rbrace$ coprime to $n$.
Note $\varphi(1) = 1$, since $\gcd(1, 1) = 1$.

Example: for $n = 12$, the numbers in $\lbrace 1, \dots, 12 \rbrace$ coprime to 12 are $1, 5, 7, 11$, so $\varphi(12) = 4$.

**Lemma 1.2.5.** For $n \ge 2$, $\varphi(n) = \lvert (\mathbb{Z}/n\mathbb{Z})^\ast \rvert$.

*Proof.* The only difference between the two counts is the number $n$ itself, which is in $\lbrace 1, \dots, n \rbrace$ but not in $\lbrace 1, \dots, n - 1 \rbrace$.
Since $\gcd(n, n) = n \neq 1$, it is not counted anyway. So the two counts agree, and Lemma 1.2.4 concludes. ∎

**Theorem 1.2.6.** For $n \ge 2$:

$$n = \sum_{d \mid n} \varphi(d),$$

where the sum runs over all positive divisors $d$ of $n$.

*Proof.* Let $V = \lbrace 1, 2, \dots, n \rbrace$. For each $d$ with $1 \le d \le n$, let

$$V_d = \lbrace v \in V : \gcd(v, n) = d \rbrace,$$

the numbers whose gcd with $n$ is exactly $d$. Every $v \in V$ has exactly one gcd with $n$, so it lies in exactly one $V_d$:
the sets $V_d$ form a **partition** of $V$ (they are disjoint and cover $V$). Hence

$$n = \lvert V \rvert = \lvert V_1 \rvert + \lvert V_2 \rvert + \dots + \lvert V_n \rvert.$$

Now we compute each $\lvert V_d \rvert$.

- If $d$ does not divide $n$, then $V_d = \emptyset$: a gcd with $n$ always divides $n$. These terms contribute 0.
- If $d$ divides $n$: $\gcd(v, n) = d$ means $v = v'd$ for some $v'$ with $1 \le v' \le n/d$, and $\gcd(v', n/d) = 1$
  (after dividing $v$ and $n$ by their gcd $d$, nothing is left in common). So the elements of $V_d$ correspond to the numbers
  in $\lbrace 1, \dots, n/d \rbrace$ coprime to $n/d$, and $\lvert V_d \rvert = \varphi(n/d)$.

Therefore

$$n = \sum_{d \mid n} \lvert V_d \rvert = \sum_{d \mid n} \varphi\!\left(\frac{n}{d}\right) = \sum_{d \mid n} \varphi(d).$$

The last equality holds because as $d$ runs over the divisors of $n$, so does $n/d$ (in reverse order):
for $n = 12$, the divisors $1, 2, 3, 4, 6, 12$ give $n/d = 12, 6, 4, 3, 2, 1$, the same numbers. So the two sums have the same terms. ∎

> [!NOTE]
> **The partition for $n = 12$.**
>
> | $d$ | $V_d$ (numbers in $1..12$ with $\gcd(v, 12) = d$) | $\lvert V_d \rvert$ | $\varphi(12/d)$ |
> |---|---|---|---|
> | 1 | 1, 5, 7, 11 | 4 | $\varphi(12) = 4$ |
> | 2 | 2, 10 | 2 | $\varphi(6) = 2$ |
> | 3 | 3, 9 | 2 | $\varphi(4) = 2$ |
> | 4 | 4, 8 | 2 | $\varphi(3) = 2$ |
> | 6 | 6 | 1 | $\varphi(2) = 1$ |
> | 12 | 12 | 1 | $\varphi(1) = 1$ |
>
> Total: $4 + 2 + 2 + 2 + 1 + 1 = 12$. For instance, $V_2 = \lbrace 2, 10 \rbrace = \lbrace 2 \cdot 1, 2 \cdot 5 \rbrace$, and $1, 5$ are exactly the numbers up to 6 coprime to 6.

**Lemma 1.2.7 (recursive formula).** For $n \ge 2$:

$$\varphi(n) = n - \sum_{d \mid n,\ d \neq n} \varphi(d).$$

*Proof.* Take Theorem 1.2.6 and move all terms except $\varphi(n)$ to the other side. ∎

This computes $\varphi(n)$ from the values on smaller divisors:
$\varphi(2) = 2 - \varphi(1) = 1$, $\varphi(3) = 3 - \varphi(1) = 2$, $\varphi(4) = 4 - \varphi(2) - \varphi(1) = 2$,
$\varphi(5) = 5 - \varphi(1) = 4$, $\varphi(6) = 6 - \varphi(3) - \varphi(2) - \varphi(1) = 2$.

**Lemma 1.2.8.** For $p$ prime and $k \ge 1$: $\varphi(p^k) = (p - 1)\,p^{k-1}$.

*Proof.* The divisors of $p^k$ are only $1, p, p^2, \dots, p^k$. So for $a \in \lbrace 1, \dots, p^k \rbrace$,
$\gcd(a, p^k) \neq 1$ happens exactly when the gcd is $p^l$ with $l \ge 1$, that is, when $p$ divides $a$.
The multiples of $p$ up to $p^k$ are $p, 2p, \dots, p^{k-1} \cdot p$: there are $p^{k-1}$ of them. So

$$\varphi(p^k) = p^k - p^{k-1} = (p - 1)\,p^{k-1}.$$

∎

*Example:* $p = 3$, $k = 2$. In $\lbrace 1, \dots, 9 \rbrace$ the multiples of 3 are $3, 6, 9$, that is $3^1 = 3$ numbers.
So $\varphi(9) = 9 - 3 = 6$: indeed $1, 2, 4, 5, 7, 8$ are coprime to 9.

| $n$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| $\varphi(n)$ | 1 | 1 | 2 | 2 | 4 | 2 | 6 | 4 | 6 | 4 | 10 | 4 |

---

## 1.3 Direct products and homomorphisms

### Direct products

Let $R_1, R_2, \dots, R_n$ be rings with identity, with $1 \neq 0$. The **direct product** $R_1 \times R_2 \times \dots \times R_n$
is the set of tuples $(r_1, \dots, r_n)$ with $r_i \in R_i$, with operations done **component by component**:

$$(r_1, \dots, r_n) + (s_1, \dots, s_n) = (r_1 + s_1, \dots, r_n + s_n), \qquad (r_1, \dots, r_n) \cdot (s_1, \dots, s_n) = (r_1 s_1, \dots, r_n s_n),$$

where in position $i$ we use the operations of $R_i$.

Every ring axiom holds because it holds in each component. The zero is $(0, \dots, 0)$, the identity is $(1, \dots, 1)$,
so the product is a ring with identity; it is commutative if and only if all the $R_i$ are.

*Example:* in $\mathbb{Z}/4\mathbb{Z} \times \mathbb{Z}/3\mathbb{Z}$, $(3, 2) + (2, 2) = (5, 4) = (1, 1)$ and $(3, 2) \cdot (2, 2) = (6, 4) = (2, 1)$,
where the first component is computed modulo 4 and the second modulo 3.

> **Notation.** From now on, the operation of a group $G$ is written as multiplication $\cdot$, and its neutral element as $1$ (the **identity**), unless stated otherwise.

The **direct product of groups** $G_1 \times \dots \times G_n$ is defined the same way, with component-wise multiplication.
It is a group: $(1, \dots, 1)$ is neutral, and the inverse of $(g_1, \dots, g_n)$ is $(g_1^{-1}, \dots, g_n^{-1})$,
since multiplying them gives $(g_1 g_1^{-1}, \dots, g_n g_n^{-1}) = (1, \dots, 1)$ in both orders.

**Example: $\mathbb{Z}/4\mathbb{Z} \times \mathbb{Z}/3\mathbb{Z}$.** It is a commutative ring with $4 \cdot 3 = 12$ elements.
With $(\mathbb{Z}/4\mathbb{Z})^\ast = \lbrace 1, 3 \rbrace$ and $(\mathbb{Z}/3\mathbb{Z})^\ast = \lbrace 1, 2 \rbrace$:

- zero element: $(0, 0)$;
- invertible elements (4): $(1, 1)$, $(1, 2)$, $(3, 1)$, $(3, 2)$;
- zero divisors (7): $(0, 1)$, $(0, 2)$, $(1, 0)$, $(2, 0)$, $(3, 0)$, $(2, 1)$, $(2, 2)$.

Call $a = (1, 1)$, $b = (1, 2)$, $c = (3, 1)$, $d = (3, 2)$. The group of invertible elements has this table:

| $\cdot$ | $a$ | $b$ | $c$ | $d$ |
|---|---|---|---|---|
| $a$ | $a$ | $b$ | $c$ | $d$ |
| $b$ | $b$ | $a$ | $d$ | $c$ |
| $c$ | $c$ | $d$ | $a$ | $b$ |
| $d$ | $d$ | $c$ | $b$ | $a$ |

Every element squares to $a = (1, 1)$, the identity, just like in $(\mathbb{Z}/12\mathbb{Z})^\ast$. This is not a coincidence (see the CRT below).

**Lemma 1.3.1.** Let $R_1, \dots, R_n$ be commutative rings with identity and $1 \neq 0$, and let $(r_1, \dots, r_n) \neq (0, \dots, 0)$. Then $(r_1, \dots, r_n)$

1. is a zero divisor if and only if some component $r_i$ is $0$ or a zero divisor;
2. is invertible if and only if every component $r_i$ is invertible ($r_i \in R_i^\ast$ for all $i$).

*Proof.*

**Point 1, "only if".** Suppose $(r_1, \dots, r_n)(s_1, \dots, s_n) = (0, \dots, 0)$ with $(s_1, \dots, s_n) \neq (0, \dots, 0)$.
Component by component, $r_i s_i = 0$ for every $i$. Since the tuple $s$ is not zero, some $s_j \neq 0$.
Then $r_j s_j = 0$ with $s_j \neq 0$: either $r_j = 0$, or $r_j \neq 0$ and then it is a zero divisor.

**Point 1, "if".** Suppose $r_i$ is $0$ or a zero divisor for some $i$. Build a tuple $s$ as follows:

- in position $i$: if $r_i = 0$, put $s_i = 1$; if $r_i$ is a zero divisor, put an $s_i \neq 0$ with $r_i s_i = 0$;
- in every other position $j \neq i$: put $s_j = 0$.

Then $s \neq (0, \dots, 0)$ (position $i$ is nonzero), and $r \cdot s = (0, \dots, 0)$: position $i$ gives $r_i s_i = 0$ by construction,
the others give $r_j \cdot 0 = 0$. So $r$ is a zero divisor.

*Example:* $(2, 1)$ in $\mathbb{Z}/4\mathbb{Z} \times \mathbb{Z}/3\mathbb{Z}$. The first component 2 is a zero divisor ($2 \cdot 2 = 4 \equiv 0$), so take $s = (2, 0)$:
$(2, 1)(2, 0) = (4, 0) = (0, 0)$. And for $(0, 1)$, take $s = (1, 0)$: $(0, 1)(1, 0) = (0, 0)$.

**Point 2.** $(r_1, \dots, r_n)$ is invertible if and only if some $(s_1, \dots, s_n)$ gives $(r_1 s_1, \dots, r_n s_n) = (1, \dots, 1)$,
that is $r_i s_i = 1$ for every $i$. This happens if and only if each $r_i$ has an inverse $s_i$ in $R_i$. ∎

### Homomorphisms

A **homomorphism** is a map that respects the operations: it does not matter whether you operate first and then apply the map, or the other way round.

**Definition (rings).** Let $R, S$ be rings with identity. A ring homomorphism $\psi : R \to S$ satisfies

1. $\psi(1) = 1$ and $\psi(0) = 0$;
2. $\psi(r_1 + r_2) = \psi(r_1) + \psi(r_2)$ for all $r_1, r_2 \in R$;
3. $\psi(r_1 \cdot r_2) = \psi(r_1) \cdot \psi(r_2)$ for all $r_1, r_2 \in R$.

It is an **isomorphism** if it is also bijective.

*Example:* for $m \ge 2$, reduction modulo $m$, $\mathbb{Z} \to \mathbb{Z}/m\mathbb{Z}$, $a \mapsto [a]_m$, is a ring homomorphism:
by definition of the operations, $[a + b]_m = [a]_m + [b]_m$ and $[ab]_m = [a]_m [b]_m$. It is not an isomorphism (it is not injective: $0$ and $m$ both go to $[0]_m$).

**Lemma 1.3.2.** If $\psi : R \to S$ is a ring isomorphism, then $\psi^{-1} : S \to R$ is a ring isomorphism too.

*Proof.* $\psi^{-1}$ exists and is bijective because $\psi$ is bijective; and $\psi^{-1}(1) = 1$, $\psi^{-1}(0) = 0$ because $\psi(1) = 1$, $\psi(0) = 0$.
It remains to show that $\psi^{-1}$ respects $+$ and $\cdot$.

We cannot compute $\psi^{-1}$ directly, so the trick is: **apply $\psi$ to both sides and use that $\psi$ is injective.**
Let $s_1, s_2 \in S$. We want $\psi^{-1}(s_1 + s_2) = \psi^{-1}(s_1) + \psi^{-1}(s_2)$. Apply $\psi$ to each side:

- left: $\psi(\psi^{-1}(s_1 + s_2)) = s_1 + s_2$;
- right: $\psi(\psi^{-1}(s_1) + \psi^{-1}(s_2)) = \psi(\psi^{-1}(s_1)) + \psi(\psi^{-1}(s_2)) = s_1 + s_2$, using that $\psi$ respects $+$.

Both sides have the same image under $\psi$. Since $\psi$ is injective, they are equal.
The same argument with $\cdot$ in place of $+$ shows $\psi^{-1}(s_1 s_2) = \psi^{-1}(s_1)\,\psi^{-1}(s_2)$. ∎

**Lemma 1.3.3.** Let $\psi : R \to S$ be a ring homomorphism. If $r \in R$ is invertible, then $\psi(r)$ is invertible and $\psi(r)^{-1} = \psi(r^{-1})$.

*Proof.* $\psi(r)\,\psi(r^{-1}) = \psi(r r^{-1}) = \psi(1) = 1$, and in the same way $\psi(r^{-1})\,\psi(r) = 1$.
So $\psi(r^{-1})$ is the inverse of $\psi(r)$. ∎

> [!NOTE]
> **Example: $p : \mathbb{Z}/21\mathbb{Z} \to \mathbb{Z}/7\mathbb{Z}$, $[a]_{21} \mapsto [a]_7$.**
> This map is well defined: if $a \equiv b \pmod{21}$, then $21 \mid a - b$, so also $7 \mid a - b$. It is a homomorphism.
>
> - **Invertible elements go to invertible elements.** $[5]_{21}$ is invertible with inverse $[17]_{21}$ ($5 \cdot 17 = 85 = 4 \cdot 21 + 1$).
>   It maps to $[5]_7$, whose inverse is $[3]_7$ ($5 \cdot 3 = 15 = 2 \cdot 7 + 1$). As Lemma 1.3.3 predicts, $p([17]_{21}) = [17]_7 = [3]_7$.
> - **Zero divisors do *not* necessarily go to zero divisors.** $[3]_{21}$ and $[7]_{21}$ are zero divisors ($3 \cdot 7 = 21 \equiv 0$),
>   but $p([3]_{21}) = [3]_7$ is invertible and $p([7]_{21}) = [0]_7$ is zero: neither is a zero divisor.

**Definition (groups).** Let $G, H$ be groups. A group homomorphism $\psi : G \to H$ satisfies

1. $\psi(1) = 1$;
2. $\psi(g_1 g_2) = \psi(g_1)\,\psi(g_2)$ for all $g_1, g_2 \in G$.

It is an **isomorphism** if it is also bijective.

**Lemma 1.3.4.** Let $\psi : G \to H$ be a group homomorphism. Then $\psi(g)^{-1} = \psi(g^{-1})$ for every $g \in G$,
and if $\psi$ is an isomorphism, then $\psi^{-1}$ is an isomorphism too.
The notes leave the proof as an exercise: see [Exercise 2](exercises/algebra.md#exercise-2).
It follows the same pattern as Lemmas 1.3.3 and 1.3.2.

**Lemma 1.3.5.** Let $\psi : R \to S$ be a ring homomorphism. Restricting it to the invertible elements gives a group homomorphism
$\psi|_{R^\ast} : R^\ast \to S^\ast$. If $\psi$ is a ring isomorphism, then $\psi|_{R^\ast}$ is a group isomorphism.

*Proof.* By Lemma 1.3.3, $\psi$ maps invertible elements to invertible elements: $\psi(R^\ast) \subseteq S^\ast$.
So $\psi|_{R^\ast}$ really lands in $S^\ast$, and it respects multiplication because $\psi$ does: it is a group homomorphism.

Now let $\psi$ be an isomorphism. By Lemma 1.3.2, $\psi^{-1}$ is a homomorphism too, so by the same argument $\psi^{-1}(S^\ast) \subseteq R^\ast$.
Applying $\psi$ to this inclusion:

$$S^\ast = \psi(\psi^{-1}(S^\ast)) \subseteq \psi(R^\ast) \subseteq S^\ast.$$

The chain starts and ends with $S^\ast$, so all the inclusions are equalities: $\psi(R^\ast) = S^\ast$.
So $\psi|_{R^\ast}$ is surjective onto $S^\ast$; it is injective because $\psi$ is. Hence it is a bijection, that is, a group isomorphism. ∎

**Definition.** Two rings $R, S$ are **isomorphic**, written $R \cong S$, if there is a ring isomorphism between them.
The same for groups: $G \cong H$. Isomorphic structures are "the same up to renaming the elements".

**Lemma 1.3.6.** Let $R_1, \dots, R_n$ be commutative rings with identity and $1 \neq 0$. Then

$$(R_1 \times \dots \times R_n)^\ast \cong R_1^\ast \times \dots \times R_n^\ast.$$

*Proof.* By Lemma 1.3.1 (point 2), the two sides contain exactly the same tuples: those with every component invertible.
So the map $(r_1, \dots, r_n) \mapsto (r_1, \dots, r_n)$ is well defined and bijective, and it respects multiplication
(which is component-wise on both sides). It is an isomorphism. ∎

*Example:* $(\mathbb{Z}/4\mathbb{Z} \times \mathbb{Z}/3\mathbb{Z})^\ast = \lbrace 1, 3 \rbrace \times \lbrace 1, 2 \rbrace$, the 4 elements $a, b, c, d$ found above.

### Chinese remainder theorem

**Theorem 1.3.7 (Chinese remainder theorem, CRT).** Let $m_1, \dots, m_n$ be positive integers, pairwise coprime
(every two of them have gcd 1), and let $m = m_1 m_2 \cdots m_n$. Then the map

$$\mathbb{Z}/m\mathbb{Z} \to \mathbb{Z}/m_1\mathbb{Z} \times \dots \times \mathbb{Z}/m_n\mathbb{Z}, \qquad [a]_m \mapsto ([a]_{m_1}, \dots, [a]_{m_n})$$

is a ring isomorphism.

In words: knowing $a$ modulo $m$ is **the same information** as knowing $a$ modulo each $m_i$.

*Proof.*

- **Well defined.** The image must not depend on the representative. If $a \equiv b \pmod m$, then $m \mid a - b$;
  since each $m_i$ divides $m$, also $m_i \mid a - b$, so $a \equiv b \pmod{m_i}$ for every $i$.
- **Homomorphism.** Straightforward: reducing modulo each $m_i$ respects sums and products, and $[1]_m \mapsto ([1], \dots, [1])$, $[0]_m \mapsto ([0], \dots, [0])$.
- **Surjective.** This is the Chinese remainder theorem in its modular-arithmetic version (the one about systems of congruences):
  for any choice of $a_1, \dots, a_n$ there is an integer $a$ with $a \equiv a_i \pmod{m_i}$ for every $i$.
  So every tuple $([a_1], \dots, [a_n])$ is the image of some $[a]_m$.
- **Injective.** Both sets are finite with the same number of elements, $m = m_1 \cdots m_n$.
  A surjective map between finite sets of the same size is also injective. ∎

> [!NOTE]
> **The CRT for $12 = 4 \cdot 3$.** Here is the whole map $\mathbb{Z}/12\mathbb{Z} \to \mathbb{Z}/4\mathbb{Z} \times \mathbb{Z}/3\mathbb{Z}$:
>
> | $a$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
> |---|---|---|---|---|---|---|---|---|---|---|---|---|
> | $a \bmod 4$ | 0 | 1 | 2 | 3 | 0 | 1 | 2 | 3 | 0 | 1 | 2 | 3 |
> | $a \bmod 3$ | 0 | 1 | 2 | 0 | 1 | 2 | 0 | 1 | 2 | 0 | 1 | 2 |
>
> All 12 pairs appear exactly once: the map is a bijection. The units $1, 5, 7, 11$ of $\mathbb{Z}/12\mathbb{Z}$ go to
> $(1, 1), (1, 2), (3, 1), (3, 2)$, exactly the units $a, b, c, d$ of the product found earlier.
>
> It fails without coprimality: for $4 = 2 \cdot 2$, the map $\mathbb{Z}/4\mathbb{Z} \to \mathbb{Z}/2\mathbb{Z} \times \mathbb{Z}/2\mathbb{Z}$
> sends both $0$ and $2$ to $(0, 0)$, so it is not injective.

**Remark.** Since $\mathbb{Z}/12\mathbb{Z} \cong \mathbb{Z}/4\mathbb{Z} \times \mathbb{Z}/3\mathbb{Z}$, Lemma 1.3.5 gives
$(\mathbb{Z}/12\mathbb{Z})^\ast \cong (\mathbb{Z}/4\mathbb{Z} \times \mathbb{Z}/3\mathbb{Z})^\ast$, and by Lemma 1.3.6 this is
$(\mathbb{Z}/4\mathbb{Z})^\ast \times (\mathbb{Z}/3\mathbb{Z})^\ast$. This explains why both tables above have every element squaring to the identity.

**Lemma 1.3.8.** Let $m_1, \dots, m_n$ be pairwise coprime and $m = m_1 \cdots m_n$. Then

$$(\mathbb{Z}/m\mathbb{Z})^\ast \cong (\mathbb{Z}/m_1\mathbb{Z})^\ast \times \dots \times (\mathbb{Z}/m_n\mathbb{Z})^\ast, \qquad \text{and in particular} \qquad \varphi(m) = \varphi(m_1) \cdots \varphi(m_n).$$

*Proof.* The same chain as in the remark, in general:

1. by the CRT, $\mathbb{Z}/m\mathbb{Z} \cong \mathbb{Z}/m_1\mathbb{Z} \times \dots \times \mathbb{Z}/m_n\mathbb{Z}$;
2. by Lemma 1.3.5, the groups of invertible elements are isomorphic: $(\mathbb{Z}/m\mathbb{Z})^\ast \cong (\mathbb{Z}/m_1\mathbb{Z} \times \dots \times \mathbb{Z}/m_n\mathbb{Z})^\ast$;
3. by Lemma 1.3.6, the right side is $\cong (\mathbb{Z}/m_1\mathbb{Z})^\ast \times \dots \times (\mathbb{Z}/m_n\mathbb{Z})^\ast$.

Isomorphic groups have the same number of elements, and a product of sets has as many elements as the product of their sizes. So
$\lvert (\mathbb{Z}/m\mathbb{Z})^\ast \rvert = \lvert (\mathbb{Z}/m_1\mathbb{Z})^\ast \rvert \cdots \lvert (\mathbb{Z}/m_n\mathbb{Z})^\ast \rvert$,
which by Lemma 1.2.5 reads $\varphi(m) = \varphi(m_1) \cdots \varphi(m_n)$. ∎

*Example:* $\varphi(12) = \varphi(4)\,\varphi(3) = 2 \cdot 2 = 4$. But careful: $\varphi(4) \neq \varphi(2)\,\varphi(2) = 1$, because 2 and 2 are not coprime.

**Corollary 1.3.9.** Let $m = p_1^{e_1} p_2^{e_2} \cdots p_r^{e_r}$ be the prime factorization of $m$ (distinct primes $p_i$, exponents $e_i \ge 1$). Then

$$\varphi(m) = p_1^{e_1 - 1}(p_1 - 1)\; p_2^{e_2 - 1}(p_2 - 1) \cdots p_r^{e_r - 1}(p_r - 1) = m \left(1 - \frac{1}{p_1}\right)\left(1 - \frac{1}{p_2}\right) \cdots \left(1 - \frac{1}{p_r}\right).$$

*Proof.* Powers of distinct primes are pairwise coprime, so Lemma 1.3.8 gives $\varphi(m) = \varphi(p_1^{e_1}) \cdots \varphi(p_r^{e_r})$.
By Lemma 1.2.8, $\varphi(p_i^{e_i}) = p_i^{e_i - 1}(p_i - 1)$, which gives the first formula.
For the second, write each factor as $p_i^{e_i - 1}(p_i - 1) = p_i^{e_i}\left(1 - \frac{1}{p_i}\right)$, and note that the product of the $p_i^{e_i}$ is $m$. ∎

*Example:* $100 = 2^2 \cdot 5^2$, so $\varphi(100) = \varphi(2^2)\,\varphi(5^2) = (2 \cdot 1) \cdot (5 \cdot 4) = 40$.
With the second formula: $100 \cdot \frac{1}{2} \cdot \frac{4}{5} = 40$.

Note that the formula **needs the factorization of $m$**.

> [!NOTE]
> **Why this matters for RSA.** For $n = pq$ with $p, q$ distinct primes, $\varphi(n) = (p - 1)(q - 1)$ is easy to compute
> if you know $p$ and $q$. If you only know $n$, no efficient way to compute $\varphi(n)$ is known, because it would require factoring $n$.
> This asymmetry is what RSA (section 2.3) is built on.

---

# Cheat sheet

- Semigroup → monoid → group, and ring → commutative ring with identity → field: each step adds one requirement.
- The invertible elements of a monoid (or of a ring) form a group: $H^\ast$, $R^\ast$.
- $(ab)^{-1} = b^{-1}a^{-1}$. Cancellation only works for invertible elements.
- Zero divisors are never invertible. In a **finite** ring, every nonzero element is one or the other.
- $[a]_m$ is invertible $\iff \gcd(a, m) = 1$; it is a zero divisor $\iff 1 < \gcd(a, m) < m$.
- $\mathbb{Z}/m\mathbb{Z}$ is a field $\iff m$ is prime.
- $\varphi(n) = \lvert (\mathbb{Z}/n\mathbb{Z})^\ast \rvert$; $\sum_{d \mid n} \varphi(d) = n$; $\varphi(p^k) = (p-1)p^{k-1}$.
- Homomorphisms preserve invertible elements, not zero divisors.
- CRT: $\mathbb{Z}/m\mathbb{Z} \cong \mathbb{Z}/m_1\mathbb{Z} \times \dots \times \mathbb{Z}/m_n\mathbb{Z}$ for pairwise coprime $m_i$; hence $\varphi$ is multiplicative on coprime factors.
- $\varphi(m) = m \prod_{p \mid m} (1 - 1/p)$, which requires the factorization of $m$.
