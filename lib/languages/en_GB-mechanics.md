---
name: en_GB
language: British English
layer: mechanics
---

# British English mechanics (en_GB)

The proofread-scope language file for British English — typography, punctuation, quotation, and other objective conventions that the proofread pass applies. Loaded by skills when the input language is determined to be British English, or when the user passes `en_GB` (or selects British English when `en`, `en_GB`, and `en_US` all exist) as a language argument.

The companion file `en_GB-style.md` carries the redline / edit scope — address, AI-tell manifestations, interference patterns, and genre-level adjustments.

## Typography

| Convention | Realisation |
|---|---|
| Thousands separator | Comma: 1,234,567 |
| Decimal separator | Full stop: 123.45 |
| Range | EN-dash without spaces: 2–5 |
| Parenthetical insertion | EN-dash with spaces: red – I think |
| Date (short) | DD/MM/YYYY: 04/07/2026 |
| Date (long) | 4 July 2026 |
| Time | Full stop, 24-hour: 14.30 |
| Abbreviation full stop | Full stop at truncation, none at contraction: Mr, Dr, Ltd; but etc., vol. Does not apply to initialisms: GDP, NATO, BBC. |
| Oxford comma | No: red, white and blue |
| Currency — symbol | Before the number, no space: £100 |
| Currency — word | After the number, with a space: 100 pounds |
| Currency — ISO code | Before the number, with a no-break space: GBP 100 |
| Number and unit | No-break space: 17 kg |
| Angular degree | Directly after the number: 90° |
| Temperature degree | No-break space between number and degree: 25 °C |
| Percent in figures | Space: 14 % |
| Percent in running text | Symbol kept: 14%, sometimes written out: 14 per cent |
| Degrees in running text | Symbol kept: 90° |

## Quotation marks

Outer quotation marks: ‘ (U+2018) opening, ’ (U+2019) closing.

Inner quotation marks (quotation within a quotation): “ (U+201C) opening, ” (U+201D) closing — the opposite of American English.

## Quotation conventions

Overrides to the universal *Quotation* rules in `rules/quotation.md`.

### Run-in quotation

Apply the universal regime, with these typographic substitutions:

- Replace the placeholder `"…"` (outer) with ‘…’.
- Replace the placeholder `'…'` (inner) with “…”.

**Punctuation relative to quotation marks.** Full stops and commas are placed inside the quotation only when they belong to the quoted material:

- He called it ‘revolutionary’.
- ‘It was revolutionary.’

This is the opposite of the American convention, which always places full stops and commas inside.

### Block quotation

Apply the universal regime unchanged.

### Dialogue

Apply the universal regime with British outer marks (single):

- ‘I'll come,’ she said.
- ‘Will you?’ she asked.

Question marks and exclamation marks belong to the spoken utterance and stay inside the quotation.

## Punctuation conventions

### Dashes

EN-dash (–) with spaces is the British standard for parenthetical insertions and dramatic pauses. The same dash is used for ranges, but without spaces. EM-dash (—) is reserved for American English and does not appear in British text.

### Abbreviation introduction

When an abbreviation is not already established and familiar to the reader, introduce it by writing the full name first, followed by the abbreviation in parentheses:

> the General Data Protection Regulation (GDPR)

Subsequently use the abbreviation alone. Generally familiar abbreviations (UN, FBI, NATO) need no introduction.

## Greetings and closings

Email and letter greetings: comma after the salutation (*Dear Susanne,*). Closings: comma after the closing phrase (*Best regards,*) on its own line, then the name on the next line.
