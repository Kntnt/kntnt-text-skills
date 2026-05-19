---
name: pac
description: Manual context loader that loads the PAC technique (Premise, Analysis, Conclusion — analytical arc) into the current session. After invocation, the agent can apply or reference PAC outside /write or /edit — for structuring reports and analytical sections, discussing the arc, or applying it to an existing text. Activates only via the explicit /pac slash command.
disable-model-invocation: true
---

# /pac

Load the technique into context, then confirm briefly that PAC is ready. Do not summarise its content unless the user asks.

## Files to read

1. `../../lib/techniques/pac.md` — the technique: the three parts, where PAC applies, visibility, variants, and concrete examples.
