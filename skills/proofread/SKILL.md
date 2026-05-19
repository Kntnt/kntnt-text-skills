---
name: proofread
description: Conservative proofreading. The first and lightest of the three review skills — proofread ⊂ redline ⊂ edit. Corrects only objectively wrong things — spelling, grammar, punctuation, duplicated or missing words, obvious wrong-word errors, and the typographic and language conventions of the matching language file. Never changes style, word order, structure, voice, or argumentation. Use whenever the user writes "/proofread" — alone (operates on the most recent text in the conversation) or followed by text, a file reference, or a URL. An optional language argument (e.g. `/proofread sv`, `/proofread en_GB`) can be supplied. Trigger on "proofread", "proofreading", "copyedit", "copyediting", "korrekturläs", "korra", "fix the typos", "check the spelling", "spell-check". Auto-detects language when no argument is given. Preserves original formatting.
---

# /proofread

Apply the procedure in `../../lib/protocols/proofread.md` to the user's input.

## Language determination

Follow `../../lib/protocols/language.md` in **detect mode** — source the language from the input text.

Only the *Mechanics* section of the loaded language file (or of `default.md`) applies to this skill. The *Style* section is out of scope here — it is used by the redline / edit passes.

## Files to read

1. `../../lib/protocols/language.md` — the language determination procedure.
2. `../../lib/protocols/proofread.md` — the procedure and the full scope.
3. `../../lib/rules/writing.md` — universal writing conventions.
4. `../../lib/languages/<lang>.md` — the specific language file determined above. If none exists for the determined language, use `../../lib/languages/default.md` instead.
5. `../../lib/protocols/input.md` — only when the input source needs resolving (file reference, URL, bare `/proofread`).
6. `../../lib/protocols/output.md` — only as needed to deliver the result.
