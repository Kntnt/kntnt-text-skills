---
name: redline
description: Three-phase critical editorial review — silent proofread, then a finding list, then settle each finding with the user one at a time via accept / reject / counter / delegate. Human-in-the-loop counterpart of `/edit`, which runs the same passes without the dialogue. Optional flags: see SKILL.md body for `--max-iterations`. Activates only via the explicit `/redline` slash command.
disable-model-invocation: true
---

# /redline

Three-phase critical editorial review with human-in-the-loop settling.

## Language determination

Resolve the language via `../../lib/protocols/language-resolution.md` in *detect mode* — the source language is inferred from the input text.

Phase 1 (proofread) applies only the *Mechanics* section of the loaded language file. Phase 2 (redline) applies both the *Mechanics* and *Style* sections. When the file has no *Style* section (or when only `default-mechanics.md` is loaded), Phase 2 still runs but without language-specific style overlays — the universal style foundation in `rules/style.md` carries the pass.

## Rule application

Apply the universal punctuation rules in `../../lib/rules/writing.md` always. Apply the matching sections of `../../lib/rules/constructions.md` (quotation, abbreviation, headed-text, lists) only when the input contains those constructions. Section-level filtering is cognitive — the file is loaded in full and the relevant sections are read against the input.

## Phase 1 — silent proofread

Apply `../../lib/protocols/proofread.md` against the loaded rule files and the *Mechanics* section of the loaded language file. The corrected text flows directly into Phase 2 — it is not delivered as a separate intermediate output.

## Phase 2 — critical review

Apply `../../lib/protocols/redline.md` against `../../lib/rules/style.md`, the *Style* section of the loaded language file (where it exists), the applicable file in `../../lib/genres/`, and the applicable file in `../../lib/techniques/`. The pass produces a finding list.

If no genre matches clearly via triggers or semantic likeness, use the genre whose frontmatter has `default: true`. Do not read multiple genre files in full to compare — the frontmatter inventory plus the fallback flag is sufficient to decide.

When reading the chosen genre file, skip sections preceded by `<!-- scope: write -->`; read only unmarked sections and sections preceded by `<!-- scope: review -->`. Write-scoped sections describe drafting concerns (structure, length, headings, address) that add no value to a review pass.

## Genre fast-path

Before issuing the Files-to-read batches, check two conditions against the input text and the user's prompt:

1. **No structural markers in the input.** No H1 heading, no standfirst, no byline, no attributed-quote pattern.
2. **No genre word in the user's prompt.** None of the trigger terms catalogued in `lib/genres/_index.md` for any non-`general` genre — *artikel*, *article*, *reportage*, *kundcase*, *case*, *case study*, *kundreferens*, *referenscase*, *krönika*, *column*, *kåseri*, *personal essay*, *opinionstext*, *opinion*, *debattartikel*, *debattinlägg*, *åsiktstext*, *op-ed*, *opinion piece*, *debate article*, *pressmeddelande*, *press release*, *press-release*, *rapport*, *report*, *whitepaper*, *white paper*, *vitbok*, *puff*, *teaser*, *standfirst*, *ingress*, *meta description*, *metabeskrivning*, *webbcopy*, *web copy*, *webbtext*, *web text*, *blogginlägg*, *blog post*, or close semantic equivalents.

**When both conditions hold,** commit to the `general` genre immediately. Skip the read of `_index.md` and skip the matched-genre read entirely. Load `lib/genres/general.md` directly in Batch 1; its `default_technique` frontmatter is `none`, so no technique file is loaded in Batch 2. Batch 2 is therefore skipped.

**When either condition is broken,** follow the standard two-batch procedure below: Batch 1 reads `_index.md`, Batch 2 reads the matched `<genre>.md` and `<technique>.md`.

The last-resort floor remains the safety net: if the fast-path commits to `general` for material that actually wants another genre, the redline pass surfaces it as a last-resort developmental finding, which raises the subagent floor to 1.

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

- `../../lib/protocols/dialogue.md` — Phase 3 settling protocol.
- `../../lib/protocols/io.md` — input detection and output routing.
- `../../lib/protocols/language-resolution.md` — language candidate, file inventory, overlay loader, fallback reporting.
- `../../lib/protocols/proofread.md` — Phase 1 procedure.
- `../../lib/protocols/redline.md` — Phase 2 procedure.
- `../../lib/protocols/subagent.md` — loaded speculatively (only used on delegation in Phase 3).
- `../../lib/rules/constructions.md` — construction-scoped rules; apply the sections that match constructions in the input.
- `../../lib/rules/style.md` — Phase 2 universal style foundation.
- `../../lib/rules/writing.md` — universal punctuation rules.
- `../../lib/languages/<lang>.md` (otherwise `../../lib/languages/default-mechanics.md`).
- One of the following based on the *Genre fast-path* check above:
  - **Fast-path (both conditions hold):** `../../lib/genres/general.md` — committed genre. No `_index.md` read.
  - **Standard (either condition broken):** `../../lib/genres/_index.md` — to identify the content type.

**Batch 2.** Skipped under the fast-path. Under the standard path, after the genre and technique are identified from Batch 1's `_index.md`:

- The matching `../../lib/genres/<type>.md`.
- The matching `../../lib/techniques/<technique>.md`.

## Output

The output protocol routes the polished final text after Phase 3 completes.
