# Baseline — version 0.5.4

> Generated on 2026-05-28 from `evals/workspace/<skill>/iteration-1/` for each of the four task skills against plugin version 0.5.4. Executor and grader subagents were Sonnet (`claude-sonnet-4-6`) per the run guardrail. Each case was run once per configuration (with-skill and without-skill); variance across repeated runs was therefore not measured and the stddev cells below are blank by design. From this point on, regressions are measured against this baseline; any drop in the with-skill pass rate is a release blocker until investigated.

## Suite shape

| Dimension | Count |
|---|---|
| Total cases | 80 |
| Total assertions | 299 (with-skill and without-skill graded against the same set) |
| Skills covered | `/proofread`, `/redline`, `/edit`, `/write` |
| Languages covered | sv, en_GB, en_US, plus sv_FI (overlay fixture), de (fallback fixture) |
| Required cases | 8 — fallback, overlay, fast-path-hit, fast-path-standard, max-iterations × 3, last-resort-floor |
| Cases per skill | proofread = 19, redline = 22, edit = 20, write = 19 |
| Cases per language per skill (sv / en_GB / en_US) | proofread: 6 / 6 / 6 — redline: 9 / 6 / 6 — edit: 8 / 6 / 6 — write: 7 / 6 / 6 |

The cases-per-language totals satisfy both contractual minima — ≥6 per skill in total, and ≥6 per language per skill for each language with a shipped `<lang>.md`.

## Per-assertion pass rate

| Skill | With-skill pass rate | Without-skill pass rate | Delta |
|---|---|---|---|
| proofread | 66 / 66 (100%) | 47 / 66 (71%) | +29 pp |
| redline | 87 / 87 (100%) | 41 / 87 (47%) | +53 pp |
| edit | 72 / 72 (100%) | 33 / 72 (46%) | +54 pp |
| write | 74 / 74 (100%) | 31 / 74 (42%) | +58 pp |

## Per-language pass rate

| Language | With-skill pass rate | Without-skill pass rate | Delta |
|---|---|---|---|
| sv | 111 / 111 (100%) | 41 / 111 (37%) | +63 pp |
| en_GB | 85 / 85 (100%) | 49 / 85 (58%) | +42 pp |
| en_US | 94 / 94 (100%) | 61 / 94 (65%) | +35 pp |
| sv_FI (overlay) | 5 / 5 (100%) | 1 / 5 (20%) | +80 pp |
| de (fallback) | 4 / 4 (100%) | 0 / 4 (0%) | +100 pp |

## Per-required-case status

Each required case must pass every expectation in the with-skill configuration; the without-skill comparison shows the value the skill adds.

| Case | id | With-skill | Without-skill | Notes |
|---|---|---|---|---|
| fallback-default-mechanics-on-german-text | 401 | 4 / 4 | 0 / 4 | Fallback notice printed in the reply verbatim; baseline misses every protocol expectation. |
| overlay-loader-sv_FI-territorial-variant | 402 | 5 / 5 | 1 / 5 | Variant `Typography` H2 replaces base; others carried through. |
| fast-path-hit-short-unsignalled-sv-text | 403 | 4 / 4 | 0 / 4 | `_index.md` not read; commits to `general`. |
| fast-path-standard-flow-on-structured-article | 404 | 5 / 5 | 0 / 5 | Standard flow reads `_index.md` and `article.md`; output reflects article-genre review-scoped rules. |
| max-iterations-natural-language-redline | 405 | 4 / 4 | 0 / 4 | *en runda räcker* → 1 (transcript states ceiling N=1 would apply on delegation; no-delegation branch ran). |
| max-iterations-natural-language-edit | 406 | 4 / 4 | 1 / 4 | *max två rundor* → 2, subagent invoked, early convergence at round 1. |
| max-iterations-natural-language-write | 407 | 4 / 4 | 1 / 4 | *iterera max tre gånger* → 3, no post-draft dialogue. |
| last-resort-floor-raises-to-one-when-flag-zero | 408 | 4 / 4 | 0 / 4 | Floor raised to 1 despite `--max-iterations=0`; observation delivered as closing note. |

All eight required cases pass every with-skill expectation. Every skill is at 100 %; every language is at 100 %.

## With-skill vs. without-skill comparison

| Metric | with-skill | without-skill | Delta |
|---|---|---|---|
| Aggregate pass rate | 299 / 299 (100.0%) | 152 / 299 (50.8%) | +49.2 pp |
| Mean time per case | not measured | not measured | n/a |
| Mean tokens per case | not measured | not measured | n/a |
| Stddev pass rate | n/a (single run per configuration) | n/a | n/a |

Per-case timing and token use were not stored at run time, so the time / token rows are unfilled. Variance was not measured because each case ran once per configuration; the user weighed the cost of repeat runs against the marginal information gain and chose single-pass. The skill-creator pipeline can produce three-runs-per-configuration variance in a subsequent iteration if desired.

## Observations and follow-ups

- **Every with-skill cell is 100 %.** All four skills, all five languages, and every required case pass every expectation. The without-skill baseline scores 42–71 % per skill and 20–65 % per language, so the skill adds 29–58 percentage points per skill and 35–100 percentage points per language.
- **Test-design lessons baked into the suite.** The 0.5.4 baseline reaches 100 % because two earlier test-design weaknesses were fixed:
  - **Untestable invariants reworded (0.5.3).** Three assertions on the fast-path and natural-language-max-iterations cases described invariants or counterfactual paths that no single executor transcript can demonstrate. They were reworded to test what a single run actually produces — the protocol claim is preserved; only the framing changed.
  - **Fixtures extended to match assertion coverage (0.5.4).** Several assertions checked for properties (currency form, decimal separator, initialism handling, specific AI-tell terms, Oxford comma in a polished series) whose triggers were absent from the fixtures. Adding a single sentence to `en_GB-typography-errors.md`, `en_US-typography-errors.md`, and `en_US-style-errors.md` gave every assertion an observable target without contradicting any existing case.
  - **Conjunction-style assertions split into per-term checks (0.5.4).** Four assertions of the form "X, Y and Z are flagged" were split into per-term sub-assertions so future regressions surface the exact term that dropped, instead of "the conjunction did not fully pass". Assertion count rose from 290 to 299.
- **Sweden-Swedish is the largest with-skill / without-skill delta.** `sv` carries +63 pp because most of the protocol-semantic cases (genre resolution, fast-path, subagent ceiling, last-resort floor) ride on Swedish fixtures. The English locales (`en_GB` +42 pp, `en_US` +35 pp) have smaller deltas because the baseline LLM already does most of the English typography corrections on its own.
- **The fallback and overlay deltas are largest in absolute terms.** `de` (fallback to `default-mechanics.md`) goes from 0 % to 100 %, and `sv_FI` (overlay loader) goes from 20 % to 100 %. The language-resolution protocol is doing real work in the cases where the baseline LLM has no anchor.
- **Non-discriminating output-correctness assertions remain.** Several proofread / edit assertions that the baseline already satisfies on its own merits (Oxford comma corrections, British spelling drift, overlong-heading shortening, US quotation conventions) help confirm the skill does not regress on the easy cases, but they do not measure marginal skill value. Future iterations could pair such assertions with a protocol-semantic check to tighten the signal.
- **No flaky cases detected.** Variance was not measured (single-pass), but no case showed obvious model dependency in its transcript.

## How to refresh this baseline

1. Re-run the pipeline per the *Running the suite* section in `evals/README.md` for each of the four skills. The executor and grader scripts live under `evals/workspace/` (gitignored); the recipe is the same.
2. Aggregate the per-skill grading outputs and refresh the tables above.
3. Update the front-matter note with the new ISO date and the plugin version being baselined.
4. Commit the refreshed `baseline.md`. From that point on, regressions are measured against the new baseline; any drop in the with-skill pass rate is a release blocker until investigated.
