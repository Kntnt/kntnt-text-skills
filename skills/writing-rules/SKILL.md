---
name: writing-rules
description: Manual context loader that loads the plugin's writing rules and general style guidance into the current session, optionally for a specific language. After invocation, the agent has the typographic, grammatical, and stylistic rule set available for any ad-hoc writing the user does in the same session — without invoking /write or /edit. Accepts an optional language argument (e.g. `/writing-rules sv`, `/writing-rules en_GB`); without one, loads all installed language files so that any subsequent language is covered. Activates only via the explicit /writing-rules slash command.
disable-model-invocation: true
---

# /writing-rules

Load the rule files into context, then confirm briefly that the rules are ready. Do not summarise their content unless the user asks.

## Language determination

If the user passed a language argument (e.g. `sv`, `sv_SE`, `en`, `en_GB`, `en_US`), load that language's mechanics and style files (`<lang>-mechanics.md` plus `<lang>-style.md` where it exists). If the named language has no specific files in `../../lib/languages/`, load `../../lib/languages/default-mechanics.md` and mention this in the reply (in English):

> No language file found for [language]. Baseline conventions from `default-mechanics.md` apply. Add `lib/languages/<code>-mechanics.md` and `lib/languages/<code>-style.md` for stricter control.

Without an argument, load every `*-mechanics.md` and `*-style.md` file in `../../lib/languages/` so the session has full coverage for any subsequent ad-hoc writing.

## Files to read

This loader provides full session coverage and reads every rule file regardless of input (no conditional rule loading):

1. `../../lib/rules/writing.md` — universal punctuation: comma, dash, parenthesis.
2. `../../lib/rules/quotation.md` — quotation (run-in, block, dialogue).
3. `../../lib/rules/abbreviations.md` — initialisms and acronyms.
4. `../../lib/rules/headed-text.md` — body-text self-sufficiency.
5. `../../lib/rules/lists.md` — list punctuation and capitalisation.
6. `../../lib/rules/style.md` — substantive style guidance: organising principle, repetition rule, techniques, cognitive load, understatement, precision, transitions, address and voice, pedagogy, attributed quotes, AI-tell principle, training-language interference, global rules (source fabrication ban, AI metaphor ban, rhetorical question rule).
7. `../../lib/languages/<lang>-mechanics.md` and `../../lib/languages/<lang>-style.md` — the language files per the determination above. When the named language has no specific files, `../../lib/languages/default-mechanics.md` is loaded instead.
