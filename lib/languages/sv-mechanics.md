---
name: sv
language: Swedish
layer: mechanics
---

# Swedish mechanics (sv)

The proofread-scope language file for Swedish — typography, punctuation, quotation, grammar, and other objective conventions that the proofread pass applies. Loaded by skills when the input language is determined to be Swedish, or when the user passes `sv` or a Swedish territorial variant as a language argument.

The companion file `sv-style.md` carries the redline / edit scope — address, AI-tell manifestations, interference patterns, and genre-level adjustments.

## Typography

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
| Genitiv av namn på -s, -x, -z | Noll-markering är förstahandsval: *Marx teorier*, *CoMaps föregångare*. Apostrof ensam (*Andreas'*) endast vid genuin tvetydighet. *'s* (*CoMaps's*) är aldrig korrekt på svenska. Se grammatikregeln nedan för undantag. |

## Quotation marks

Outer quotation marks: ” (U+201D) on both sides — Swedish does not distinguish opening and closing forms.

Inner quotation marks (quotation within a quotation): ’ (U+2019) on both sides.

Never use «…» or "…" with the angular forms reserved for other languages.

## Quotation conventions

Overrides to the universal *Quotation* rules in `rules/quotation.md`.

### Run-in quotation

Apply the universal regime, with these typographic substitutions:

- Replace the placeholder `"…"` with ”…”.
- Replace the placeholder `'…'` (inner quotation) with ’…’.

Full stops and commas go inside the quotation only when they belong to the quoted material: *Han kallade det ”revolutionerande”.* but *”Det var revolutionerande.”*

### Block quotation

Apply the universal regime unchanged. The blockquote indentation is the marker; no Swedish-specific override.

### Dialogue and attribution

Swedish distinguishes typographically between word-for-word quotation and rendered attribution. The two forms carry different promises to the reader.

- **Verbatim quotation.** Quotation marks ”…” signal that the words are reproduced exactly as the person said them — the writer vouches for the precise wording.
- **Rendered attribution.** Speech dash (talstreck, en-dash followed by space) signals that content and meaning are reproduced faithfully, but the writer may have adjusted word choice, removed disfluencies, hesitations, and colloquial constructions for readability. It looks like direct speech without the promise of word-for-word reproduction.

Examples:

> ”Jag tycker att det är helt oacceptabelt.” — verbatim, the writer guarantees the wording.
>
> – Jag tycker att det är helt oacceptabelt. — rendered, the meaning is faithful but the wording may be polished.

In articles, case studies, and press releases, rendered attribution with the speech dash is the standard. Verbatim quotation marks are used only when exact reproduction is essential — for instance, when a precise phrasing is itself the news.

A continued speech across paragraphs: each new paragraph by the same speaker opens with a speech dash; no closing mark is needed.

## Punctuation conventions

### Dashes

EN-dash (–) with spaces around it is the Swedish standard for all dash uses — insertions, parenthetical additions, speech dashes, dramatic turns. Never EM-dash (—). The EM-dash is reserved for American English.

### Abbreviation introduction

When an abbreviation is not already established and familiar, introduce it by writing the full name first, followed by the abbreviation in parentheses:

> Sveriges Lås- och Säkerhetsleverantörers Riksförbund (SLR) arbetar för att…

Subsequently use the abbreviation alone. Do not invert the order, do not use dashes instead of parentheses, do not introduce abbreviations that occur only once or twice — use the full name or a natural short form throughout (*riksförbundet*).

### Lower-case initialisms

Initialisms that have become everyday words are written in lower case without full stops: tv, vd, it, brf, sms, bnp, dna, pc, cd. They are normally not spelled out in running text — they function as their own words. Spelling out *verkställande direktör (vd)* in running text is disruptive for a generally familiar form.

### Upper-case initialisms

Initialisms that have not become everyday words are written in capitals without full stops. The spelled-out form follows normal capitalisation — lower case unless it is a proper name. Capitals in the abbreviation arise from the abbreviation, not from proper-name status:

- SEO = search engine optimization
- GDPR = general data protection regulation
- HTML = hypertext markup language

Not: *SEO = Search Engine Optimization* — that confuses the rule.

## Grammar specifics

### Compound words

Swedish writes compounds as one word: *sjukvårdspersonal*, not *sjukvårds personal*. Split-compound errors (*särskrivning*) change meaning and must be corrected. This is one of the most common Swedish writing errors.

### De/dem

*De* for the subject form (*De kom hem*), *dem* for the object form (*Jag såg dem*). The proofread pass corrects misuse.

### Sin/sitt/sina vs. hans/hennes/dess

Reflexive forms (*sin*, *sitt*, *sina*) refer back to the sentence's subject. Possessive forms (*hans*, *hennes*, *dess*) refer to someone other than the subject. Mixing the two changes meaning.

### En/ett agreement

Common gender (*en bil*) and neuter (*ett hus*) agreement must be maintained throughout — articles, adjectives, pronouns.

### Genitiv av namn på -s, -x, -z

När ett namn (egennamn eller annat substantiv) i grundform slutar på ett s-ljud — alltså på bokstaven *-s*, *-x* eller *-z* — ska genitiv normalt markeras med **noll-markering**: grundformen får stå oförändrad och får sin genitivfunktion av sammanhanget. Det är förstahandsvalet enligt Isof / Språkrådets Frågelådan, TT-språket och Språkkonsulterna.

- *Marx teorier* (inte *Marx's teorier*, inte *Marx' teorier*)
- *CoMaps föregångare* (inte *CoMaps's föregångare*)
- *Anders bok*, *Lars cykel*, *Felix skor*

**Apostrof ensam** (*Andreas'*) är tillåten endast när noll-markeringen är genuint tvetydig — alltså när läsaren riskerar att läsa formen som nominativ snarare än genitiv och kontexten inte räddar tolkningen. Använd den sparsamt; i de flesta löpande texter räcker noll-markeringen.

**Engelsk apostrof-s** (*'s*) — *CoMaps's föregångare*, *Andreas's bok* — är **aldrig** korrekt på svenska. Det är en interferens från engelskan och ska rättas. Förstahandsvalet är att stryka *'s* helt och behålla grundformen (*CoMaps föregångare*, *Andreas bok*); endast om den formen är genuint tvetydig kan en ensam apostrof användas (*Andreas'*).

**Fonetiskt undantag.** När namnets uttal slutar på en *vokal* eller på *annan konsonant än ett tydligt s-ljud* — trots att stavningen har *-s*, *-x* eller *-z* sist — ska slut-*s* för genitiv läggas till på vanligt sätt, eftersom genitivet annars inte hörs:

- *Alices bok* (uttalas /aˈliːsəs/ — basformen slutar på vokal i uttalet)
- *Assanges försvar* (uttalas med /ʃ/, inte /s/, i slutet)
- *Buschs anförande* (uttalas med /ʃ/-ljud)
- *Louises kommentar* (basformen slutar på vokal i uttalet)
- *Ibrahimovics mål* (basformen slutar på /tʃ/-ljud, inte /s/)

**Stam som inte slutar på s-ljud.** För namn vars grundform inte slutar på ett s-ljud lägger man på vanligt vis till *-s* i genitiv, även om stavningen råkar ha andra sibilanter i sig:

- *Lagerkvists romaner*
- *Wallenbergs intressen*

Regeln gäller även varumärken och företagsnamn som slutar på *-s*, *-x* eller *-z* (*CoMaps*, *Volvox*). Noll-markering är förstahandsvalet; apostrof ensam endast vid tvetydighet; *'s* aldrig.

Källor: Isof / Språkrådets Frågelådan, TT-språket, Språkkonsulterna.

## Greetings and closings

Greetings use *!* not *,*: *Hej Susanne!* not *Hej Susanne,*. The comma is an English convention and reads as imported.

Closing salutations have no comma before the name line: *Med vänlig hälsning* on its own line, then the name on the next line — no comma between them.
