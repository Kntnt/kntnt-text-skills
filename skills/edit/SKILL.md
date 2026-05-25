---
name: edit
description: AFK (away-from-keyboard) variant of /redline — proofread ⊂ redline ⊂ edit, the deepest skill. Same Phase 1 (silent proofread) and Phase 2 (critical review per protocols/redline.md) as /redline; Phase 3 settles findings via an internal subagent per protocols/subagent.md instead of user dialogue. Optional language argument (`/edit sv`, `/edit en_GB`). Scope from proofreading up to and including line editing; substantive editing surfaces only as a single last-resort note. Activates only via the explicit `/edit` slash command.
disable-model-invocation: true
---

# /edit

Three-phase critical editorial review settled by an internal subagent.

## Language determination

Follow `../../lib/protocols/language.md` in **detect mode** — source the language from the input text.

Phase 1 (proofread) applies only the *Mechanics* section of the loaded file. Phase 2 (redline) applies both *Mechanics* and *Style*. When `default.md` is in use, only *Mechanics* exists — Phase 2 still runs but without language-specific style overlays (the universal style foundation in `rules/style.md` carries the pass).

## Phase 1 — silent proofread

Apply `../../lib/protocols/proofread.md` against `../../lib/rules/writing.md` and the loaded language file. The corrected text flows directly into Phase 2 — it is not delivered as a separate intermediate output.

## Phase 2 — critical review

Apply `../../lib/protocols/redline.md` against `../../lib/rules/style.md`, the loaded language file, the applicable file in `../../lib/genres/`, and the applicable file in `../../lib/techniques/`. The pass produces a finding list.

If no genre matches clearly via triggers or semantic likeness, use the genre whose frontmatter has `default: true`. Do not read multiple genre files in full to compare — the frontmatter inventory plus the fallback flag is sufficient to decide.

When reading the chosen genre file, skip sections preceded by `<!-- scope: write -->`; read only unmarked sections and sections preceded by `<!-- scope: review -->`. Write-scoped sections describe drafting concerns (structure, length, headings, address) that add no value to a review pass.

## Phase 3 — subagent settling

Settle the finding list via `../../lib/protocols/subagent.md` — main agent and subagent iterate as colleagues for up to three rounds, early consensus preferred. The polished text is delivered via the output protocol matching the input form (see *Files to read*). No user-facing summary of the internal dialogue is produced.

The single exception is the last-resort finding from `protocols/redline.md` — when the text is so far from publication that line editing cannot fix it, or when it is structured as one content type but the material wants another. That single decision is escalated to the user as a closing note.

## Files to read

Read in this order:

1. `../../lib/protocols/language.md` — the language determination procedure.
2. `../../lib/protocols/proofread.md`, `../../lib/rules/writing.md`, and the language file determined above (specific `lib/languages/<lang>.md`, otherwise `lib/languages/default.md`) — Phase 1.
3. `bin/list-frontmatter.sh lib/genres/` — to identify the content type.
4. The matching `../../lib/genres/<type>.md` and `../../lib/techniques/<technique>.md`.
5. `../../lib/rules/style.md` and `../../lib/protocols/redline.md` — Phase 2.
6. `../../lib/protocols/subagent.md` — Phase 3.
7. `../../lib/protocols/input.md` — to determine the input form. Then `../../lib/protocols/output-inline.md` if the input is inline; otherwise `../../lib/protocols/output-files.md`.

## Output

The output protocol routes the polished final text after Phase 3 completes.
