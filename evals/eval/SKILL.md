---
name: eval
description: Maintainer-only eval-capture command. In-session, after a real /write, /edit or /redline session the maintainer is satisfied with, turn that session into a dimension-tagged eval case by propose-and-ratify. Lives entirely under evals/; never reads or modifies the skills under lib/. Activate only when the maintainer explicitly invokes /eval to capture the current session as an eval case. Do not activate on bare requests to evaluate, grade or review something.
---

# /eval — capture a session as an eval case

`/eval` turns a real worked-on session into a dimension-tagged eval case. Invoke
it in-session once you are satisfied with a `/write`, `/edit` or `/redline` run
and want its lessons pinned as a regression case. It proposes a candidate,
shows it for line-by-line ratification, and persists nothing until you commit.

This command is eval tooling, not part of the shipped plugin. It lives entirely
under `evals/` and never reads from, modifies, or adds any mechanism to the
skills under `lib/`. It is not auto-discovered or auto-invoked: run it only when
the maintainer asks for it by name.

## What it reads

The **session transcript** is the source. The maintainer's **running feedback**
during the session — the remarks naming what the pass missed or should have
done — is the primary fault source. The before/after **diff** between the
agent's output and the accepted result corroborates it. Nothing else is needed:
the case is derived from what actually happened, not re-invented.

For unit verification and as the wire format, a session is captured as a
transcript file (see `evals/fixtures/capture-transcript-edit.md` and
`-write.md` for the shape): a header naming `skill`, `language` and the invoked
`prompt`; a `## Maintainer feedback` section of quoted remarks; and a `## Diff`
fenced block. When run live in-session, assemble the same three pieces from the
conversation.

## Phase 1 — propose (writes nothing)

Run the deterministic proposer over the transcript:

```bash
uv run evals/capture.py <transcript.md>
```

It returns a candidate case as JSON without touching `evals.json` or any
per-skill file:

- a **brief** (for a `/write` case) or **input text** plus expected findings
  (for `/edit` / `/redline`);
- a list of **dimension-tagged assertions** (`register` for named faults,
  `mechanics` / `protocol` where applicable), each carrying the verbatim
  feedback remark it was **traced** to;
- all names (people, companies, products) already **anonymised** to
  `[Person N]` / `[Company N]` placeholders.

Assertion shape follows the skill. For `/edit` and `/redline` the assertions
are deterministic — *fault* is corrected to *target*, or the fault is flagged
and corrected. For `/write` they are negative or structural — a fresh draft
must not contain the fault, or the opening must reach substance by a named
sentence — because a write case grades a fresh draft, not a correction of an
input. The dimension on each assertion comes from
`evals/classify_dimensions.py`, the same classifier that tags the rest of the
suite, so a captured case is scored on the same footing as a hand-authored one.

## Phase 2 — ratify line by line

Present the candidate to the maintainer and settle it **one assertion at a
time**. For each assertion, the maintainer may **accept** it as proposed,
**edit** its text (re-classify the dimension with `classify_dimensions.classify`
if the edit changes the fault), or **reject** it (drop it from the case).
Confirm the proposed brief or input text and the case name the same way. Show
each assertion's traced feedback remark so the maintainer can judge whether the
assertion faithfully captures the fault.

Then take a **commit-or-skip** decision:

- **skip** — persist nothing. The session leaves no trace in the suite. This is
  the default when the maintainer is unsure the case is worth keeping.
- **commit** — append the ratified case to the suite.

## Phase 3 — commit (only after ratification)

On commit, append the case to the aggregated suite `evals/evals.json` in object
form (`{text, dimension}`, dropping the proposal-only `source` trace) under a
fresh id, and regenerate the per-skill `evals/<skill>/evals.json` files,
flattened to plain strings so they still validate against the stock
skill-creator schema. `capture.commit(case)` does both in one call:

```python
# After ratification, from evals/:
import capture
new_id = capture.commit(ratified_case)
```

Re-running the per-skill regeneration by hand is never needed: `commit` does it.
After committing, run the audit gate and the capture tests to confirm the suite
is still well-formed:

```bash
uv run scripts/audit.py
uv run evals/tests/test_capture.py
```

## What stays out of scope

Running real sessions, giving real register feedback, ratifying real cases, and
the publish-or-skip judgement are the maintainer's — `/eval` only mechanises the
propose, anonymise and commit steps around that judgement. The dimension schema
and the aggregator breakout belong to the suite (issue #44). No LLM-judge rubric
is involved.
