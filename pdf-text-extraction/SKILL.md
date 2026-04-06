---
name: pdf-text-extraction
description: Extract text from PDFs and convert PDFs to Markdown in constrained/offline environments. Use when Codex needs to read assignments, reports, or notebooks from PDF files, especially when `pdftotext` or Python PDF libraries are unavailable, when text is encoded via font `ToUnicode` maps, or when completeness must be verified to avoid missing sections/pages.
---

# PDF Text Extraction

Use this skill to extract complete text from PDFs and turn it into clean Markdown without silently dropping sections.

## Workflow

1. Identify the exact PDF filename.
2. Try standard extraction tools first (`pdftotext`, `pdftohtml`, `pdfinfo`).
3. Check for local Python PDF libraries (`pypdf`, `PyPDF2`, `pdfplumber`, `fitz`).
4. If unavailable, parse `FlateDecode` streams directly with Python `zlib`.
5. Choose the extraction path:
   - TeX-style text streams (`TJ`/`Tj` with readable content)
   - Encoded notebook/browser export streams (hex strings + `ToUnicode`)
6. Post-process line wraps, page numbers, and split math fragments (e.g., `R^2`).
7. Validate completeness against expected section numbering before delivering output.

## Fast Triage

Use these checks first:

```bash
rg --files -g '*.pdf'
file target.pdf
which pdftotext
which pdftohtml
which pdfinfo
```

Check Python libraries:

```bash
python3 - <<'PY'
mods = ["pypdf", "PyPDF2", "pdfplumber", "fitz"]
for m in mods:
    try:
        __import__(m)
        print(m, "OK")
    except Exception:
        print(m, "NO")
PY
```

## Path A: TeX-Style PDF Streams (Preferred Fallback)

Use this path when decompressed streams contain readable `BT ... TJ/Tj` content.

Extract by:

- Decompressing `FlateDecode` streams.
- Parsing `TJ` and `Tj` operators.
- Decoding PDF literal strings (escaped parens, octal escapes).
- Reconstructing spaces from large kerning values in `TJ` arrays.
- Handling common TeX ligature bytes (`ff`, `fi`, `fl`, `ffi`, `ffl`) if needed.

Typical signals:

- Streams contain `BT`, `TJ`, `Tj`.
- TeX CMap resources may appear (`TeX-cmr10-builtin-*`, etc.).

## Path B: Notebook / Browser-Export PDF (Encoded Text)

Use this path when page text appears as hex strings like `<002C005100...>` and not readable ASCII.

Extract by:

- Parsing page `/Resources` font mappings (`/Fxx -> object ref`).
- Parsing each font's `/ToUnicode` CMap stream.
- Tracking the active font (`Tf`) while parsing `Tj` / `TJ`.
- Decoding text bytes through the current font's `ToUnicode` mapping.
- Grouping lines using text operators (`Tm`, `Td`, `TD`, `T*`, `ET`).

This is usually enough to recover notebook markdown/text outputs and result summaries for search/review.

## Critical Pitfall: Stream Length Handling

When reading compressed streams manually:

- Use the exact byte count from `/Length`.
- Do not blindly `rstrip()` stream bytes before `zlib.decompress()`.

Reason:

- Some PDFs lose one compressed byte if trailing newlines are trimmed.
- Decompression then fails or truncates, which can silently drop an entire section/problem/page.

If a section is missing, inspect all text-like streams and confirm none failed decompression due to a length mismatch.

## Completeness Validation (Required)

Before finalizing extracted output, verify:

- All top-level sections/problems are present (`1.`, `2.`, `3.`, ...).
- All expected subparts exist (`(a)`, `(b)`, ...).
- Continuations across page boundaries were merged correctly.

Search for likely omissions or formatting splits:

- `"2."` or other missing problem numbers
- `"Part ("`
- `"R^2"` and split forms (`R` on one line, `2` on the next)
- `"forecast"` or other expected keywords from the assignment

## Markdown Cleanup Rules

Apply these cleanup steps after extraction:

- Remove standalone page numbers.
- Join wrapped lines into paragraphs/list items.
- Repair split math tokens (`R` + `2` -> `R^2` when context matches).
- Repair hyphenated wraps (`one-` + `period` -> `one-period`).
- Wrap filenames/scripts in backticks (e.g., `topics.csv`, `generation.py`).

## Output Pattern

Prefer this output pattern for difficult PDFs:

- Save an intermediate extraction file: `*_extracted.txt`
- Save the cleaned final output as Markdown
- Include the source PDF filename in the Markdown header/metadata

## Practical Notes

- If you successfully extract only parts of a document, assume the extraction is incomplete until section numbering is checked.
- If a PDF contains mixed stream types, inspect every text-capable stream object before concluding the document is complete.
- If repeated use is expected, add a `scripts/` helper to this skill for deterministic extraction and reuse.

