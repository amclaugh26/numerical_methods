<!-- Source: finm320-26-hw2.pdf -->

# FINM 32000: Homework 2

Due Tuesday April 7, 2026 at 11:59pm

## Problem 1

Consider a particular stock index that is defined to have value equal to the price of a fixed basket of non-dividend-paying stocks. Suppose that it follows the Black-Scholes dynamics with $\sigma = 0.4$, and that the time-0 index level is $S_0 = 100$. Consider a three-month ($=0.25$ year) up-and-out European put, struck at 95, with a discretely monitored knock-out barrier at 114, observed at times $0.02, 0.04, \ldots, 0.24$. That is, our option knocks out if and only if the index is at or above 114 at an observation time (where the unit of time in this course will always be years, unless otherwise indicated). Let the constant risk-free interest rate be $r = 0$.

### (a)

Write a Python function to price our option at time 0 using a trinomial tree with probabilities specified in L2.21. Some of the code is already provided for you.

The provided code uses the time step $\Delta t = T/N$ as suggested in class. We will want the barrier-monitoring times to be represented in the tree, preferably without introducing unequal time intervals anywhere, so we will want to choose $N$ a multiple of 25. Your code should be able to accept any such $N$; a user who desires high accuracy can choose $N$ large; a user who desires high speed can choose $N$ small. For FINM 32000, please report a price using $N$ chosen large enough that your output has converged, in your judgment (no proof needed), to within $0.01 of the true price. In this example, $N = 100$ will not be sufficient.

The provided code chooses the space step $\Delta x$ such that the log of the barrier level $H = 114$ is exactly halfway between consecutive log price levels of the tree. Subject to this constraint, it chooses $\Delta x$ close to the recommended $\sigma \sqrt{3\Delta t}$ value. In other words, the constraint is that there exists an integer $j$ such that $\log(114)$ is halfway between the $j$th and $(j+1)$th log-price levels:

$$
\log S_0 + (j + 0.5)\Delta x = \log H.
$$

And the integer $j$ is chosen such that the $\Delta x$ which satisfies the constraint is approximately $\sigma \sqrt{3\Delta t}$, so we take $j$ to be the nearest integer to

$$
\frac{\log(H/S_0)}{\sigma \sqrt{3\Delta t}} - 0.5.
$$

Why do we have this "halfway between" requirement? If you try instead putting $\log H$ at a log-price level, you will find the accuracy to be worse than the "halfway between" procedure, for this discretely monitored barrier option.

### (b)

Consider an up-and-in put with the same terms. Specifically, this option has the same strike, expiry, barrier, and monitoring dates, but it pays at expiry the put payoff only if the index was at or above the 114 knock-in barrier at some monitoring date; otherwise, it pays nothing.

Using your part (a) result, find the time-0 price of the up-and-in put.

### (c)

Consider a continuously monitored barrier option paying at time $T = 0.25$ the amount

$$
(95 - S_{0.25})^+ \mathbf{1}_{\max_{0 \le t \le 0.25} S_t < 114},
$$

where the indicator variable $\mathbf{1}(A) := \mathbf{1}_A := 1$ if event $A$ occurs, 0 otherwise.

#### (c1)

Is the time-0 price of the continuously monitored barrier option greater than or smaller than the time-0 price of the discretely monitored option in (a)? Justify briefly without doing any numerical calculations. One sentence is enough.

#### (c2)

The continuously monitored barrier option can be replicated by a portfolio of $T$-expiry options, long 1 plain vanilla put struck at 95, and short $\alpha$ plain vanilla calls struck at 136.8.

The replication strategy is as follows. If $S$ does not hit the barrier before time $T$, then simply collect the time-$T$ payout of the 95 put, as desired. If $S$ does hit the barrier, then at the time when $S$ is at the barrier, the 1 unit of the vanilla put has value that exactly cancels the value of the $-\alpha$ units of the plain vanilla call; so at that time, we close out the portfolio positions, for a net payment of zero, as desired.

Solve analytically for the quantity $\alpha$ that makes this replication strategy valid, and find the time-0 value of the continuously monitored barrier option. Do not use a tree.

## Problem 1: Coding

The HW2 template code is in `finm320-26-hw2.ipynb`.

Complete the coding of `TreeEngine.price_upandout(self, dynamics, contract)` in that notebook. In the template, the unfinished lines are the definitions of `nu`, `Pu`, `Pd`, and `Pm`, plus the backward-induction update line `optionprice =  # complete this`. The comment inside the time loop also leaves room for any barrier-handling logic you need to add.

The notebook currently defines

- `hw2contract = UpAndOutPut(K=95, T=0.25, barrier=107, observationinterval=0.02)`
- `hw2dynamics = GBMdynamics(S=100, sigma=0.4, rGrow=0, r=0)`
- `hw2tree = TreeEngine(N=100)`

and the call `hw2tree.price_upandout(hw2dynamics, hw2contract)` must run properly once you complete the template.

The template already checks that `N` places the observation dates on the tree by raising a `ValueError` when `contract.observationinterval / deltat` is not an integer. Your implementation should still work for other valid values of `N`, and the contract and dynamics parameters should not be hard-coded into `price_upandout`.

Do not modify the header of `price_upandout` unless you want to add "type hints". You may modify other lines in the file.

You do not need to make your code valid for contract parameters that would alter the contract's logic. In particular, you may assume that $H > S_0 > K$. Thus, you do not need to strive for maximum generality. But parameter perturbations that preserve the basic nature of the problem should run properly.

One template note: the notebook currently uses barrier `107`, whereas the PDF problem statement above says `114`. Reconcile that discrepancy before treating any notebook-produced number as a final answer.

Problem 2 in the notebook reuses HW1 code. The template explicitly says to use the same `GBMdynamics` class from HW1, and it also reuses `CallOption` and `AnalyticEngine`. Once those HW1 components are available in the HW2 notebook, the sample call

```python
hw2analytic.IV(
    GBMdynamics(sigma=None, rGrow=0, S=100, r=0),
    CallOption(K=100, T=0.5, price=12),
)
```

should run properly as well.

## Problem 1: Discussion

- Note that the introductory paragraph of Problem 1 specifies the option contract and the underlying dynamics. That paragraph says nothing about valuation method or algorithm. The knock-out dates described in that paragraph are features of the contract. They are written into the terms of the option. Whatever methodology or algorithm that a modeler might choose to value the contract, whether analytic approximation, a tree with 500 steps, a tree with 5000 steps, or Monte Carlo, has no impact on the specification of the contract, which dictates that the barrier observation times are $0.02, 0.04, \ldots, 0.24$.
- A useful diagnostic: test whether your code, with the barrier conditions removed, prices Europeans correctly compared to Black-Scholes.
- When you introduce the barrier, one possible cause of error is code that fails to detect that you are at a monitoring date.

Beware of code that tests whether two floating point numbers are equal by naively using `==`.

Consider this example in Python:

```python
0.14 / 0.02 == 7
# False
```

This happens because a computer may calculate `0.14 / 0.02` as `7.000000000000001`.

Floating point arithmetic should not be assumed to be exact. If you need to test whether two floating point numbers `x` and `y` are equal, then instead of using `==`, it would be better to test whether `abs(x - y)` is smaller than some tolerance.

## Problem 2

### (a)

Interest rate is 0. A non-dividend-paying stock $S$ has time-0 price $S_0 = 100$. At time 0, you observe the dollar prices of at-the-money ($K = 100$) European calls on $S$ at 0.5-year and 1-year expiries to be 11.25 and 12.00, respectively.

Find the time-0 Black-Scholes implied volatilities of these two options.

### (b)

Consider an at-the-money European call on $S$ with expiry 0.75. Suppose that you try to price it by assuming that its implied volatility is equal to the midpoint, the arithmetic average, of the 0.5-expiry and the 1.0-expiry implied volatilities. Under that assumption, what would be the time-0 price of the 0.75-expiry call?

### (c)

The price computed in (b) would allow arbitrage involving the 0.75-expiry call and one of the other contracts. Describe the steps of this arbitrage.

You may assume either cash settlement or physical settlement of these options, but specify what your assumption is.

Cash settlement of an in-the-money option at time $T$ means that you receive $S_T - K$ dollars if you are long the contract, and $K - S_T$ dollars if you are short the contract.

Physical settlement of an in-the-money option at time $T$ means that you receive 1 share of stock and $-K$ dollars if you are long the contract, or $-1$ share of stock and $+K$ dollars if you are short the contract.

Conclusion: expiry interpolation should not be done by linear interpolation of implied volatility. A better alternative would be linear interpolation of the total implied variance $\sigma_{\mathrm{imp}}^2 T$.
