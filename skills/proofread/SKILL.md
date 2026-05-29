---
name: proofread
description: Conservative proofreading of an existing text — mechanical errors only (spelling, grammar, punctuation, typography per the loaded language), no style touch-ups. Activate when the user explicitly invokes this plugin's proofread skill — `/proofread`, `/kntnt-text-skills:proofread`, `kntnt text skills proofread`, `text-proofread-skill`, "proofread X with Kntnt's skill", "Kntnt's text proofread skill", or similar plugin-anchored phrasing. Do not activate on bare requests to "proofread", "fix typos", or "spell-check".
---

# /proofread

Conservative proofreading: corrects mechanical errors only (spelling, grammar, punctuation, typography per the loaded language). Doesn't touch style, word order, or argumentation. Pass an optional language argument (`/proofread sv`, `/proofread en_GB`) to force a language; without it, the language is detected from the input.

When activated, apply the procedure in `../../lib/protocols/proofread.md` to the user's input.

## Language determination

Resolve the language via `../../lib/protocols/language-resolution.md` in *detect mode* — the source language is inferred from the input text. Only the *Mechanics* section of the loaded language file applies to this skill; the *Style* section is out of scope.

## Genre selection

This skill does not consult a genre file — only mechanics apply. The plugin-wide fallback rule still holds: if any genre selection becomes necessary, use the genre whose frontmatter has `default: true`.

## Rule application

Apply the universal punctuation rules in `../../lib/rules/writing.md` always. Apply the matching sections of `../../lib/rules/constructions.md` (quotation, abbreviation, headed-text, lists) only when the input contains those constructions. Section-level filtering is cognitive — the file is loaded in full and the relevant sections are read against the input.

## Files to read

> The list below is a coverage requirement, not a sequence of unconditional reads. Before each Read, check whether the file's content is already in your conversation context — from any prior turn, phase, or skill invocation in this session. If it is, skip it. The user's input file or URL is always fetched fresh.

> Reads that are not skipped above fire in batches. Each batch below groups files with no mutual dependency; issue all of them as a single parallel tool call, then advance to the next batch when the previous returns.

**Batch 1.** Issue these reads in parallel:

- `../../lib/protocols/io.md` — input detection and output routing.
- `../../lib/protocols/language-resolution.md` — language candidate, file inventory, overlay loader, fallback reporting.
- `../../lib/protocols/proofread.md` — the procedure and the full scope.
- `../../lib/rules/writing.md` — universal punctuation rules.
- `../../lib/rules/constructions.md` — construction-scoped rules; apply the sections that match constructions in the input.
- `../../lib/languages/<lang>.md` — the specific language file determined above (apply only its mechanics section). If none exists for the determined language, use `../../lib/languages/default-mechanics.md` instead.
