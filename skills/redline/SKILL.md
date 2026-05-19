---
name: redline
description: Three-phase critical editorial review — proofread ⊂ redline ⊂ edit, this is the middle skill. Phase 1 silently applies the conservative proofread pass (spelling, grammar, punctuation, and the loaded language file's conventions). Phase 2 performs the critical-review pass per protocols/redline.md against rules/style.md, the applicable content-type and technique files, and the loaded language file. Phase 3 settles each finding with the user one at a time via protocols/dialogue.md — the user accepts, rejects, counters, or delegates. Use whenever the user writes "/redline" — alone or followed by text, a file reference, or a URL. An optional language argument (e.g. `/redline sv`, `/redline en_GB`) can be supplied. Trigger on "redline", "redlining", "line edit", "line editing", "redaktöra", "granska texten". Scope is from proofreading up to and including line editing; substantive or developmental editing is raised only as a single last-resort finding when the text requires it.
---

# /redline

Three-phase critical editorial review with human-in-the-loop settling.

## Language determination

If the user passed a language argument (e.g. `sv`, `sv_SE`, `en`, `en_GB`, `en_US`), use it. Otherwise determine language in two steps:

1. **Detect** the language of the input text.
2. **Inventory** the matching files in `../../lib/languages/`:
   - If multiple files exist for the detected language, ask the user which to use.
   - If a single file exists, use it without asking.
   - If no file exists for the detected language, fall back to `../../lib/languages/default.md` and mention this in the reply (in English):
     > No language file found for [language]. Baseline conventions from `default.md` apply. Add `lib/languages/<code>.md` for stricter control.

Phase 1 (proofread) applies only the *Mechanics* section of the loaded file. Phase 2 (redline) applies both *Mechanics* and *Style*. When `default.md` is in use, only *Mechanics* exists — Phase 2 still runs but without language-specific style overlays (the universal style foundation in `rules/style.md` carries the pass).

## Phase 1 — silent proofread

Apply `../../lib/protocols/proofread.md` against `../../lib/rules/writing.md` and the loaded language file. The corrected text flows directly into Phase 2 — it is not delivered as a separate intermediate output.

## Phase 2 — critical review

Apply `../../lib/protocols/redline.md` against `../../lib/rules/style.md`, the loaded language file, the applicable file in `../../lib/genres/`, and the applicable file in `../../lib/techniques/`. The pass produces a finding list.

## Phase 3 — dialogue settling

Settle each finding via `../../lib/protocols/dialogue.md`. The user accepts, rejects, counters, or delegates. On delegation, hand the remaining open findings to `../../lib/protocols/subagent.md` and deliver the polished text directly.

## Files to read

Read in this order:

1. `../../lib/protocols/proofread.md`, `../../lib/rules/writing.md`, and the language file determined above (specific `lib/languages/<lang>.md`, otherwise `lib/languages/default.md`) — Phase 1.
2. `bin/list-frontmatter.sh lib/genres/` — to identify the content type.
3. The matching `../../lib/genres/<type>.md` and `../../lib/techniques/<technique>.md`.
4. `../../lib/rules/style.md`, `../../lib/protocols/redline.md`, and `../../lib/protocols/finding-format.md` — Phase 2.
5. `../../lib/protocols/dialogue.md` — Phase 3.
6. `../../lib/protocols/input.md` and `../../lib/protocols/output.md` — as needed.
7. `../../lib/protocols/subagent.md` — only on delegation.

## Output

The output protocol routes the polished final text after Phase 3 completes.
