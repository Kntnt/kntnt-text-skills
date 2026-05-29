---
name: edit
description: Three-phase AFK editorial review of an existing text — silent proofread, critical review against the full rule set, automatic application of the finding list. Activate when the user explicitly invokes this plugin's edit skill: `/edit`, `/kntnt-text-skills:edit`, `kntnt text skills edit`, `text-edit-skill`, "edit X with Kntnt's skill", "Kntnt's text edit skill", or similar plugin-anchored phrasing. Do not activate on bare requests to "edit" or "fix" something.
---

# /edit

Reviews your text for mechanical errors (spelling, grammar, punctuation) and editorial concerns (clarity, style, structure), applies the fixes automatically, and returns the polished result. Optionally takes `--max-iterations=N` (0–3) to run additional review rounds that re-examine the fixes before delivery; default 0 is a single pass.

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

## Genre resolution

Resolve the genre and technique via `../../lib/protocols/genre-resolution.md`. The protocol consumes the input text and the user's prompt; it produces a committed genre and a committed technique that determine which files are read below.

## Phase 3 — settling

**Default behaviour.** The main agent applies the finding list directly to the corrected text and delivers the polished result via the output protocol matching the input form (see *Files to read*). No subagent is invoked.

**Subagent opt-in.** The subagent loop in `../../lib/protocols/subagent.md` runs only when explicitly requested. The ceiling on iterations comes from the `--max-iterations=N` flag in the invocation:

- `--max-iterations=0` (default): no subagent — main agent applies directly as above.
- `--max-iterations=1` / `=2` / `=3`: invoke the subagent with that ceiling. The subagent's convergence rules in `subagent.md` still apply — if main agent and subagent agree after an earlier round, the loop stops there.
- `N > 3` is clamped to 3 (the protocol maximum).

**Natural-language parity.** For the phrases that map to `N`, see *Natural-language parity* in `../../lib/protocols/subagent.md` (loaded as part of Batch 1). The flag wins on conflict; ask if the prompt is ambiguous.

**Last-resort floor.** When the redline pass produces the last-resort finding from `protocols/redline.md` (the text is structured as one content type but the material wants another, or is below the line-editing repair threshold), the subagent floor is raised to 1 even if the flag is 0 — one round to sanity-check the observation before it reaches the user. The last-resort decision itself is escalated to the user as a closing note.

## Files to read

> The list below is a coverage requirement, not a sequence of unconditional reads. Before each Read, check whether the file's content is already in your conversation context — from any prior turn, phase, or skill invocation in this session. If it is, skip it. The user's input file or URL is always fetched fresh.

> Reads that are not skipped above fire in batches. Each batch below groups files with no mutual dependency; issue all of them as a single parallel tool call, then advance to the next batch when the previous returns.

**Batch 1.** Issue these reads in parallel:

- `../../lib/protocols/genre-resolution.md` — genre and technique resolution, including the fast-path that may exit before `_index.md` is read.
- `../../lib/protocols/io.md` — input detection and output routing.
- `../../lib/protocols/language-resolution.md` — language candidate, file inventory, overlay loader, fallback reporting.
- `../../lib/protocols/proofread.md` — Phase 1 procedure.
- `../../lib/protocols/redline.md` — Phase 2 procedure.
- `../../lib/protocols/subagent.md` — Phase 3 settling protocol.
- `../../lib/rules/constructions.md` — construction-scoped rules; apply the sections that match constructions in the input.
- `../../lib/rules/style.md` — Phase 2 universal style foundation.
- `../../lib/rules/writing.md` — universal punctuation rules.
- `../../lib/languages/<lang>.md` (otherwise `../../lib/languages/default-mechanics.md`).

**Conditional reads.** Per the genre-resolution protocol's fast-path exit:

- `../../lib/genres/_index.md` — read only when the fast-path does not exit (either condition broken).
- The matching `../../lib/genres/<type>.md` — under the fast-path, the committed fallback genre's file; under the standard flow, the genre file the index resolved to.
- The matching `../../lib/techniques/<technique>.md` — read only when the committed genre's `default_technique` is not `none`.

## Output

The output protocol routes the polished final text after Phase 3 completes.
