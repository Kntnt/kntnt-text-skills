---
name: default
language: (baseline)
layer: mechanics
---

# Default mechanics (baseline)

The fallback mechanics file. Loaded when no language-specific mechanics file exists for the input language. Provides international-standard conventions where they exist (ISO 8601 dates, SI unit spacing, etc.) and internationally neutral defaults where no standard applies.

When a calling skill falls back to this file, it also reports in the reply that a language-specific file is missing and suggests creating one.

There is no companion `default-style.md`. The style layer (address, AI-tell manifestations, interference patterns, genre adjustments) is inherently language-and-culture-bound and has no meaningful baseline.

## Typography

| Convention | Realisation |
|---|---|
| Thousands separator | Thin no-break space (U+202F): 1 234 567 — per ISO 31-0 |
| Decimal separator | Full stop: 123.45 |
| Range | EN-dash without spaces: 2–5 |
| Parenthetical insertion | EN-dash with spaces: red – I think |
| Date (short) | ISO 8601: YYYY-MM-DD (2026-07-04) |
| Date (long) | 4 July 2026 |
| Time | ISO 8601, 24-hour, colon: 14:30 |
| Abbreviation full stop | Full stop at truncation, none at contraction: Mr, Dr, Ltd; but etc., vol. Does not apply to initialisms. |
| Oxford comma | No: red, white and blue |
| Currency — word | After the number, with a space: 100 dollars |
| Currency — ISO code | After the number, with a no-break space: 100 EUR |
| Number and unit | No-break space: 17 kg — per SI |
| Angular degree | Directly after the number: 90° |
| Temperature degree | No-break space between number and degree: 25 °C — per SI |
| Percent in figures | No-break space: 14 % — per SI |
| Percent in running text | Symbol kept: 14% |
| Degrees in running text | Symbol kept: 90° |

## Quotation marks

Straight ASCII quotation marks throughout — outer `"…"`, inner `'…'`. These are universally readable; Markdown/Pandoc smart-quote rendering produces typographically correct marks per language at render time when configured.

## Quotation conventions

Apply the universal regime in the *Quotation* section of `rules/constructions.md` as written. Use straight ASCII marks for all three modes (run-in, block, dialogue).

**Punctuation relative to quotation marks.** Apply the logical (British) convention: full stops and commas go inside the quotation marks only when they belong to the quoted material:

- He called it "revolutionary".
- "It was revolutionary."

## Punctuation conventions

**Dashes.** EN-dash (–) with spaces for parenthetical insertions and dramatic pauses. EN-dash without spaces for ranges.

**Abbreviation introduction.** When an abbreviation is not already established and familiar to the reader, introduce it by writing the full name first, followed by the abbreviation in parentheses:

> the General Data Protection Regulation (GDPR)

Subsequently use the abbreviation alone. Generally familiar abbreviations (UN, FBI, NATO) need no introduction.

## Greetings and closings

Comma after the salutation (*Dear Susanne,*). Comma after the closing phrase (*Best regards,*) on its own line, then the name on the next line.
