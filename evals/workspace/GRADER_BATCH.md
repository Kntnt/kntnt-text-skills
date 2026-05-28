# Grader (batched)

You are grading multiple test cases for the kntnt-text-skills plugin baseline. Each case in your prompt list has two configurations (`with_skill` and `without_skill`); you must produce a `grading.json` for each one — so a batch of N cases means 2N grading files.

## Inputs you receive in your prompt

A list of case directories. For each, both `with_skill/` and `without_skill/` are to be graded.

Structure on disk:
```
<case_dir>/
├── eval_metadata.json          ← case spec with assertions
├── with_skill/run-1/outputs/   ← {output.md, transcript.md, user_notes.md}
└── without_skill/run-1/outputs/← {output.md, transcript.md, user_notes.md}
```

## Steps per case-config

1. Read `<case_dir>/eval_metadata.json` — note `eval_id`, `eval_name`, `skill_name`, `language`, `prompt`, `expected_output`, and the `assertions` array.
2. Read the three output files in `<case_dir>/<config>/run-1/outputs/`.
3. For each assertion (in order), decide pass/fail and produce a short evidence string:
   - **Protocol-semantics assertions** (which files read, genre committed, fast-path vs. standard flow, fallback notice text, overlay applied, subagent ceiling, last-resort floor). Primary evidence: `transcript.md`. PASS only when the transcript shows the right path actually fired — a claim without a corresponding `## Files read` listing or `## Genre resolution` decision is FAIL.
   - **Output-correctness assertions** (typography, spelling, dash form, genitive form, fallback notice text verbatim, comma placement). Primary evidence: `output.md`. PASS when the rule is genuinely applied.
   - For `without_skill` configuration: assertions describing protocol behaviour will frequently FAIL — that is the point of the comparison. Do not lower the bar. Pass without-skill assertions only when the baseline output genuinely meets them on its own merits.
4. Write `<case_dir>/<config>/run-1/grading.json` with this exact shape:

```json
{
  "expectations": [
    {"text": "<assertion text, verbatim>", "passed": true, "evidence": "<short quote or summary citing transcript/output>"}
  ],
  "summary": {"passed": <int>, "failed": <int>, "total": <int>, "pass_rate": <float 0..1>}
}
```

`expectations[].text` must match the original assertion text verbatim. Include all assertions in order.

## Hard constraints

- Process every case-config in your list. Skipping is a bug.
- Write JSON files only; no commentary outside them.
- Do not modify any other files. The plugin under `skills/` and `lib/` is read-only.
- Be terse in `evidence` — one short sentence is enough; quote a phrase if it helps.
- Burden of proof for PASS is on the assertion. When ambiguous, FAIL with a one-line note.

When done, end your response with: `Graded N cases (2N grading.json files written).`
