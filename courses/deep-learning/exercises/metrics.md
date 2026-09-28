# Exercises: metrics, softmax and gradient descent

Exercises on sections 1 and 2 of the [summary](../summary.md), with solutions.
Exercises 1 and 2 use the example data of the notebook `ML_metrics.ipynb`, so you can check the results by running it;
the others are not in the course material and are meant for practice.

---

### Exercise 1

A binary classifier gives these predictions (1 = positive):

| | | | | | | | | | | |
|---|---|---|---|---|---|---|---|---|---|---|
| **true** | 1 | 0 | 1 | 1 | 0 | 0 | 1 | 0 | 1 | 0 |
| **predicted** | 1 | 0 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 0 |

Build the confusion matrix, then compute accuracy, precision, recall and F1.

<details>
<summary>Solution</summary>

Going through the ten pairs:

- TP (true 1, predicted 1): positions 1, 3, 7, so **TP = 3**;
- FN (true 1, predicted 0): positions 4, 9, so **FN = 2**;
- FP (true 0, predicted 1): position 6, so **FP = 1**;
- TN (true 0, predicted 0): positions 2, 5, 8, 10, so **TN = 4**.

|  | Predicted positive | Predicted negative |
|---|---|---|
| **Actually positive** | 3 | 2 |
| **Actually negative** | 1 | 4 |

$$\text{Accuracy} = \frac{3 + 4}{10} = 0.7 \qquad \text{Precision} = \frac{3}{3 + 1} = 0.75 \qquad \text{Recall} = \frac{3}{3 + 2} = 0.6$$

$$F_1 = 2 \cdot \frac{0.75 \cdot 0.6}{0.75 + 0.6} = \frac{0.9}{1.35} \approx 0.667$$

These are the values printed by the notebook. Note that `confusion_matrix` of scikit-learn puts the negative class first, so it prints
`[[4, 1], [2, 3]]`: rows are the true classes (0, then 1), columns the predicted ones.

</details>

---

### Exercise 2

True values $[3, -0.5, 2, 7]$, predictions $[2.5, 0, 2, 8]$. Compute MAE, MSE and RMSE.

<details>
<summary>Solution</summary>

The errors $y_i - \hat{y}_i$ are $0.5, -0.5, 0, -1$.

$$\text{MAE} = \frac{0.5 + 0.5 + 0 + 1}{4} = 0.5 \qquad \text{MSE} = \frac{0.25 + 0.25 + 0 + 1}{4} = 0.375 \qquad \text{RMSE} = \sqrt{0.375} \approx 0.612$$

The error of 1 is half of the total absolute error, but two thirds of the total squared error: squaring gives more weight to the largest mistake.

</details>

---

### Exercise 3

A mailbox receives 1,000 emails, 50 of which are spam. A filter marks 50 emails as spam: 40 are really spam, 10 are good emails.

1. Compute accuracy, precision and recall, with "spam" as the positive class.
2. A second filter never marks anything as spam. What is its accuracy? Which metric shows that it is useless?

<details>
<summary>Solution</summary>

1. TP = 40, FP = 10, FN = 50 - 40 = 10, TN = 950 - 10 = 940.
   Accuracy = $(40 + 940)/1000 = 0.98$, precision = $40/50 = 0.8$, recall = $40/50 = 0.8$.
2. TP = 0, FP = 0, FN = 50, TN = 950. Accuracy = $950/1000 = 0.95$: almost as good as the real filter.
   But recall = $0/50 = 0$: it catches no spam at all. With imbalanced classes, accuracy alone is misleading.

</details>

---

### Exercise 4

Apply softmax to the scores $[1, 2, 3]$. Then add 10 to every score and apply it again: what changes?

<details>
<summary>Solution</summary>

$e^1 \approx 2.718$, $e^2 \approx 7.389$, $e^3 \approx 20.086$, with sum $30.193$. The probabilities are about $0.090$, $0.245$, $0.665$.

Adding 10 to every score multiplies every $e^{y_i}$ by the same factor $e^{10}$, which cancels out between numerator and denominator:
**the probabilities do not change**. Softmax depends only on the differences between the scores.

</details>

---

### Exercise 5

Gradient descent on $e(w) = w^2$ (that is, $\frac{1}{2} C w^2$ with $C = 2$), starting from $w = 4$.
Do three steps with $\eta = 0.25$, $0.5$, $0.75$ and $1.25$. Which behavior of the summary's table do you get each time?

<details>
<summary>Solution</summary>

$e'(w) = 2w$, so each step is $w \leftarrow w - 2\eta w = (1 - 2\eta)\, w$. The thresholds of the summary are $1/C = 0.5$ and $2/C = 1$.

| $\eta$ | factor $1 - 2\eta$ | $w$ after 1, 2, 3 steps | behavior |
|---|---|---|---|
| 0.25 | 0.5 | 2, 1, 0.5 | $\eta < 1/C$: slow, steady convergence |
| 0.5 | 0 | 0, 0, 0 | $\eta = 1/C$: minimum in one step |
| 0.75 | -0.5 | -2, 1, -0.5 | $1/C < \eta < 2/C$: converges oscillating |
| 1.25 | -1.5 | -6, 9, -13.5 | $\eta > 2/C$: diverges |

</details>

---

### Exercise 6

Verify that the neuron $h(x) = g(+10 - 20 x_1 - 20 x_2)$, with $g$ the sigmoid, computes (NOT $x_1$) AND (NOT $x_2$).
Then find weights for a neuron computing $x_1$ AND (NOT $x_2$).

<details>
<summary>Solution</summary>

| $x_1$ | $x_2$ | $10 - 20x_1 - 20x_2$ | $h(x)$ |
|---|---|---|---|
| 0 | 0 | 10 | $\approx 1$ |
| 0 | 1 | -10 | $\approx 0$ |
| 1 | 0 | -10 | $\approx 0$ |
| 1 | 1 | -30 | $\approx 0$ |

It is 1 only when both inputs are 0.

For $x_1$ AND (NOT $x_2$) the output must be 1 only for $(1, 0)$. One choice is $g(-10 + 20 x_1 - 20 x_2)$:
$(0,0) \to -10$, $(0,1) \to -30$, $(1,0) \to 10$, $(1,1) \to -10$. Only $(1, 0)$ gives a positive sum. Many other weights work too.

</details>
