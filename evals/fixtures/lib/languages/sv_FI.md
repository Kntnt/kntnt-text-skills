---
name: sv_FI
language: Finland Swedish
inherits: "@sv.md"
---

# Finland Swedish (sv_FI)

Territorial variant of Swedish for Finland. Inherits from `sv.md` and overrides only the H2 sections that differ. All other H2 sections under `<!-- layer: mechanics -->` and `<!-- layer: style -->` are carried through from the base file unchanged.

This overlay fixture exists for the eval suite — it exercises the overlay loader documented in `lib/protocols/language-resolution.md`. Real Finland-Swedish coverage would extend the same pattern.

<!-- layer: mechanics -->
## Typography

| Convention | Realisation |
|---|---|
| Thousands separator | Thin no-break space (U+202F): 1 234 567 |
| Decimal separator | Comma: 123,45 |
| Range | EN-dash without spaces: 2–5 |
| Parenthetical insertion | EN-dash with spaces: rött – tror jag |
| Date (short) | YYYY-MM-DD: 2026-07-04 |
| Date (long) | den 4 juli 2026 |
| Time | Colon, 24-hour: 14:30 — Finland-Swedish follows the Finnish colon convention rather than the Sweden-Swedish full stop. |
| Abbreviation full stop | Full stop at truncation, none at contraction: dr, vd, kr; but dir., dvs., osv. Does not apply to initialisms and acronyms: SEO, HTML, FN. |
| Oxford comma | No: rött, vitt och blått |
| Currency — symbol | After the number, with a no-break space: 100 € |
| Currency — word | After the number, with a space: 100 euro |
| Currency — ISO code | After the number, with a no-break space: 100 EUR |
| Number and unit | No-break space: 17 kg |
| Angular degree | Directly after the number: 90° |
| Temperature degree | No-break space between number and degree: 25 °C |
| Percent in figures | No-break space: 14 % |
| Percent in running text | Written out: 14 procent (except in technical text) |
| Degrees in running text | Written out: 45 grader (except in technical text) |

<!-- layer: style -->
