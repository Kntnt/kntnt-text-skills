# Dialogue protocol

The settling procedure for a critical-review finding list when the user is in the loop. Each finding is presented to the user one at a time; the user decides what happens.

## Presentation format

One finding is presented at a time, in the four-part format defined by the calling skill's redline pass. The fourth part — the prompt — is a short closing line that invites one of the four response modes below; the agent does not enumerate the modes every time, since the user knows them, and a simple "What do you think?" or "Apply?" is enough.

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

The user signals that they have had enough dialogue and want the agent to decide — "just do it", "gör vad du tycker är bäst", "kör hårt", "do whatever". The agent stops asking and settles the remaining open findings directly, then delivers the polished text via the output protocol. No user-facing summary of any internal work is produced — the user sees only the polished text.

The behaviour on delegation depends on the calling skill's `--max-iterations=N` flag (or its natural-language equivalent):

- **Without the flag (default `N=0`).** The main agent applies the remaining findings directly to the text — no subagent round.
- **With the flag set to `1`, `2`, or `3`.** The main agent invokes `subagent.md` with that ceiling on iterations. Convergence rules in `subagent.md` still apply.
- **Last-resort finding present in the remaining tail.** The floor is raised to 1 even when the flag is 0 — one subagent round to sanity-check before the closing note reaches the user.

Delegation can be partial — the user can say "just do the remaining ones" mid-flow. Findings already settled in dialogue stand; the open tail is delegated under the rules above.

## Pacing

A long text produces many findings. The agent presents them in batches the user can engage with — not all findings at once. The batching is at the agent's discretion based on the text's length and the finding count.

Small, related findings can be grouped into a single presentation when grouping does not obscure the individual proposals — e.g., three anglicism substitutions in the same paragraph can share one marking and one combined solution if accepting one without the others is unlikely. The user can still reject parts of a grouped finding by saying which.

Findings the agent is highly confident about can be presented as confirmations to verify rather than as questions — "I'm replacing X with Y unless you object". Still one at a time, still per the four-part format, but with a lighter prompt.

The agent does not artificially inflate the finding list. Empty or trivial findings are dropped, not raised for show.
