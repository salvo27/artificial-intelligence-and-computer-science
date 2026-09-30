# Algebra: exercises

Exercises on sections 1.1 to 1.4 of the notes, with solutions.
Exercises 1 and 2 are the proofs the notes leave to the reader; the others practice the computations.
Exercises 11 to 16 (section 1.4) are not in the notes: they follow the examples of the notes on other numbers.
Try each one before opening the solution.

Back to the [summary](../summary.md).

---

### Exercise 1

**(Lemma 1.2.1)** Let $m \ge 2$. Prove that if $a \equiv c$ and $b \equiv d \pmod m$, then
$a + b \equiv c + d \pmod m$ and $ab \equiv cd \pmod m$.

<details>
<summary>Solution</summary>

By hypothesis $m \mid a - c$ and $m \mid b - d$.

- Sum: $(a + b) - (c + d) = (a - c) + (b - d)$ is a sum of two multiples of $m$, so it is a multiple of $m$.
- Product: add and subtract $ad$:

$$ab - cd = ab - ad + ad - cd = a(b - d) + d(a - c).$$

Both terms are multiples of $m$, so their sum is too.

This is what makes $[a] + [b] = [a + b]$ and $[a][b] = [ab]$ well defined on $\mathbb{Z}/m\mathbb{Z}$.

</details>

---

### Exercise 2

**(Lemma 1.3.4)** Let $\psi : G \to H$ be a group homomorphism. Prove that:

1. $\psi(g)^{-1} = \psi(g^{-1})$ for every $g \in G$;
2. if $\psi$ is an isomorphism, then $\psi^{-1}$ is an isomorphism too.

<details>
<summary>Solution</summary>

1. $\psi(g)\,\psi(g^{-1}) = \psi(g g^{-1}) = \psi(1) = 1$, and in the same way $\psi(g^{-1})\,\psi(g) = 1$.
   So $\psi(g^{-1})$ is the inverse of $\psi(g)$, which is unique (Lemma 1.1.3).

2. $\psi^{-1}$ exists and is bijective because $\psi$ is. Since $\psi(1) = 1$, we get $\psi^{-1}(1) = 1$.
   For $h_1, h_2 \in H$, apply $\psi$ to both candidates:

   $$\psi\big(\psi^{-1}(h_1)\,\psi^{-1}(h_2)\big) = \psi(\psi^{-1}(h_1))\,\psi(\psi^{-1}(h_2)) = h_1 h_2 = \psi\big(\psi^{-1}(h_1 h_2)\big).$$

   Since $\psi$ is injective, $\psi^{-1}(h_1)\,\psi^{-1}(h_2) = \psi^{-1}(h_1 h_2)$, so $\psi^{-1}$ is a homomorphism.

</details>

---

### Exercise 3

Split the nonzero elements of $\mathbb{Z}/12\mathbb{Z}$ into invertible elements and zero divisors.
For each zero divisor $[a]$, give a $[b] \neq [0]$ with $[a][b] = [0]$.

<details>
<summary>Solution</summary>

By Lemma 1.2.2 it only depends on $\gcd(a, 12)$.

- **Invertible** ($\gcd = 1$): $1, 5, 7, 11$. Each is its own inverse: $5^2 = 25$, $7^2 = 49$, $11^2 = 121$ are all $\equiv 1$.
- **Zero divisors** ($\gcd > 1$): $2, 3, 4, 6, 8, 9, 10$. Following the proof of Lemma 1.2.2, take $b = 12 / \gcd(a, 12)$:

| $a$ | 2 | 3 | 4 | 6 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|
| $\gcd(a, 12)$ | 2 | 3 | 4 | 6 | 4 | 3 | 2 |
| $b$ | 6 | 4 | 3 | 2 | 3 | 4 | 6 |

Check: $\varphi(12) = 4$, which matches the 4 invertible elements.

</details>

---

### Exercise 4

Compute $[17]^{-1}$ in $\mathbb{Z}/43\mathbb{Z}$ and $[7]^{-1}$ in $\mathbb{Z}/40\mathbb{Z}$.

<details>
<summary>Solution</summary>

Use the extended Euclidean algorithm.

**17 modulo 43.**

$$43 = 2 \cdot 17 + 9, \qquad 17 = 1 \cdot 9 + 8, \qquad 9 = 1 \cdot 8 + 1.$$

Going back up:

$$1 = 9 - 8 = 9 - (17 - 9) = 2 \cdot 9 - 17 = 2(43 - 2 \cdot 17) - 17 = 2 \cdot 43 - 5 \cdot 17.$$

So $17 \cdot (-5) \equiv 1$, and $[17]^{-1} = [-5] = [38]$. Check: $17 \cdot 38 = 646 = 15 \cdot 43 + 1$.

**7 modulo 40.**

$$40 = 5 \cdot 7 + 5, \qquad 7 = 1 \cdot 5 + 2, \qquad 5 = 2 \cdot 2 + 1.$$

$$1 = 5 - 2 \cdot 2 = 5 - 2(7 - 5) = 3 \cdot 5 - 2 \cdot 7 = 3(40 - 5 \cdot 7) - 2 \cdot 7 = 3 \cdot 40 - 17 \cdot 7.$$

So $[7]^{-1} = [-17] = [23]$. Check: $7 \cdot 23 = 161 = 4 \cdot 40 + 1$.

</details>

---

### Exercise 5

Compute $\varphi(97)$, $\varphi(1024)$, $\varphi(36)$ and $\varphi(100)$.

<details>
<summary>Solution</summary>

- $97$ is prime: $\varphi(97) = 96$.
- $1024 = 2^{10}$: $\varphi(2^{10}) = (2 - 1) \cdot 2^9 = 512$.
- $36 = 2^2 \cdot 3^2$: $\varphi(36) = \varphi(4)\,\varphi(9) = 2 \cdot 6 = 12$. Equivalently, $36 (1 - \tfrac{1}{2})(1 - \tfrac{1}{3}) = 12$.
- $100 = 2^2 \cdot 5^2$: $\varphi(100) = \varphi(4)\,\varphi(25) = 2 \cdot 20 = 40$.

</details>

---

### Exercise 6

Check Theorem 1.2.6 ($\sum_{d \mid n} \varphi(d) = n$) for $n = 12$.

<details>
<summary>Solution</summary>

The divisors of 12 are $1, 2, 3, 4, 6, 12$:

$$\varphi(1) + \varphi(2) + \varphi(3) + \varphi(4) + \varphi(6) + \varphi(12) = 1 + 1 + 2 + 2 + 2 + 4 = 12.$$

</details>

---

### Exercise 7

Show that $(\mathbb{Z}/8\mathbb{Z})^\ast$ and $(\mathbb{Z}/5\mathbb{Z})^\ast$ both have 4 elements but are not isomorphic.

<details>
<summary>Solution</summary>

$(\mathbb{Z}/8\mathbb{Z})^\ast = \lbrace 1, 3, 5, 7 \rbrace$ and $(\mathbb{Z}/5\mathbb{Z})^\ast = \lbrace 1, 2, 3, 4 \rbrace$.

In $(\mathbb{Z}/8\mathbb{Z})^\ast$ every element squares to 1: $3^2 = 9$, $5^2 = 25$ and $7^2 = 49$ are all $\equiv 1 \pmod 8$.

Suppose $\psi : (\mathbb{Z}/5\mathbb{Z})^\ast \to (\mathbb{Z}/8\mathbb{Z})^\ast$ were an isomorphism. Then
$\psi(2^2) = \psi(2)^2 = 1 = \psi(1)$, and since $\psi$ is injective, $2^2 = 1$ in $\mathbb{Z}/5\mathbb{Z}$.
But $2^2 = 4 \neq 1$. So no isomorphism exists.

</details>

---

### Exercise 8

Find the integers $x$ with $0 \le x < 105$ such that

$$x \equiv 2 \pmod 3, \qquad x \equiv 3 \pmod 5, \qquad x \equiv 2 \pmod 7.$$

<details>
<summary>Solution</summary>

$3, 5, 7$ are pairwise coprime and $3 \cdot 5 \cdot 7 = 105$. By the CRT (Theorem 1.3.7) the map
$\mathbb{Z}/105\mathbb{Z} \to \mathbb{Z}/3\mathbb{Z} \times \mathbb{Z}/5\mathbb{Z} \times \mathbb{Z}/7\mathbb{Z}$ is bijective,
so there is **exactly one** solution in $\lbrace 0, \dots, 104 \rbrace$.

To find it, solve the first two congruences together. The numbers $\equiv 3 \pmod 5$ are $3, 8, 13, \dots$;
the first one that is also $\equiv 2 \pmod 3$ is $8$. So $x \equiv 8 \pmod{15}$.

Now the candidates are $8, 23, 38, \dots$; the first one that is $\equiv 2 \pmod 7$ is $23$ ($23 = 3 \cdot 7 + 2$).

**Solution:** $x = 23$.

</details>

---

### Exercise 9

In $\mathbb{Z}/4\mathbb{Z} \times \mathbb{Z}/3\mathbb{Z}$, count the invertible elements and the zero divisors.
Then use the CRT to explain why the answer matches $\mathbb{Z}/12\mathbb{Z}$.

<details>
<summary>Solution</summary>

By Lemma 1.3.1, $(a, b)$ is invertible if and only if both components are:
$a \in \lbrace 1, 3 \rbrace$ and $b \in \lbrace 1, 2 \rbrace$, so **4 invertible elements**.

Out of 12 elements, one is zero, and every other element of a finite ring is invertible or a zero divisor (Theorem 1.1.7).
So there are $12 - 1 - 4 = 7$ **zero divisors**.

By the CRT, $\mathbb{Z}/12\mathbb{Z} \cong \mathbb{Z}/4\mathbb{Z} \times \mathbb{Z}/3\mathbb{Z}$, and an isomorphism maps units to units
(Lemma 1.3.5). Indeed $\mathbb{Z}/12\mathbb{Z}$ also has 4 units ($\varphi(12) = 4$) and 7 zero divisors (see Exercise 3).

</details>

---

### Exercise 10

The homomorphism $p : \mathbb{Z}/21\mathbb{Z} \to \mathbb{Z}/7\mathbb{Z}$, $[a]_{21} \mapsto [a]_7$, maps $[5]_{21}$ to $[5]_7$.
Without computing $[5]_7^{-1}$ directly, find it from $[5]_{21}^{-1}$.
Then give an example showing that $p$ does not map zero divisors to zero divisors.

<details>
<summary>Solution</summary>

$5 \cdot 17 = 85 = 4 \cdot 21 + 1$, so $[5]_{21}^{-1} = [17]_{21}$.
By Lemma 1.3.3, $[5]_7^{-1} = p([17]_{21}) = [17]_7 = [3]_7$. Check: $5 \cdot 3 = 15 = 2 \cdot 7 + 1$.

$[3]_{21}$ is a zero divisor ($3 \cdot 7 = 21 \equiv 0$), but $p([3]_{21}) = [3]_7$ is invertible, because $\mathbb{Z}/7\mathbb{Z}$ is a field.

</details>

---

### Exercise 11

Compute the order of every element of $(\mathbb{Z}/7\mathbb{Z})^\ast$. Is the group cyclic? Which elements are generators, and how many should there be?

<details>
<summary>Solution</summary>

The group has order $\varphi(7) = 6$, so the possible orders are $1, 2, 3, 6$ (Lagrange).

- $2$: $2, 4, 8 \equiv 1$, so $o(2) = 3$.
- $3$: $3, 9 \equiv 2, 6, 18 \equiv 4, 12 \equiv 5, 15 \equiv 1$, so $o(3) = 6$.
- $4 = 2^2$: $o(4) = \frac{3}{\gcd(3, 2)} = 3$ (Lemma 1.4.5).
- $5 = 3^5$ (from the list above): $o(5) = \frac{6}{\gcd(6, 5)} = 6$.
- $6 \equiv -1$: $(-1)^2 = 1$, so $o(6) = 2$.
- $o(1) = 1$.

There is an element of order 6, so the group is cyclic (Lemma 1.4.8). The generators are $3$ and $5$: exactly $\varphi(6) = 2$, as Lemma 1.4.9 predicts.

</details>

---

### Exercise 12

Show that $[3]$ is a generator of $(\mathbb{Z}/31\mathbb{Z})^\ast$, using Lemma 1.4.16. You may use: $3^{15} \equiv 30$, $3^{10} \equiv 25$, $3^6 \equiv 16 \pmod{31}$.

<details>
<summary>Solution</summary>

The group has order $\varphi(31) = 30 = 2 \cdot 3 \cdot 5$. The primes dividing 30 are 2, 3, 5, and the exponents to test are $30/2 = 15$, $30/3 = 10$, $30/5 = 6$.
None of $3^{15}, 3^{10}, 3^6$ is $\equiv 1$, so by Lemma 1.4.16 $o([3]) = 30$: $[3]$ is a generator and the group is cyclic.

Three tests instead of checking the 8 divisors of 30 one by one.

</details>

---

### Exercise 13

Is $(\mathbb{Z}/20\mathbb{Z})^\ast$ cyclic? Answer in two ways: with Theorem 1.4.18, and by computing the largest possible order of an element with Lemma 1.4.14.

<details>
<summary>Solution</summary>

**With the theorem.** $20 = 4 \cdot 5$ with $4, 5 \ge 3$ and $\gcd(4, 5) = 1$: case 1, so **not cyclic**.

**With orders.** $(\mathbb{Z}/20\mathbb{Z})^\ast \cong (\mathbb{Z}/4\mathbb{Z})^\ast \times (\mathbb{Z}/5\mathbb{Z})^\ast$, of orders 2 and 4. An element of the first factor has order 1 or 2,
one of the second has order 1, 2 or 4. The order of a pair is the lcm, at most $\mathrm{lcm}(2, 4) = 4$. But the group has order $\varphi(20) = 8$, so no element generates it.

Directly: $(\mathbb{Z}/20\mathbb{Z})^\ast = \lbrace 1, 3, 7, 9, 11, 13, 17, 19 \rbrace$, and $3, 7, 13, 17$ have order 4, while $9, 11, 19$ have order 2.

</details>

---

### Exercise 14

How many elements of each order does $(\mathbb{Z}/21\mathbb{Z})^\ast$ have? Follow the method of the $(\mathbb{Z}/75\mathbb{Z})^\ast$ example.

<details>
<summary>Solution</summary>

$21 = 3 \cdot 7$, so $(\mathbb{Z}/21\mathbb{Z})^\ast \cong (\mathbb{Z}/3\mathbb{Z})^\ast \times (\mathbb{Z}/7\mathbb{Z})^\ast$, cyclic groups of orders 2 and 6. It has $2 \cdot 6 = 12$ elements.

In a cyclic group there are $\varphi(a)$ elements of order $a$:

- $(\mathbb{Z}/3\mathbb{Z})^\ast$: order 1: 1 element; order 2: 1 element.
- $(\mathbb{Z}/7\mathbb{Z})^\ast$: order 1: 1; order 2: 1; order 3: $\varphi(3) = 2$; order 6: $\varphi(6) = 2$.

A pair has order equal to the lcm of the orders:

| order | pairs (order in $\mathbb{Z}/3$, order in $\mathbb{Z}/7$) | count |
|---|---|---|
| 1 | (1, 1) | $1 \cdot 1 = 1$ |
| 2 | (2, 1), (1, 2), (2, 2) | $1 + 1 + 1 = 3$ |
| 3 | (1, 3) | $1 \cdot 2 = 2$ |
| 6 | (2, 3), (1, 6), (2, 6) | $2 + 2 + 2 = 6$ |

Total $1 + 3 + 2 + 6 = 12$. No element of order 12: not cyclic (again case 1 of Theorem 1.4.18, $21 = 3 \cdot 7$).

</details>

---

### Exercise 15

Compute $3^{100} \bmod 7$ and $2^{1000} \bmod 13$ without a computer.

<details>
<summary>Solution</summary>

By Fermat, $3^6 \equiv 1 \pmod 7$, so exponents only matter modulo 6 (Corollary 1.4.4). $100 = 6 \cdot 16 + 4$, so $3^{100} \equiv 3^4 = 81 = 11 \cdot 7 + 4 \equiv 4$.

By Fermat, $2^{12} \equiv 1 \pmod{13}$. $1000 = 12 \cdot 83 + 4$, so $2^{1000} \equiv 2^4 = 16 \equiv 3$.

</details>

---

### Exercise 16

Find $[5]^{-1}$ in $(\mathbb{Z}/13\mathbb{Z})^\ast$ and $[7]^{-1}$ in $(\mathbb{Z}/15\mathbb{Z})^\ast$ using Lemma 1.4.11 (3), then check with a multiplication.

<details>
<summary>Solution</summary>

**Modulo 13**, the group has order 12, so $[5]^{-1} = [5]^{11}$. Since $5^2 = 25 \equiv -1$, we get $5^4 \equiv 1$, so actually $o(5) = 4$ and $5^{11} = 5^{8} \cdot 5^{3} \equiv 5^3 = 5^2 \cdot 5 \equiv -5 \equiv 8$.
Check: $5 \cdot 8 = 40 = 3 \cdot 13 + 1$.

**Modulo 15**, the group has order $\varphi(15) = 8$, so $[7]^{-1} = [7]^7$. We know $7^2 \equiv 4$ and $7^4 \equiv 1$, so $7^7 = 7^4 \cdot 7^2 \cdot 7 \equiv 4 \cdot 7 = 28 \equiv 13$.
Check: $7 \cdot 13 = 91 = 6 \cdot 15 + 1$.

Using the order instead of $\lvert G \rvert$ is quicker: $g^{-1} = g^{o(g) - 1}$ too, for example $[7]^{-1} = [7]^3 = [13]$.

</details>

