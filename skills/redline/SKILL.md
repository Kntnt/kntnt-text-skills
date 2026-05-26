---
name: redline
description: Three-phase critical editorial review with human-in-the-loop settling — proofread ⊂ redline ⊂ edit, the middle skill. Phase 1 silently applies the conservative proofread pass. Phase 2 produces a finding list per protocols/redline.md against rules/style.md, the applicable content-type and technique files, and the loaded language file. Phase 3 settles each finding with the user one at a time via protocols/dialogue.md (accept / reject / counter / delegate); on delegation, the `--max-iterations=N` flag (0–3, default 0) controls whether the remaining tail is applied directly by the main agent or routed through the subagent loop. Optional language argument (`/redline sv`, `/redline en_GB`). Scope from proofreading up to and including line editing; substantive editing surfaces only as a single last-resort finding. Activates only via the explicit `/redline` slash command.
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

Settle each finding via `../../lib/protocols/dialogue.md`. The user accepts, rejects, counters, or delegates.

**Delegation behaviour depends on the `--max-iterations=N` flag** (or its natural-language equivalent in the prompt):

- `--max-iterations=0` (default): on delegation, the main agent applies the remaining open findings directly and delivers the polished text. No subagent is invoked.
- `--max-iterations=1` / `=2` / `=3`: on delegation, the remaining open findings are handed to `../../lib/protocols/subagent.md` with that ceiling on iterations. The subagent's convergence rules still apply — early consensus stops the loop. `N > 3` is clamped to 3.

**Natural-language parity.** The model parses these expressions in the prompt to the same value as the flag (flag wins on conflict; ask if ambiguous):

- *iterera max tre gånger* / *iterate up to three times* / *kör djupt* / *deep review* → 3
- *max två rundor* / *two rounds max* → 2
- *en runda räcker* / *one round* → 1
- *hoppa över subagent* / *skip subagent* → 0

**Last-resort floor.** When the redline pass surfaces the last-resort developmental finding, the subagent floor is raised to 1 even if the flag is 0 — one round to sanity-check the observation before it reaches the user as a closing note.

## Files to read

> The list below is a coverage requirement, not a sequence of unconditional reads. Before each Read, check whether the file's content is already in your conversation context — from any prior turn, phase, or skill invocation in this session. If it is, skip it. The user's input file or URL is always fetched fresh.

> Reads that are not skipped above fire in batches. Each batch below groups files with no mutual dependency; issue all of them as a single parallel tool call, then advance to the next batch when the previous returns.

**Batch 1.** Issue these reads in parallel:

- `../../lib/protocols/proofread.md` — Phase 1 procedure.
- `../../lib/protocols/redline.md` — Phase 2 procedure.
- `../../lib/protocols/dialogue.md` — Phase 3 settling protocol.
- `../../lib/rules/writing.md` — universal punctuation rules.
- Whichever construction-scoped rule files match the input (`quotation.md`, `abbreviations.md`, `headed-text.md`, `lists.md`) per *Conditional rule loading* above.
- `../../lib/languages/<lang>-mechanics.md` and `../../lib/languages/<lang>-style.md` where it exists (otherwise `../../lib/languages/default-mechanics.md`).
- `../../lib/genres/_index.md` — to identify the content type.
- `../../lib/rules/style.md` — Phase 2 universal style foundation.
- `../../lib/protocols/input.md` — to determine the input form.
- Both `../../lib/protocols/output-inline.md` and `../../lib/protocols/output-files.md` — loaded speculatively so the matching one is ready once the input form is known.
- `../../lib/protocols/subagent.md` — loaded speculatively (only used on delegation in Phase 3).

**Batch 2.** After the genre and technique are identified from Batch 1's `_index.md`:

- The matching `../../lib/genres/<type>.md`.
- The matching `../../lib/techniques/<technique>.md`.

## Output

The output protocol routes the polished final text after Phase 3 completes.
