---
name: web-copy
swedish_term: webbcopy
default_technique: abt
triggers:
  - webbcopy
  - "web copy"
  - webbtext
  - "web text"
---

# Web copy

## Purpose

Web copy is not a page-template content type. It is the principle set for writing text intended for web reading – used by other skills and specifications that produce specific page types (landing pages, pillar pages, cornerstone content, service pages, product pages, about pages, category pages). When this content type is invoked, the output follows these principles. The structural shell of the actual page – which sections, what CTA, what blocks – is dictated by the calling context or the brief, not by this file.

Readers of web copy are scanning, not reading linearly. They arrive cold from search or referral, do not always know where on the site they have landed and need to find what they want and skip the rest. Every choice in web copy serves that scanning behaviour.

<!-- scope: write -->
## Stylistic nuance

Scanability is the organising constraint. All other choices serve it.

Headlines and subheadings are content declarations, not teases. When the reader jumps in mid-page, the heading must immediately tell her what the section is about so she can decide whether to read it or move on. Never clever, never cliffhanger-style, never teasing. The heading is a contract with the scanner about the contents of the section.

Short, direct paragraphs. No throat-clearing, no preamble. Get to the point.

Visual typography is used where it carries information. Bullet lists when the content is genuinely a list. Tables when content is genuinely comparative. Pull quotes when a single sentence carries weight. Callouts (GFM `> [!NOTE]` syntax in markdown) for sidebars that genuinely break out of the main flow. Definition lists (`<dl>`/`<dt>`/`<dd>`) for term-definition pairs. Collapsible details (`<details>`/`<summary>`) for progressive disclosure of secondary information. Each visual element must serve the information – decoration breaks scanability rather than supporting it.

Direct, active voice. The reader is spoken to as an individual. The risk is not first-person plural or the company name – those are fine on a web page. The risk is the text *describing* instead of *speaking*. When prose slides into abstract reference (*Decision-makers in the housing industry face complex challenges…*) the reader's sense of being addressed disappears. The feeling of address is built through direct active verbs, questions and concrete situations the reader recognises – not through the pronoun. Direct second-person is used sparingly and as a deliberate emphasis device (*You, the marketing director – have you thought about this?*), not as a default pronoun.

Headline length: maximum 60 characters.

<!-- scope: write -->
## Default technique

ABT – both as an outer structural arc over the whole page and, more characteristically, as iterative microstructure within sections. A pillar page can carry an outer ABT: a brief A introducing the reader's situation, one or more B-sections describing the problem space, T-sections presenting the solution. But the more distinctive use on the web is *iterative* ABT – each section, each argument, each reasoning block can carry its own mini-ABT: *this is so (A), but we have this problem (B), the solution is this (T)*. Not overdone. Not every paragraph. Present as a tool wherever a point needs to be hooked and landed. See `lib/techniques/abt.md`.

<!-- scope: review -->
## Common pitfalls

Clever headlines or cliffhangers. The scanner sees only the heading. A heading that reads *And then something unexpected happened* does not deliver a content declaration. The section gets skipped.

Headings that do not keep their promise. If the subheading says *Three things to check before procurement* and the paragraph then drifts into something else, the declaration is broken. The scanner notices and loses trust in the rest of the page.

Linear structure that assumes top-to-bottom reading. Bridges like *now let us turn to*, *as we said above*, *in the next section we will* do not work when the reader has landed mid-page. Each section should be readable from a cold start – the goal points that way even if it cannot be absolute.

Visual typography as decoration. Bullet lists where the content is not a list. Callouts because the page *needs a visual break*. Tables for content that is not comparative. Pull quotes that highlight nothing meaningful. Each visual element must earn its place by serving the information; otherwise it breaks scanability instead of supporting it.

Text that describes instead of speaks. When prose slides into abstract reference without points where the reader feels seen, the sense of address disappears. First-person plural or the company name are not the problem – the problem is the absence of moments where the reader can locate herself in the text.

ABT as visible formula. Used repeatedly in identical form, ABT becomes a pattern the reader sees through and dismisses. The tool can be masked: let the reader infer the *but*; assume A is already shared; vary placement; sometimes deliver only T after an implicit B. The risk is not heavy use – it is regularity that makes the structure visible.

## Trigger keywords

Triggers: webbcopy, web copy, webbtext, web text.

The lean trigger principle applies. Both languages with canonical forms. Compounds and variants (*text för webben*, *writing for the web*, *skriva för webben*) are handled by the agent's semantic matching.

Web copy fires on an explicit signal that the text is *for the web*, not on a page-type name. Does not trigger on: landningssida, landing page, pillar page, cornerstone content, tjänstesida, produktsida, service page, product page. These are page-type signals handled by dedicated skills that reference web-copy principles internally. Does not trigger on: webbplats, sajt, hemsida, website, site, homepage – unless the user explicitly asks for *text* or *copy* for them.
