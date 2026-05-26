---
name: abt
description: Manual context loader that loads the ABT technique (And, But, Therefore — narrative arc) into the current session. After invocation, the agent can apply or reference ABT outside /write or /edit — for ad-hoc structuring questions, technique discussions, or applying the arc to an existing text. Activates only via the explicit /abt slash command.
disable-model-invocation: true
---

# /abt

Load the technique into context, then confirm briefly that ABT is ready. Do not summarise its content unless the user asks.

## Files to read

> The list below is a coverage requirement, not a sequence of unconditional reads. Before each Read, check whether the file's content is already in your conversation context — from any prior turn, phase, or skill invocation in this session. If it is, skip it. The user's input file or URL is always fetched fresh.

1. `../../lib/techniques/abt.md` — the technique: the three parts, variants, in medias res, the decisive point that the structure must stay invisible, and concrete examples.
