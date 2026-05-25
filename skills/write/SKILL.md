---
name: write
description: Four-phase content creation. Phase 1 acquires a brief over nine fields the user accepts, modifies, or discusses. Phase 2 presents the idea (structure, tone, ABT/PAC plan, address, length). Phase 3 writes the draft against the applicable content-type, technique, and language files. Phase 4 polishes via the redline pass with subagent settling — only the polished final text is delivered. Optional language argument (`/write sv`, `/write en_GB`); without it the skill proposes a target language and asks the user to confirm. Blog posts disambiguate to article or column. Activates only via the explicit `/write` slash command.
disable-model-invocation: true
---

# /write

Four-phase content creation.

## Language determination

Propose a target language and confirm with the user (propose mode). The resolution procedure:

1. **Argument.** If the user passed a language argument (e.g. `sv`, `sv_SE`, `en`, `en_GB`, `en_US`), use it as the candidate. A bare argument (`sv`, `en`) that matches no file directly but matches several territorial variants goes to the disambiguation question below.
2. **Propose.** Without an argument, propose a target language based on the prompt's language (Swedish prompt → Swedish text) and any source material, and ask the user to confirm.
3. **Inventory.** Look for `<lang>-mechanics.md` and `<lang>-style.md` in `../../lib/languages/` for the candidate:
   - One language match: load both layers if both exist; if only the mechanics file exists, drafting proceeds without a language-specific style overlay.
   - Several language matches: ask the user which to use.
   - No match: fall back to `../../lib/languages/default-mechanics.md` and mention this in the reply (in English):
     > No language file found for [language]. Baseline conventions from `default-mechanics.md` apply. Add `lib/languages/<code>-mechanics.md` and `lib/languages/<code>-style.md` for stricter control.

Honour the chosen language for the rest of the run.

Phase 3 (draft) and Phase 4 (redline + subagent) use both layers (`<lang>-mechanics.md` and `<lang>-style.md`). When only `default-mechanics.md` is available, drafting proceeds with the universal style foundation in `rules/style.md` carrying the style layer.

## Phase 1 — brief acquisition

Propose values for the nine briefing fields based on the prompt and any available source material:

1. **Working title**
2. **Target audience**
3. **Sender purpose** — what the sender gains from the audience reading the text (drives the CTA).
4. **Reader takeaway** — what the reader gains from reading.
5. **Angle** — perspective, point of entry, main point.
6. **Hook** — the B in ABT.
7. **Channel** — web, press release, e-book chapter, case study, newsletter, etc.
8. **Length** — approximate word count.
9. **Content type** — one of the installed types in `../../lib/genres/` plus the default technique from that type's frontmatter (or the user's named override).

For each field, present the proposed value and let the user accept, modify, or discuss. No field is silently filled. Acceptance can be expressed as a blanket *accept all* — that is itself a position-taking and is honoured.

After Phase 1, every field has an agreed value.

## Phase 2 — idea presentation

With all nine fields confirmed, present a short idea: structure, tone, ABT or PAC plan, address, approximate length.

**Default behaviour.** Wait for the user's acceptance or modification before Phase 3.

**Bypass behaviour.** If the user has pre-authorised in the initial prompt or earlier in the conversation that the agent should proceed without waiting after the idea is presented (*kör på*, *skriv direkt utan att fråga*, *just produce the draft*, *no need to wait for approval*), present the idea, assume acceptance, and continue to Phase 3 immediately. The idea is always presented; only the wait is skipped under bypass.

No subagent is invoked in Phase 2.

## Phase 3 — draft

Write the draft per the applicable content-type file, technique file, and language file(s).

## Phase 4 — automatic redline review with subagent settling

Apply the same review machinery as `/edit` to the draft.

### Conditional rule loading for Phase 4

Inspect the drafted text before loading the construction-scoped rule files. Load only the rule files that match constructions actually present in the draft:

- Always: `../../lib/rules/writing.md` — the universal punctuation rules (comma, dash, parenthesis).
- If the draft contains quotation marks, dialogue, or block quotations: `../../lib/rules/quotation.md`.
- If the draft contains initialisms or acronyms: `../../lib/rules/abbreviations.md`.
- If the draft contains H1, headings, subheadings, or a standfirst structure: `../../lib/rules/headed-text.md`.
- If the draft contains bulleted, numbered, or definition lists: `../../lib/rules/lists.md`.

Then apply `../../lib/protocols/proofread.md` (silent Phase 4a) against those rule files and the language mechanics file, followed by `../../lib/protocols/redline.md` (Phase 4b) against `../../lib/rules/style.md`, the language style file, the chosen genre file, and the chosen technique file — producing a finding list. Settle the findings via `../../lib/protocols/subagent.md` — main agent and subagent iterate as colleagues for up to three rounds, early consensus preferred. The main agent has final decision authority. The polished text is delivered to the user via the output protocol matching the input form (see *Files to read*). No user-facing summary of the internal dialogue is produced.

There is no post-draft user-facing dialogue.

## Technique override

The user can override the default technique in the `/write` prompt — *use ABT*, *force PAC*, *without ABT*, *no technique*. The override applies via Phase 1's *Content type* field — propose the override rather than the content type's default.

If the user names a technique that has no corresponding file in `../../lib/techniques/` (e.g., *PAS* when only `abt.md` and `pac.md` are present), refuse and report:

> Technique 'X' is not installed in the plugin. Available techniques: ABT, PAC. Add `lib/techniques/x.md` first, or choose an installed technique, or proceed without a technique.

Techniques are not applied from training data; they must be present as installed files.

## Content-type detection

At the start of Phase 1, read `../../lib/genres/_index.md` to retrieve all type metadata in one read. Match the user's prompt against the triggers semantically — canonical forms plus idiosyncratic terms are sufficient; infer compounds and conjugations. The best match becomes the proposal for the *Content type* field in Phase 1.

When the prompt or metadata triggers a disambiguation rule (blogginlägg → article-or-column; e-book chapter → ask per chapter), present the disambiguation question. Negative triggers (`not_triggers`) prevent false positives. If no genre matches clearly via triggers or semantic likeness, propose the genre whose frontmatter has `default: true` — do not read multiple genre files in full to compare.

Once the type is confirmed, read the content-type file. Skip sections preceded by `<!-- scope: review -->`; read only unmarked sections and sections preceded by `<!-- scope: write -->`. Review-scoped sections describe checks (common pitfalls, repetition rules) for a post-hoc critical review of an existing text — they add no value when the drafting itself is following the genre's write-scoped rules. Other content-type files are not read during this invocation.

## Files to read

Read in this order when the user invokes `/write`:

1. `../../lib/genres/_index.md` — for content-type detection.
2. The matching `../../lib/genres/<type>.md` — once the type is confirmed in Phase 1.
3. `../../lib/techniques/<technique>.md` — once the technique is confirmed.
4. `../../lib/rules/style.md`, `../../lib/rules/writing.md`, and the language files determined above (specific `lib/languages/<lang>-mechanics.md` plus `lib/languages/<lang>-style.md` where it exists, otherwise `lib/languages/default-mechanics.md`) — for the draft.
5. `../../lib/protocols/input.md` — to determine the input form when source material is provided.
6. `../../lib/protocols/proofread.md` and `../../lib/protocols/redline.md` — for Phase 4 review of the draft. Load the construction-scoped rule files (`quotation.md`, `abbreviations.md`, `headed-text.md`, `lists.md`) only for the constructions present in the draft per *Conditional rule loading for Phase 4* above.
7. `../../lib/protocols/subagent.md` — for Phase 4 settling.
8. `../../lib/protocols/output-inline.md` if the input is inline; otherwise `../../lib/protocols/output-files.md` — to deliver the result.

## Special handling

**Blog post.** *Blogginlägg* / *blog post* / *skriv för bloggen* / *write for the blog* is not a content type. When such a phrase appears, ask whether the post should be written as article or column. Never opinion piece, never report.

**E-book.** E-books are not a content type. Each chapter is written as one of the existing content types (article, case study, or report most commonly). When `/write` is invoked for an e-book, ask per chapter which content type applies.

**Out of scope.** Ad copy, Google Ads copy, *annonscopy*. Bare social-media copy without a linked-text teaser purpose. If the user requests one of these, report that the plugin does not cover it.
