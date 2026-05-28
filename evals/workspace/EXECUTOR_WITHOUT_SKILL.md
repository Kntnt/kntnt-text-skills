# Executor — without-skill baseline

You are running a baseline for a single text-editing test case. There is no skill — apply your own best judgment.

The case spec is in `eval_metadata_blind.json` next to your `outputs/` directory:

```
<case_dir>/
├── eval_metadata_blind.json      ← read this (NOT eval_metadata.json — that one carries assertions you must not see)
├── with_skill/...
└── without_skill/run-1/outputs/  ← write your three files here (this run)
```

Read `eval_metadata_blind.json` to obtain `prompt`, `files`, and `language`. Do NOT read `eval_metadata.json` — that file contains the grading assertions and would contaminate the baseline.

You may read the fixture file(s) listed in `files`. Do NOT read anything else under `/Users/thomas/Desktop/kntnt-text-skills/` — in particular, do not look at `skills/`, `lib/`, `evals/evals.json`, or other workspace cases. The plugin is hidden from you on purpose.

## How to execute

1. If there are fixtures, read them — they are the user's input.
2. Interpret the prompt as a normal user request. `/proofread sv` means "proofread this Swedish text"; `/redline` means "give me a critical editorial review"; `/edit` means "edit this for me"; `/write` means "draft this for me".
3. Apply your best judgment — typography, style, structure, whatever you think serves the user.
4. There is no protocol to follow; record your process honestly.

## Mandatory outputs

Write inside the `outputs/` directory in your prompt:

1. `output.md` — the result you would deliver to the user.
2. `transcript.md` — structured markdown with these H2 sections:
   - `## Files read`
   - `## Approach` — what you did and why, in two or three sentences.
   - `## Findings` — *(if you'd flag anything)* the issues or changes you'd raise.
   - `## Caveats` — uncertainties; what a stricter style guide might add.
3. `user_notes.md` — anything you'd flag back to the user. Empty file is acceptable.

## Hard constraints

- Write ONLY inside `outputs/`.
- Do not read other files under `/Users/thomas/Desktop/kntnt-text-skills/` outside the listed fixtures and `eval_metadata.json`.
- Do not invoke sub-subagents.
