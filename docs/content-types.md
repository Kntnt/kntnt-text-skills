# Content types and techniques

What the plugin knows how to write, the narrative and analytical arcs it applies, and the bans that hold across every type. To add a content type or technique, see [`extending.md`](extending.md).

## Content types

The plugin covers ten content types — the last is a fallback:

| Content type | Swedish term | Default technique |
|---|---|---|
| Article / reportage / blog post | artikel | ABT |
| Case study | kundcase | ABT |
| Press release | pressmeddelande | none |
| Web copy | webbcopy | ABT (outer arc plus iterative microstructure) |
| Teaser | puff | mini-ABT (microstructure) |
| Report / whitepaper | rapport | PAC |
| Column | krönika | ABT (drawing, freely visible) |
| Opinion piece | opinionstext | ABT (pushing, explicit-argumentative) |
| GitHub README | README för GitHub | none |
| General (fallback) | allmän text | none |

Each content type has its own file in `lib/genres/` describing its purpose and context, stylistic nuance (tone, length, structure, headline conventions, address), default technique, and common pitfalls. The files are compact — only what distinguishes the type from the general rules. Language-specific realisations (e.g. which mark renders attribution in a particular language) come from the loaded language files. Sections within each genre file are annotated with `<!-- scope: write -->` or `<!-- scope: review -->` markers so write-only sections are skipped during review passes and vice versa; sections relevant to both phases are left unmarked.

Maximum headline length is 60 characters for every H1, H2, H3, and below across all content types.

**Blog post.** *Blog post* / *blogginlägg* is not a content type of its own. When you ask for a blog post, the plugin asks whether it should be written as article or column.

**E-book.** E-books are handled chapter by chapter. The plugin asks per chapter which content type fits (article, case study, or report are the most common).

**Out of scope.** Ad copy, Google Ads copy, and bare social-media copy without a teaser purpose are explicitly outside the plugin's coverage.

## Techniques

Two techniques are installed out of the box:

- **ABT (And, But, Therefore)** — narrative arc. Sets the scene, introduces an obstacle or question, delivers the resolution. Default for article, case study, web copy, teaser, column, and opinion piece. The structure should be invisible to the reader — if the text feels formulaic, the technique has failed.
- **PAC (Premise, Analysis, Conclusion)** — analytical arc. Establishes the underlying material, analyses what it means, draws the conclusion. Default for report. Tolerates and even welcomes being visible at the section level — the reader of a report expects to see the path from data to conclusion.

Each technique file describes the arc concretely with variants (nesting, iteration, in medias res for ABT; nesting and partial PAC for PAC) and concrete examples.

**Techniques are not applied from training data.** If a user asks the plugin to use a technique that does not exist as an installed file in `lib/techniques/` (e.g. *PAS*), the plugin refuses and points to the alternatives. This is deliberate: techniques are installed artefacts, not claimed capabilities.

## Global rules

Three global rules apply across all content types wherever the redline pass runs — `/redline` Phase 2, `/edit` Phase 2, and `/write` Phase 4:

- **Source fabrication ban.** Every source cited — book, article, study, author, interview subject, dataset, statistic with attribution — must exist and be verified. The only exception is when the user explicitly requests a fictional source (e.g. a hypothetical interview subject as part of a thought experiment).
- **AI metaphor ban.** The plugin does not invent metaphors. If a metaphor exists in the source material, it can be used and deepened — by staying with that one metaphor. Invented metaphors are typically flat and undermine the text.
- **Rhetorical question rule.** The plugin does not invent rhetorical questions. If they appear in the source material, they can be kept and improved. Strict in report; looser in column and opinion where rhetorical address is part of the genre — but never as filler.
