# Executor — with-skill configuration

You are running a single test case for the kntnt-text-skills plugin. The plugin lives at `/Users/thomas/Desktop/kntnt-text-skills/` and is READ-ONLY — do not modify anything under `skills/`, `lib/`, `evals/fixtures/`, or `evals/evals.json`. You may only write inside the `outputs/` directory listed in your prompt.

The case spec is in `eval_metadata.json` next to your `outputs/` directory:

```
<case_dir>/
├── eval_metadata.json          ← read this
├── with_skill/run-1/outputs/   ← write your three files here (this run)
└── without_skill/...
```

Read `eval_metadata.json` to obtain: `eval_id`, `eval_name`, `skill_name`, `language`, `prompt`, `files` (list of fixture paths relative to the plugin root), and `assertions` (the expectations the grader will check — read these so you know what evidence to record).

## How to execute

1. Read the skill spec at `/Users/thomas/Desktop/kntnt-text-skills/skills/<skill_name>/SKILL.md`. Then read the `../../lib/...` files it references — in parallel batches where the spec says to.
2. Read the fixture file(s) listed in `files`. If `files` is empty, the user prompt itself is the input.
3. Apply the skill's protocol literally. Be honest about which paths fired — fast-path vs. standard flow, specific-match vs. fallback, which genre committed and on what trigger, which technique loaded, what `--max-iterations` ceiling N would be passed to subagent.md.
4. For `/redline`: simulate Phase 3 silently — assume the user accepts every finding — and produce the polished final text.
5. For cases that test the subagent loop (`--max-iterations` flag or natural-language equivalent): do NOT actually spawn a subagent. Record in the transcript the ceiling value N the protocol would pass and what subagent.md says it would do with it. The transcript IS the evidence.
6. For `/write` cases: a short draft (a paragraph or two) is enough — this run measures protocol fidelity, not length.
7. **Case 402 overlay quirk.** The fixture `evals/fixtures/lib/languages/sv_FI.md` is to be treated as if it lived at `lib/languages/sv_FI.md`. That is the variant under test for the overlay loader.

## Mandatory outputs

Write all three files inside the `outputs/` directory in your prompt:

1. `output.md` — the final delivered text (post-skill). For process-only cases with no transformed text, write a short explanatory note and put the substantive evidence in the transcript.
2. `transcript.md` — structured markdown with these H2 sections (omit a section only when it does not apply; do not invent extra ones):
   - `## Files read` — full list of paths you read, in order.
   - `## Language resolution` — candidate language, which file loaded (or fallback), overlay applied? what changed?
   - `## Genre / technique resolution` — *(/redline, /edit, /write only)* committed genre, fast-path vs. standard flow with the trigger that decided it, technique loaded.
   - `## Phase log` — one short paragraph per phase that ran.
   - `## Subagent ceiling` — *(when the skill has `--max-iterations`)* value of N, source (flag / natural-language phrase / default / last-resort floor), what subagent.md would do.
   - `## Fallback notice` — *(when no specific language file matched)* the exact text printed to the user, verbatim from `language-resolution.md`.
   - `## Findings` — *(/redline, /edit only)* bulleted list of findings before settling.
3. `user_notes.md` — anything you couldn't verify or want flagged. Empty file is acceptable.

## Hard constraints

- Write ONLY inside `outputs/`. Do not create siblings.
- Do not modify anything outside `outputs/`.
- Do not invoke sub-subagents. You are the executor; the dialogue phase and any "delegate to subagent" steps are SIMULATED in the transcript, not actually executed.
- Be concise. Transcripts are for grading; one or two sentences per item beats a wall of text.

The expectations array in `eval_metadata.json` tells you exactly what the grader will look for — make sure your transcript provides the evidence each one needs.
