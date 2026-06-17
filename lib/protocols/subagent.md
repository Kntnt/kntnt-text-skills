# Subagent protocol

The adversarial-review mechanic for settling editorial work without user-facing dialogue. A second agent, briefed to assume the text is AI-generated or translated, re-reads the result before delivery so register faults that survive the main agent's own pass are caught. The calling skill invokes this protocol when it has a critical-review finding list (or a draft and a finding list) and wants the polished result delivered directly – either because the skill is AFK by design, or because a parent dialogue has been delegated to internal settling, or because the skill produces new content and reviews it before delivery.

## Invocation conditions

The calling skill decides whether to invoke this protocol from the iteration ceiling it resolves:

- **`--max-iterations=N` flag (or natural-language equivalent) in the calling skill's invocation.** `N=1`, `=2`, `=3` set the ceiling on iterations for the current run; `N=0` opts out – the calling skill applies its redline findings directly and does not invoke this protocol. `N > 3` is clamped to 3. The calling skill is responsible for parsing the flag and the natural-language equivalents enumerated under *Natural-language parity* below, and passing the resulting ceiling into this protocol. Whether `N` defaults to 1 (one adversarial round) or to 0 (opt-out) is the calling skill's decision, stated in that skill; this protocol runs whatever positive ceiling it is handed.
- **Last-resort finding from the redline pass raises the floor to 1.** When the redline pass produces a developmental observation per `redline.md` (the text is structured as one content type but the material wants another, or is below the line-editing repair threshold), the calling skill raises the iteration floor to 1 – one round of subagent sanity-check – even if the resolved ceiling was 0. The closing note to the user about the last-resort decision is delivered after that round.

The iteration ceiling passed in is an upper bound, not a target. The convergence rules in *Iteration rules* below still apply – early termination is desirable, with the one floor that the adversarial register pass runs at least once before the loop can end.

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

## The subagent's stance

The subagent is an adversarial register reviewer: a demanding native-language editor who *assumes the text is AI-generated or translated* and reads every sentence asking whether it still gives that away. It applies the loaded language file's Smell Test and hunts the AI-tell constructions named in the loaded rule and language files – the patterns that survive an objective gate but still read as machine-made or translated prose. This is the stance the earlier collegial framing missed: a colleague who *wants the text to succeed* converges on cosmetic edits and signs off prose that still reads as translated, where an editor who assumes the worst about the text keeps probing.

The adversarial stance is toward the **text**, not toward the writer. The reviewer assumes the prose is guilty until it reads as natively written; it does not assume the writer is careless. Findings are delivered constructively – every one names the tell and proposes the native phrasing – exactly as the redline finding format requires. The register layer is where the reviewer is hardest; for the objective layers (mechanics, content-type integrity, technique arc) the redline protocol's *confidence and silence* still holds – a layer that holds up produces no finding.

It briefs in English (the plugin meta-language) and answers in the language of the text under review.

## Iteration rules

- Maximum three subagent calls per invocation. Three permitted, not three mandatory.
- The adversarial register pass runs at least once. "Satisfied" – the main agent's or the subagent's – may not end the loop before that pass has happened. A loop that started must produce at least one round in which the subagent has read the text under its adversarial register stance; only after that can satisfaction close it.
- Iteration n+1 happens only if both: (a) the main agent has a concrete unresolved question or specific objection to test; (b) the subagent did not, in round n, declare itself satisfied – subject to the floor above.
- A register finding is never dropped silently. The reviewer may dismiss one only with an explicit reason recorded in the dialogue (the phrasing is in fact idiomatic, the apparent tell is a deliberate quotation, etc.). Silent omission of a register finding is forbidden; for the objective layers, *confidence and silence* from the redline protocol still applies – a layer that holds up simply produces nothing.
- Calling the reviewer "just to be safe" beyond the first adversarial round is forbidden.
- Repetition without new content does not count as an iteration and may be aborted.
- Early termination is desirable once the adversarial floor is met. As soon as the main agent is satisfied with the revised text and the register pass has run, the loop ends.

## The cycle within one iteration

1. Main agent sends the text plus the findings (and the prior dialogue when iterating).
2. Subagent reads, applies what it agrees with, pushes back on what it does not and produces a revised text plus comments.
3. Main agent reads the revised text and the subagent's comments. It either accepts the result (loop ends) or formulates the next round's questions.

The main agent has final decision authority. The subagent reviews and proposes; it does not decide.

## Authority

The main agent applies the changes the dialogue settled on – accepting some, rejecting some, integrating some – and delivers the result via the output protocol.

## Reporting

No user-facing summary of the internal dialogue is produced. The user sees only the polished text and any output-protocol response. The subagent dialogue is internal scaffolding.

The one exception is when the subagent surfaces a finding that requires a developmental-editing decision the main agent cannot make alone – e.g., the text is structured as one content type but the material wants another. In that single case the main agent reports the issue to the user as a closing note and asks for a decision. This is the same last-resort finding described in the redline protocol, routed up through the subagent loop.
