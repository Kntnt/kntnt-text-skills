---
name: edit
description: Three-phase critical editorial review that settles the finding list directly without user dialogue, delivering the polished text. AFK (away-from-keyboard) variant of `/redline`, which settles each finding with the user one at a time. Optional flags: see SKILL.md body for `--max-iterations`. Activates only via the explicit `/edit` slash command.
disable-model-invocation: true
---

# /edit

Three-phase critical editorial review settled by an internal subagent.

## Language determination

Source the language from the input text (detect mode). The resolution procedure:

1. **Argument.** If the user passed a language argument (e.g. `sv`, `sv_SE`, `en`, `en_GB`, `en_US`), use it as the candidate. A bare argument (`sv`, `en`) that matches no file directly but matches several territorial variants goes to the disambiguation question below.
2. **Detect.** Without an argument, infer the language from the input text.
3. **Inventory.** Look for `<lang>.md` in `../../lib/languages/` for the candidate:
   - One match: use it. The file carries both layers in named sections; the calling phase determines which section applies. If the file contains no *Style* section for the language, Phase 2 proceeds without a language-specific style overlay.
   - Several matches: ask the user which to use.
   - No match: fall back to `../../lib/languages/default-mechanics.md` and mention this in the reply (in English):
     > No language file found for [language]. Baseline conventions from `default-mechanics.md` apply. Add `lib/languages/<code>.md` for stricter control.

Phase 1 (proofread) applies only the *Mechanics* section. Phase 2 (redline) applies both the *Mechanics* and *Style* sections. When only `default-mechanics.md` is available, Phase 2 still runs but without language-specific style overlays — the universal style foundation in `rules/style.md` carries the pass.

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

Trigger 1 from the redline last-resort floor remains the safety net: if the fast-path commits to `general` for material that actually wants another genre, the redline pass surfaces it as a last-resort developmental finding, which then raises the subagent floor to 1.

## Phase 3 — settling

**Default behaviour.** The main agent applies the finding list directly to the corrected text and delivers the polished result via the output protocol matching the input form (see *Files to read*). No subagent is invoked.

**Subagent opt-in.** The subagent loop in `../../lib/protocols/subagent.md` runs only when explicitly requested. The ceiling on iterations comes from the `--max-iterations=N` flag in the invocation:

- `--max-iterations=0` (default): no subagent — main agent applies directly as above.
- `--max-iterations=1` / `=2` / `=3`: invoke the subagent with that ceiling. The subagent's convergence rules in `subagent.md` still apply — if main agent and subagent agree after an earlier round, the loop stops there.
- `N > 3` is clamped to 3 (the protocol maximum).

**Natural-language parity.** The model parses these expressions in the prompt to the same value as the flag (flag wins on conflict; ask if ambiguous):

- *iterera max tre gånger* / *iterate up to three times* / *kör djupt* / *deep review* → 3
- *max två rundor* / *two rounds max* → 2
- *en runda räcker* / *one round* → 1
- *hoppa över subagent* / *skip subagent* → 0

**Last-resort floor.** When the redline pass produces the last-resort finding from `protocols/redline.md` (the text is structured as one content type but the material wants another, or is below the line-editing repair threshold), the subagent floor is raised to 1 even if the flag is 0 — one round to sanity-check the observation before it reaches the user. The last-resort decision itself is escalated to the user as a closing note.

## Files to read

> The list below is a coverage requirement, not a sequence of unconditional reads. Before each Read, check whether the file's content is already in your conversation context — from any prior turn, phase, or skill invocation in this session. If it is, skip it. The user's input file or URL is always fetched fresh.

> Reads that are not skipped above fire in batches. Each batch below groups files with no mutual dependency; issue all of them as a single parallel tool call, then advance to the next batch when the previous returns.

**Batch 1.** Issue these reads in parallel:

- `../../lib/protocols/proofread.md` — Phase 1 procedure.
- `../../lib/protocols/redline.md` — Phase 2 procedure.
- `../../lib/protocols/subagent.md` — Phase 3 settling protocol.
- `../../lib/rules/writing.md` — universal punctuation rules.
- `../../lib/rules/constructions.md` — construction-scoped rules; apply the sections that match constructions in the input.
- `../../lib/languages/<lang>.md` (otherwise `../../lib/languages/default-mechanics.md`).
- `../../lib/rules/style.md` — Phase 2 universal style foundation.
- `../../lib/protocols/io.md` — input detection and output routing.
- One of the following based on the *Genre fast-path* check above:
  - **Fast-path (both conditions hold):** `../../lib/genres/general.md` — committed genre. No `_index.md` read.
  - **Standard (either condition broken):** `../../lib/genres/_index.md` — to identify the content type.

**Batch 2.** Skipped under the fast-path. Under the standard path, after the genre and technique are identified from Batch 1's `_index.md`:

- The matching `../../lib/genres/<type>.md`.
- The matching `../../lib/techniques/<technique>.md`.

## Output

The output protocol routes the polished final text after Phase 3 completes.
