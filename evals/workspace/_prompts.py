# /// script
# requires-python = ">=3.12"
# ///
"""Generate executor and grader prompts for the kntnt-text-skills eval run.

Emits the prompt body to stdout so the orchestrator can pipe it into a
Bash subprocess or paste it into an Agent() tool call. Supports any
iteration / run-number — the previous version hardcoded iteration-1 /
run-1, which made the variance pipeline impossible.
"""

from __future__ import annotations

import argparse
import json
import pathlib

REPO = pathlib.Path(__file__).resolve().parents[2]
SUITE = json.loads((REPO / "evals" / "evals.json").read_text())


def case_by_id(eid: int) -> dict:
    """Return the case dict with the given id; raise KeyError when none matches."""
    for c in SUITE["evals"]:
        if c["id"] == eid:
            return c
    raise KeyError(eid)


def case_dir(case: dict, iteration: int) -> pathlib.Path:
    """Workspace directory for one case under the given iteration."""
    return (
        REPO
        / "evals"
        / "workspace"
        / case["skill_name"]
        / f"iteration-{iteration}"
        / f"eval-{case['id']:03d}-{case['name']}"
    )


def with_skill_prompt(case: dict, iteration: int, run_n: int) -> str:
    """Build the with-skill executor prompt: run the case through its SKILL.md protocol."""
    skill_dir = REPO / "skills" / case["skill_name"]
    outputs_dir = case_dir(case, iteration) / "with_skill" / f"run-{run_n}" / "outputs"
    files_block = (
        "\n".join(f"- `{f}` (absolute: `{REPO / f}`)" for f in case.get("files", []))
        or "_(no input fixture files)_"
    )
    return f"""You are an executor running a single test case for the kntnt-text-skills plugin. \
The plugin lives at `{REPO}` and is READ-ONLY — do not modify anything under \
`skills/`, `lib/`, `evals/fixtures/`, or `evals/evals.json`. You may only write under the outputs directory below.

# Skill under test
- Skill name: `/{case["skill_name"]}`
- Skill spec: `{skill_dir / "SKILL.md"}`
- The spec is authoritative. Read it (and the `../../lib/...` files it references) and follow it literally. \
Treat the SKILL.md and its referenced lib files as the only source of truth for protocol behaviour.

# Case
- User prompt: `{case["prompt"]}`
- Input fixture file(s):
{files_block}
- For the redline case-402 overlay fixture (`evals/fixtures/lib/languages/sv_FI.md`), treat it as if it sat in `lib/languages/sv_FI.md` — that is the variant under test.

# How to execute
1. Read the skill spec and the lib files it references, in parallel where possible.
2. Read the fixture file(s). For non-fixture cases (no `files`), the prompt itself is the input — apply the skill to the prompt text.
3. Apply the skill protocol to the input. Be honest about which paths fired (fast-path vs. standard flow, fallback vs. specific match, which genre committed, which technique, which subagent ceiling).
4. For skills with a dialogue phase (`/redline`): default behaviour is to simulate Phase 3 silently — assume the user accepts every finding — and produce the polished final text. \
EXCEPTION: cases whose prompt scripts the user's dialogue responses (e.g., "I accept finding 1, reject finding 2, counter finding 3 with X") MUST follow those scripted responses literally. Record each finding's outcome in `## Phase log` (one row per finding with the response taken).
5. For cases that test the subagent loop (`--max-iterations` or natural-language equivalents), do NOT actually spawn a subagent; instead record in the transcript the ceiling value N that the protocol would pass, and what subagent.md would do with it. The transcript IS the evidence.
6. For `/write` cases that test technique resolution and subagent ceiling, a short draft (a paragraph or two) is enough — this run is about protocol fidelity, not length.

# Outputs (mandatory, all three files)
Write under: `{outputs_dir}`

1. `output.md` — the final delivered text (post-skill). For process-only cases where there is no transformed text to deliver, write a short note explaining that and put the substantive evidence in the transcript.
2. `transcript.md` — a structured markdown report with these sections (use exactly these H2 headings):
   - `## Files read` — full list, in the order you read them. Cite absolute paths.
   - `## Language resolution` — which language candidate, which file loaded (or fallback to `default-mechanics.md`), whether an overlay applied and what changed, and which scope (Mechanics-only for /proofread, Mechanics+Style for /redline /edit /write).
   - `## Genre / technique resolution` — (only for /redline, /edit, /write) which genre committed, fast-path vs. standard flow with the trigger that decided it, which technique loaded.
   - `## Phase log` — one short paragraph per phase that actually ran. For /redline Phase 3 with scripted responses, one row per finding: "Finding N — <ACCEPTED|REJECTED|COUNTER|DELEGATED> — <one-line outcome>".
   - `## Subagent ceiling` — (only when the skill has the `--max-iterations` mechanism) the N value, where it came from (flag, natural-language phrase, default, last-resort floor), and what subagent.md would do.
   - `## Fallback notice` — (only when no specific language file matched) the exact text that would be printed to the user, verbatim from `language-resolution.md`.
   - `## Findings` — (only for /redline / /edit) a bulleted list of the findings before settling. For each finding, cite the loaded file the finding is grounded in.
3. `user_notes.md` — anything you couldn't verify or want flagged. Empty file is fine.

# Hard constraints
- Write ONLY inside `{outputs_dir}`. Do not create the directory's parents or siblings.
- Do not modify any file outside that directory.
- Do not invoke other agents. You are the executor.
- Be concise. The transcript is for grading; one or two sentences per item beats a wall of text."""


def without_skill_prompt(case: dict, iteration: int, run_n: int) -> str:
    """Build the baseline executor prompt: handle the case by best judgment, with no skill."""
    outputs_dir = (
        case_dir(case, iteration) / "without_skill" / f"run-{run_n}" / "outputs"
    )
    files_block = (
        "\n".join(f"- `{REPO / f}`" for f in case.get("files", []))
        or "_(no input fixture files; prompt is the only input)_"
    )
    return f"""You are running a baseline for a single text-editing test case. \
There is no skill — apply your own best judgment to the prompt. \
You may read the fixture file(s) below to see the input; do NOT read anything else under `{REPO}`.

# Case
- User prompt: `{case["prompt"]}`
- Input fixture file(s):
{files_block}

# How to execute
1. If there are fixture file(s), read them. They are the user's input.
2. Interpret the prompt as a normal user request. (E.g. `/proofread sv` means "proofread this Swedish text"; `/redline` means "give me a critical editorial review"; `/write` means "draft this for me".)
3. Apply your best judgment — typography, style, structure, whatever you think serves the user.
4. There is no protocol to follow; record your process honestly in the transcript.

# Outputs (mandatory, all three files)
Write under: `{outputs_dir}`

1. `output.md` — the result you would deliver to the user.
2. `transcript.md` — a structured markdown report with these sections (use exactly these H2 headings):
   - `## Files read`
   - `## Approach` — what you did and why, in two or three sentences.
   - `## Findings` — (only if you'd flag anything) the issues or changes you'd raise.
   - `## Caveats` — any uncertainties; what a stricter style guide might add.
3. `user_notes.md` — anything you'd flag back to the user. Empty file is fine.

# Hard constraints
- Write ONLY inside `{outputs_dir}`.
- Do not read any other files under `{REPO}` outside the listed fixtures.
- Do not invoke other agents."""


def grader_prompt(case: dict, config: str, iteration: int, run_n: int) -> str:
    """Build the grader prompt that scores one configuration's outputs against the case's expectations."""
    run_dir = case_dir(case, iteration) / config / f"run-{run_n}"
    outputs_dir = run_dir / "outputs"
    grading_path = run_dir / "grading.json"
    # Expectations are object-form `{text, dimension}` in the suite; the grader
    # grades the plain assertion text, so flatten to the text here exactly as
    # `_setup.py` does for the runner path. A still-flat suite (bare strings)
    # degrades gracefully — the text is the string itself.
    expectations = case.get("expectations", [])
    expectation_texts = [
        e["text"] if isinstance(e, dict) else e for e in expectations
    ]
    exp_block = "\n".join(
        f"  {i + 1}. {text}" for i, text in enumerate(expectation_texts)
    )
    return f"""You are grading one configuration of one test case for the kntnt-text-skills plugin.

# Case
- id: {case["id"]}
- name: `{case["name"]}`
- skill: `/{case["skill_name"]}`
- configuration: `{config}`
- run: {run_n} of N
- prompt: `{case["prompt"]}`
- expected outcome: {case.get("expected_output", "")}

# Expectations to grade
{exp_block}

# Inputs
- Outputs directory: `{outputs_dir}`
  - `output.md` — the final text the executor produced
  - `transcript.md` — the executor's process narrative
  - `user_notes.md` — optional executor notes
- For the `with_skill` configuration the executor was instructed to record process explicitly in the transcript (which files read, which genre committed, fast-path vs. standard flow, fallback notice, subagent ceiling, etc.). The transcript is primary evidence for protocol-semantics expectations; `output.md` is primary evidence for output-correctness expectations.

# Grading rules
- For each expectation, return `passed: true/false` plus an `evidence` field that quotes or summarises what supports the verdict.
- PASS only when the evidence is genuine, not surface compliance. A transcript that *claims* "fast-path exited" without the corresponding `## Files read` list reflecting it is FAIL.
- For the `without_skill` configuration: treat the expectation as a target the baseline run is being measured against. Be honest — without the skill, many protocol expectations will fail. That is the point of the comparison. Do not lower the bar.
- When evidence is ambiguous, the burden of proof is on the expectation: mark it FAIL with a note.

# Output
Write JSON to: `{grading_path}`

Exact shape:
```json
{{
  "expectations": [
    {{"text": "<expectation 1>", "passed": <bool>, "evidence": "<quote or summary>"}}
  ],
  "summary": {{"passed": <int>, "failed": <int>, "total": <int>, "pass_rate": <float 0..1>}}
}}
```

The `expectations[].text` must match the original expectation text verbatim. Include all {len(expectations)} expectations in order. Do not add commentary outside the JSON file."""


def main() -> None:
    """Parse CLI args and print the requested executor or grader prompt to stdout."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "cmd", choices=("with", "without", "grade-with", "grade-without")
    )
    parser.add_argument("eval_id", type=int)
    parser.add_argument("--iteration", type=int, default=2)
    parser.add_argument("--run", type=int, default=1)
    args = parser.parse_args()

    case = case_by_id(args.eval_id)
    if args.cmd == "with":
        print(with_skill_prompt(case, args.iteration, args.run))
    elif args.cmd == "without":
        print(without_skill_prompt(case, args.iteration, args.run))
    elif args.cmd == "grade-with":
        print(grader_prompt(case, "with_skill", args.iteration, args.run))
    elif args.cmd == "grade-without":
        print(grader_prompt(case, "without_skill", args.iteration, args.run))


if __name__ == "__main__":
    main()
