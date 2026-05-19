# Dialogue protocol

The settling procedure for a critical-review finding list when the user is in the loop. Each finding is presented to the user one at a time; the user decides what happens.

## Presentation format

One finding is presented at a time. Each finding has four parts, in this order:

1. **Marking.** A concrete pointer into the text — a short quote (the offending span as it appears in the text) or a structural reference ("the standfirst", "the third paragraph under the first H2", "the closing section"). The user must be able to find the location without searching.
2. **Problem.** What is wrong, expressed in one or two sentences, with explicit rule reference where one applies (the relevant section of the loaded style, content-type, technique, writing, or language file). When the finding rests on reader-experience consequence rather than a named rule, the consequence is named concretely.
3. **Solution.** A concrete proposal — the rewritten span, the restructured paragraph order, the new headline, the deleted word. The proposal is specific enough that "accept" applies it without further interpretation.
4. **Prompt.** A short closing line that invites one of the four response modes below. The agent does not enumerate the modes every time — the user knows them; a simple "What do you think?" or "Apply?" is enough.

Findings are presented one at a time, not in a wall-of-text list. The user responds, the agent moves on. See "Pacing" below for how to handle long finding lists.

## Response modes

When the agent presents a finding, the user can respond in four ways. The agent's behaviour for each is described below.

### (a) Accept

The user accepts the proposal. The agent applies the change. Acceptance can be expressed as "yes", "do it", "OK", "kör", "applicera", or any equivalent signal — or as a blanket "accept all" covering several open findings at once. A blanket acceptance is itself a position-taking and is honoured.

### (b) Reject

The user rejects the proposal. The agent drops it and moves on. Rejection can be expressed as "no", "skip it", "nej", "hoppa", "lämna det" — or by the user simply continuing past the finding without engaging with it. The agent does not press a rejected finding.

### (c) Counter-proposal or objection

The user pushes back — proposes a different change, objects to the agent's reasoning, suggests an alternative phrasing, or argues that the original is fine. The agent evaluates the user's counter against the loaded rule files and its own prior analysis.

If the agent has grounds to stand by its original proposal, it does so and defends with concrete arguments — citing the rule, the content-type expectation, or the substantive consequence. If the user's counter is stronger, the agent acknowledges and adopts it.

Tone: direct, substantive, not sycophantic, not stubborn for its own sake. The agent is a colleague, not a yes-machine and not a contrarian.

### (d) Delegate

The user signals that they have had enough dialogue and want the agent to decide — "just do it", "gör vad du tycker är bäst", "kör hårt", "do whatever". The agent stops asking and hands the remaining open findings to the subagent settling procedure, then delivers the polished text via the output protocol. No user-facing summary of the internal dialogue is produced — the user sees only the polished text.

Delegation can be partial — the user can say "just do the remaining ones" mid-flow. Findings already settled in dialogue stand; the open tail is delegated.

## Pacing

A long text produces many findings. The agent presents them in batches the user can engage with — not all findings at once. The batching is at the agent's discretion based on the text's length and the finding count.

Small, related findings can be grouped into a single presentation when grouping does not obscure the individual proposals — e.g., three anglicism substitutions in the same paragraph can share one marking and one combined solution if accepting one without the others is unlikely. The user can still reject parts of a grouped finding by saying which.

Findings the agent is highly confident about can be presented as confirmations to verify rather than as questions — "I'm replacing X with Y unless you object". Still one at a time, still per the four-part format, but with a lighter prompt.

The agent does not artificially inflate the finding list. Empty or trivial findings are dropped, not raised for show.
