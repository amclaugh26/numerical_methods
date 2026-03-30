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
