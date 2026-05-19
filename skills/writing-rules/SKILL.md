---
name: writing-rules
description: Manual context loader that loads the plugin's writing rules and general style guidance into the current session, optionally for a specific language. After invocation, the agent has the typographic, grammatical, and stylistic rule set available for any ad-hoc writing the user does in the same session — without invoking /write or /edit. Accepts an optional language argument (e.g. `/writing-rules sv`, `/writing-rules en_GB`); without one, loads all installed language files so that any subsequent language is covered. Activates only via the explicit /writing-rules slash command.
disable-model-invocation: true
---

# /writing-rules

Load the rule files into context, then confirm briefly that the rules are ready. Do not summarise their content unless the user asks.

## Language determination

If the user passed a language argument (e.g. `sv`, `sv_SE`, `en`, `en_GB`, `en_US`), load only that language file. If the named language has no specific file in `../../lib/languages/`, load `../../lib/languages/default.md` and mention this in the reply (in English):

> No language file found for [language]. Baseline conventions from `default.md` apply. Add `lib/languages/<code>.md` for stricter control.

Without an argument, load all language files in `../../lib/languages/` so the session has full coverage for any subsequent ad-hoc writing.

## Files to read

1. `../../lib/rules/writing.md` — universal writing conventions: punctuation, dashes, quotation (run-in, block, dialogue), abbreviations, body-text self-sufficiency, lists.
2. `../../lib/rules/style.md` — substantive style guidance: organising principle, repetition rule, techniques, cognitive load, understatement, precision, transitions, address and voice, pedagogy, attributed quotes, AI-tell principle, training-language interference, global rules (source fabrication ban, AI metaphor ban, rhetorical question rule).
3. `../../lib/languages/<lang>.md` — the language file(s) per the determination above. When the named language has no specific file, `../../lib/languages/default.md` is loaded instead.
