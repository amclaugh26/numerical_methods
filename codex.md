# Codex Notes

This file is for persistent repo-specific notes that should make future FINM assignments faster to process. Append to it over time rather than replacing it.

## Current Conventions

- Keep generated assignment instructions at the repo root as `homework<N>instructions.md`.
- Source files currently follow this pattern:
  - PDF: `finm320-26-hw<N>.pdf`
  - Notebook: `finm320-26-hw<N>.ipynb`
  - Data: `data/hw<N>-*.csv`
- Preserve original problem numbering and subpart labels.
- Normalize equations into Markdown math where the PDF layout would otherwise break readability.
- Keep copied questions faithful to the PDF, but clean obvious extraction artifacts like broken spacing or split formulas.

## Fast Workflow For New Homework

1. Locate the new assignment files with `rg --files`.
2. Check whether the corresponding instructions file already exists.
3. Try the easy PDF path first:
   - `pdftotext -layout`
   - `pdfinfo`
4. If those tools are unavailable, fall back to local `python3` extraction.
5. Create `homework<N>instructions.md` with:
   - title
   - due date
   - problem statements
   - equations rewritten cleanly in LaTeX/Markdown
   - footnotes preserved when relevant
6. Verify the result by reading the generated Markdown back once before finishing.

## Environment Notes

- As of 2026-03-30, the WSL environment did not have these PDF utilities installed:
  - `pdftotext`
  - `pdfinfo`
  - `pdftoppm`
  - `qpdf`
  - `mutool`
  - `gs`
  - `tesseract`
- `python3` is available in WSL.
- Common PDF Python libraries were not installed in WSL at that time:
  - `pypdf`
  - `PyPDF2`
  - `pdfplumber`
- Windows interop commands existed but failed from this shell session:
  - `python.exe`
  - `powershell.exe`
  - `cmd.exe`
- Practical implication: if the PDF contains embedded text, a small custom `python3` parser may be the fastest reliable fallback.

## PDF Transcription Guidance

- Prefer embedded-text extraction over OCR whenever possible.
- If the PDF uses TeX fonts, expect word spacing to be encoded via `TJ` kerning values rather than literal spaces.
- If formulas are split across lines during extraction, rewrite them directly in Markdown math instead of preserving the broken layout.
- Pay special attention to:
  - subscripts like `F_0`
  - superscripts like `k^2`
  - Greek symbols like `sigma`, `alpha`
  - footnote markers
  - quoted notebook filenames such as `hw1.ipynb`

## Quality Checklist

- Confirm the assignment title and due date.
- Confirm every problem and subpart from the PDF appears in the Markdown file.
- Confirm formulas are readable and mathematically intact.
- Confirm references to notebooks and data files match actual repo filenames.
- Confirm the output file name matches the homework number.

## Homework 1 Notes

- `finm320-26-hw1.pdf` was text-based and recoverable without OCR.
- The generated instructions file is `homework1instructions.md`.
- Problem 2 included a footnote about polynomial skew parameterizations and SVI; that footnote was worth preserving explicitly.

## Problem 1 Support Notes

- In Problem 1(a), "calculate the forward price" means infer the time-0 forward price from option midpoints using put-call parity. It does not mean forecast the future index level.
- The key formula is:
  - `F = K + exp(r*T) * (CallMid - PutMid)`
- Compute midpoint prices first:
  - `CallMid = (CallBid + CallAsk) / 2`
  - `PutMid = (PutBid + PutAsk) / 2`
- To choose the strike used for the final forward estimate, minimize:
  - `abs(CallMid - PutMid)`
- The absolute value matters because `CallMid - PutMid` changes sign around the forward. The assignment wants the strike where that difference is closest to zero.
- The "ATM row" is only used to estimate a scalar forward `F`. Do not use the ATM strike itself as the OTM classification threshold afterward.
- For Problem 1(b), determine OTM status using `F`, not the chosen ATM strike:
  - if `Strike > F`, the call is OTM
  - if `Strike < F`, the put is OTM
- When the put is OTM, convert the put midpoint into an implied call midpoint using:
  - `ImpliedCallMid = PutMid + exp(-r*T) * (F - Strike)`
- The combined call-price column for the IV solver should be:
  - `CallOrImpliedCall = CallMid` when `Strike > F`
  - `CallOrImpliedCall = ImpliedCallMid` when `Strike < F`
- A good implementation pattern is:
  - `options['CallOrImpliedCall'] = np.where(options['Strike'] > F, options['CallMid'], options['ImpliedCallMid'])`

## Problem 1 Debugging Notes

- If the code computing `ImpliedCallMid` uses `(CallBid - CallAsk) / 2`, that is wrong. That calculates half the negative spread, not a midpoint or implied call.
- If the IV calculation throws `TypeError: AnalyticEngine.BSpriceCall() missing 1 required positional argument: 'contract'`, the bug is inside `AnalyticEngine.IV`, not in the `options['IV']` apply line.
- The correct Brent root line is:
  - `brentq(lambda sigma_guess: self.BSpriceCall(dynamics_try.update_sigma(sigma_guess), contract) - C, lo, hi)`
- Before trusting the skew plot, verify:
  - the chosen ATM row
  - the scalar `F`
  - the first few rows of `PutMid`, `CallMid`, `ImpliedCallMid`, and `CallOrImpliedCall`
  - that the IV plot contains values across the full strike range
- For this specific Homework 1 dataset, the current logic selects strike `2265` as the near-ATM row and implies `F` of about `2265.4012`. This is a useful quick sanity check if the notebook is rerun later.

## Communication Notes

- Likely confusion points to explain early when helping on similar assignments:
  - the difference between spot, forward, and the chosen ATM strike
  - why `abs(CallMid - PutMid)` is used
  - why OTM classification is based on `F`
  - why the notebook converts OTM puts into implied calls before solving for IV
- When reviewing homework progress, prioritize checking alignment with the assignment wording over only checking whether the notebook runs.

## Problem 2 Support Notes

- For Problem 2(a), the fitting target is the quartic volatility skew:
  - `sigma_p(k) = alpha0 + alpha1*k + alpha2*k**2 + alpha3*k**3 + alpha4*k**4`
- The assignment objective is least squares across strikes:
  - minimize `sum((observed_IV - sigma_p(k))**2)`
- `numpy.polyfit(k, iv_obs, 4)` is an appropriate direct way to solve that least-squares problem.
- `np.polyfit` returns coefficients in descending powers:
  - `[alpha4, alpha3, alpha2, alpha1, alpha0]`
- `np.polyval(coeffs, k)` and `np.poly1d(coeffs)` expect that same descending-power order. Do not reorder coefficients before using `polyval` or `poly1d`.
- If the user wants homework-style named alphas, map them explicitly:
  - `alpha4, alpha3, alpha2, alpha1, alpha0 = coeffs`
- Use `k = log(Strike / F)` for Problem 2, consistent with the prompt. The fit and the plot should both be against `k`, not raw strike.
- A good plotting pattern is:
  - markers: observed IV vs `k`
  - line: fitted `sigma_p(k)` on a smooth `k_grid`

## Problem 2 Interpretation Notes

- "Most overpriced" in part (b) is defined in implied-vol terms, not dollar-price terms.
- The correct residual is:
  - `IVResidual = IV - SigmaP`
- The most overpriced contract is the strike with the largest positive IV residual:
  - `idxmax()` on `IVResidual`
- For this specific Homework 1 notebook state, the current overpriced strike output is `2570`, which corresponds to an OTM call because `2570 > F`.
- In part (c), the key chain-rule result is:
  - `dPrice/dalpha1 = vega * d(sigma_p)/dalpha1`
- Since `d(sigma_p)/dalpha1 = k`, the rowwise sensitivity is:
  - `skewsensitivity = vega * k`
- In code, prefer:
  - `options['skewsensitivity'] = options['vega'] * options['k']`
  rather than multiplying by a separate free-floating `k` variable.

## Problem 2 Vega Notes

- The notebook's `BSvega` routine expects a `GBMdynamics` object and a `CallOption` object.
- For Problem 2(c)/(d), the vega at each strike should use the fitted model volatility `SigmaP` at that strike, not the observed IV.
- A correct rowwise pattern is:
  - `options['vega'] = options.apply(lambda row: hw1analytic.BSvega(GBMdynamics(X=F, r=r, rGrow=0, sigma=row['SigmaP']), CallOption(K=row.Strike, T=T)), axis=1)`
- Using call vega is fine here because Black-Scholes call and put vegas are the same for the same strike and maturity.

## Problem 2 Review Checklist

- Confirm `k` is computed as `log(Strike / F)`.
- Confirm the fitted curve is evaluated from the quartic coefficients without reordering errors.
- Confirm any "overpriced" result is based on `IV - SigmaP`, not on raw price residuals.
- Confirm `vega` uses fitted `SigmaP`.
- Confirm `skewsensitivity = vega * k`.
- Confirm part (d) uses:
  - `idxmax()` for the biggest gainer
  - `idxmin()` for the biggest loser
- If reviewing for submission quality, check whether the notebook or writeup explicitly states the analytical formula for part (c), since code alone may not satisfy a "write a formula" instruction.

## Homework 1 Problem 2 Sanity Checks

- Current notebook output for part (b): overpriced strike `2570`.
- Current notebook output for part (d): biggest gainer `2385`, biggest loser `2100`.
- `np.polyfit` does not enforce the prompt's positivity condition `sigma_p(k) > 0`; if needed, add a quick check that fitted values remain positive over the observed `k` range.

## Homework 2 Process Notes

- Before reviewing or modifying a homework notebook, confirm the active notebook filename from the user's current context. For Homework 2, the working file was `homework_2.ipynb`, not `finm320-26-hw2.ipynb`.
- When the user asks for review or guidance, default to explanation mode first and avoid editing unless the user explicitly asks for file changes.
- Compare the notebook against the assignment instructions before reviewing individual cells. This catches template mismatches early and avoids debugging the wrong contract.
- For submission checks, review both:
  - code correctness
  - markdown/writeup completeness, labels, and typos
- Common last-pass issues were:
  - stale template parameters
  - missing subpart writeups even when code existed
  - mislabeled maturities in final answers
  - missing closing `$` in markdown math

## Homework 2 Barrier Tree Notes

- The Homework 2 PDF used barrier `114`, while one template reference used `107`. Always trust the assignment instructions over stale template placeholders.
- In the trinomial tree, smaller array indices corresponded to higher stock prices because:
  - `Sgrid = S0 * exp(linspace(N, -N) * deltax)`
- With that indexing convention:
  - up child = `optionprice[:-2]`
  - middle child = `optionprice[1:-1]`
  - down child = `optionprice[2:]`
- For the barrier recursion:
  - compute the parent-layer option values first
  - shrink the stock-price layer with `Sgrid = Sgrid[1:-1]`
  - apply the barrier mask only on observation layers
- Use integer observation-step logic, not float-time modulo checks. A good pattern is:
  - `step = int(round(t / deltat))`
  - `obs_steps = int(round(contract.observationinterval / deltat))`
  - apply the barrier when `step % obs_steps == 0 and step != 0`
- For this assignment, convergence evidence was:
  - `N=100` -> about `5.31198`
  - `N=500` -> about `5.30432`
  - `N=1000` -> about `5.30155`
  - `N=10000` -> about `5.30107`
  So `N=1000` was sufficient for the stated `$0.01` tolerance.

## Homework 2 Barrier Option Notes

- For the discretely monitored up-and-in put, use knock-in / knock-out parity:
  - `UpAndInPut = VanillaPut - UpAndOutPut`
- For the continuously monitored up-and-out put replication in part `1(c2)`:
  - barrier `H = 114`
  - put strike `K = 95`
  - call strike `136.8`
  - replication weight `alpha = K / H = 95 / 114`
- The time-0 replicated value is:
  - `V0 = P(100, 95, 0.25) - (95/114) * C(100, 136.8, 0.25)`
- A concise explanation for the "halfway between" barrier placement:
  - putting the barrier on a node forces a discontinuity directly onto a node value
  - putting it halfway between adjacent log-price nodes represents the discontinuity between nodes and reduces asymmetric approximation error

## Homework 2 Term Structure Notes

- For ATM European calls on a non-dividend-paying stock with `r = 0`, call price must be nondecreasing in maturity for fixed strike.
- In Homework 2, the midpoint-IV price for the `0.75`-year call came out to about `12.08153`, which exceeded the observed `1.0`-year call price `12.00`.
- The clean arbitrage argument in part `2(c)` is:
  - assume cash settlement
  - short the overpriced `0.75`-year call
  - long the cheaper `1.0`-year call with the same strike
  - collect the time-0 price difference
  - at `t = 0.75`, the remaining `1.0`-year call value is always enough to cover the short call's cash-settlement obligation
- Do not overcomplicate that part with a convex-combination argument if simple maturity monotonicity already proves the arbitrage.
