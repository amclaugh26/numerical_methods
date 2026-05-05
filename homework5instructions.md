# FINM 32000: Homework 5

**Due Friday May 8, 2026 at 11:59pm**

---

## Problem 1

Let $r$ be the constant interest rate. Let $0 < T_1 < T_2$.

### (a)

Let $F_t$ be the time-$t$ forward price for $T_2$-delivery of some arbitrary underlying $S$, not necessarily tradeable. Recall that a forward price is not the same thing as the value of a forward contract. By definition of the time-$t$ forward price $F_t$ for $T_2$-delivery:

> a forward contract paying $S_{T_2} - F_t$ at time $T_2$ has time-$t$ value $0$.

Let $f_t$ be the time-$t$ value of a $T_2$-forward contract on the same underlying, but with some delivery price $K$ (not necessarily equal to $F_t$).

Express $f_t$ in terms of $K$ and $F_t$ and a discount factor.

*Hint:* Consider a portfolio long one $(K, T_2)$-forward contract and short one $(F_t, T_2)$-forward contract. The portfolio has (in terms of $f_t$) what value at time $t$? The portfolio pays how much at expiration?

---

### (b)

If $S$ is a stock paying no dividends, the forward price must be $F_t = S_t e^{r(T_2 - t)}$; otherwise, arbitrage would exist.

> If, say, $F_t > S_t e^{r(T_2 - t)}$, then arbitrage would exist: at time $t$, borrow $S_t$ dollars, buy the stock, and short the forward (with delivery price $F_t$ and time-$t$ value $0$). At time $T_2$, deliver the stock, and receive $F_t$, which is more than enough to cover your accumulated debt of $S_t e^{r(T_2 - t)}$ dollars.

However, if $S$ is the spot price of a barrel of crude oil (so, for all $t$, the time-$t$ price for time-$t$ delivery is $S_t$ per barrel), then this argument fails. Explain briefly (one or two sentences, no math) why this specific arbitrage does not apply to crude oil, by specifically pinpointing, in the quote above, why we cannot simply replace "stock" with "crude oil."

*Hint:* Consider practical complications.

---

So we need more assumptions to relate $F_t$ and $S_t$ (here and in (c)–(g), $S$ denotes spot crude oil, and $F_t$ denotes the time-$t$ forward price for $T_2$-delivery crude oil). One approach is to assume a specific model of the risk-neutral dynamics of $S$. For instance, let us assume that $S$ satisfies the **Exponential Ornstein–Uhlenbeck (XOU)** model:

$$
S_t = \exp(X_t), \qquad dX_t = \kappa(\alpha - X_t)\,dt + \sigma\,dW_t
$$

where $W$ is Brownian motion under risk-neutral measure.

Then, since $r$ is constant and $E_t\!\left(e^{-r(T_2-t)}(S_{T_2} - F_t)\right)$ must be $0$, one can calculate

$$
F_t = E_t(S_{T_2}) = \exp\!\left[ e^{-\kappa(T_2-t)}\log S_t + \alpha\!\left(1 - e^{-\kappa(T_2-t)}\right) + \frac{\sigma^2}{4\kappa}\!\left(1 - e^{-2\kappa(T_2-t)}\right) \right]
$$

where $E_t$ is time-$t$ conditional expectation. Suppose $\kappa = 0.472$, $\alpha = 4.4$, $\sigma = 0.368$, $r = 0.05$, and the time-$0$ spot price is $S_0 = 106.9$.

Let $C$ be the time-$0$ price of a $K$-strike $T_1$-expiry European call on $F$. So this call pays $(F_{T_1} - K)^+$. Let the call option have strike $K = 103.2$ and expiration $T_1 = 0.5$. Let the forward have delivery date $T_2 = 0.75$. See `finm320-26-hw5.ipynb`.

---

### (c) — *Coding task*

Estimate $C(S_0)$ using Monte Carlo simulation of $S$ with 100 timesteps on $[0, T_1]$. Choose the number of paths large enough that the standard error (the sample standard deviation divided by the square root of the number of paths) is less than $0.05$. Report the standard error. Do not use any variance reduction technique.

---

### (d) — *Coding task*

Estimate $\partial C / \partial S$ by using Monte Carlo simulation to calculate

$$
\frac{C(S_0 + 0.01) - C(S_0)}{0.01}
$$

For the $C(S_0 + 0.01)$ calculation, reuse the same normal random variables which you generated for the $C(S_0)$ calculation. (Do not re-generate random variables to compute $C(S_0 + 0.01)$.)

---

### (e)

Calculate analytically $\partial f_0 / \partial S$, where $f_0$ is the time-$0$ value of a position long one forward contract on a barrel of crude oil, with delivery date $T_2$ and some fixed delivery price $K$.

---

### (f)

Suppose you want to hedge a position short one call (so your hedge portfolio should replicate a position long one call), by continuously rebalancing a position in $T_2$-delivery forward contracts. Your hedge portfolio at time $0$ should be long how many forward contracts? Your final answer should be a number.

The delivery price $K$ of the forward contracts is irrelevant to the answer here; it would affect only how many units of the bank account to carry in the portfolio (which I am not asking you to compute).

---

### (g)

Consider the following "purchase agreement" contract. The holder of this contract receives time-$T_2$ delivery of $\lambda$ barrels of crude oil, and pays, at time $T_2$, a delivery price of $K$ dollars per barrel. The $\lambda$ is chosen at time $T_1$ by the holder of the purchase agreement, subject to the restriction that $4000 \leq \lambda \leq 5000$; in particular, $\lambda = 0$ is not a valid choice, because the contract is a commitment to purchase at least 4000 barrels. Using your answer to (c), without running any new simulations, find the time-$0$ value of this contract.

Here $K$, $T_1$, $T_2$ have the same values as above.

*Hint:* Assume the holder acts optimally; thus $\lambda$ is either $4000$ or $5000$, depending on $F_{T_1}$.

---

## Problem 2

Suppose that a non-dividend-paying stock has dynamics

$$
dS_t = rS_t\,dt + \sigma(t)S_t\,dW_t \tag{1}
$$

where $W$ is Brownian motion under risk-neutral probabilities, and where the time-dependent but non-random volatility function $\sigma : [0, T] \to \mathbb{R}$ is piecewise continuous and sufficiently integrable.

Lecture 2.29 shows that this particular type of local volatility function $\sigma$ (to be specific: the type of function that depends on $t$ but does not depend on $S$, nor on anything else that is random) has an explicit relationship with the Black-Scholes implied volatility $\sigma_{\text{imp}}$.

### (a)

Are the dynamics (1) capable of generating a non-constant (with respect to $T$) term-structure of implied volatility? Are they capable of generating an implied volatility skew (non-constant with respect to $K$)? Explain briefly.

---

### (b)

Let $S_0 = 100$ and $r = 0.05$. At time $0$, you observe the prices of at-the-money ($K = 100$) European calls at $0.1$-year, $0.2$-year, and $0.5$-year expiries to be $5.25$, $7.25$, and $9.5$, respectively. First find the Black-Scholes implied volatilities of the three options. Then find (calibrate) a time-varying local volatility function $\sigma : [0, 0.5] \to \mathbb{R}$ consistent with these option prices. A step function suffices (but other answers are also acceptable).

---

### (c)

Consistently with your local volatility function $\sigma$ from part (b), find the time-$0$ price of an at-the-money European call with expiry $0.4$, and find the time-$0.1$ implied volatility of that call (the European call with expiry $T = 0.4$). Do not use a tree or finite difference or Monte Carlo calculation.

---

## Notebook Coding Todos — `finm320-26-hw5.ipynb`

### `MCengine.price_call_XOU(contract, dynamics)` — answers 1(c) and 1(d)

This is the only stub requiring implementation. It must return `(call_price, standard_error, call_delta)`.

**What to implement:**

1. **Simulate XOU paths** using Euler-Maruyama on the OU process for $X_t = \log S_t$ over $N = 100$ timesteps on $[0, T_1]$.
   - Draw all standard normals using `self.rng.normal()`.
   - Simulate paths for $S_0$ (baseline) and for $S_0 + \varepsilon$ (bump), **reusing the same normals** — shift the initial condition of $X_0$, not the noise.

2. **Compute forward price** $F_{T_1}$ at each path endpoint using the closed-form formula:
   $$F_{T_1} = \exp\!\left[ e^{-\kappa(T_2-T_1)}\log S_{T_1} + \alpha\!\left(1 - e^{-\kappa(T_2-T_1)}\right) + \frac{\sigma^2}{4\kappa}\!\left(1 - e^{-2\kappa(T_2-T_1)}\right) \right]$$

3. **Compute call payoff** $\max(F_{T_1} - K_1, 0)$ on each path, discount at $e^{-rT_1}$, and average → `call_price`.

4. **Standard error** → sample standard deviation of discounted payoffs divided by $\sqrt{M}$ → `standard_error`. Adjust $M$ (currently `1000`) upward until SE $< 0.05$.

5. **Delta** → run the same simulation with $S_0 + \varepsilon$ using the same normals, compute the bumped call price, and return $(\text{bumped price} - \text{call\_price}) / \varepsilon$ → `call_delta`. Here `epsilon = 0.01`.

**Notebook wiring:**
- `hw5dynamics = XOU(kappa=0.472, alpha=4.4, sigma=0.368, S0=106.9, r=0.05)`
- `hw5contract = CallOnForwardPrice(K1=103.2, T1=0.5, T2=0.75)`
- `hw5MC = MCengine(N=100, M=1000, epsilon=0.01, seed=0)` — increase `M` as needed

**No coding required for:** Problems 1(a), 1(b), 1(e), 1(f), 1(g), or Problem 2 (all analytical/written).
