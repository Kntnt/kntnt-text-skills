---
name: sv
language: Swedish
inherits:
---

# Swedish (sv)

Language conventions for Swedish. Loaded by skills when the input language is determined to be Swedish, or when the user passes `sv` or a Swedish territorial variant as a language argument.

A territorial variant file (e.g., `sv_FI.md`) may explicitly inherit from this file via `inherits: @sv.md` in its frontmatter and override the sections where it differs.

The file is organised in two layers. *Mechanics* is the proofread scope — typography, punctuation, quotation, grammar, and other objective conventions that the proofread pass applies. *Style* is the redline / edit scope — address, AI-tell manifestations, interference patterns, and genre-level adjustments that the critical-review passes apply on top of the proofread pass.

## Mechanics

### Typography

| Convention | Realisation |
|---|---|
| Thousands separator | Thin no-break space (U+202F): 1 234 567 |
| Decimal separator | Comma: 123,45 |
| Range | EN-dash without spaces: 2–5 |
| Parenthetical insertion | EN-dash with spaces: rött – tror jag |
| Date (short) | YYYY-MM-DD: 2026-07-04 |
| Date (long) | den 4 juli 2026 |
| Time | Full stop, 24-hour: 14.30 |
| Abbreviation full stop | Full stop at truncation, none at contraction: dr, vd, kr; but dir., dvs., osv. Does not apply to initialisms and acronyms: SEO, HTML, FN. |
| Oxford comma | No: rött, vitt och blått |
| Currency — symbol | After the number, with a no-break space: 100 € |
| Currency — word | After the number, with a space: 100 kronor |
| Currency — ISO code | After the number, with a no-break space: 100 SEK |
| Number and unit | No-break space: 17 kg |
| Angular degree | Directly after the number: 90° |
| Temperature degree | No-break space between number and degree: 25 °C |
| Percent in figures | No-break space: 14 % |
| Percent in running text | Written out: 14 procent (except in technical text) |
| Degrees in running text | Written out: 45 grader (except in technical text) |

### Quotation marks

Outer quotation marks: ” (U+201D) on both sides — Swedish does not distinguish opening and closing forms.

Inner quotation marks (quotation within a quotation): ’ (U+2019) on both sides.

Never use «…» or "…" with the angular forms reserved for other languages.

### Quotation conventions

Overrides to the universal *Quotation* rules in `rules/writing.md`.

#### Run-in quotation

Apply the universal regime, with these typographic substitutions:

- Replace the placeholder `"…"` with ”…”.
- Replace the placeholder `'…'` (inner quotation) with ’…’.

Full stops and commas go inside the quotation only when they belong to the quoted material: *Han kallade det ”revolutionerande”.* but *”Det var revolutionerande.”*

#### Block quotation

Apply the universal regime unchanged. The blockquote indentation is the marker; no Swedish-specific override.

#### Dialogue and attribution

Swedish distinguishes typographically between word-for-word quotation and rendered attribution. The two forms carry different promises to the reader.

- **Verbatim quotation.** Quotation marks ”…” signal that the words are reproduced exactly as the person said them — the writer vouches for the precise wording.
- **Rendered attribution.** Speech dash (talstreck, en-dash followed by space) signals that content and meaning are reproduced faithfully, but the writer may have adjusted word choice, removed disfluencies, hesitations, and colloquial constructions for readability. It looks like direct speech without the promise of word-for-word reproduction.

Examples:

> ”Jag tycker att det är helt oacceptabelt.” — verbatim, the writer guarantees the wording.
>
> – Jag tycker att det är helt oacceptabelt. — rendered, the meaning is faithful but the wording may be polished.

In articles, case studies, and press releases, rendered attribution with the speech dash is the standard. Verbatim quotation marks are used only when exact reproduction is essential — for instance, when a precise phrasing is itself the news.

A continued speech across paragraphs: each new paragraph by the same speaker opens with a speech dash; no closing mark is needed.

### Punctuation conventions

#### Dashes

EN-dash (–) with spaces around it is the Swedish standard for all dash uses — insertions, parenthetical additions, speech dashes, dramatic turns. Never EM-dash (—). The EM-dash is reserved for American English.

#### Abbreviation introduction

When an abbreviation is not already established and familiar, introduce it by writing the full name first, followed by the abbreviation in parentheses:

> Sveriges Lås- och Säkerhetsleverantörers Riksförbund (SLR) arbetar för att…

Subsequently use the abbreviation alone. Do not invert the order, do not use dashes instead of parentheses, do not introduce abbreviations that occur only once or twice — use the full name or a natural short form throughout (*riksförbundet*).

#### Lower-case initialisms

Initialisms that have become everyday words are written in lower case without full stops: tv, vd, it, brf, sms, bnp, dna, pc, cd. They are normally not spelled out in running text — they function as their own words. Spelling out *verkställande direktör (vd)* in running text is disruptive for a generally familiar form.

#### Upper-case initialisms

Initialisms that have not become everyday words are written in capitals without full stops. The spelled-out form follows normal capitalisation — lower case unless it is a proper name. Capitals in the abbreviation arise from the abbreviation, not from proper-name status:

- SEO = search engine optimization
- GDPR = general data protection regulation
- HTML = hypertext markup language

Not: *SEO = Search Engine Optimization* — that confuses the rule.

### Grammar specifics

#### Compound words

Swedish writes compounds as one word: *sjukvårdspersonal*, not *sjukvårds personal*. Split-compound errors (*särskrivning*) change meaning and must be corrected. This is one of the most common Swedish writing errors.

#### De/dem

*De* for the subject form (*De kom hem*), *dem* for the object form (*Jag såg dem*). The proofread pass corrects misuse.

#### Sin/sitt/sina vs. hans/hennes/dess

Reflexive forms (*sin*, *sitt*, *sina*) refer back to the sentence's subject. Possessive forms (*hans*, *hennes*, *dess*) refer to someone other than the subject. Mixing the two changes meaning.

#### En/ett agreement

Common gender (*en bil*) and neuter (*ett hus*) agreement must be maintained throughout — articles, adjectives, pronouns.

### Greetings and closings

Greetings use *!* not *,*: *Hej Susanne!* not *Hej Susanne,*. The comma is an English convention and reads as imported.

Closing salutations have no comma before the name line: *Med vänlig hälsning* on its own line, then the name on the next line — no comma between them.

## Style

### Address and voice

Per-content-type pronoun usage layered on top of the universal *Address and voice* guidance in `rules/style.md`.

- **Web copy, article.** *Du* sparingly and as deliberate emphasis; more often the sense of address without explicit *du* (*Vad är det här bra för?* rather than *Du undrar nog…*). *Vi* invites the reader (*Vi tittar närmare på…*).
- **Column and personal articles.** Almost always *du*. The writer can be visible without *jag*; when motivated, *jag* is used. Free language permitted — sentence fragments, conjunctions as openers, direct tone.
- **Reports and e-book chapters.** No *du*. *Vi* refers to the reporting or acting organisation (the internal team, or — when the consultant is embedded — the client's organisation including the consultant). When the consultant is an external auditor coming from outside, the client is addressed as *ni*. The subject under examination is referred to in the third person, by name.
- **Case study.** *Du* is avoided. The interviewees carry the narrative. The sender is referred to in the third person — never as *vi* or *vår lösning* in the writer's voice.
- **Press release.** No *du* at all. Neutral, journalistic tone.

The impersonal pronoun *man* is used only where it is justified. If it can be avoided naturally, avoid it.

### AI-tell manifestations (Lukttest)

Constructions that reveal AI authorship in Swedish — typically calques from English AI tropes:

- *Låt mig vara helt tydlig* (calque of *Let me be perfectly clear*)
- *I en värld där…* (calque of *In a world where…*)
- *Det är värt att notera att…* (calque of *It's worth noting that…*)
- *Dyk djupare* (calque of *dive deeper*)
- *Sammanfattningsvis* at the start of a conclusion — too formulaic
- *Operativa frågor*, *strategiska val*, *proaktiv approach* — management jargon. Describe instead what is concretely meant.

The Smell Test (*Lukttestet*): read each sentence and ask "would a Swedish journalist at DI or SvD write this?" If the answer is no, rewrite.

### Interference from English (anglicisms)

Common anglicisms to substitute when writing Swedish:

- *regulatorer* → *myndigheter* or *tillsynsmyndigheter*
- *adressera* (in the sense "take up") → *ta upp* or *behandla*
- *navigera* (metaphorically) → *hantera*
- *leverera* (in the sense "give") → *ge* or *erbjuda*
- *metrik* → *mätvärde* or *nyckeltal*

The list is illustrative, not exhaustive. The principle is: prefer the established Swedish term over the English loan when both work. Use established English terms only when they are genuinely the natural choice in the field.

### Genre adjustments

#### Press release

The speech dash is the standard for attribution. Quotation marks are used only when verbatim reproduction is essential.

#### Case study

Same: speech dashes for attribution; quotation marks reserved for verbatim quotation. The interviewee drives the narrative through attributed speech-dash quotes; the writer keeps a low profile.

#### Report

Swedish typographic rules apply rigorously: *procent* written out in running text, no-break space between number and unit, dates in ISO format or written out (*den 24 mars kl. 20.00*). Abbreviations introduced with the full form at first occurrence per `rules/writing.md` — *sökmotoroptimering (SEO)* — then abbreviated.

#### Teaser

The Swedish term *puff* is the user's idiomatic form. *Ingress* is the user's term for *standfirst* — not for the lead paragraph. Listed explicitly in the teaser triggers because the mapping from English does not always hold.

#### General

Common subgenres carry idiosyncratic Swedish names: *mejl*, *PM*, *promemoria*, *brev*. Listed explicitly in the general triggers.
