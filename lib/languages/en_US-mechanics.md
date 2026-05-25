---
name: en_US
language: American English
layer: mechanics
---

# American English mechanics (en_US)

The proofread-scope language file for American English — typography, punctuation, quotation, and other objective conventions that the proofread pass applies. Loaded by skills when the input language is determined to be American English, or when the user passes `en_US` (or selects American English when `en`, `en_GB`, and `en_US` all exist) as a language argument.

The companion file `en_US-style.md` carries the redline / edit scope — address, AI-tell manifestations, interference patterns, and genre-level adjustments.

## Typography

| Convention | Realisation |
|---|---|
| Thousands separator | Comma: 1,234,567 |
| Decimal separator | Full stop: 123.45 |
| Range | EN-dash without spaces: 2–5 |
| Parenthetical insertion | EM-dash without spaces: red—I think |
| Date (short) | MM/DD/YYYY: 07/04/2026 |
| Date (long) | July 4, 2026 |
| Time | Colon, 12-hour: 2:30 PM |
| Abbreviation full stop | Always full stop: Mr., Dr., Inc. Does not apply to initialisms: CEO, HTML, NASA. |
| Oxford comma | Yes: red, white, and blue |
| Currency — symbol | Before the number, no space: $100 |
| Currency — word | After the number, with a space: 100 dollars |
| Currency — ISO code | Before the number, with a no-break space: USD 100 |
| Number and unit | No-break space: 17 kg |
| Angular degree | Directly after the number: 90° |
| Temperature degree | Directly after the number: 77°F |
| Percent in figures | Directly after the number: 14% |
| Percent in running text | Symbol kept: 14% |
| Degrees in running text | Symbol kept: 90° |

## Quotation marks

Outer quotation marks: “ (U+201C) opening, ” (U+201D) closing.

Inner quotation marks (quotation within a quotation): ‘ (U+2018) opening, ’ (U+2019) closing — the opposite of British English.

## Quotation conventions

Overrides to the universal *Quotation* rules in `rules/quotation.md`.

### Run-in quotation

Apply the universal regime, with these typographic substitutions:

- Replace the placeholder `"…"` (outer) with “…”.
- Replace the placeholder `'…'` (inner) with ‘…’.

**Punctuation relative to quotation marks.** Full stops and commas always go inside the quotation marks, regardless of whether they belong to the quoted material:

- He called it “revolutionary.”
- “It was revolutionary.”

This is the opposite of the British convention, which places punctuation outside unless it belongs to the quote. Colons and semicolons go outside the quote in both varieties.

### Block quotation

Apply the universal regime unchanged.

### Dialogue

Apply the universal regime with American outer marks (double):

- “I'll come,” she said.
- “Will you?” she asked.

Question marks and exclamation marks belong to the spoken utterance and stay inside the quotation.

## Punctuation conventions

### Dashes

EM-dash (—) without surrounding spaces is the American standard for parenthetical insertions and dramatic pauses—as in this sentence. The EN-dash is used only for ranges (without spaces) and is not the parenthetical dash in American English.

### Abbreviation introduction

When an abbreviation is not already established and familiar to the reader, introduce it by writing the full name first, followed by the abbreviation in parentheses:

> the General Data Protection Regulation (GDPR)

Subsequently use the abbreviation alone. Generally familiar abbreviations (UN, FBI, NATO) need no introduction.

## Greetings and closings

Email and letter greetings: comma after the salutation (*Dear Susanne,*). Colon for formal business letters (*Dear Ms. Andersson:*). Closings: comma after the closing phrase (*Best regards,*) on its own line, then the name on the next line.
