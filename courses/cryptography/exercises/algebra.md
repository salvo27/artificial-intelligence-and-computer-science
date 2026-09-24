# Algebra: exercises

Exercises on sections 1.1, 1.2 and 1.3 of the notes, with solutions.
Exercises 1 and 2 are the proofs the notes leave to the reader; the others practice the computations.
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
