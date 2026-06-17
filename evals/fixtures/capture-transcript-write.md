<!--
Synthetic transcript fixture for the /eval capture command (issue #45).

A fabricated mini /write session with planted maintainer feedback. Unlike the
edit fixture, a /write case has no input text to correct: its source is a brief
and the faults are properties a *fresh* draft must avoid (negative assertions)
or structural targets the opening must hit. Names (Erik Svensson, Ericsson) are
present so the anonymiser has something to scrub from the proposed brief.

Same wire format as the edit fixture: header, run narrative, the maintainer's
running feedback, and the before/after diff between the first draft and the
polished one.
-->
skill: write
language: en_GB
prompt: /write en_GB a short blog post about district heating, kör på

# Session

Maintainer invoked `/write en_GB` with a brief for a short blog post. The agent
ran the four phases and delivered a draft. The maintainer flagged what the
polish should have removed and what the opening should do.

## Maintainer feedback

- "The draft opens with *In a world where energy matters…* — that is a calque opening cliché, a fresh draft must not contain it."
- "*It's worth noting that* appears twice — an AI-tell construction; the draft must not contain it."
- "The opening buries the lede; the substance must arrive by sentence two, not the fourth."
- "*delve into the tapestry of* is AI vocabulary — strip it."

## Diff

```diff
- In a world where energy matters, let us delve into the tapestry of district
- heating. It's worth noting that Erik Svensson at Ericsson has views on this.
+ District heating is changing fast. Erik Svensson sets out why over the next
+ five years three forces reshape the network.
```
