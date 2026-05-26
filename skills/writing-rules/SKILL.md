---
name: writing-rules
description: Manual context loader that loads the plugin's writing rules and general style guidance into the current session, optionally for a specific language. After invocation, the agent has the typographic, grammatical, and stylistic rule set available for any ad-hoc writing the user does in the same session — without invoking /write or /edit. Accepts an optional language argument (e.g. `/writing-rules sv`, `/writing-rules en_GB`); without one, loads all installed language files so that any subsequent language is covered. Activates only via the explicit /writing-rules slash command.
disable-model-invocation: true
---

# /writing-rules

Load the rule files into context, then confirm briefly that the rules are ready. Do not summarise their content unless the user asks.

## Language determination

If the user passed a language argument (e.g. `sv`, `sv_SE`, `en`, `en_GB`, `en_US`), load that language's file (`<lang>.md`) — both layers live in named sections inside the file. If the named language has no specific file in `../../lib/languages/`, load `../../lib/languages/default-mechanics.md` and mention this in the reply (in English):

> No language file found for [language]. Baseline conventions from `default-mechanics.md` apply. Add `lib/languages/<code>.md` for stricter control.

Without an argument, load every `<lang>.md` file in `../../lib/languages/` (plus `default-mechanics.md`) so the session has full coverage for any subsequent ad-hoc writing.

## Files to read

> The list below is a coverage requirement, not a sequence of unconditional reads. Before each Read, check whether the file's content is already in your conversation context — from any prior turn, phase, or skill invocation in this session. If it is, skip it. The user's input file or URL is always fetched fresh.

> Reads that are not skipped above fire in batches. Each batch below groups files with no mutual dependency; issue all of them as a single parallel tool call, then advance to the next batch when the previous returns.

**Batch 1.** Issue every rule file in parallel (this loader provides full session coverage and reads every rule file regardless of input — no conditional rule loading):

- `../../lib/rules/writing.md` — universal punctuation: comma, dash, parenthesis.
- `../../lib/rules/constructions.md` — construction-scoped rules: quotation (run-in, block, dialogue), initialisms and acronyms, body-text self-sufficiency, list punctuation and capitalisation.
- `../../lib/rules/style.md` — substantive style guidance: organising principle, repetition rule, techniques, cognitive load, understatement, precision, transitions, address and voice, pedagogy, attributed quotes, AI-tell principle, training-language interference, global rules (source fabrication ban, AI metaphor ban, rhetorical question rule).
- `../../lib/languages/<lang>.md` — the language file per the determination above. When the named language has no specific file, `../../lib/languages/default-mechanics.md` is loaded instead.
