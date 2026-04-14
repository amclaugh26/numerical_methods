## Problem 1

The Gold Dragon Coin (GDC) is a unit of currency in Westeros. Let $$S$$ denote the GDC/USD
exchange rate (the USD value of 1 GDC). Assume $$S$$ has dynamics

$$
dS_t = (r-q)S_tdt + \sigma(S_t,t)S_tdW_t,
$$

where W is Brownian motion under the [USD] risk-neutral probability measure. The USD interest
rate is $$r = 0.06$$, the GDC interest rate is $$q = 0.01$$, today’s time-0 spot is $$S_0 = 100$$, and

$$
\sigma(S,t) := \mathrm{min}[0.2+5(\mathrm{log}(S/100))^2+0.1\exp{-t}, 0.6].
$$

### (a)

Find the time-0 price of an American-style put on the GDC. The put has strike 95 and expiry
0.75.

### (b)

Find the time-0 price of a European-style call, with strike 10 and expiry 0.25, on an American
put on the GDC, to be issued at time 0.25 if the European call is exercised (therefore, the
put will not already have been exercised prior to time 0.25). The American put has strike 95
and expiry 0.75.

This call is an example of a compound option. At time 0.25 it gives the call holder the right
to buy the underlying put for 10. The underlying put will have the usual exercise privilege
on the time interval [0.25,0.75], at strike 95.

Example of usage: A company whose expenses are in USD but anticipates receiving a GDC
revenue stream may want to have the put (from part (a)) to hedge the FX risk (specifically,
the risk of GDC weakening against USD). But suppose that the revenue stream may or may
not happen, depending on whether or not the ruling house of Westeros selects this company
as a vendor at time 0.25, so the company does not wish to pay full price for a put that may
or may not turn out to be needed. On the other hand, the company does wish to act soon to
prepare a hedge, because the company fears that GDC will weaken by time 0.25, and the put
will become more expensive. This motivates the company to ask the Iron Bank of Braavos,
what it would cost, to buy a call on the put. Your job is to help the Iron Bank quote a price.
All prices are, as usual, in USD unless stated otherwise.

Complete the coding of the function price compound localvol in the provided ipynb file. Use
a trinomial tree. Your code may reject N for which the call expiry fails to be represented in the tree.
In choosing ∆x, follow L2.33 and choose the “representative” volatility σavg to be σ(S0,0). The
amount of work done by your algorithm in this problem should grow like N2 as N grows (no proof
required). If it grows like N3 in this problem, then your algorithm has some major inefficiency.

## Problem 2

### (a)

In the Black-Scholes model with interest rate r, no dividends, and volatility σ, approximate
the time-0 delta of an at-the-money (K = S0) vanilla call with expiry T, by applying a
first-order Taylor expansion to the exact formula, and obtaining an explicit approximation
formula in terms of the given parameters.

Then evaluate this approximation to two decimal places, assuming σ = 0.2 and T = 0.25 and
r = 0.01.

### (b)

Suppose that some option, or some portfolio/combination of options – let’s call it the “com-
bination” – has a time-0 pricing function C(S) with respect to an underlying stock S.
Define the combination’s time-0 dollar delta to be its delta multiplied by S0:

$$
S_0\frac{\partial C}{\partial S}
$$

which equals the dollar value of the stock position in the delta hedge (quantity $$ \frac{∂C}{∂S}$$ shares ×
price $$S_0$$ dollars per share).

Define the combination’s time-0 dollar gamma to be its gamma multiplied by $$ S^2_0/100$$:

$$
\frac{S^2_0}{100} \mathrm{x} \frac{\partial^2 C}{\partial S^2}
$$

which equals the dollar value of stock shares that need to be purchased/sold in order to
rebalance a delta hedge, per 1 percent movement in the stock price.

(because: the shares of stock to be purchased/sold is $$\frac{\partial^2 C}{\partial S^2}$$ per dollar movement in $$S$$.

So the dollars of stock to be purchased/sold is $$S_0\frac{\partial^2 C}{\partial S^2}$$ per dollar movement in $$S$$.

So the dollars of stock to be purchased/sold is $$S_0 \frac{\partial^2 C}{\partial S^2} \mathrm{x} \frac{S_0}{100}$$ per 1 percent change in $$S$$.)

Suppose that at time 0, the underlying stock has price $$S_0 = 4$$, and the option combination
has price 5, dollar delta 3, and dollar gamma 0.02.

Use a second-order Taylor expansion (with zeroth, first, and second order terms) to approxi-
mate the time-0 value of the contract, given an underlying stock price 3.6.

Hint: convert the dollar delta and dollar gamma into delta and gamma, and apply Taylor
expansion to C.