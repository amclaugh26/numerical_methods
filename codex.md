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
