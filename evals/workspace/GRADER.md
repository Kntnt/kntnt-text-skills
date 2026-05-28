# Grader

You are grading one configuration of one test case for the kntnt-text-skills plugin baseline.

## Inputs you receive in your prompt

- `case_dir` — directory containing `eval_metadata.json` and per-config `outputs/`
- `config` — either `with_skill` or `without_skill`
- The run directory is `<case_dir>/<config>/run-1/`; outputs sit at `<case_dir>/<config>/run-1/outputs/`.

## Steps

1. Read `<case_dir>/eval_metadata.json` for the case spec — `eval_id`, `eval_name`, `skill_name`, `language`, `prompt`, `expected_output`, and the `assertions` array (the expectations you are grading).
2. Read the three output files:
   - `<case_dir>/<config>/run-1/outputs/output.md`
   - `<case_dir>/<config>/run-1/outputs/transcript.md`
   - `<case_dir>/<config>/run-1/outputs/user_notes.md`
3. For protocol-semantics expectations (which files read, which genre committed, fast-path vs. standard flow, fallback notice text, overlay applied, subagent ceiling, last-resort floor), the `transcript.md` is your primary evidence source — it documents which paths actually fired.
4. For output-correctness expectations (typography, spelling, genitive form, dash type, etc.), `output.md` is your primary evidence source.
5. Read the fixture file(s) referenced under `files` ONLY if you need to verify that a transformation actually happened (e.g., the input contained `Marx's teorier` and the output contains `Marx teorier`). Do not read the plugin source under `skills/` or `lib/`.

## Grading rules

- PASS only when evidence is genuine. A claim in the transcript without corroboration (e.g., "fast-path fired" without `## Files read` showing `_index.md` was NOT read) is FAIL.
- For the `without_skill` configuration, expectations targeting protocol behaviours will frequently fail — that is the whole point of the comparison. Do NOT lower the bar; the baseline must be measured honestly. Pass without-skill expectations only when the baseline output genuinely satisfies them on its own merits.
- When evidence is ambiguous, the burden of proof is on the expectation: mark FAIL with a short note.

## Output

Write JSON to `<case_dir>/<config>/run-1/grading.json`. Exact shape:

```json
{
  "expectations": [
    {"text": "<assertion text, verbatim>", "passed": true, "evidence": "<short quote or summary citing transcript/output>"}
  ],
  "summary": {"passed": <int>, "failed": <int>, "total": <int>, "pass_rate": <float 0..1>}
}
```

The `expectations[].text` must match the original assertion text verbatim. Include all assertions in order. Write no commentary outside the JSON file.
