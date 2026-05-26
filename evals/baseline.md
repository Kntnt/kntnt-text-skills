# Baseline — version 0.3.0

> **This file is a baseline scaffold, not a real run.** Generated on 2026-05-27 (baseline-template; populate by running the pipeline). The author of slice #29 (`evals/` wired to skill-creator) could not invoke the skill-creator pipeline from the subagent context — no authenticated Claude API session, no SDK key, no way to spawn the executor and grader subagents the pipeline requires. The structural baseline below documents the slots a real run must fill. To replace this template with the real baseline, run the pipeline as described in `evals/README.md` and overwrite this file with the aggregated results.

## Suite shape

| Dimension | Count |
|---|---|
| Total cases | 80 |
| Skills covered | `/proofread`, `/redline`, `/edit`, `/write` |
| Languages covered | sv, en_GB, en_US, plus sv_FI (overlay fixture), de (fallback fixture) |
| Required cases | 8 — fallback, overlay, fast-path-hit, fast-path-standard, max-iterations × 3, last-resort-floor |
| Cases per skill | proofread = 19, redline = 22, edit = 20, write = 19 |
| Cases per language per skill (sv / en_GB / en_US) | proofread: 6 / 6 / 6 — redline: 9 / 6 / 6 — edit: 8 / 6 / 6 — write: 7 / 6 / 6 |

The cases-per-language totals satisfy both contractual minima — ≥6 per skill in total, and ≥6 per language per skill for each language with a shipped `<lang>.md`.

## Per-assertion pass rate

Populate after running the pipeline. The skill-creator runner emits per-iteration `grading.json` files with one row per expectation in the case. Aggregate the rows into the table below.

| Skill | With-skill pass rate | Without-skill pass rate | Delta |
|---|---|---|---|
| proofread | ___ / ___ ( __% ) | ___ / ___ ( __% ) | __ |
| redline | ___ / ___ ( __% ) | ___ / ___ ( __% ) | __ |
| edit | ___ / ___ ( __% ) | ___ / ___ ( __% ) | __ |
| write | ___ / ___ ( __% ) | ___ / ___ ( __% ) | __ |

## Per-language pass rate

| Language | With-skill pass rate | Without-skill pass rate | Delta |
|---|---|---|---|
| sv | ___ / ___ ( __% ) | ___ / ___ ( __% ) | __ |
| en_GB | ___ / ___ ( __% ) | ___ / ___ ( __% ) | __ |
| en_US | ___ / ___ ( __% ) | ___ / ___ ( __% ) | __ |
| sv_FI (overlay) | ___ / ___ ( __% ) | ___ / ___ ( __% ) | __ |
| de (fallback) | ___ / ___ ( __% ) | ___ / ___ ( __% ) | __ |

## Per-required-case status

Each required case must pass every expectation in the with-skill configuration; the without-skill comparison shows the value the skill adds.

| Case | id | With-skill | Without-skill | Notes |
|---|---|---|---|---|
| fallback-default-mechanics-on-german-text | 401 | __ / __ | __ / __ | Should print the fallback notice in the reply. |
| overlay-loader-sv_FI-territorial-variant | 402 | __ / __ | __ / __ | Variant `Typography` H2 replaces base; others carried through. |
| fast-path-hit-short-unsignalled-sv-text | 403 | __ / __ | __ / __ | `_index.md` not read; commits to `general`. |
| fast-path-standard-flow-on-structured-article | 404 | __ / __ | __ / __ | `_index.md` read; commits to `article`. |
| max-iterations-natural-language-redline | 405 | __ / __ | __ / __ | *en runda räcker* → 1. |
| max-iterations-natural-language-edit | 406 | __ / __ | __ / __ | *max två rundor* → 2. |
| max-iterations-natural-language-write | 407 | __ / __ | __ / __ | *iterera max tre gånger* → 3. |
| last-resort-floor-raises-to-one-when-flag-zero | 408 | __ / __ | __ / __ | Floor raises to 1 despite `--max-iterations=0`. |

## With-skill vs. without-skill comparison

| Metric | with-skill | without-skill | Delta |
|---|---|---|---|
| Aggregate pass rate | __% | __% | __ |
| Mean time per case | __ s | __ s | __ s |
| Mean tokens per case | __ | __ | __ |
| Stddev pass rate | __ | __ | __ |

## Observations and follow-ups

Populate from the analyst pass after the run completes. Cover at minimum:

- Assertions that pass at 100% in both configurations (non-discriminating — candidates for removal or sharpening).
- High-variance cases (potentially flaky or model-dependent).
- Time and token deltas (does the skill add material wall-clock cost?).
- Per-language gaps (any language where the with-skill pass rate is lower than the others — points at a missing or weak rule).
- Required-case regressions (any of the eight required cases failing — block the release).

## How to replace this template with a real baseline

1. Run the pipeline per the *Running the suite* section in `evals/README.md` for each of the four skills.
2. Aggregate the per-skill `benchmark.json` outputs into the tables above (totals, per-language, per-required-case).
3. Replace the front-matter note with: *Generated on `<ISO date>` from `evals/workspace/<skill>/iteration-1/benchmark.json` for each skill against plugin version 0.3.0.*
4. Commit the populated `baseline.md`. From that point on, regressions are measured against this baseline; any drop in the with-skill pass rate is a release blocker until investigated.
