# Subagent protocol

The colleague-consultation mechanic for settling editorial work without user-facing dialogue. The calling skill invokes this protocol when it has a critical-review finding list (or a draft and a finding list) and wants the polished result delivered directly – either because the skill is AFK by design, or because a parent dialogue has been delegated to internal settling, or because the skill produces new content and reviews it before delivery.

## Invocation conditions

This protocol is opt-in. The calling skill invokes it only when one of the following triggers fires:

- **Explicit `--max-iterations=N` flag (or natural-language equivalent) in the calling skill's invocation.** `N=0` means do not invoke this protocol; `N=1`, `=2`, `=3` set the ceiling on iterations for the current run. `N > 3` is clamped to 3. The calling skill is responsible for parsing the flag and the natural-language equivalents enumerated under *Natural-language parity* below, and passing the resulting ceiling into this protocol.
- **Last-resort finding from the redline pass raises the floor to 1.** When the redline pass produces a developmental observation per `redline.md` (the text is structured as one content type but the material wants another, or is below the line-editing repair threshold), the calling skill raises the iteration floor to 1 – one round of subagent sanity-check – even if the flag was 0. The closing note to the user about the last-resort decision is delivered after that round.

When neither trigger fires, the calling skill applies the redline findings directly without invoking this protocol. The default behaviour of the calling skill is therefore no subagent round.

The iteration ceiling passed in is an upper bound, not a target. The convergence rules in *Iteration rules* below still apply – early termination is desirable.

## Natural-language parity

The calling skill parses these expressions in its prompt to the same value as the `--max-iterations=N` flag. The flag wins on conflict; ask the user if the prompt is ambiguous.

- *iterera max tre gånger* / *iterate up to three times* / *kör djupt* / *deep review* → 3
- *max två rundor* / *two rounds max* → 2
- *en runda räcker* / *one round* → 1
- *hoppa över subagent* / *skip subagent* → 0

This enumeration is the single source of truth. Skills reference it rather than restating it inline.

## The subagent

The main agent spawns a subagent with access to the same procedural and rule material the main agent used in the redline pass – the loaded protocol files, the loaded objective rule files, the substantive style foundation, the applicable content-type file and the applicable technique file. The subagent is briefed with:

- The text under review (the corrected text after the proofread pass).
- The list of findings the main agent has produced via the redline pass.
- The main agent's motivation for each finding when it is not self-evident.
- Any prior dialogue history the main agent considers relevant, so that already-settled findings are not revisited.

The subagent acts as a senior editorial colleague. It briefs in English (the plugin meta-language) and answers in the language of the text under review.

## Iteration rules

- Maximum three subagent calls per invocation. Three permitted, not three mandatory.
- Iteration n+1 happens only if both: (a) the main agent has a concrete unresolved question or specific objection to test; (b) the subagent did not, in round n, declare itself satisfied.
- Calling the colleague "just to be safe" is forbidden.
- Repetition without new content does not count as an iteration and may be aborted.
- Early termination is desirable, not a failure. As soon as the main agent is satisfied with the revised text, the loop ends.

## The cycle within one iteration

1. Main agent sends the text plus the findings (and the prior dialogue when iterating).
2. Subagent reads, applies what it agrees with, pushes back on what it does not and produces a revised text plus comments.
3. Main agent reads the revised text and the subagent's comments. It either accepts the result (loop ends) or formulates the next round's questions.

The main agent has final decision authority. The subagent is a colleague, not a manager.

## Authority

The main agent applies the changes the dialogue settled on – accepting some, rejecting some, integrating some – and delivers the result via the output protocol.

## Reporting

No user-facing summary of the internal dialogue is produced. The user sees only the polished text and any output-protocol response. The subagent dialogue is internal scaffolding.

The one exception is when the subagent surfaces a finding that requires a developmental-editing decision the main agent cannot make alone – e.g., the text is structured as one content type but the material wants another. In that single case the main agent reports the issue to the user as a closing note and asks for a decision. This is the same last-resort finding described in the redline protocol, routed up through the subagent loop.
