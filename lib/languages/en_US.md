---
name: en_US
language: American English
---

# American English (en_US)

The language file for American English — both the proofread-scope mechanics (typography, punctuation, quotation) and the redline / edit-scope style (address, AI-tell manifestations, interference patterns, genre adjustments). Loaded by skills when the input language is determined to be American English, or when the user passes `en_US` (or selects American English when `en`, `en_GB`, and `en_US` all exist) as a language argument. `/proofread` applies only the mechanics section; `/redline`, `/edit`, and `/write` apply both.

<!-- layer: mechanics -->
## Mechanics (proofread scope)

### Typography

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

### Quotation marks

Outer quotation marks: “ (U+201C) opening, ” (U+201D) closing.

Inner quotation marks (quotation within a quotation): ‘ (U+2018) opening, ’ (U+2019) closing — the opposite of British English.

### Quotation conventions

Overrides to the universal *Quotation* rules in `rules/constructions.md`.

#### Run-in quotation

Apply the universal regime, with these typographic substitutions:

- Replace the placeholder `"…"` (outer) with “…”.
- Replace the placeholder `'…'` (inner) with ‘…’.

**Punctuation relative to quotation marks.** Full stops and commas always go inside the quotation marks, regardless of whether they belong to the quoted material:

- He called it “revolutionary.”
- “It was revolutionary.”

This is the opposite of the British convention, which places punctuation outside unless it belongs to the quote. Colons and semicolons go outside the quote in both varieties.

#### Block quotation

Apply the universal regime unchanged.

#### Dialogue

Apply the universal regime with American outer marks (double):

- “I'll come,” she said.
- “Will you?” she asked.

Question marks and exclamation marks belong to the spoken utterance and stay inside the quotation.

### Punctuation conventions

#### Dashes

EM-dash (—) without surrounding spaces is the American standard for parenthetical insertions and dramatic pauses—as in this sentence. The EN-dash is used only for ranges (without spaces) and is not the parenthetical dash in American English.

#### Abbreviation introduction

When an abbreviation is not already established and familiar to the reader, introduce it by writing the full name first, followed by the abbreviation in parentheses:

> the General Data Protection Regulation (GDPR)

Subsequently use the abbreviation alone. Generally familiar abbreviations (UN, FBI, NATO) need no introduction.

### Greetings and closings

Email and letter greetings: comma after the salutation (*Dear Susanne,*). Colon for formal business letters (*Dear Ms. Andersson:*). Closings: comma after the closing phrase (*Best regards,*) on its own line, then the name on the next line.

<!-- layer: style -->
## Style (redline / edit scope)

### Address and voice

Direct second-person *you* is the only address form available; the language lacks a T-V distinction. The variation across genres is therefore not pronoun-driven but tonal — direct *you* in column or web copy, impersonal *the reader* or third-person in report.

For the universal per-genre voice guidance, see `rules/style.md`.

### AI-tell manifestations

Constructions that reveal AI authorship in American English:

- *Let me be perfectly clear* — performative claim that reveals the opposite.
- *In a world where…* — opening cliché.
- *It's worth noting that…* / *It is important to note that…* — empty bridge.
- *Delve into* / *dive deeper* — AI darling verbs.
- *In summary* / *To summarize* opening a conclusion — too formulaic.
- *Multifaceted*, *tapestry*, *navigate* (used metaphorically), *leverage* (as a verb), *streamline*, *robust*, *comprehensive*, *ultimately*, *unprecedented* — AI vocabulary tells.
- *Furthermore* and *moreover* used as crutches between paragraphs — symptom of weak structure.
- *Game-changer*, *paradigm shift*, *next-generation* — overused intensifiers.
- Management jargon: *strategic*, *proactive*, *synergies*, *holistic approach*, *circle back*, *touch base* — describe instead what is concretely meant.

The Smell Test: read each sentence and ask "would a writer at the *New York Times* or *The Atlantic* write this?" If the answer is no, rewrite.

### Interference from other registers

American English is the dominant variety in AI training data, so cross-language interference is the smaller risk. Watch instead for register drift inside American English:

- Corporate jargon bleeding into editorial prose.
- Tech-industry diction in non-tech contexts.
- Marketing register in factual contexts.

If the target register is editorial, hold the line against corporate or marketing register even when the underlying subject is business.

### Genre adjustments

#### Press release

American attribution uses double quotation marks around direct speech. Speech dashes are not an American convention.

#### Case study

Double quotation marks for attributed speech. The carrying-voices principle from `rules/style.md` applies regardless of language.
