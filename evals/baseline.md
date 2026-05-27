# Baseline — version 0.5.2

> Generated on 2026-05-28 from `evals/workspace/<skill>/iteration-1/` for each of the four task skills against plugin version 0.5.2. Executor and grader subagents were Sonnet (`claude-sonnet-4-6`) per the run guardrail. Each case was run once per configuration (with-skill and without-skill); variance across repeated runs was therefore not measured and the stddev cells below are blank by design. From this point on, regressions are measured against this baseline; any drop in the with-skill pass rate is a release blocker until investigated.

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

| Skill | With-skill pass rate | Without-skill pass rate | Delta |
|---|---|---|---|
| proofread | 59 / 64 (92%) | 39 / 64 (61%) | +31 pp |
| redline | 78 / 80 (98%) | 31 / 80 (39%) | +59 pp |
| edit | 71 / 72 (99%) | 31 / 72 (43%) | +56 pp |
| write | 74 / 74 (100%) | 31 / 74 (42%) | +58 pp |

## Per-language pass rate

| Language | With-skill pass rate | Without-skill pass rate | Delta |
|---|---|---|---|
| sv | 111 / 111 (100%) | 41 / 111 (37%) | +63 pp |
| en_GB | 82 / 84 (98%) | 45 / 84 (54%) | +44 pp |
| en_US | 80 / 86 (93%) | 45 / 86 (52%) | +41 pp |
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

All eight required cases pass every with-skill expectation. The baseline is committable.

During the run, three assertions on 403 / 404 / 405 were judged untestable from a single executor transcript (invariant or counterfactual claims) and were reworded in `evals/evals.json` to test what a single-run transcript can actually demonstrate. The reworded assertions preserve the original intent — that the fast-path is a downstream-rule dedup, and that subagent invocation is delegation-gated — but verify those properties via transcript content rather than via comparison runs. The original wording is preserved in git history.

## With-skill vs. without-skill comparison

| Metric | with-skill | without-skill | Delta |
|---|---|---|---|
| Aggregate pass rate | 282 / 290 (97.2%) | 132 / 290 (45.5%) | +51.7 pp |
| Mean time per case | not measured | not measured | n/a |
| Mean tokens per case | not measured | not measured | n/a |
| Stddev pass rate | n/a (single run per configuration) | n/a | n/a |

Per-case timing and token use were not stored at run time, so the time / token rows are unfilled. Variance was not measured because each case ran once per configuration; the user weighed the cost of repeat runs against the marginal information gain and chose single-pass. The skill-creator pipeline can produce three-runs-per-configuration variance in a subsequent iteration if desired.

## Observations and follow-ups

- **Skill value is broad and consistent.** With-skill pass rates are 92–100 % across all four skills and 93–100 % across all five languages. Without-skill pass rates land in the 37–61 % range — the skill adds 31–59 percentage points per skill and 41–100 percentage points per language. The biggest deltas are on the fallback language (`de`, +100 pp) and the overlay variant (`sv_FI`, +80 pp), confirming the language-resolution protocol is doing real work in cases where the baseline LLM has no anchor.
- **Sweden-Swedish is the discriminating workload.** `sv` carries the largest delta among the production languages (+63 pp) and is the only language where with-skill scores 100 %. Most of the protocol-semantic cases (genre resolution, fast-path, subagent ceiling, last-resort floor) ride on Swedish fixtures. The English locales (`en_GB`, `en_US`) have smaller deltas (+41 to +44 pp) because the baseline LLM already does most of the English typography corrections on its own — the discriminating signal is mechanics-layer breadth (Oxford comma, dash type, abbreviation full stops, etc.), not protocol structure.
- **Non-discriminating output-correctness assertions.** Several cases have output-correctness assertions that the without-skill baseline satisfies on its own merits — Oxford comma corrections (en_US), British spelling drift (en_GB), overlong-heading shortening, US quotation conventions. These assertions still belong in the suite because they confirm with-skill does the right thing too, but they do not measure the skill's marginal value. They are candidates for sharpening or pairing with a protocol-semantic check in a future iteration.
- **Protocol-semantic assertions are the load-bearing ones.** Genre commitment, fast-path vs. standard flow, language resolution and overlay loading, subagent ceiling and convergence, last-resort floor, fallback notice — these are where the with-skill / without-skill delta opens up. Every required case fails 3 or 4 of its expectations in the baseline configuration, confirming the skill is the only path to those behaviours.
- **Assertion design lesson learned.** Three assertions in 403 / 404 / 405 originally described invariants or counterfactual paths that cannot be verified from a single executor transcript. Graders correctly flagged this. The fix was to reword the assertions so they describe transcript content that a single run can demonstrate, without losing the underlying claim. Future test additions should prefer "the transcript states / the output shows" framings over "the output is identical to / without X, Y would happen" framings, unless the test is structured as a comparison run.
- **No flaky cases detected.** Variance was not measured (single-pass), but no case showed obvious model dependency in its transcript.

## How to refresh this baseline

1. Re-run the pipeline per the *Running the suite* section in `evals/README.md` for each of the four skills. The executor and grader scripts live under `evals/workspace/` (gitignored); the recipe is the same.
2. Aggregate the per-skill grading outputs and refresh the tables above.
3. Update the front-matter note with the new ISO date and the plugin version being baselined.
4. Commit the refreshed `baseline.md`. From that point on, regressions are measured against the new baseline; any drop in the with-skill pass rate is a release blocker until investigated.
