---
name: en_GB
language: British English
---

# British English (en_GB)

The language file for British English — both the proofread-scope mechanics (typography, punctuation, quotation) and the redline / edit-scope style (address, AI-tell manifestations, interference patterns, genre adjustments). Loaded by skills when the input language is determined to be British English, or when the user passes `en_GB` (or selects British English when `en`, `en_GB`, and `en_US` all exist) as a language argument. `/proofread` applies only the mechanics section; `/redline`, `/edit`, and `/write` apply both.

<!-- layer: mechanics -->
## Mechanics (proofread scope)

### Typography

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

### Quotation marks

Outer quotation marks: ‘ (U+2018) opening, ’ (U+2019) closing.

Inner quotation marks (quotation within a quotation): “ (U+201C) opening, ” (U+201D) closing — the opposite of American English.

### Quotation conventions

Overrides to the universal *Quotation* rules in `rules/constructions.md`.

#### Run-in quotation

Apply the universal regime, with these typographic substitutions:

- Replace the placeholder `"…"` (outer) with ‘…’.
- Replace the placeholder `'…'` (inner) with “…”.

**Punctuation relative to quotation marks.** Full stops and commas are placed inside the quotation only when they belong to the quoted material:

- He called it ‘revolutionary’.
- ‘It was revolutionary.’

This is the opposite of the American convention, which always places full stops and commas inside.

#### Block quotation

Apply the universal regime unchanged.

#### Dialogue

Apply the universal regime with British outer marks (single):

- ‘I'll come,’ she said.
- ‘Will you?’ she asked.

Question marks and exclamation marks belong to the spoken utterance and stay inside the quotation.

### Punctuation conventions

#### Dashes

EN-dash (–) with spaces is the British standard for parenthetical insertions and dramatic pauses. The same dash is used for ranges, but without spaces. EM-dash (—) is reserved for American English and does not appear in British text.

#### Abbreviation introduction

When an abbreviation is not already established and familiar to the reader, introduce it by writing the full name first, followed by the abbreviation in parentheses:

> the General Data Protection Regulation (GDPR)

Subsequently use the abbreviation alone. Generally familiar abbreviations (UN, FBI, NATO) need no introduction.

### Greetings and closings

Email and letter greetings: comma after the salutation (*Dear Susanne,*). Closings: comma after the closing phrase (*Best regards,*) on its own line, then the name on the next line.

<!-- layer: style -->
## Style (redline / edit scope)

### Address and voice

Direct second-person *you* is the only address form available; the language lacks a T-V distinction. The variation across genres is therefore not pronoun-driven but tonal — direct *you* in column or web copy, impersonal *the reader* or third-person in report.

For the universal per-genre voice guidance, see `rules/style.md`.

### AI-tell manifestations

Constructions that reveal AI authorship in British English:

- *Let me be perfectly clear* — performative claim that reveals the opposite.
- *In a world where…* — opening cliché.
- *It's worth noting that…* / *It is important to note that…* — empty bridge.
- *Delve into* / *dive deeper* — AI darling verbs.
- *In summary* / *To summarise* opening a conclusion — too formulaic.
- *Multifaceted*, *tapestry*, *navigate* (used metaphorically), *leverage* (as a verb), *streamline*, *robust*, *comprehensive*, *ultimately* — AI vocabulary tells.
- *Furthermore* and *moreover* used as crutches between paragraphs — symptom of weak structure.
- Management jargon: *strategic*, *proactive*, *synergies*, *holistic approach* — describe instead what is concretely meant.

The Smell Test: read each sentence and ask "would a writer at the *Guardian* or *Financial Times* write this?" If the answer is no, rewrite.

### Interference from American English

British text occasionally drifts toward American constructions. Watch for and substitute:

- American *-ize* / *-ization* spellings → British *-ise* / *-isation* (where the *-ise* form is the British preference; note that some words like *capsize* are *-ize* in both).
- *Going forward* → *in future* or omit.
- *Reach out to* → *contact* or *get in touch with*.
- *Leverage* as a verb → *use*, *exploit*, *draw on*.
- *On accident* → *by accident*.
- AmE punctuation inside quotation marks → place punctuation outside unless it belongs to the quote.
- AmE date order (MM/DD/YYYY) → DD/MM/YYYY.
- *Train station* (now common in BrE too) vs. traditional *railway station* — judgement call by register.

### Genre adjustments

#### Press release

British attribution uses inverted commas around direct speech. Speech dashes are not a British convention.

#### Case study

Quotation marks (single, British convention) for attributed speech. The carrying-voices principle from `rules/style.md` applies regardless of language.
