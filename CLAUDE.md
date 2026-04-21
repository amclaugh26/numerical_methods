# CLAUDE.md — FINM 320 Numerical Methods Workspace

## Course Context

This repo contains weekly homework assignments for FINM 320-26 (Numerical Methods in Finance). Each assignment arrives as a PDF and a starter `.ipynb` file. The workflow each week is:

1. Extract the PDF into a clean Markdown instructions file.
2. Set up the template notebook for that week's work.

---

## File Naming Conventions

| Artifact | Pattern |
|---|---|
| Assignment PDF | `finm320-26-hw<N>.pdf` |
| Starter/working notebook | `finm320-26-hw<N>.ipynb` |
| Instructions Markdown | `homework<N>instructions.md` |
| Data files | `data/hw<N>-*.csv` |

Always confirm the active notebook filename from the user's current IDE context — sometimes a scratch copy like `homework_<N>.ipynb` is the actual working file.

---

## Weekly Setup Workflow

### Step 1 — PDF to Markdown

Use the `pdf-text-extraction` skill (`pdf-text-extraction/SKILL.md`) as the primary reference.

Quick triage order:
1. Check for `pdftotext` / `pdfinfo` (likely unavailable — see Environment Notes below).
2. Check for Python PDF libraries (`pypdf`, `pdfplumber`, `fitz`).
3. Fall back to custom `python3` zlib/stream parser.

Output: `homework<N>instructions.md` at repo root, containing:
- Assignment title and due date
- All problems and subparts with original numbering preserved
- Equations rewritten cleanly in LaTeX/Markdown math (not broken fragments)
- Footnotes kept when relevant
- References to notebooks and data files matching actual repo filenames

Run the quality checklist before finishing:
- [ ] Title and due date present
- [ ] Every problem and subpart from the PDF is included
- [ ] Formulas are readable and mathematically intact
- [ ] Notebook/data filenames match actual repo files
- [ ] Output filename matches the homework number

### Step 2 — Notebook Template Setup

After generating the instructions file, review the starter `.ipynb` to identify:
- Stub functions marked `# You complete the coding of this function`
- Placeholder lines like `qu =   #fill this in`
- Any stale template parameters that don't match the current assignment's values (e.g., wrong barrier, wrong strike)

Flag any mismatches to the user before diving into implementation. Always trust the PDF instructions over stale template placeholders.

---

## PDF to Markdown Conversion Notes

### Tool availability (as of 2026-04-20)

- `pdftotext` is available at `/mingw64/bin/pdftotext` in the Git Bash / MINGW64 shell — **use this first**.
- `pdfinfo` is available via MiKTeX at `C:/Users/armcl/AppData/Local/Programs/MiKTeX/...`.
- The WSL environment (as of 2026-03-30) lacks both; `python3 + zlib` is the WSL fallback.
- Run `pdftotext -layout <file>.pdf -` to stream extracted text directly to stdout for inspection before writing to a file.

### Greek letters and math symbols are silently dropped

`pdftotext` drops Greek letters (κ, θ, σ, α, ν, etc.) and many special characters (→, ≥, ℝ) without warning — they are replaced by nothing, leaving broken expressions like `drt = ( - rt)dt + dWt`.

**Always cross-reference the starter notebook** to recover the correct symbols:
- Class instantiation parameters reveal the Greek letters used (e.g., `Vasicek(kappa=3, theta=0.05, sigma=0.03)` → $\kappa=3$, $\theta=0.05$, $\sigma=0.03$).
- CEV dynamics from `CEV(volcoeff=3, alpha=-0.5)` → $\nu=3$, $\alpha=-0.5$.
- Variable names in stub functions also indicate intended math notation.

### Other common extraction artifacts

| Raw extraction | Corrected form |
|---|---|
| `( - rt)` | `κ(θ - rt)` |
| `with parameters  = 3,  = 0.05,  = 0.03` | `κ = 3, θ = 0.05, σ = 0.03` |
| `f : R  R` | `f : ℝ → ℝ` |
| `h  0` | `h → 0` |
| `0  t  T` | `0 ≤ t ≤ T` |
| `O(h2)` | `O(h²)` |
| `Xt1+` | `Xt^{1+α}` |

### Post-extraction checklist

- [ ] All top-level problems present (`1.`, `2.`, ...)
- [ ] All subparts present (`(a)`, `(b)`, ...)
- [ ] Greek letters restored from notebook class definitions
- [ ] Inequality and arrow symbols restored
- [ ] Superscripts/subscripts rendered correctly in LaTeX
- [ ] Notebook filenames in the instructions match actual repo filenames

---

## Environment Notes

As of 2026-03-30, the WSL environment lacked these tools:
- CLI: `pdftotext`, `pdfinfo`, `pdftoppm`, `qpdf`, `mutool`, `gs`, `tesseract`
- Python: `pypdf`, `PyPDF2`, `pdfplumber`
- Windows interop (`python.exe`, `powershell.exe`) also failed from WSL

`python3` with `zlib` is available and is the reliable fallback for PDF stream extraction.

---

## Persistent Notes

For problem-level domain notes (put-call parity derivations, trinomial tree indexing conventions, vega formulas, debugging tips, sanity-check values), see `codex.md`. Append new notes there after each assignment rather than replacing existing content.

---

## Review Mode

When the user asks for review or guidance on a notebook cell, default to explanation first — do not edit the file unless the user explicitly asks for changes. Before reviewing individual cells, compare the notebook against `homework<N>instructions.md` to catch template mismatches early.

Common last-pass issues before submission:
- Stale template parameters
- Missing subpart writeups even when code exists
- Mislabeled maturities or strikes in final answers
- Missing closing `$` in Markdown math cells
