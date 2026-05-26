---
name: redline
description: Three-phase critical editorial review with human-in-the-loop settling — proofread ⊂ redline ⊂ edit, the middle skill. Phase 1 silently applies the conservative proofread pass. Phase 2 produces a finding list per protocols/redline.md against rules/style.md, the applicable content-type and technique files, and the loaded language file. Phase 3 settles each finding with the user one at a time via protocols/dialogue.md (accept / reject / counter / delegate). Optional language argument (`/redline sv`, `/redline en_GB`). Scope from proofreading up to and including line editing; substantive editing surfaces only as a single last-resort finding. Activates only via the explicit `/redline` slash command.
disable-model-invocation: true
---

# /redline

Three-phase critical editorial review with human-in-the-loop settling.

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

## Phase 3 — dialogue settling

Settle each finding via `../../lib/protocols/dialogue.md`. The user accepts, rejects, counters, or delegates. On delegation, hand the remaining open findings to `../../lib/protocols/subagent.md` and deliver the polished text directly.

## Files to read

> The list below is a coverage requirement, not a sequence of unconditional reads. Before each Read, check whether the file's content is already in your conversation context — from any prior turn, phase, or skill invocation in this session. If it is, skip it. The user's input file or URL is always fetched fresh.

Read in this order:

1. `../../lib/protocols/proofread.md` — Phase 1 procedure.
2. `../../lib/rules/writing.md` plus whichever construction-scoped rule files match the input (`quotation.md`, `abbreviations.md`, `headed-text.md`, `lists.md`), and the language mechanics file determined above (specific `lib/languages/<lang>-mechanics.md`, otherwise `lib/languages/default-mechanics.md`) — Phase 1.
3. `../../lib/genres/_index.md` — to identify the content type.
4. The matching `../../lib/genres/<type>.md` and `../../lib/techniques/<technique>.md`.
5. `../../lib/rules/style.md`, the language style file `../../lib/languages/<lang>-style.md` where it exists, and `../../lib/protocols/redline.md` — Phase 2.
6. `../../lib/protocols/dialogue.md` — Phase 3.
7. `../../lib/protocols/input.md` — to determine the input form. Then `../../lib/protocols/output-inline.md` if the input is inline; otherwise `../../lib/protocols/output-files.md`.
8. `../../lib/protocols/subagent.md` — only on delegation.

## Output

The output protocol routes the polished final text after Phase 3 completes.
