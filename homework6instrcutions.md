# FINM 32000: Homework 6

Due Friday May 15, 2026 at 11:59pm

## Problem 1

Let $S$ be the column vector with components $S^{[1]}, S^{[2]}$, where the stock prices $S^{[j]}$ have risk-neutral dynamics

$$
dS_t^{[j]} = rS_t^{[j]}\,dt + \sigma^{[j]}S_t^{[j]}\,dW_t^{[j]}, \qquad j = 1,2
$$

with risk-free interest rate $r = 0.05$, and constant volatilities $\sigma^{[1]} = 0.3$, $\sigma^{[2]} = 0.2$. The time-0 prices are $S_0^{[1]} = 100$, $S_0^{[2]} = 110$. The $P$-Brownian motions $W^{[1]}$ and $W^{[2]}$ have correlation $\rho = 0.8$.

### (a)

Let $X$ be the column vector with components $X^{[1]}, X^{[2]}$ where $X^{[j]} := \log S^{[j]}$. Find the covariance matrix of $X_T$.

Hint: One approach is to manually fill in the covariance matrix, using relationships such as

$$
\operatorname{Cov}(W_T^{[1]}, W_T^{[2]}) = 0.8T
$$

in combination with the volatilities.

Another approach is to use matrix multiplication: write $X_T$ as a nonrandom vector plus $\Sigma W_T$ where $\Sigma$ is the nonrandom diagonal matrix with diagonal elements $\sigma^{[1]}, \sigma^{[2]}$, and $W$ is the random column vector with components $W^{[1]}, W^{[2]}$. Then

$$
\operatorname{Cov}(X_T)
= E(\Sigma W_T W_T^\top \Sigma^\top)
= \Sigma \operatorname{Cov}(W_T)\Sigma^\top
= T\Sigma \operatorname{Corr}(W_T)\Sigma^\top.
$$

Consider a basket

$$
H := \frac{1}{2}S^{[1]} + \frac{1}{2}S^{[2]}
$$

of one-half of a share of each stock.

### (b)

Using 10000 standard Monte Carlo simulations, estimate the time-0 price $C$ of an option that pays $(H_T - 110)^+$ at time $T = 1.0$. Also give the standard error [the sample standard deviation, divided by the square root of the number of simulations] of your Monte Carlo estimate.

You may either use a random number generator that produces normals with a given covariance matrix (which you found in (a)), or alternatively use a random number generator that produces independent normals which you then transform to introduce correlation.

In either approach, each of the 10000 simulations should use just one $\mathbb{R}^2$-valued random vector $Z$ of simulated normal zero-mean random variables.

### (c)

Use 10000 antithetic pairs $(Z, -Z)$ to estimate $C$, together with a standard error (L6.8).

Consider the "geometric basket"

$$
G := \left(S^{[1]}S^{[2]}\right)^{1/2}.
$$

### (d)

The random variable $\log G_T$ is normally distributed (because it's a linear transformation of a multivariate normal vector). Show that $\log G_T$ has expectation

$$
\frac{1}{2}\log(S_0^{[1]}S_0^{[2]})
+ \left(r - \frac{(\sigma^{[1]})^2 + (\sigma^{[2]})^2}{4}\right)T
$$

and variance

$$
\frac{(\sigma^{[1]})^2 + 2\rho\sigma^{[1]}\sigma^{[2]} + (\sigma^{[2]})^2}{4}T.
$$

### (e)

Let $C_G$ be the time-0 price of a geometric basket option paying $(G_T - K)^+$ at time $T$. Express $C_G$ in terms of the function $C_{BS}$ defined in FINM 33000 L6. Specifically, fill in the blanks:

$$
C_G = C_{BS}(\underline{\hspace{3cm}}, 0, K, T, \underline{\hspace{3cm}}, r, \underline{\hspace{3cm}}).
$$

Your answer should be a general formula, in which you have not substituted $0.8$ for $\rho$, etc. (You may also do the substitutions, but don't neglect the general formula).

### (f)

Using a geometric basket option as a control variate, run $M = 10000$ Monte Carlo simulations to estimate $C$, together with a standard error. Use the control variate estimate $\hat{C}^{cv,\hat{\beta}}_M$ from L6.13 or L6.14. Use the (asymptotically valid) standard error $\hat{\sigma}^{cv,\hat{\beta}}_M / \sqrt{M}$.

See the ipynb file.

## Problem 2

Each unit of the bank account has price $B_t = e^{rt}$ for all $t \ge 0$.

### (a)

Let $S_t$ be the time-$t$ price of a stock that continuously pays a constant proportional dividend yield $q$. This means that each 1 share of $S$ at time 0 will grow, via dividend reinvestment, to $e^{qt}$ shares of $S$ at each time $t \ge 0$. Thus the stock, divorced from its dividend stream, should not be regarded as a holdable/tradeable asset. Rather, units of the "bundle" should be regarded as holdable/tradeable, where 1 unit of the bundle is defined to be

$$
e^{qt} \text{ shares of stock, at all times } t \ge 0.
$$

Aside from the above information, do not assume any specific dynamics for $S$.

By replication, find the time-$t$ value of a forward contract which pays $S_T - K$ at time $T$, where $t \le T$. How many shares of $S$, and what dollar value in the bank account, does the replicating portfolio hold at time $t$?

Conclude that the time-$t$ forward price for time-$T$ delivery of $S_T$ is

$$
F_t = S_t e^{(r-q)(T-t)}.
$$

(The forward price is not the same thing as the value of a forward contract.)

### (b)

Let $S_t$ be the time-$t$ price of a stock that pays a fixed dollar dividend $D$ discretely at time $T_0$, where $0 < T_0 < T$. Assume $S$ does not pay any other dividends between time 0 and $T$.

Let us regard as holdable/tradeable the following bundle. One unit of the bundle consists of:

| Holding | Time |
| --- | --- |
| 1 share | at all times $t < T_0$ |
| 1 share plus $De^{-rT_0}$ units of bank account | at all times $t \ge T_0$ |

Like the case of a continuous proportional dividend yield in (a), the bundle here in (b) absorbs the dividend payments. Unlike (a), the bundle in (b) allocates the dividend into bank account units, not into more stock shares. We are still not assuming any specific dynamics for $S$.

By replication, find the time-$t$ value of a forward contract which pays $S_T - K$ at time $T$. How many shares of $S$, and what dollar value in the bank account, does the replicating portfolio hold at time $t$? The answer depends on whether $t < T_0$ or $t \ge T_0$.

Conclude that the time-$t$ forward price for time-$T$ delivery of $S_T$ is

$$
F_t =
\begin{cases}
S_t e^{r(T-t)}, & \text{if } t \ge T_0, \\
S_t e^{r(T-t)} - De^{r(T-T_0)}, & \text{if } t < T_0.
\end{cases}
$$

(The forward price is not the same thing as the value of a forward contract.)

Intuitively, $F_t = E_t S_T$ can be calculated by growing $S_t$ using drift $r$ from today $t$ until delivery date $T$, combined with growing the $-D$ dollars, from the date $T_0$ when $S$ gives away the $D$ dollars, until the forward contract's delivery date $T$. (This does not require comment from you, this is just giving you a different perspective on the replication result.)

## Price dynamics of stocks that pay dividends

To prepare for part (c) below: Diffusion/SDE models of price dynamics easily adapt to include continuous dividend yields, but a more realistic dividend model for single stocks is a discrete dividend.

- The dynamics of a stock $S$ that pays out a continuous dividend $q$ can be modeled by adjusting the drift to $r - q$, meaning that the drift term is $(r - q)S_t\,dt$.

  When pricing Americans, the early exercise condition needs to be checked at every time step.

- The dynamics of a stock $S$ that pays a discrete dividend of $D$ dollars to holders at time $T_0$ can be modeled with a drift of $r$, along with a down-jump of $D$ dollars at time $T_0$. But what prevents $S$ from going negative due to the down-jump? A simple approach is to use the SDE to model the forward price dynamics (which will not jump at time $T_0$), rather than directly modeling the spot $S$. The initial spot $S_0$ needs to be converted into a forward price, which evolves according to the SDE. When a payout of an option on $S$ needs to be computed, the forward needs to be converted back into spot. These conversions use the (b) result.

  When pricing Americans, assuming $r \ge 0$, the early exercise condition needs to be checked only at time $T_0$, immediately prior to the stock dropping $D$ dollars.

### (c)

Complete the code in `finm320-26-hw6-p2.ipynb` to find, using finite differences, the time-0 price of a 100-strike 0.25-expiry American call option on a stock $S$ that pays a discrete dividend of 2 dollars at time 0.15, assuming that the time-$t$ forward price $X_t$ for the time-0.25 delivery of $S$ has the CEV dynamics

$$
dX_t = 3X_t^{0.5}\,dW_t
$$

and $r = 0.05$.

Only two lines of code need to be completed.

The $F$ notation here corresponds to the $X$ notation in the Python code.
