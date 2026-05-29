---
name: writing-rules
description: Loads the plugin's writing rules, construction-scoped rules, substantive style, and language-specific mechanics into the session. Activate when the user explicitly invokes this plugin's writing-rules loader: `/writing-rules`, `/kntnt-text-skills:writing-rules`, `kntnt text skills writing rules`, "load Kntnt's writing rules", "Kntnt's writing-rules loader", or similar plugin-anchored phrasing. Do not activate on casual mentions of writing rules or style guidance.
---

# /writing-rules

Loads the plugin's writing rules and style guidance — universal punctuation, construction-scoped rules, substantive style, and language-specific mechanics — into the current session. Optionally takes a language argument (`/writing-rules sv`, `/writing-rules en_GB`) to load only one language's rules; without it, all installed language files are loaded.

When activated, load the rule files into context, then confirm briefly that the rules are ready. Do not summarise their content unless the user asks.

## Language determination

When the user passes a language argument, resolve it via `../../lib/protocols/language-resolution.md` — the argument step of the protocol applies; no source-mode inference is needed because the argument is present (the protocol's *detect* and *propose* modes are only consulted when no argument is given).

Without an argument, this loader skips resolution entirely and loads every `<lang>.md` file in `../../lib/languages/` (plus `default-mechanics.md`) so the session has full coverage for any subsequent ad-hoc writing. Apply the overlay procedure in the protocol to any variant file whose frontmatter declares `inherits` before the session uses it.

## Files to read

> The list below is a coverage requirement, not a sequence of unconditional reads. Before each Read, check whether the file's content is already in your conversation context — from any prior turn, phase, or skill invocation in this session. If it is, skip it. The user's input file or URL is always fetched fresh.

> Reads that are not skipped above fire in batches. Each batch below groups files with no mutual dependency; issue all of them as a single parallel tool call, then advance to the next batch when the previous returns.

**Batch 1.** Issue every rule file in parallel (this loader provides full session coverage and reads every rule file regardless of input — no conditional rule loading):

- `../../lib/protocols/language-resolution.md` — argument step, file inventory, overlay loader, fallback reporting (used when an argument is given).
- `../../lib/rules/writing.md` — universal punctuation: comma, dash, parenthesis.
- `../../lib/rules/constructions.md` — construction-scoped rules: quotation (run-in, block, dialogue), initialisms and acronyms, body-text self-sufficiency, list punctuation and capitalisation.
- `../../lib/rules/style.md` — substantive style guidance: organising principle, repetition rule, techniques, cognitive load, understatement, precision, transitions, address and voice, pedagogy, attributed quotes, AI-tell principle, training-language interference, global rules (source fabrication ban, AI metaphor ban, rhetorical question rule).
- `../../lib/languages/<lang>.md` — the language file per the determination above. When the named language has no specific file, `../../lib/languages/default-mechanics.md` is loaded instead. With no argument, every `<lang>.md` plus `default-mechanics.md` is loaded.
