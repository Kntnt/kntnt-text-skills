---
name: proofread
description: Conservative proofreading — proofread ⊂ redline ⊂ edit, the lightest of three review skills. Corrects only objectively wrong things (spelling, grammar, punctuation, duplicated or missing words, wrong-word errors, and the loaded language file's typographic and mechanic conventions). Never changes style, word order, structure, voice, or argumentation — those are the redline / edit passes. Use whenever the user writes `/proofread` (alone — operates on the most recent text in the conversation — or followed by text, a file reference, or a URL). English trigger phrases — `proofread`, `proofreading`, `copyedit`, `copyediting`, `fix the typos`, `check the spelling`, `spell-check`. Swedish equivalents (`korrekturläs`, `korra`, `rätta stavfel`) and similar phrasings in other languages are understood semantically. Optional language argument (`/proofread sv`, `/proofread en_GB`); without it, auto-detects from the input. Preserves original formatting.
---

# /proofread

Apply the procedure in `../../lib/protocols/proofread.md` to the user's input.

## Language determination

Source the language from the input text (detect mode). The resolution procedure:

1. **Argument.** If the user passed a language argument (e.g. `sv`, `sv_SE`, `en`, `en_GB`, `en_US`), use it as the candidate. A bare argument (`sv`, `en`) that matches no file directly but matches several territorial variants (e.g. `en` matches `en_GB` and `en_US`) goes to the disambiguation question below.
2. **Detect.** Without an argument, infer the language from the input text.
3. **Inventory.** Look for `<lang>-mechanics.md` in `../../lib/languages/` for the candidate:
   - One match: use it.
   - Several matches (e.g. `en` matches `en_GB-mechanics.md` and `en_US-mechanics.md`): ask the user which to use.
   - No match: fall back to `../../lib/languages/default-mechanics.md` and mention this in the reply (in English):
     > No language file found for [language]. Baseline conventions from `default-mechanics.md` apply. Add `lib/languages/<code>-mechanics.md` for stricter control.

Only the mechanics file applies to this skill. The style file (`<lang>-style.md`) is out of scope here — it is used by the redline / edit passes.

## Genre selection

This skill does not consult a genre file — only mechanics apply. The plugin-wide fallback rule still holds: if any genre selection becomes necessary, use the genre whose frontmatter has `default: true`.

## Conditional rule loading

Inspect the input before loading rule files. Load only the rule files that match constructions actually present in the input:

- Always: `../../lib/rules/writing.md` — the universal punctuation rules (comma, dash, parenthesis).
- If the input contains quotation marks, dialogue, or block quotations: `../../lib/rules/quotation.md`.
- If the input contains initialisms or acronyms: `../../lib/rules/abbreviations.md`.
- If the input contains H1, headings, subheadings, or a standfirst structure: `../../lib/rules/headed-text.md`.
- If the input contains bulleted, numbered, or definition lists: `../../lib/rules/lists.md`.

A short paragraph with none of those constructions loads only `writing.md`.

## Files to read

> The list below is a coverage requirement, not a sequence of unconditional reads. Before each Read, check whether the file's content is already in your conversation context — from any prior turn, phase, or skill invocation in this session. If it is, skip it. The user's input file or URL is always fetched fresh.

1. `../../lib/protocols/proofread.md` — the procedure and the full scope.
2. `../../lib/rules/writing.md` — universal punctuation rules.
3. Whichever construction-scoped rule files match the input (`quotation.md`, `abbreviations.md`, `headed-text.md`, `lists.md`) per *Conditional rule loading* above.
4. `../../lib/languages/<lang>-mechanics.md` — the specific mechanics file determined above. If none exists for the determined language, use `../../lib/languages/default-mechanics.md` instead.
5. `../../lib/protocols/input.md` — to determine the input form (inline text, file, or URL).
6. `../../lib/protocols/output-inline.md` if the input is inline; otherwise `../../lib/protocols/output-files.md` — to deliver the result.
