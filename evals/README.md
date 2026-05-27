# Eval suite

Test cases that exercise the four task skills — `/proofread`, `/redline`, `/edit`, `/write` — against the rules and protocols in `lib/`. The suite is wired to the [skill-creator](https://github.com/anthropics/skills/tree/main/skill-creator) pipeline.

## Layout

- `evals.json` — single aggregated suite. Every case carries `skill_name`, so it can be routed per skill while keeping one canonical list.
- `<skill>/evals.json` — per-skill files (`proofread`, `redline`, `edit`, `write`) generated from the aggregated file. Each matches the per-skill schema in `skill-creator/references/schemas.md`. Use these when the runner expects one `evals.json` per skill directory.
- `fixtures/` — committed input files referenced by `evals[].files`. Includes an overlay-loader fixture at `fixtures/lib/languages/sv_FI.md`.
- `baseline.md` — populated baseline for version 0.5.4 (generated 2026-05-28); 299 assertions, 100 % with-skill across every skill and language.
- `workspace/` — runner output (per-iteration directories, grading JSON, HTML viewer). Gitignored.

The aggregated `evals.json` is the source of truth. Regenerate the per-skill files when the aggregated file changes:

```bash
python3 -c "import json,pathlib;d=json.load(open('evals/evals.json'));[pathlib.Path(f'evals/{s}/evals.json').write_text(json.dumps({'skill_name':s,'evals':[e for e in d['evals'] if e['skill_name']==s]},indent=2,ensure_ascii=False)) for s in ('proofread','redline','edit','write')]"
```

## Running the suite

```bash
# 1. Run the skill-creator runner per skill (with-skill and baseline are launched together)
python -m scripts.run_loop --skill-path skills/<skill> --eval-set evals/<skill>/evals.json

# 2. Aggregate the iteration into a benchmark
python -m scripts.aggregate_benchmark evals/workspace/<skill>/iteration-1 --skill-name <skill>

# 3. Generate the static HTML viewer (no browser auto-open)
python <skill-creator-path>/eval-viewer/generate_review.py \
    evals/workspace/<skill>/iteration-1 \
    --skill-name <skill> \
    --benchmark evals/workspace/<skill>/iteration-1/benchmark.json \
    --static evals/workspace/<skill>/iteration-1/review.html
```

The runner needs access to `skill-creator` itself; install it from the Anthropic skill marketplace and call its scripts as above.

## Scaling rule for new languages

When a new `lib/languages/<lang>.md` lands, at least three cases per affected skill must land in the same commit. The audit script does not yet enforce this; treat the rule as a PR checklist item until it does.

## Assertions vs. qualitative review

Per-assertion checks (the `expectations` list on each case) cover only objectively verifiable outcomes — typography, spelling, quotation-mark form, genitive form, fast-path exit, max-iterations parsing, fallback messaging, overlay semantics. Subjective qualities (does the text sound natural, does the AI-tell stripping read well) are judged qualitatively via the skill-creator HTML viewer. Both layers are part of every iteration.

## Required test cases

The cases below exist by issue contract and other slices depend on them. Names are stable.

- `fallback-default-mechanics-on-german-text` — id 401, proofread, exercises the `default-mechanics.md` fallback and the fallback notice.
- `overlay-loader-sv_FI-territorial-variant` — id 402, redline, exercises the overlay loader (`inherits: "@sv.md"`) from slice #24.
- `fast-path-hit-short-unsignalled-sv-text` — id 403, redline, exercises the fast-path exit from slice #28.
- `fast-path-standard-flow-on-structured-article` — id 404, redline, the standard-flow counterpart from slice #28.
- `max-iterations-natural-language-redline` / `-edit` / `-write` — ids 405–407, exercise the natural-language parsing of `--max-iterations` per skill that has the flag.
- `last-resort-floor-raises-to-one-when-flag-zero` — id 408, edit, exercises the subagent floor raise when a developmental finding lands with the flag at 0.
