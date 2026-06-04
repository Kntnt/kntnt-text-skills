---
name: article
swedish_term: artikel
default_technique: abt
triggers:
  - artikel
  - article
  - reportage
not_triggers:
  - "'report' or 'rapport' as the first word of a quoted working title (reportage from a conference, etc.)"
disambiguation:
  blogginlägg: "ask article-or-column"
  blog_post: "ask article-or-column"
  "skriv för bloggen": "ask article-or-column"
  "write for the blog": "ask article-or-column"
---

# Article

## Purpose

The article is pedagogical and informative, written with a dampened authorial voice. It conveys knowledge to a reader who came to learn or understand something. The same span covers reportage and feature articles where the writer reports from a place, an event or a topic – and standard knowledge articles for a blog, magazine or knowledge hub.

The reader of an article is interested in the subject but not in the writer's person. The writer's voice is present in structure and pace, not in personal exposure.

Blog posts are not a separate content type. When the user signals a blog post, ask whether to write as article or column.

## Stylistic nuance

<!-- scope: write -->
### Structure

Every article opens in this order:

1. **Headline (H1).** Maximum 60 characters, informative and inviting.
2. **Standfirst (italic).** Maximum about sixty words, self-contained. Functions as the article's teaser elsewhere – in newsletters, on the home page, in other contexts. The standfirst has its own mini-ABT: start with the necessary fact (A), introduce the conflict (B), continue with what to do about it (T) and close with a CTA that lures further reading. The writing rules for the text inside the standfirst live in `teaser.md` – the standfirst is structurally a special-case teaser. The two files cross-reference.
3. **Byline.** Text: the byline name from the brief.
4. **Lead.** The first paragraph of the body. Comes directly after the byline, without a preceding H2. Introduces the topic and sets expectation. It genuinely is the first paragraph of the article – not a continuation of the standfirst. The lead takes a different angle than the standfirst. If the standfirst summarises the risks, the lead can introduce the pattern of behaviour the article wants to break. Standfirst and lead must not begin with the same word.
5. **First subheading (H2).** Then the rest of the article continues with H2 subheadings and body text as usual.

**Multi-paragraph lead.** Normally the lead is a single paragraph, but a multi-paragraph lead can be justified when the article's opening requires a scenario (situation → complication → promise). In such cases the ABT structure should be clear: one or two paragraphs set the scene (A), one paragraph introduces the complication (B), and the last paragraph delivers the article's promise or roadmap (T). A multi-paragraph lead requires that the last paragraph make an explicit promise that the rest of the article then fulfils – do not omit anything that has been promised.

<!-- scope: review -->
### Repetition rule (specific to article elements)

H1, standfirst, lead and the first H2 section lie dangerously close to each other. The repetition rule from `rules/style.md` applies strictly here. Each element has its own distinct job: H1 plus standfirst form a self-contained teaser; the lead introduces and drives forward; the first H2 section concretises with details and examples. Rule of thumb: if you can strike the title, standfirst or lead without the reader missing any new information, you have repeated yourself.

<!-- scope: write -->
### Paragraphs

Normally two to three sentences, maximum about eighty words. Varying sentence length. A single sentence – or a single word – is acceptable when motivated.

<!-- scope: write -->
### Subheadings

H2, maximum 60 characters, descriptive. Normally two to three paragraphs between them. The last subheading introduces the closing section.

<!-- scope: write -->
### Closing

Fulfil the opening's promise. The last section (under its own H2) should invite the reader to do something concrete based on what the article has been about. The section should contain a link to a page that helps the reader carry out the action (e.g., a contact form, a product page, a landing page). The link's URL and anchor text come from the brief.

<!-- scope: write -->
### Headline length

Maximum 60 characters for H1 and every subheading at every level.

<!-- scope: write -->
### In medias res opening

A particularly powerful device. An outer ABT that encloses the whole text. The outer A is baked into the scene – never placed as a separate exposition paragraph before B, because then the device is lost. The outer B is the in medias res scene itself, the hook. The outer T is the bridge paragraph that reveals the scene's frame (*It was not an attack…*) followed by the rest of the article. The rest of the article is the outer T and has its own overarching ABT, which can in turn be nested or iterated. Use the device sparingly and only when the situation has genuine drama. Otherwise it becomes mannerism. See `lib/techniques/abt.md`.

<!-- scope: write -->
## Default technique

ABT – applied invisibly. The reader should never feel the structure. See `lib/techniques/abt.md`.

<!-- scope: review -->
## Common pitfalls

Visible ABT formula. The structure must stay below the surface. If the text feels as if it follows a pattern, the technique has failed.

Standfirst and lead repeating each other. The standfirst is the article's teaser; the lead is the article's first paragraph. Different jobs, different angles.

Subheadings that tease rather than declare. Even though the article tolerates more atmospheric headings than web copy or report, subheadings still must not mislead. The promise made by the subheading is the contract with the reader.

Bridges that announce the structure. *Now we will turn to…*, *in the next section we will discuss…* – these break the flow. Seamless transitions are the goal; explicit bridges are a fallback when seamless does not work.

Quoted half-measures. If the article has interviewees, choose carrying voices or no quotes at all. The middle path – one or two quotes as garnish – does not work. See `rules/style.md`.

Invented metaphors and rhetorical questions. The global rules apply. See `rules/style.md`.

## Trigger keywords

Triggers: artikel, article, reportage.

The lean trigger principle applies. Canonical forms in both languages plus the Swedish term *reportage* because it does not always semantically match from English. Compounds and conjugations (*kunskapsartikel*, *fördjupningsartikel*, etc.) are handled by the agent's semantic matching.

Blog-post disambiguation: when the prompt uses *blogginlägg*, *blog post*, *skriv för bloggen* or *write for the blog*, ask whether the post should be written as article or column.

E-book disambiguation: when the prompt mentions an e-book or e-book chapter, ask per chapter which content type applies.

Does not trigger: when *report* or *rapport* appears as the first word of a quoted working title (e.g., *write an article with the working title "Report from the security conference"*) – that is reportage-article territory.
