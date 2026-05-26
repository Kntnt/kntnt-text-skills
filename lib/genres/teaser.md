---
name: teaser
swedish_term: puff
default_technique: abt
triggers:
  - puff
  - teaser
  - standfirst
  - ingress
  - "meta description"
  - metabeskrivning
---

# Teaser

## Purpose

Teaser is the parent concept for short, freestanding text whose only job is to move a scanning reader from *skip* to *click* or *read further*. A teaser is not its own text — it is a port to another text.

Special cases of teaser, each with their own positional or format constraints:

- *Standfirst* in an article — lives between H1 and the body; doubles as the article's teaser when the article is featured elsewhere. Positional rules in `article.md`; writing rules here.
- *Meta description* — the SERP body text under the title, technically capped at approximately 160 characters.
- *Newsletter teaser* — lives inside an email newsletter, linking to an article or page.
- *Social-media post for a linked article* — including LinkedIn posts when the purpose is to tease a linked text. Bare social copy without that purpose is out of scope for the plugin.
- *Website teaser modules* — *latest from the blog*, *current case study*, archive pages, *read also* blocks — all variants of the same form.

The reader of a teaser is scanning: in a newsletter inbox, on a homepage, in a social feed. She has not decided to read anything yet — the teaser's job is to help her make that decision. Click or skip; nothing in between.

## Stylistic nuance

<!-- scope: write -->
### Structure

1. *Headline.* Typically the same as the headline of the text being teased, but can be its own. Functions as content declaration and interest hook.
2. *Condensed body.* Summarise what the text is about without giving away the interesting details. Lure the reader. Serve as the longer-form content declaration. The reader should know what she gets and want it.
3. *Lightweight CTA.* *Read the guide*, *See the analysis*, *See how they did it*. The action is always click. Generic *Read more* is weaker than a verb that names the promise.

<!-- scope: write -->
### Mini-ABT as microstructure

The genre standard: start with the necessary fact (A), introduce the conflict or question (B), hint at the solution or promise (T), end with the CTA. The entire arc fits within about sixty words — that is the craft. The *but* and *therefore* do not have to be explicit; implication is enough.

<!-- scope: write -->
### Tone

Tone matches the source text's voice but condensed. A teaser for an article should sound like the article's author, not like a marketing department. The standfirst in an article is the article's own entry to itself.

<!-- scope: write -->
### Voice and address

Direct, active. Direct second-person sparingly and as emphasis. The source text's address choices govern. A case-study teaser holds distance (the client's voice carries); an article teaser can be more direct.

<!-- scope: write -->
### Length

Standard about sixty words for newsletter blocks, web modules, standalone teasers, and standfirsts. Meta descriptions: maximum 160 characters, aim for 155. Other social-media platforms: the platform's own length and tone conventions apply on top of these principles.

<!-- scope: write -->
### Headline length

Maximum 60 characters.

<!-- scope: write -->
### Meta title

When the teaser format is meta description, generate a meta title as well. The title obeys the standard headline rule (60 characters) and does not include company-name suffixes (*| Company*) — the CMS template adds those.

### Standalone readability

The teaser must function with no surrounding context — the reader has not seen the source yet. No unresolved pronouns, no backward references, no assumed prior understanding. The standalone-readability principle from the *Headed text* section of `rules/constructions.md` applies more strictly here than anywhere else.

<!-- scope: write -->
## Default technique

Mini-ABT — see *Stylistic nuance* above. Inherited from `lib/techniques/abt.md` but applied at microstructure scale (the whole teaser is the ABT, not a section of a longer text).

<!-- scope: review -->
## Common pitfalls

Clickbait or overstatement. *You will never believe what X did*, *The incredible truth about Y*. The content declaration breaks when the reader clicks. Trust is spent on the first click and not recovered.

Giving away the solution. The teaser answers its own B. There is nothing left to click for. T should be hinted at, not delivered.

Vague or generic. *We have written an interesting article about marketing*. Says nothing about what the reader gets. The content declaration is empty.

Missing or unclear CTA. The action is always click — but the act of clicking is not enough. The CTA must name the promise the click delivers. A generic *Read more* underperforms a task-specific verb.

Not standalone. The teaser opens with *The system solves the problem* — but *the system* has not been introduced. Definite forms and pronouns presume a context the reader does not have.

Lost source voice. The teaser sounds like a marketing department when the source is an author-driven article. Or the reverse: a case-study teaser that sounds like the article author's voice instead of holding the client's voice central. The teaser inherits the source text's tone.

## Trigger keywords

Triggers: puff, teaser, standfirst, ingress, meta description, metabeskrivning.

The lean trigger principle applies. Swedish *puff* and *ingress* (the user's term for standfirst, not lead paragraph) are listed explicitly because they are idiosyncratic. *Standfirst* is shared across languages. Compounds and conjugations (*skriv en puff*, *puffa för*, *newsletter teaser*, *social teaser*, *SEO title*, *SEO description*, *blurb*) are handled by the agent's semantic matching.

Does not trigger: LinkedIn posts, Facebook posts, social media posts *without* teaser framing — these are bare social copy and out of scope. Ad copy, *annonscopy*, Google Ads — explicitly out of scope. Generic *short text* — too broad to commit.
