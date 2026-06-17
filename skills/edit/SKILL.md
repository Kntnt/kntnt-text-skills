---
name: edit
description: Three-phase AFK editorial review of an existing text – silent proofread, critical review against the full rule set, automatic application of the finding list. Activate when the user explicitly invokes this plugin's edit skill – `/edit`, `/kntnt-text-skills:edit`, `kntnt text skills edit`, `text-edit-skill`, "edit X with Kntnt's skill", "Kntnt's text edit skill" or similar plugin-anchored phrasing. Do not activate on bare requests to "edit" or "fix" something.
---

# /edit

Reviews your text for mechanical errors (spelling, grammar, punctuation) and editorial concerns (clarity, style, structure), applies the fixes automatically and returns the polished result. Optionally takes `--max-iterations=N` (0–3) to set how many adversarial review rounds re-examine the fixes before delivery; default 1 runs one round, `0` opts out, `2`/`3` raise the ceiling.

## Language determination

Resolve the language via `${CLAUDE_PLUGIN_ROOT}/lib/protocols/language-resolution.md` in *detect mode* – the source language is inferred from the input text.

Phase 1 (proofread) applies only the *Mechanics* section of the loaded language file. Phase 2 (redline) applies both the *Mechanics* and *Style* sections. When the file has no *Style* section (or when only `default-mechanics.md` is loaded), Phase 2 still runs but without language-specific style overlays – the universal style foundation in `rules/style.md` carries the pass.

## Rule application

Apply the universal punctuation rules in `${CLAUDE_PLUGIN_ROOT}/lib/rules/writing.md` always. Apply the matching sections of `${CLAUDE_PLUGIN_ROOT}/lib/rules/constructions.md` (quotation, abbreviation, headed-text, lists) only when the input contains those constructions. Section-level filtering is cognitive – the file is loaded in full and the relevant sections are read against the input.

## Phase 1 – silent proofread

Apply `${CLAUDE_PLUGIN_ROOT}/lib/protocols/proofread.md` against the loaded rule files and the *Mechanics* section of the loaded language file. The corrected text flows directly into Phase 2 – it is not delivered as a separate intermediate output.

## Phase 2 – critical review

Apply `${CLAUDE_PLUGIN_ROOT}/lib/protocols/redline.md` against `${CLAUDE_PLUGIN_ROOT}/lib/rules/style.md`, the *Style* section of the loaded language file (where it exists), the applicable file in `${CLAUDE_PLUGIN_ROOT}/lib/genres/` and the applicable file in `${CLAUDE_PLUGIN_ROOT}/lib/techniques/`. The pass produces a finding list.

If no genre matches clearly via triggers or semantic likeness, use the genre whose frontmatter has `default: true`. Do not read multiple genre files in full to compare – the frontmatter inventory plus the fallback flag is sufficient to decide.

When reading the chosen genre file, skip sections preceded by `<!-- scope: write -->`; read only unmarked sections and sections preceded by `<!-- scope: review -->`. Write-scoped sections describe drafting concerns (structure, length, headings, address) that add no value to a review pass.

## Genre resolution

Resolve the genre and technique via `${CLAUDE_PLUGIN_ROOT}/lib/protocols/genre-resolution.md`. The protocol consumes the input text and the user's prompt; it produces a committed genre and a committed technique that determine which files are read below.

## Phase 3 – settling

**Default behaviour.** Run one adversarial review round through the subagent loop in `${CLAUDE_PLUGIN_ROOT}/lib/protocols/subagent.md`. The default exists because the main agent applying its own redline findings to its own corrected text, in the same context, is too weak a check for register – it converges on cosmetic edits and calls translated-reading prose publication-ready. One round of an adversarial register reviewer is the floor that catches the AI-tell and translated-reading faults a same-context pass misses.

**Iteration ceiling.** The `--max-iterations=N` flag sets how many rounds the loop may run:

- `--max-iterations=1` (default): one adversarial round. The subagent's convergence rules in `subagent.md` apply – the round runs, then the main agent applies what the dialogue settled and delivers.
- `--max-iterations=2` / `=3`: raise the ceiling. The loop stops early once main agent and subagent agree, but may not stop before the adversarial register pass has run at least once.
- `--max-iterations=0`: opt out – the main agent applies the finding list directly to the corrected text without a subagent round. This is the explicit escape hatch, not the default.
- `N > 3` is clamped to 3 (the protocol maximum).

**Natural-language parity.** For the phrases that map to `N`, see *Natural-language parity* in `${CLAUDE_PLUGIN_ROOT}/lib/protocols/subagent.md` (loaded as part of Batch 1). The flag wins on conflict; ask if the prompt is ambiguous.

**Last-resort floor.** When the redline pass produces the last-resort finding from `protocols/redline.md` (the text is structured as one content type but the material wants another, or is below the line-editing repair threshold), the subagent floor is raised to 1 even if the flag is 0 – one round to sanity-check the observation before it reaches the user. The last-resort decision itself is escalated to the user as a closing note.

## Files to read

> The list below is a coverage requirement, not a sequence of unconditional reads. Before each Read, check whether the file's content is already in your conversation context – from any prior turn, phase or skill invocation in this session. If it is, skip it. The user's input file or URL is always fetched fresh.

> Reads that are not skipped above fire in batches. Each batch below groups files with no mutual dependency; issue all of them as a single parallel tool call, then advance to the next batch when the previous returns.

**Batch 1.** Issue these reads in parallel:

- `${CLAUDE_PLUGIN_ROOT}/lib/protocols/genre-resolution.md` – genre and technique resolution, including the fast-path that may exit before `_index.md` is read.
- `${CLAUDE_PLUGIN_ROOT}/lib/protocols/io.md` – input detection and output routing.
- `${CLAUDE_PLUGIN_ROOT}/lib/protocols/language-resolution.md` – language candidate, file inventory, overlay loader, fallback reporting.
- `${CLAUDE_PLUGIN_ROOT}/lib/protocols/proofread.md` – Phase 1 procedure.
- `${CLAUDE_PLUGIN_ROOT}/lib/protocols/redline.md` – Phase 2 procedure.
- `${CLAUDE_PLUGIN_ROOT}/lib/protocols/subagent.md` – Phase 3 settling protocol.
- `${CLAUDE_PLUGIN_ROOT}/lib/rules/constructions.md` – construction-scoped rules; apply the sections that match constructions in the input.
- `${CLAUDE_PLUGIN_ROOT}/lib/rules/style.md` – Phase 2 universal style foundation.
- `${CLAUDE_PLUGIN_ROOT}/lib/rules/writing.md` – universal punctuation rules.
- `${CLAUDE_PLUGIN_ROOT}/lib/languages/<lang>.md` (otherwise `${CLAUDE_PLUGIN_ROOT}/lib/languages/default-mechanics.md`).

**Conditional reads.** Per the genre-resolution protocol's fast-path exit:

- `${CLAUDE_PLUGIN_ROOT}/lib/genres/_index.md` – read only when the fast-path does not exit (either condition broken).
- The matching `${CLAUDE_PLUGIN_ROOT}/lib/genres/<type>.md` – under the fast-path, the committed fallback genre's file; under the standard flow, the genre file the index resolved to.
- The matching `${CLAUDE_PLUGIN_ROOT}/lib/techniques/<technique>.md` – read only when the committed genre's `default_technique` is not `none`.

## Output

The output protocol routes the polished final text after Phase 3 completes.
