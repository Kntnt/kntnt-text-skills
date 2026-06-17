---
name: write
description: Four-phase content creation from a brief – brief acquisition, idea presentation, draft, automatic polish. Requires a language argument. Activate when the user explicitly invokes this plugin's write skill – `/write`, `/kntnt-text-skills:write`, `kntnt text skills write`, `text-write-skill`, "write X with Kntnt's skill", "Kntnt's text write skill" or similar plugin-anchored phrasing. Do not activate on bare requests to "write" or "draft" something.
---

# /write

Walks you through writing a piece from a brief: first you agree on the brief itself (audience, purpose, angle, hook, channel, length, content type), then it proposes an idea, then drafts, then polishes the draft. Requires a language argument first (`sv`, `en_GB`, `en_US`); the brief follows. Optionally takes `--max-iterations=N` (0–3) to set how many adversarial review rounds run during the polish step; default 1 runs one round, `0` opts out, `2`/`3` raise the ceiling.

## Language determination

Resolve the language via `${CLAUDE_PLUGIN_ROOT}/lib/protocols/language-resolution.md` in *propose mode* – propose a target language based on the prompt's language (Swedish prompt → Swedish text) and any source material, and confirm with the user. Honour the chosen language for the rest of the run.

Phase 3 (draft) and Phase 4 (redline + subagent) use both the *Mechanics* and *Style* sections of the loaded language file. When the file has no *Style* section (or when only `default-mechanics.md` is loaded), drafting proceeds with the universal style foundation in `rules/style.md` carrying the style layer.

## Phase 1 – brief acquisition

Propose values for the nine briefing fields based on the prompt and any available source material:

1. **Working title**
2. **Target audience**
3. **Sender purpose** – what the sender gains from the audience reading the text (drives the CTA).
4. **Reader takeaway** – what the reader gains from reading.
5. **Angle** – perspective, point of entry, main point.
6. **Hook** – the B in ABT.
7. **Channel** – web, press release, e-book chapter, case study, newsletter, etc.
8. **Length** – approximate word count.
9. **Content type** – one of the installed types in `${CLAUDE_PLUGIN_ROOT}/lib/genres/` plus the default technique from that type's frontmatter (or the user's named override).

For each field, present the proposed value and let the user accept, modify or discuss. No field is silently filled. Acceptance can be expressed as a blanket *accept all* – that is itself a position-taking and is honoured.

After Phase 1, every field has an agreed value.

## Phase 2 – idea presentation

With all nine fields confirmed, present a short idea: structure, tone, ABT or PAC plan, address, approximate length.

**Default behaviour.** Wait for the user's acceptance or modification before Phase 3.

**Bypass behaviour.** If the user has pre-authorised in the initial prompt or earlier in the conversation that the agent should proceed without waiting after the idea is presented (*kör på*, *skriv direkt utan att fråga*, *just produce the draft*, *no need to wait for approval*), present the idea, assume acceptance and continue to Phase 3 immediately. The idea is always presented; only the wait is skipped under bypass.

No subagent is invoked in Phase 2.

## Phase 3 – draft

Write the draft per the applicable content-type file, technique file and language file(s).

## Phase 4 – automatic redline review

Apply the same review machinery as `/edit` to the draft.

### Rule application for Phase 4

Apply the universal punctuation rules in `${CLAUDE_PLUGIN_ROOT}/lib/rules/writing.md` always. Apply the matching sections of `${CLAUDE_PLUGIN_ROOT}/lib/rules/constructions.md` (quotation, abbreviation, headed-text, lists) only when the draft contains those constructions. Section-level filtering is cognitive – the file is loaded in full as part of Batch 2 below and the relevant sections are read against the draft once it exists.

Then apply `${CLAUDE_PLUGIN_ROOT}/lib/protocols/proofread.md` (silent Phase 4a) against those rule files and the *Mechanics* section of the loaded language file, followed by `${CLAUDE_PLUGIN_ROOT}/lib/protocols/redline.md` (Phase 4b) against `${CLAUDE_PLUGIN_ROOT}/lib/rules/style.md`, the *Style* section of the language file, the chosen genre file and the chosen technique file – producing a finding list.

### Settling

**Default behaviour.** Run one adversarial review round through the subagent loop in `${CLAUDE_PLUGIN_ROOT}/lib/protocols/subagent.md`. The default exists because the main agent applying its own redline findings to its own draft, in the same context, is too weak a check for register – it converges on cosmetic edits and calls translated-reading prose publication-ready. One round of an adversarial register reviewer is the floor that catches the AI-tell and translated-reading faults a same-context pass misses.

**Iteration ceiling.** The `--max-iterations=N` flag sets how many rounds the loop may run:

- `--max-iterations=1` (default): one adversarial round. The subagent's convergence rules in `subagent.md` apply – the round runs, then the main agent applies what the dialogue settled and delivers.
- `--max-iterations=2` / `=3`: raise the ceiling. The loop stops early once main agent and subagent agree, but may not stop before the adversarial register pass has run at least once.
- `--max-iterations=0`: opt out – the main agent applies the finding list directly to the drafted text without a subagent round. This is the explicit escape hatch, not the default.
- `N > 3` is clamped to 3 (the protocol maximum).

**Natural-language parity.** For the phrases that map to `N`, see *Natural-language parity* in `${CLAUDE_PLUGIN_ROOT}/lib/protocols/subagent.md` (loaded as part of Batch 2). The flag wins on conflict; ask if the prompt is ambiguous.

**Last-resort floor.** When the redline pass produces the last-resort finding from `protocols/redline.md`, the subagent floor is raised to 1 even if the flag is 0 – one round to sanity-check the observation before it reaches the user as a closing note.

The main agent has final decision authority. No user-facing summary of any internal dialogue is produced. There is no post-draft user-facing dialogue beyond the optional last-resort closing note.

## Technique override

The user can override the default technique in the `/write` prompt – *use ABT*, *force PAC*, *without ABT*, *no technique*. The override applies via Phase 1's *Content type* field – propose the override rather than the content type's default.

If the user names a technique that has no corresponding file in `${CLAUDE_PLUGIN_ROOT}/lib/techniques/` (e.g., *PAS* when only `abt.md` and `pac.md` are present), refuse and report:

> Technique 'X' is not installed in the plugin. Available techniques: ABT, PAC. Add `lib/techniques/x.md` first, or choose an installed technique or proceed without a technique.

Techniques are not applied from training data; they must be present as installed files.

## Content-type detection

At the start of Phase 1, read `${CLAUDE_PLUGIN_ROOT}/lib/genres/_index.md` to retrieve all type metadata in one read. Match the user's prompt against the triggers semantically – canonical forms plus idiosyncratic terms are sufficient; infer compounds and conjugations. The best match becomes the proposal for the *Content type* field in Phase 1.

When the prompt or metadata triggers a disambiguation rule (blogginlägg → article-or-column; e-book chapter → ask per chapter), present the disambiguation question. Negative triggers (`not_triggers`) prevent false positives. If no genre matches clearly via triggers or semantic likeness, propose the genre whose frontmatter has `default: true` – do not read multiple genre files in full to compare.

Once the type is confirmed, read the content-type file. Skip sections preceded by `<!-- scope: review -->`; read only unmarked sections and sections preceded by `<!-- scope: write -->`. Review-scoped sections describe checks (common pitfalls, repetition rules) for a post-hoc critical review of an existing text – they add no value when the drafting itself is following the genre's write-scoped rules. Other content-type files are not read during this invocation.

## Files to read

> The list below is a coverage requirement, not a sequence of unconditional reads. Before each Read, check whether the file's content is already in your conversation context – from any prior turn, phase or skill invocation in this session. If it is, skip it. The user's input file or URL is always fetched fresh.

> Reads that are not skipped above fire in batches. Each batch below groups files with no mutual dependency; issue all of them as a single parallel tool call, then advance to the next batch when the previous returns.

**Batch 0.** Before Phase 1 begins:

- `${CLAUDE_PLUGIN_ROOT}/lib/genres/_index.md` – for Phase 1 content-type detection.

**Batch 1.** After Phase 1 confirms the content type and technique:

- The matching `${CLAUDE_PLUGIN_ROOT}/lib/genres/<type>.md`.
- The matching `${CLAUDE_PLUGIN_ROOT}/lib/techniques/<technique>.md`.

**Batch 2.** After Phase 2 confirmation, issue all remaining reads in parallel:

- `${CLAUDE_PLUGIN_ROOT}/lib/protocols/io.md` – input detection and output routing.
- `${CLAUDE_PLUGIN_ROOT}/lib/protocols/language-resolution.md` – language candidate, file inventory, overlay loader, fallback reporting.
- `${CLAUDE_PLUGIN_ROOT}/lib/protocols/proofread.md` – for Phase 4a.
- `${CLAUDE_PLUGIN_ROOT}/lib/protocols/redline.md` – for Phase 4b.
- `${CLAUDE_PLUGIN_ROOT}/lib/protocols/subagent.md` – for Phase 4 settling.
- `${CLAUDE_PLUGIN_ROOT}/lib/rules/constructions.md` – construction-scoped rules; the relevant sections are applied cognitively in Phase 4 against the draft.
- `${CLAUDE_PLUGIN_ROOT}/lib/rules/style.md` – substantive style guidance for drafting and Phase 4 review.
- `${CLAUDE_PLUGIN_ROOT}/lib/rules/writing.md` – universal punctuation rules.
- The language file determined above: `${CLAUDE_PLUGIN_ROOT}/lib/languages/<lang>.md` (otherwise `${CLAUDE_PLUGIN_ROOT}/lib/languages/default-mechanics.md`).

## Special handling

**Blog post.** *Blogginlägg* / *blog post* / *skriv för bloggen* / *write for the blog* is not a content type. When such a phrase appears, ask whether the post should be written as article or column. Never opinion piece, never report.

**E-book.** E-books are not a content type. Each chapter is written as one of the existing content types (article, case study or report most commonly). When `/write` is invoked for an e-book, ask per chapter which content type applies.

**Out of scope.** Ad copy, Google Ads copy, *annonscopy*. Bare social-media copy without a linked-text teaser purpose. If the user requests one of these, report that the plugin does not cover it.
