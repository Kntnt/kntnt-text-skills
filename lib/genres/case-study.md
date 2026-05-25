---
name: case-study
swedish_term: kundcase
default_technique: abt
triggers:
  - kundcase
  - case
  - "case study"
  - kundreferens
  - referenscase
---

# Case study

## Purpose

A case study is built on the principles of article and reportage — standfirst, lead, ABT, seamless transitions, a closing that invites action — but has its own structural backbone. The text carries the customer, not the sender. The interviewee drives the narrative through attributed direct speech per the *carrying voices* mode in `rules/style.md`. The writer's voice keeps a low profile and provides structure and context.

## Stylistic nuance

<!-- scope: write -->
### Structure

1. **Headline (H1).** Describes what the customer achieves, the solution that is used, or the value the customer gets — not the sender. Maximum 60 characters. Right: *Ystadbostäder chose a digital lock system with physical keys*. Wrong: *SafeTeam delivers lock systems to Ystadbostäder*.
2. **Standfirst (bold).** Who the customer is, what was done, and what the result was. Maximum about sixty words, self-contained, functions as a teaser. Its own mini-ABT applies as in article. Writing rules for the standfirst text live in `teaser.md`.
3. **About the customer (H2).** Who the customer is, size, business, history. Only what the reader needs to understand what is at stake. Normally one to three paragraphs. Quantify when possible and relevant (number of apartments, revenue, geographical spread).
4. **The challenge or the situation (H2).** What triggered the assignment. Quantify when possible (square metres, number of units, timeframe). Describe the situation from the customer's perspective, not the supplier's.
5. **The solution and the implementation (H2, often several).** Here the interviewee carries the narrative through attributed direct speech. Each subheading has a clear function (procurement, implementation, operation, service, support). The writer's voice provides structure and context; the interviewee provides substance, judgement, and experience. Per the *carrying voices* mode, each section other than opening and closing should have a quoted utterance. The half-measure (*Daniel maintains that…* without quoted speech) does not work.
6. **Block quotation.** Lift one — at most two — strong utterances as block quotations. Choose for valuating or characterising content, not to repeat the nearest attributed quote. Place normally after the first or second attributed section.
7. **Recommendation (H2).** Let the interviewee explicitly say that they are satisfied or recommend the solution. Without this point, the text is not a case study but a project description.
8. **Closing (H2, short).** Two to four sentences directed at the reader inviting a concrete next step (e.g., *Get in touch with your nearest office*). Must contain a link to a page that helps the reader move on (contact form, product page, landing page). The link's URL and anchor text come from the brief. When it falls naturally, the recommendation and the closing can be woven together in a shared closing section.

<!-- scope: write -->
### Length

Medium-length case study: about one thousand words; in-depth: about fifteen hundred. Length follows the material's complexity; do not pad to hit a target.

<!-- scope: write -->
### Address

Direct second-person is avoided throughout. The interviewee carries the narrative. The sender is referred to in the third person — never as *we* or *our solution* in the writer's voice. The pronoun system that realises this is set by the loaded language file.

<!-- scope: write -->
### Attributed direct speech

Apply the loaded language file's dialogue conventions for attribution. The principle from `rules/style.md` is the carrying-voices mode; the typographic realisation (quotation marks, speech dash, etc.) is set by the language file. Verbatim quotation is reserved for cases where the exact wording is itself essential — see the Quotation section of `rules/writing.md` and the language file's overrides.

<!-- scope: review -->
### Repetition rule (specific to case-study elements)

H1, standfirst, lead, *About the customer*, and *The challenge* lie dangerously close to each other. The repetition rule from `rules/style.md` applies. Each element must have its own job. H1 names the solution or the value. The standfirst gives the result. The lead opens the narrative (anecdote, question, concrete situation). *About the customer* gives the background. *The challenge* tells what triggered the assignment. If two elements can be struck without the reader missing new information, you have repeated yourself.

<!-- scope: write -->
### In medias res opening

Case studies suit in medias res particularly well when the situation has natural drama (an acute problem, a drill, an event that exposes the value of the solution). The scene then replaces the lead and stands before *About the customer*. See the in medias res mechanic in `lib/techniques/abt.md`.

<!-- scope: write -->
## Default technique

ABT. The interviewee's voice and the case-study structure carry the narrative; the ABT arc runs underneath. See `lib/techniques/abt.md`.

<!-- scope: review -->
## Common pitfalls

Starting with the sender. Always start with the customer. The first sentence the reader encounters in body text — after H1 and standfirst — must be about the customer's situation, not the supplier's offering.

*Our solution*, *our team* in the writer's voice. The customer's voice carries the text. The supplier is referred to in the third person.

*The problem was that they…* framing. Use *the challenge they faced* or the customer's own description. Problem framings imply that the supplier is the rescuer and the customer was helpless — the wrong dynamic for a case study.

Hidden sales text disguised as a case study. The supplier's superiority is shown through the customer's results, not stated. Let the evidence speak.

Half-measure attribution. A couple of attributed quotes as garnish while the rest is *Martin maintains that…* — does not work. If quoted utterances are introduced, make them the text's backbone. See `rules/style.md`.

Closing that pushes sales instead of inviting next steps. The closing names a concrete action the reader can take — visit a contact form, request a quote, see the product page. The pressure is on the action, not on the sale.

Quote that misrepresents the interviewee. Each quoted utterance is reviewed for what it signals about the person. If a quote risks giving the wrong impression, rewrite the bridge so the context is clear, or choose a different part of the interview. See `rules/style.md`.

## Trigger keywords

Triggers: kundcase, case, case study, kundreferens, referenscase.

The lean trigger principle applies. *Kundcase* and *kundreferens* are idiosyncratic Swedish terms listed explicitly because they do not always match semantically from English. Compounds and conjugations are handled by the agent's semantic matching.
