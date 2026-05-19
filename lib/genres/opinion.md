---
name: opinion
swedish_term: opinionstext
default_technique: abt
triggers:
  - opinionstext
  - opinion
  - debattartikel
  - debattinlägg
  - åsiktstext
  - "op-ed"
  - "opinion piece"
  - "debate article"
---

# Opinion piece

## Purpose

An opinion piece is a polemical text published in a public context to argue for or against a position. The author's voice is visible and load-bearing — but unlike the column, the position pushes outward rather than drawing inward. Typical channels: trade-press opinion pages, business-press debate pages, the author's own publication.

Distinguished from article: the article *informs* with a dampened authorial voice; the opinion piece *argues* with a positioned authorial voice. Same topic, different register.

Distinguished from column: the column is *drawing* — it draws the reader along through a story. Opinion is *pushing* — it pushes a message out. The column entertains while making a point; the opinion piece argues to convince or move.

Distinguished from report: the report *analyses* from a neutral position; the opinion piece *argues* from a declared position.

## Stylistic nuance

### Headings

H1 is a declarative thesis (*A new kind of agency threatens traditional agencies*) — not metaphorical, not narrative, not evocative. H2 subheadings are declarative argument-headlines (*Traditional agencies fail to meet demand*, *Disruptive change threatens traditional agencies*) or imperative calls to action (*Transform*, *Broaden the portfolio*, *Don't be a boiled frog*). Headings carry the argument — they tell the reader where each section is going before she gets there.

### Headline length

Maximum 60 characters.

### Tone — pushing

The text drives a message outward. Polemical, serious, deliberate. Humour is absent or rare — the opinion piece is not entertainment.

### Address

Explicit first person appears naturally when the writer is stating her own view (*I believe the agency market is facing a disruptive reshaping*, *My hope with this article is…*). Used sparingly enough that the focus stays on the argument, but the personal source of the position must be clear. Direct second-person is uncommon — the target audience is typically abstract (an industry, a collective recipient) rather than an individual reader.

### Opening

Thesis declared upfront in the standfirst or the first paragraph. The reader knows early what the writer thinks and where the text is going.

### Free language

Sentence fragments and conjunction-as-sentence-opener are permitted but used more sparingly than in column — only when the rhetorical effect is clear. The genre tolerates *But…!* as a fragment for emphasis; it does not tolerate fragments for rhythm alone.

### Rhetorical repetition

A phrase that returns after each argument, building cumulative effect, is well-suited to the opinion piece. From `rules/style.md`: this technique is used only in opinion-driven texts, never in fact articles or press releases.

### Sources

Inline references where the argument requires them. Source provenance reinforces the polemic. The agent never invents sources — see the global rule in `rules/style.md`.

### Length

Typically six hundred to fifteen hundred words. The argument's complexity governs length.

### Ending

Call to action — typically not a commercial CTA but an exhortation: *It is time to act*. The opinion piece lands in something concrete; an opinion piece that does not know what should happen is not finished.

## Default technique

ABT — applied in explicit-argumentative mode. The structure can and typically should be visible: opening conditions / status quo (A) → problem or mismatch (B) → action or transformation (T). The reader is meant to see each step. This is the inverse of column's preference for hidden structure — but the same A-B-T core. See `lib/techniques/abt.md`.

## Common pitfalls

Personal anecdote that softens the argument. The opinion piece pushes. Long scenes or self-reflective passages drain drive. If the material is reflective rather than argumentative — choose column.

Thesis omitted or hidden too long. The opinion piece's reader should know early what the author thinks. A thesis that appears halfway through is concealed polemic. Standfirst or the first paragraph should declare the position.

Fabricated sources or pseudo-authority. The opinion piece carries inline references. The agent must not invent books, authors, studies, or industry data to support an argument. The global rule applies: every cited source must exist and be verified.

Missing call to action. The opinion piece typically lands in something concrete — *transform*, *broaden the portfolio*, *it is time to act*. A piece that does not know what should happen is not finished.

AI-generated metaphors. The agent does not create new metaphors. If a metaphor exists in the source material, it can be used and developed — by staying with that one metaphor. The agent does not invent variants or add new metaphors. See `rules/style.md`.

ABT as visible formula in form rather than substance. The structure can be visible, but the labelling must not feel mechanical. Subheadings carry the argument — never as *A:*, *B:*, *T:*.

Finger-pointing or condescension toward the counterposition. The general rule from `rules/style.md` applies — argue without blame. Make the case for one's own position; do not attack the dignity of those who disagree.

Lost authorial position. The text drifts into neutral exposition and stops being an opinion piece. The author must remain visible as the source of the position.

## Trigger keywords

Triggers: opinionstext, opinion, debattartikel, debattinlägg, åsiktstext, op-ed, opinion piece, debate article.

The lean trigger principle applies. The Swedish *debattartikel*, *debattinlägg*, and *åsiktstext* are idiosyncratic and listed explicitly. Compounds and conjugations (*skriv en opinionstext*, *skriv en debattartikel*, *write an op-ed*, *write a debate piece*) are handled by the agent's semantic matching.

Blog-post disambiguation: blog posts are not opinion pieces. When the prompt uses *blogginlägg* or *blog post*, ask whether to write as article or column — never opinion.

Does not trigger: *skriv ett inlägg* alone (too broad), *kommentar* (different genre), *tweet* / *post* / *X-tråd* (other formats), *åsikt* or *tycker* without *text* / *artikel* / *opinion* (too weak a signal).
