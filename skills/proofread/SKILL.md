---
name: proofread
description: Conservative proofreading — proofread ⊂ redline ⊂ edit, the lightest of three review skills. Corrects only objectively wrong things (spelling, grammar, punctuation, duplicated or missing words, wrong-word errors, and the loaded language file's typographic and mechanic conventions). Never changes style, word order, structure, voice, or argumentation — those are the redline / edit passes. Use whenever the user writes `/proofread` (alone — operates on the most recent text in the conversation — or followed by text, a file reference, or a URL). English trigger phrases — `proofread`, `proofreading`, `copyedit`, `copyediting`, `fix the typos`, `check the spelling`, `spell-check`. Swedish equivalents (`korrekturläs`, `korra`, `rätta stavfel`) and similar phrasings in other languages are understood semantically. Optional language argument (`/proofread sv`, `/proofread en_GB`); without it, auto-detects from the input. Preserves original formatting.
---

# /proofread

Apply the procedure in `../../lib/protocols/proofread.md` to the user's input.

## Language determination

Follow `../../lib/protocols/language.md` in **detect mode** — source the language from the input text.

Only the *Mechanics* section of the loaded language file (or of `default.md`) applies to this skill. The *Style* section is out of scope here — it is used by the redline / edit passes.

## Genre selection

This skill does not consult a genre file — only *Mechanics* applies. The plugin-wide fallback rule still holds: if any genre selection becomes necessary, use the genre whose frontmatter has `default: true`.

## Files to read

1. `../../lib/protocols/language.md` — the language determination procedure.
2. `../../lib/protocols/proofread.md` — the procedure and the full scope.
3. `../../lib/rules/writing.md` — universal writing conventions.
4. `../../lib/languages/<lang>.md` — the specific language file determined above. If none exists for the determined language, use `../../lib/languages/default.md` instead.
5. `../../lib/protocols/input.md` — only when the input source needs resolving (file reference, URL, bare `/proofread`).
6. `../../lib/protocols/output.md` — only as needed to deliver the result.
