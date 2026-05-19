---
name: redline
description: Three-phase critical editorial review — proofread ⊂ redline ⊂ edit, this is the middle skill. Phase 1 silently applies the conservative proofread pass (spelling, grammar, punctuation, and the loaded language file's conventions). Phase 2 performs the critical-review pass per protocols/redline.md against rules/style.md, the applicable content-type and technique files, and the loaded language file. Phase 3 settles each finding with the user one at a time via protocols/dialogue.md — the user accepts, rejects, counters, or delegates. Use whenever the user writes "/redline" — alone or followed by text, a file reference, or a URL. An optional language argument (e.g. `/redline sv`, `/redline en_GB`) can be supplied. Trigger on "redline", "redlining", "line edit", "line editing", "redaktöra", "granska texten". Scope is from proofreading up to and including line editing; substantive or developmental editing is raised only as a single last-resort finding when the text requires it.
---

# /redline

Three-phase critical editorial review with human-in-the-loop settling.

## Language determination

Follow `../../lib/protocols/language.md` in **detect mode** — source the language from the input text.

Phase 1 (proofread) applies only the *Mechanics* section of the loaded file. Phase 2 (redline) applies both *Mechanics* and *Style*. When `default.md` is in use, only *Mechanics* exists — Phase 2 still runs but without language-specific style overlays (the universal style foundation in `rules/style.md` carries the pass).

## Phase 1 — silent proofread

Apply `../../lib/protocols/proofread.md` against `../../lib/rules/writing.md` and the loaded language file. The corrected text flows directly into Phase 2 — it is not delivered as a separate intermediate output.

## Phase 2 — critical review

Apply `../../lib/protocols/redline.md` against `../../lib/rules/style.md`, the loaded language file, the applicable file in `../../lib/genres/`, and the applicable file in `../../lib/techniques/`. The pass produces a finding list.

## Phase 3 — dialogue settling

Settle each finding via `../../lib/protocols/dialogue.md`. The user accepts, rejects, counters, or delegates. On delegation, hand the remaining open findings to `../../lib/protocols/subagent.md` and deliver the polished text directly.

## Files to read

Read in this order:

1. `../../lib/protocols/language.md` — the language determination procedure.
2. `../../lib/protocols/proofread.md`, `../../lib/rules/writing.md`, and the language file determined above (specific `lib/languages/<lang>.md`, otherwise `lib/languages/default.md`) — Phase 1.
3. `bin/list-frontmatter.sh lib/genres/` — to identify the content type.
4. The matching `../../lib/genres/<type>.md` and `../../lib/techniques/<technique>.md`.
5. `../../lib/rules/style.md`, `../../lib/protocols/redline.md`, and `../../lib/protocols/finding-format.md` — Phase 2.
6. `../../lib/protocols/dialogue.md` — Phase 3.
7. `../../lib/protocols/input.md` and `../../lib/protocols/output.md` — as needed.
8. `../../lib/protocols/subagent.md` — only on delegation.

## Output

The output protocol routes the polished final text after Phase 3 completes.
