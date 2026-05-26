---
name: edit
description: AFK (away-from-keyboard) variant of /redline — proofread ⊂ redline ⊂ edit, the deepest skill. Same Phase 1 (silent proofread) and Phase 2 (critical review per protocols/redline.md) as /redline; Phase 3 settles findings via an internal subagent per protocols/subagent.md instead of user dialogue. Optional language argument (`/edit sv`, `/edit en_GB`). Scope from proofreading up to and including line editing; substantive editing surfaces only as a single last-resort note. Activates only via the explicit `/edit` slash command.
disable-model-invocation: true
---

# /edit

Three-phase critical editorial review settled by an internal subagent.

## Language determination

Source the language from the input text (detect mode). The resolution procedure:

1. **Argument.** If the user passed a language argument (e.g. `sv`, `sv_SE`, `en`, `en_GB`, `en_US`), use it as the candidate. A bare argument (`sv`, `en`) that matches no file directly but matches several territorial variants goes to the disambiguation question below.
2. **Detect.** Without an argument, infer the language from the input text.
3. **Inventory.** Look for `<lang>-mechanics.md` (and, where the pass needs it, `<lang>-style.md`) in `../../lib/languages/` for the candidate:
   - One match: use it. If only the mechanics file exists for the language, Phase 2 proceeds without a language-specific style overlay.
   - Several matches: ask the user which to use.
   - No match: fall back to `../../lib/languages/default-mechanics.md` and mention this in the reply (in English):
     > No language file found for [language]. Baseline conventions from `default-mechanics.md` apply. Add `lib/languages/<code>-mechanics.md` and `lib/languages/<code>-style.md` for stricter control.

Phase 1 (proofread) applies only the mechanics file. Phase 2 (redline) applies both mechanics and style. When only `default-mechanics.md` is available, Phase 2 still runs but without language-specific style overlays — the universal style foundation in `rules/style.md` carries the pass.

## Conditional rule loading

Inspect the input before loading rule files. Load only the construction-scoped rule files that match constructions actually present in the input:

- Always: `../../lib/rules/writing.md` — the universal punctuation rules (comma, dash, parenthesis).
- If the input contains quotation marks, dialogue, or block quotations: `../../lib/rules/quotation.md`.
- If the input contains initialisms or acronyms: `../../lib/rules/abbreviations.md`.
- If the input contains H1, headings, subheadings, or a standfirst structure: `../../lib/rules/headed-text.md`.
- If the input contains bulleted, numbered, or definition lists: `../../lib/rules/lists.md`.

## Phase 1 — silent proofread

Apply `../../lib/protocols/proofread.md` against the loaded rule files (per *Conditional rule loading* above) and the loaded language mechanics file. The corrected text flows directly into Phase 2 — it is not delivered as a separate intermediate output.

## Phase 2 — critical review

Apply `../../lib/protocols/redline.md` against `../../lib/rules/style.md`, the loaded language style file (where it exists), the applicable file in `../../lib/genres/`, and the applicable file in `../../lib/techniques/`. The pass produces a finding list.

If no genre matches clearly via triggers or semantic likeness, use the genre whose frontmatter has `default: true`. Do not read multiple genre files in full to compare — the frontmatter inventory plus the fallback flag is sufficient to decide.

When reading the chosen genre file, skip sections preceded by `<!-- scope: write -->`; read only unmarked sections and sections preceded by `<!-- scope: review -->`. Write-scoped sections describe drafting concerns (structure, length, headings, address) that add no value to a review pass.

## Phase 3 — subagent settling

Settle the finding list via `../../lib/protocols/subagent.md` — main agent and subagent iterate as colleagues for up to three rounds, early consensus preferred. The polished text is delivered via the output protocol matching the input form (see *Files to read*). No user-facing summary of the internal dialogue is produced.

The single exception is the last-resort finding from `protocols/redline.md` — when the text is so far from publication that line editing cannot fix it, or when it is structured as one content type but the material wants another. That single decision is escalated to the user as a closing note.

## Files to read

> The list below is a coverage requirement, not a sequence of unconditional reads. Before each Read, check whether the file's content is already in your conversation context — from any prior turn, phase, or skill invocation in this session. If it is, skip it. The user's input file or URL is always fetched fresh.

> Reads that are not skipped above fire in batches. Each batch below groups files with no mutual dependency; issue all of them as a single parallel tool call, then advance to the next batch when the previous returns.

**Batch 1.** Issue these reads in parallel:

- `../../lib/protocols/proofread.md` — Phase 1 procedure.
- `../../lib/protocols/redline.md` — Phase 2 procedure.
- `../../lib/protocols/subagent.md` — Phase 3 settling protocol.
- `../../lib/rules/writing.md` — universal punctuation rules.
- Whichever construction-scoped rule files match the input (`quotation.md`, `abbreviations.md`, `headed-text.md`, `lists.md`) per *Conditional rule loading* above.
- `../../lib/languages/<lang>-mechanics.md` and `../../lib/languages/<lang>-style.md` where it exists (otherwise `../../lib/languages/default-mechanics.md`).
- `../../lib/genres/_index.md` — to identify the content type.
- `../../lib/rules/style.md` — Phase 2 universal style foundation.
- `../../lib/protocols/input.md` — to determine the input form.
- Both `../../lib/protocols/output-inline.md` and `../../lib/protocols/output-files.md` — loaded speculatively so the matching one is ready once the input form is known.

**Batch 2.** After the genre and technique are identified from Batch 1's `_index.md`:

- The matching `../../lib/genres/<type>.md`.
- The matching `../../lib/techniques/<technique>.md`.

## Output

The output protocol routes the polished final text after Phase 3 completes.
