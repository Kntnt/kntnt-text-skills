---
name: Bug report
about: A rule, protocol or language file produces the wrong outcome on a concrete input.
title: "[bug] "
labels: bug
assignees: ""
---

## Which rule or protocol

Name the file (e.g. `lib/rules/style.md`, `lib/protocols/redline.md`) and, where applicable, the section, heading or rule number you believe is misbehaving. If the issue spans several files, list each.

## Which language file

Name the language file in play (e.g. `lib/languages/sv.md`, `lib/languages/en_GB.md` or `lib/languages/default-mechanics.md` if the fallback was used).

## Which skill

Which slash command surfaced the bug (`/proofread`, `/redline`, `/edit`, `/write`, `/writing-rules`, `/abt`, `/pac`)? Include any flags used (e.g. `--max-iterations=2`).

## Input

The exact text or prompt you fed the skill. Paste it inside a fenced code block so whitespace, punctuation and casing are preserved. If the input is long, attach it as a file or link to a gist.

```
your input here
```

## Observed outcome

What the plugin actually did. Paste the relevant part of the response.

## Expected outcome

What the rule, protocol or language file says (or should say) the plugin should have done. Quote the rule text if you can.

## Environment

- Plugin version (from `.claude-plugin/plugin.json`):
- Client (Claude Code / Cowork) and version:
- Operating system:

## Additional context

Anything else that helps reproduce the issue – related runs, screenshots, recent changes to your local copy, etc.
