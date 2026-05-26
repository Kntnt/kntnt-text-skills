---
name: write
description: Four-phase content creation. Phase 1 acquires a brief over nine fields the user accepts, modifies, or discusses. Phase 2 presents the idea (structure, tone, ABT/PAC plan, address, length). Phase 3 writes the draft against the applicable content-type, technique, and language files. Phase 4 polishes via the redline pass and by default applies the findings directly; the subagent loop in protocols/subagent.md is opt-in via `--max-iterations=N` (0–3, default 0), and a last-resort developmental finding raises the floor to 1. Only the polished final text is delivered. Optional language argument (`/write sv`, `/write en_GB`); without it the skill proposes a target language and asks the user to confirm. Blog posts disambiguate to article or column. Activates only via the explicit `/write` slash command.
disable-model-invocation: true
---

# /write

Four-phase content creation.

## Language determination

Propose a target language and confirm with the user (propose mode). The resolution procedure:

1. **Argument.** If the user passed a language argument (e.g. `sv`, `sv_SE`, `en`, `en_GB`, `en_US`), use it as the candidate. A bare argument (`sv`, `en`) that matches no file directly but matches several territorial variants goes to the disambiguation question below.
2. **Propose.** Without an argument, propose a target language based on the prompt's language (Swedish prompt → Swedish text) and any source material, and ask the user to confirm.
3. **Inventory.** Look for `<lang>.md` in `../../lib/languages/` for the candidate:
   - One language match: load the file; both layers live in named sections. If the file contains no *Style* section, drafting proceeds without a language-specific style overlay.
   - Several language matches: ask the user which to use.
   - No match: fall back to `../../lib/languages/default-mechanics.md` and mention this in the reply (in English):
     > No language file found for [language]. Baseline conventions from `default-mechanics.md` apply. Add `lib/languages/<code>.md` for stricter control.

Honour the chosen language for the rest of the run.

Phase 3 (draft) and Phase 4 (redline + subagent) use both the *Mechanics* and *Style* sections of the loaded language file. When only `default-mechanics.md` is available, drafting proceeds with the universal style foundation in `rules/style.md` carrying the style layer.

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

## Phase 4 — automatic redline review

Apply the same review machinery as `/edit` to the draft.

### Rule application for Phase 4

Apply the universal punctuation rules in `../../lib/rules/writing.md` always. Apply the matching sections of `../../lib/rules/constructions.md` (quotation, abbreviation, headed-text, lists) only when the draft contains those constructions. Section-level filtering is cognitive — the file is loaded in full as part of Batch 2 below and the relevant sections are read against the draft once it exists.

Then apply `../../lib/protocols/proofread.md` (silent Phase 4a) against those rule files and the *Mechanics* section of the loaded language file, followed by `../../lib/protocols/redline.md` (Phase 4b) against `../../lib/rules/style.md`, the *Style* section of the language file, the chosen genre file, and the chosen technique file — producing a finding list.

### Settling

**Default behaviour.** The main agent applies the finding list directly to the drafted text and delivers the polished result via the output protocol matching the input form (see *Files to read*). No subagent is invoked.

**Subagent opt-in.** The subagent loop in `../../lib/protocols/subagent.md` runs only when explicitly requested. The ceiling on iterations comes from the `--max-iterations=N` flag in the invocation:

- `--max-iterations=0` (default): no subagent — main agent applies directly as above.
- `--max-iterations=1` / `=2` / `=3`: invoke the subagent with that ceiling. The subagent's convergence rules in `subagent.md` still apply — if main agent and subagent agree after an earlier round, the loop stops there.
- `N > 3` is clamped to 3 (the protocol maximum).

**Natural-language parity.** The model parses these expressions in the prompt to the same value as the flag (flag wins on conflict; ask if ambiguous):

- *iterera max tre gånger* / *iterate up to three times* / *kör djupt* / *deep review* → 3
- *max två rundor* / *two rounds max* → 2
- *en runda räcker* / *one round* → 1
- *hoppa över subagent* / *skip subagent* → 0

**Last-resort floor.** When the redline pass produces the last-resort finding from `protocols/redline.md`, the subagent floor is raised to 1 even if the flag is 0 — one round to sanity-check the observation before it reaches the user as a closing note.

The main agent has final decision authority. No user-facing summary of any internal dialogue is produced. There is no post-draft user-facing dialogue beyond the optional last-resort closing note.

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

> The list below is a coverage requirement, not a sequence of unconditional reads. Before each Read, check whether the file's content is already in your conversation context — from any prior turn, phase, or skill invocation in this session. If it is, skip it. The user's input file or URL is always fetched fresh.

> Reads that are not skipped above fire in batches. Each batch below groups files with no mutual dependency; issue all of them as a single parallel tool call, then advance to the next batch when the previous returns.

**Batch 0.** Before Phase 1 begins:

- `../../lib/genres/_index.md` — for Phase 1 content-type detection.

**Batch 1.** After Phase 1 confirms the content type and technique:

- The matching `../../lib/genres/<type>.md`.
- The matching `../../lib/techniques/<technique>.md`.

**Batch 2.** After Phase 2 confirmation, issue all remaining reads in parallel:

- `../../lib/rules/style.md` — substantive style guidance for drafting and Phase 4 review.
- `../../lib/rules/writing.md` — universal punctuation rules.
- `../../lib/rules/constructions.md` — construction-scoped rules; the relevant sections are applied cognitively in Phase 4 against the draft.
- The language file determined above: `../../lib/languages/<lang>.md` (otherwise `../../lib/languages/default-mechanics.md`).
- `../../lib/protocols/proofread.md` — for Phase 4a.
- `../../lib/protocols/redline.md` — for Phase 4b.
- `../../lib/protocols/subagent.md` — for Phase 4 settling.
- `../../lib/protocols/io.md` — input detection and output routing.

## Special handling

**Blog post.** *Blogginlägg* / *blog post* / *skriv för bloggen* / *write for the blog* is not a content type. When such a phrase appears, ask whether the post should be written as article or column. Never opinion piece, never report.

**E-book.** E-books are not a content type. Each chapter is written as one of the existing content types (article, case study, or report most commonly). When `/write` is invoked for an e-book, ask per chapter which content type applies.

**Out of scope.** Ad copy, Google Ads copy, *annonscopy*. Bare social-media copy without a linked-text teaser purpose. If the user requests one of these, report that the plugin does not cover it.
