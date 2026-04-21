# FINM 32000: Homework 4

**Due Wednesday April 22, 2026 at 11:59pm**

---

## Problem 1

Assume that the short rate (the instantaneous spot rate of interest) follows the process

$$
dr_t = \mu(r_t, t)\,dt + \sigma(r_t, t)\,dW_t
$$

where $W_t$ is Brownian motion under risk-neutral probabilities. This framework includes models such as the Vasicek and CIR models, which correspond to particular choices of the functions $(\mu, \sigma)$, but for part (a), let's leave $\mu$ and $\sigma$ as unspecified functions.

### (a)

Consider an interest rate derivative whose time-$T$ payout has value given by some function $F(r_T)$, and whose time-$t$ price $C_t$ satisfies $C_t = C(r_t, t)$ for some smooth pricing function $C$.

Apply Ito's rule to find the risk-neutral dynamics of $C$. Then set its drift equal to $rC$, to derive a PDE for $C(r, t)$.

---

Suppose, in particular, that the risk-neutral dynamics of $r$ are given by a Vasicek model

$$
dr_t = \kappa(\theta - r_t)\,dt + \sigma\,dW_t,
$$

with parameters $\kappa = 3$, $\theta = 0.05$, $\sigma = 0.03$. Consider a $T = 5$-year discount bond (a zero-coupon bond which pays 1 at maturity $T$).

### (b)

Write code to find the time-0 price of the bond by applying a standard central-difference explicit finite difference scheme to the PDE in (a). (Therefore $C_j^n$ will be determined by $C_{j+1}^{n+1}$, $C_j^{n+1}$, and $C_{j-1}^{n+1}$.)

Complete the code in the file `finm320-26-hw4.ipynb`.

### (c)

Also write code to price the bond using an explicit upwind approximation to $\frac{\partial C}{\partial r}$ instead of the usual central difference. Specifically, for those $r_j$ such that $\kappa(\theta - r_j) \geq 0$, approximate $\frac{\partial C}{\partial r}(r_j, t_{n+1})$ using the points $C_{j+1}^{n+1}$ and $C_j^{n+1}$. For those $r_j$ such that $\kappa(\theta - r_j) < 0$, approximate $\frac{\partial C}{\partial r}(r_j, t_{n+1})$ using the points $C_j^{n+1}$ and $C_{j-1}^{n+1}$. (For $\frac{\partial^2 C}{\partial r^2}$, use the usual central-difference approximation.)

In (b) and (c), to approximate the PDE's $rC$ term, use the values of $r$ and $C$ at node $(n, j)$. (As we said in class, node $(n+1, j)$ would also be a natural choice, but let's choose $n$ instead of $n+1$.) At the grid's upper and lower boundaries $r_{\max}$ and $r_{\min}$, impose for all $t < T$ the "linearity" boundary conditions:

$$
C(r_{\max}, t) = 2C(r_{\max} - \Delta r, t) - C(r_{\max} - 2\Delta r, t)
$$

$$
C(r_{\min}, t) = 2C(r_{\min} + \Delta r, t) - C(r_{\min} + 2\Delta r, t)
$$

(This technique can help in some situations where it is not obvious what boundary conditions to use.) Thus, in each column of the grid, first solve for $C$ in the interior nodes; then deal with the top and bottom nodes.

### (d)

Suppose $f : \mathbb{R} \to \mathbb{R}$ is smooth in some open neighborhood of $x$. Show that as $h \to 0$,

$$
\frac{f(x+h) - f(x)}{h} - f'(x) = O(h)
\qquad \text{and} \qquad
\frac{f(x+h) - f(x-h)}{2h} - f'(x) = O(h^2)
$$

using Taylor's theorem. The $O(h)$ means "some function bounded by a constant times $h$, near $h = 0$." Likewise, $O(h^2)$ means "some function bounded by a constant times $h^2$, near $h = 0$." Different instances of "$O$" may mean different functions. The "constants" may depend on $x$ but not $h$.

### (e)

For all part (e) calculations: Use the grid spacings $\Delta r = 0.01$ and $\Delta t = 0.01$. Use $r_{\max} = 0.35$ and $r_{\min} = -0.25$ for the upper and lower boundaries of the grid, respectively.

Run a central-difference calculation and an upwind calculation of the bond price for $r_0 = 0.10$. Which is more accurate? The more accurate of the two solutions should agree, to three significant digits, with the exact bond price in this model: **0.7661**. The less accurate of the two solutions will be very inaccurate.

### (f)

Based on your answers to (d) and (e), insert either **"greater"** or **"less"** in each blank space in the following rule-of-thumb. No explanation necessary.

> Ignoring stability issues and considering only consistency (i.e. "truncation error," also known as "local discretization error"), the upwind explicit scheme, which uses one-sided spatial differences, discretizes the PDE with ________ accuracy than the standard explicit scheme, which uses central spatial differences.
>
> However, to actually guarantee convergence, the grid spacing must satisfy certain stability constraints, to prevent errors from propagating explosively. In a PDE exhibiting strong drift, we have seen that these constraints may allow the upwind scheme ________ freedom in choosing grid spacing, compared to the central scheme.

### (g)

The continuously-compounded yield-to-maturity of a zero-coupon bond with time-$t$ price $P_t$ and nonrandom face value $P_T$ to be paid at maturity date $T$ is

$$
\frac{\log(P_T / P_t)}{T - t}
$$

where, as always for us, $\log$ denotes natural log, and where $P_T = 1$ according to this problem's assumptions. One way to think of the time-$t$ yield to maturity $T$ is as the average of some type of time-$t$ expectation of the instantaneous spot rates from time $t$ to time $T$.

Find the yield-to-maturity of a 5-year discount bond, in the case that $r_0 = 0.12$, and in the case that $r_0 = 0.02$. (The "good" results from part (e) may be used here. The "bad" results should not be used, unless you want to fix them by modifying the grid spacings.)

Why, intuitively, is the yield for $r_0 = 0.12$ smaller than $0.12$, whereas the yield for $r_0 = 0.02$ is greater than $0.02$?

> **Comment:** Under these short-rate dynamics, there do exist analytic pricing formulas for bonds. So we do not need finite difference methods to value the simple payoff that we have here. But the finite difference scheme can be modified to handle contracts for which exact pricing formulas do not exist.

---

## Problem 2

The interest rate on the bank account is $r$. For $0 \leq t \leq T$, let $X_t$ be a time-$t$ futures or forward price, with expiration date $T$, on some underlying. (Futures prices = forward prices, if the interest rate is nonrandom, as it is here.) Under risk-neutral probabilities, assume $X$ has CEV dynamics

$$
dX_t = \nu X_t^{1+\alpha}\,dW_t, \qquad X_0 = 100
$$

with constants $\nu$, $\alpha$. The superscript on $X_t$ is an exponent (power). As a futures/forward price, $X$ has drift coefficient 0 (but prices of European options on $X$ still have drift coefficient $r$).

### (a)

Let $C(X_t, t)$ be the time-$t$ no-arbitrage price of a European put on $X$, with strike $K$ and expiry $T$. Write down a PDE, with terminal condition, for $C(X, t)$. Leave your answer in terms of $r$, $\nu$, $\alpha$, $K$, $T$.

### (b)

Let $r = 0.05$, $\nu = 3$, $\alpha = -0.5$. Use Crank-Nicolson to find the time-0 price of an American put on $X$ with strike $K = 100$ and expiry $T = 0.25$. Partial code is provided in the `ipynb` file. You may use the boundary conditions implemented in the function `FD_CrankNicolson_Engine.price_put_CEV`.

At the low-$X$ boundary, it assumes the put value equals intrinsic value (exercise value). At the high-$X$ boundary, it approximates the put value as zero. You may use the FD grid given in the `ipynb` file.

### (c)

Compute numerically the time-0 delta and gamma of the put in (b).

### (d)

Using exactly the same `FD_CrankNicolson_Engine.price_put_CEV` function as in (b) — meaning that you can change the input passed into the function, but cannot change the function's code — find the time-0 price of the American put in (b), but assuming Black-Scholes dynamics for $X$ with volatility $0.30$ and interest rate $0.05$ and $X_0 = 100$.

### (e)

Intuitively, how does the shape of the European options-implied volatility skew (as a function of strike) differ, between the (b) dynamics vs. the (d) dynamics? If you wish, you may actually compute European implied volatilities, but this is not required; the intuition is enough here.
