---
name: proofread
description: Conservative proofreading. The first and lightest of the three review skills — proofread ⊂ redline ⊂ edit. Corrects only objectively wrong things — spelling, grammar, punctuation, duplicated or missing words, obvious wrong-word errors, and the typographic and language conventions of the matching language file. Never changes style, word order, structure, voice, or argumentation. Use whenever the user writes "/proofread" — alone (operates on the most recent text in the conversation) or followed by text, a file reference, or a URL. An optional language argument (e.g. `/proofread sv`, `/proofread en_GB`) can be supplied. Trigger on "proofread", "proofreading", "copyedit", "copyediting", "korrekturläs", "korra", "fix the typos", "check the spelling", "spell-check". Auto-detects language when no argument is given. Preserves original formatting.
---

# /proofread

Apply the procedure in `../../lib/protocols/proofread.md` to the user's input.

## Language determination

If the user passed a language argument (e.g. `sv`, `sv_SE`, `en`, `en_GB`, `en_US`), use it. Otherwise determine language in two steps:

1. **Detect** the language of the input text.
2. **Inventory** the matching files in `../../lib/languages/`:
   - If multiple files exist for the detected language (e.g., both `en.md` and `en_GB.md` and `en_US.md`), ask the user which to use.
   - If a single file exists for the detected language (base or territorial), use it without asking.
   - If no file exists for the detected language, fall back to `../../lib/languages/default.md` and mention this in the reply (in English):
     > No language file found for [language]. Baseline conventions from `default.md` apply. Add `lib/languages/<code>.md` for stricter control.

Only the *Mechanics* section of the loaded language file (or of `default.md`) applies to this skill. The *Style* section is out of scope here — it is used by the redline / edit passes.

## Files to read

1. `../../lib/protocols/proofread.md` — the procedure and the full scope.
2. `../../lib/rules/writing.md` — universal writing conventions.
3. `../../lib/languages/<lang>.md` — the specific language file determined above. If none exists for the determined language, use `../../lib/languages/default.md` instead.
4. `../../lib/protocols/input.md` — only when the input source needs resolving (file reference, URL, bare `/proofread`).
5. `../../lib/protocols/output.md` — only as needed to deliver the result.
