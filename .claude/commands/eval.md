---
description: Maintainer-only – capture the current /write, /edit or /redline session as a dimension-tagged eval case (propose → ratify → commit). Project-local wrapper over evals/eval/SKILL.md; not part of the shipped plugin.
argument-hint: [transcript.md]
disable-model-invocation: true
---

The maintainer invoked `/eval` to capture a worked-on session as a dimension-tagged eval case. Optional transcript file: `$ARGUMENTS`

This is a **thin project-local wrapper**. The full procedure is the single source of truth in [`evals/eval/SKILL.md`](evals/eval/SKILL.md). It exists only so the maintainer can invoke the eval-capture tool by name from inside this repository; it is **not** part of the shipped plugin and never reaches marketplace installs. Read that skill file now and follow it exactly.

It is maintainer-only eval tooling: it lives entirely under `evals/`, never reads from or modifies the skills under `lib/`, and writes nothing until the maintainer ratifies and commits.

Follow `evals/eval/SKILL.md`:

1. **Source.** If `$ARGUMENTS` names a transcript file, use it as the source. Otherwise assemble the transcript from **this** session — the header (`skill`, `language`, the invoked `prompt`), the maintainer's running feedback, and the before/after diff — exactly as the skill's *What it reads* section describes.
2. **Phase 1 – propose (writes nothing).** Run `uv run evals/capture.py <transcript>` and present the candidate case: brief or input text, the dimension-tagged assertions with their traced feedback, names already anonymised.
3. **Phase 2 – ratify line by line.** Settle every assertion (accept / edit / reject), confirm the brief or input text and the case name, eyeball for residual names, then take the commit-or-skip decision. Persist nothing before an explicit commit.
4. **Phase 3 – commit (only after ratification).** On commit, append via `capture.commit(...)`, then run `uv run scripts/audit.py` and `uv run evals/tests/test_capture.py` to confirm the suite is still well-formed.

Do not skip the ratification gate and do not write to `evals/evals.json` until the maintainer has committed.
