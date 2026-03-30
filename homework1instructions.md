# FINM 32000: Homework 1

Due Tuesday March 31, 2026 at 11:59pm

## Problem 1

The file `hw1-rut.csv` has price data, as of 2025 February 3 (this is "time 0"), for European-style options on RUT, the Russell 2000 index, with expiry 2025 February 28.

### (a)

Given the bid and ask prices of the calls and puts, compute the midpoint price (average of bid and ask) for each contract.

Infer the time-0 forward price $F_0$ (for delivery at the time $T$ when the options expire) by plugging the midpoint call and midpoint put prices into the put-call parity relationship

$$
\mathrm{CallPrice}_0(K) - \mathrm{PutPrice}_0(K) = e^{-rT}(F_0 - K)
$$

In theoretical frictionless markets, this is valid at all strikes $K$. In practice, the near-ATM strikes are preferred when trying to infer $F_0$. Here let us use the particular strike $K$ which minimizes (among all the listed strikes in the data) the absolute value of the price difference on the left-hand side.

Assume that the continuously compounded interest rate is $r = 0.0432$ with respect to a day-count convention such that $T = 25/365$.

### (b)

Compute the implied volatility at all of the given strikes, and plot the resulting volatility skew as a function of strike.

At each strike, use the OTM option price for the implied volatility calculation. This means that at strikes $K > F_0$, use the call price, and at strikes $K < F_0$, use the put price.

For calculating put-implied volatility, you could write a Black-Scholes put-pricing function; or alternatively, convert the midpoint put price into an "implied" midpoint call price using put-call parity (see 1a), and then use the Black-Scholes call pricer on the implied call price. The code fragments in `hw1.ipynb` assume the latter approach.

Let $T = 25/365$ for the option expiry, using "calendar days". (An alternative would be to calculate option expirations using trading days, with a denominator such as 252.)

Use the code provided in `hw1.ipynb`, and see the specific instructions in the comments there.

## Problem 2

Consider the following polynomial parameterization[^1] of the time-0 implied volatility skew:

$$
\sigma_p(k) = \alpha_0 + \alpha_1 k + \alpha_2 k^2 + \alpha_3 k^3 + \alpha_4 k^4
$$

for expiry $T$, where $\alpha_0, \ldots, \alpha_4$ are such that $\sigma_p(k) > 0$ for all $k$, where

$$
k := \log(K/F_0)
$$

denotes the moneyness, or more specifically the log-moneyness, of a call or put with strike $K$, and where $F_0$ is the time-0 forward price for time-$T$ delivery of the underlying.

### (a)

Fit parameters $\alpha_0$, $\alpha_1$, $\alpha_2$, $\alpha_3$, $\alpha_4$ to the observed implied volatility skew from Problem 1, to minimize the sum, across all strikes, of the squared difference between the observed midpoint implied vol in Problem 1(b) and the "model" implied vol $\sigma_p$. Plot both the actual Problem 1(b) implied vol, and the fitted $\sigma_p$, together on the same plot, as functions of $k$.

### (b)

Relative to the fitted implied vol $\sigma_p$, which OTM option contract in the RUT data is the most "overpriced", in terms of midpoint implied vol (not in terms of dollars)? Identify that contract by giving its strike.

### (c)

Assuming that implied vol obeys the parameterization $\sigma_p$, write a formula for the sensitivity (the partial derivative) of the time-0 price (in dollars) of the $T$-expiry, $k$-moneyness call or put option, with respect to changes in the skew slope $\alpha_1$. This partial derivative, by definition, holds fixed $k$ and all of the $\alpha$ parameters, except for $\alpha_1$.

Use the fact that the time-0 vega of the call or put option is

$$
e^{-rT} F_0 \sqrt{T}\, N'(d_1)
$$

where $N'$ is the standard normal density function, and

$$
d_1 := \frac{-k}{\sigma_p(k)\sqrt{T}} + \frac{\sigma_p(k)\sqrt{T}}{2}
$$

and $r$ is the interest rate, assumed constant.

### (d)

Given the fitted parameters from 2(a), which contract's price gains the most (in dollars), and which contract's price loses the most (in dollars), when the skew slope $\alpha_1$ increases (equivalently, flattens, in the case $\alpha_1 < 0$).

Use your formula from (c). You may restrict your attention to the strikes listed in the data. Your final answer will be two strikes (biggest gainer and biggest loser) as $\alpha_1$ increases.

[^1]: I do not favor this parameterization of the volatility skew, because it has unsatisfactory asymptotic behavior. But sometimes questions about polynomial volatility skew parameterizations do get asked in interviews/assessments. (A parameterization with better asymptotic behavior is the SVI: https://arxiv.org/abs/1204.0646)
