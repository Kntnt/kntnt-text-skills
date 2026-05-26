---
name: pac
description: Manual context loader that loads the PAC technique (Premise, Analysis, Conclusion — analytical arc) into the current session. After invocation, the agent can apply or reference PAC outside /write or /edit — for structuring reports and analytical sections, discussing the arc, or applying it to an existing text. Activates only via the explicit /pac slash command.
disable-model-invocation: true
---

# /pac

Load the technique into context, then confirm briefly that PAC is ready. Do not summarise its content unless the user asks.

## Files to read

> The list below is a coverage requirement, not a sequence of unconditional reads. Before each Read, check whether the file's content is already in your conversation context — from any prior turn, phase, or skill invocation in this session. If it is, skip it. The user's input file or URL is always fetched fresh.

1. `../../lib/techniques/pac.md` — the technique: the three parts, where PAC applies, visibility, variants, and concrete examples.
