# Baseline — version 0.5.5

> Generated on 2026-05-28 from `evals/workspace/<skill>/iteration-{1,2}/`
> for each of the four task skills against plugin version 0.5.5. Executor
> and grader subagents were Sonnet (`claude-sonnet-4-6`) per the run
> guardrail and the `_runner.py` `--model` default. The 60 cases unchanged
> in v0.5.5 carry their iteration-1 numbers (one run per configuration,
> the v0.5.4 baseline); the 28 cases that were authored or modified in
> v0.5.5 (paired protocol checks, negative controls, Phase 3 dialogue,
> case 404 rewrite) carry fresh iteration-2 numbers. Variance was not
> measured because each case ran once per configuration; the stddev cells
> below are blank by design. From this point on, regressions are measured
> against this baseline; any drop in the with-skill pass rate is a
> release blocker until investigated.

## Suite shape

| Dimension | Count |
|---|---|
| Total cases | 88 |
| Total assertions | 363 (with-skill and without-skill graded against the same set) |
| Skills covered | `/proofread`, `/redline`, `/edit`, `/write` |
| Languages covered | sv, en_GB, en_US, plus sv_FI (overlay fixture) and de (fallback fixture) |
| Required cases | 8 — fallback, overlay, fast-path-hit, fast-path-standard, max-iterations × 3, last-resort-floor |
| Negative-control cases | 5 — ids 19, 20, 21 (proofread), 119 (redline), 219 (edit) |
| Phase 3 dialogue cases | 3 — ids 409, 410, 411 (redline) |
| Cases per skill | proofread = 22, redline = 26, edit = 21, write = 19 |
| Cases per language per skill (sv / en_GB / en_US) | proofread: 7 / 7 / 7 — redline: 12 / 7 / 6 — edit: 8 / 7 / 6 — write: 7 / 6 / 6 |

The cases-per-language totals satisfy both contractual minima — ≥6 per skill in total, and ≥6 per language per skill for each language with a shipped `<lang>.md`.

## Per-skill pass rate

| Skill | With-skill pass rate | Without-skill pass rate | Delta |
|---|---|---|---|
| proofread | 93 / 93 (100 %) | 53 / 93 (57 %) | +43 pp |
| redline | 114 / 114 (100 %) | 52 / 114 (46 %) | +54 pp |
| edit | 82 / 82 (100 %) | 34 / 82 (42 %) | +59 pp |
| write | 74 / 74 (100 %) | 31 / 74 (42 %) | +58 pp |

## Per-language pass rate

| Language | With-skill pass rate | Without-skill pass rate | Delta |
|---|---|---|---|
| sv | 138 / 138 (100 %) | 53 / 138 (38 %) | +62 pp |
| en_GB | 104 / 104 (100 %) | 53 / 104 (51 %) | +49 pp |
| en_US | 112 / 112 (100 %) | 63 / 112 (56 %) | +44 pp |
| sv_FI (overlay) | 5 / 5 (100 %) | 1 / 5 (20 %) | +80 pp |
| de (fallback) | 4 / 4 (100 %) | 0 / 4 (0 %) | +100 pp |

## Per-required-case status

Each required case must pass every expectation in the with-skill configuration; the without-skill comparison shows the value the skill adds.

| Case | id | With-skill | Without-skill | Notes |
|---|---|---|---|---|
| fallback-default-mechanics-on-german-text | 401 | 4 / 4 | 0 / 4 | Fallback notice printed in the reply verbatim; baseline misses every protocol expectation. |
| overlay-loader-sv_FI-territorial-variant | 402 | 5 / 5 | 1 / 5 | Variant `Typography` H2 replaces base; others carried through. |
| fast-path-hit-short-unsignalled-sv-text | 403 | 4 / 4 | 0 / 4 | `_index.md` not read; commits to `general`. |
| fast-path-standard-flow-on-structured-article | 404 | 5 / 5 | 0 / 5 | Standard flow reads `_index.md` and `article.md`; the findings list cites an article-genre review-scoped rule, satisfying the observable form introduced in v0.5.5. |
| max-iterations-natural-language-redline | 405 | 4 / 4 | 0 / 4 | *en runda räcker* → 1; no-delegation branch ran. |
| max-iterations-natural-language-edit | 406 | 4 / 4 | 1 / 4 | *max två rundor* → 2, subagent invoked, early convergence at round 1. |
| max-iterations-natural-language-write | 407 | 4 / 4 | 1 / 4 | *iterera max tre gånger* → 3, no post-draft dialogue. |
| last-resort-floor-raises-to-one-when-flag-zero | 408 | 4 / 4 | 0 / 4 | Floor raised to 1 despite `--max-iterations=0`; observation delivered as closing note. |

All eight required cases pass every with-skill expectation.

## New v0.5.5 dimensions

### Negative-control cases (false-positive discipline)

Five cases supply clean text in each language and require that `/proofread`, `/redline`, or `/edit` produce no wall of false-positive findings on text that already follows the conventions.

| Case | id | Skill | Language | With-skill | Without-skill | Notes |
|---|---|---|---|---|---|---|
| sv-negative-clean-text | 19 | proofread | sv | 6 / 6 | 4 / 6 | No corrections applied; transcript notes the clean state. |
| en_GB-negative-clean-text | 20 | proofread | en_GB | 6 / 6 | 5 / 6 | Same shape; British conventions preserved. |
| en_US-negative-clean-text | 21 | proofread | en_US | 6 / 6 | 4 / 6 | Same shape; American conventions preserved. |
| sv-negative-clean-press-release | 119 | redline | sv | 5 / 5 | 0 / 5 | Press-release genre commits cleanly; one mechanical dash correction is the only edit. |
| en_GB-negative-clean-essay | 219 | edit | en_GB | 5 / 5 | 3 / 5 | Findings limited to genuine line-edit items; no spurious style rewrites. |

Aggregate: **28 / 28 with-skill (100 %) vs 16 / 28 without-skill (57 %)**, +43 pp.

The without-skill baseline does relatively well on output text here because the LLM tends not to invent corrections on clean text either — but it lacks the protocol fidelity (genre commit, scope record, layer name) the with-skill side records.

### Phase 3 dialogue cases (redline)

Three cases exercise the redline Phase 3 protocol (accept / reject / counter / delegate) by scripting user responses in the executor prompt. The executor simulates the dialogue in-transcript per `EXECUTOR_WITH_SKILL.md`'s subagent/dialogue convention; the grader reads the transcript for the documented branches.

| Case | id | Branch | With-skill | Without-skill |
|---|---|---|---|---|
| phase-3-dialogue-mixed-accept-reject-counter | 409 | Accept finding 1, reject finding 2 with rationale, counter finding 3 with an alternative the redline takes | 6 / 6 | 5 / 6 |
| phase-3-dialogue-delegate-with-max-iterations | 410 | Accept findings 1–2; delegate the open tail to `subagent.md` with `--max-iterations=2` from the flag | 5 / 5 | 2 / 5 |
| phase-3-dialogue-counter-defended | 411 | Counter finding 2; redline defends; user accepts the defence | 6 / 6 | 4 / 6 |

Aggregate: **17 / 17 with-skill (100 %) vs 11 / 17 without-skill (65 %)**, +35 pp.

Phase 3 fidelity is *simulated* in the same way `--max-iterations` is — the executor records the branches the protocol would take, the grader reads the transcript for evidence. End-to-end Phase 3 with an interactive user is not driven by the skill-creator runner (which uses one-shot `claude -p`); that limitation is documented in `evals/README.md` and treated as a known gap rather than a defect.

## With-skill vs. without-skill comparison

| Metric | with-skill | without-skill | Delta |
|---|---|---|---|
| Aggregate pass rate | 363 / 363 (100.0 %) | 170 / 363 (46.8 %) | +53.2 pp |
| Mean time per case | not measured | not measured | n/a |
| Mean tokens per case | not measured | not measured | n/a |
| Stddev pass rate | n/a (single run per configuration) | n/a | n/a |

Per-case timing and token use were not stored at run time. Variance was not measured because each case ran once per configuration; the user weighed the cost of repeat runs against the marginal information gain and chose single-pass for iteration-2 (matching iteration-1's methodology). The skill-creator pipeline can produce three-runs-per-configuration variance in a subsequent iteration if desired.

## Methodology notes

- **Hybrid iteration.** Sixty cases (the unchanged set from v0.5.4) carry their iteration-1 grades. Twenty-eight cases (paired protocol checks, negative controls, Phase 3 dialogue, case 404 rewrite) carry iteration-2 grades. Both passes used `claude-sonnet-4-6` and the same executor and grader prompts (`EXECUTOR_*.md`, `GRADER_BATCH.md`). The carry-over is sound because: (a) the executor prompt did not change between iterations, so the unchanged cases' output and grading would not differ on a re-run except by Sonnet's own non-determinism; (b) the new v0.5.5 assertions land on cases that *did* run in iteration-2, so the new dimensions reflect fresh measurement rather than imputation.
- **Orchestrator.** Iteration-2 was driven by `evals/workspace/_runner.py`, a headless orchestrator that fans out `claude -p` subprocesses with a per-job budget cap, parallelism, the resumable-skipping pattern (existing `output.md` / `grading.json` are not regenerated unless deleted), a `--case-ids` filter for partial sweeps, and a `--model` flag (default `claude-sonnet-4-6`). It cannot be run from inside a Claude Code session — nested `claude -p` strips auth and returns 401. Documented in the runner's own docstring.
- **Sonnet-tur dependency, addressed.** Several assertions written in v0.5.5 scaffolding were initially worded such that whether the grader marked PASS depended on whether Sonnet, on the run in question, used a specific phrase or path citation in its transcript. The cases involved (205, 211, 218; style-layer-pass evidence and body-text-stability evidence) were rewritten to enumerate the semantically valid evidence forms explicitly — file-path citation, layer-naming phrase, or category enumeration for style-layer; findings-traceability rather than literal "body text unchanged" for body stability. This addresses an observed flake where the same transcript graded PASS on one round and FAIL on another.

## Observations and follow-ups

- **Every with-skill cell is 100 %.** All four skills, all five languages, every required case, every negative-control case, and every Phase 3 dialogue case pass every expectation. The without-skill baseline scores 42–57 % per skill and 38–56 % per major language. The +53.2 pp aggregate delta on 363 assertions is a substantially stronger signal than v0.5.4's +49 pp on 66 assertions: a wider suite with more discriminating dimensions, and the plugin still passes everything.
- **Without-skill rate dropped (51 % → 47 %).** Not a regression — the new v0.5.5 dimensions (paired protocol checks, fallback notice form, negative-control discipline records, Phase 3 dialogue branches) are inherently harder for a baseline LLM to satisfy. The delta widened (+49 → +53 pp) because the with-skill side held at 100 % while the without-skill side dipped on the new harder assertions.
- **Sweden-Swedish remains the largest delta.** `sv` carries +62 pp because most of the protocol-semantic cases (genre resolution, fast-path, subagent ceiling, last-resort floor, Phase 3 dialogue) ride on Swedish fixtures. The English locales (`en_GB` +49 pp, `en_US` +44 pp) have smaller deltas because the baseline LLM already does most of the English typography corrections on its own. The fallback and overlay deltas are largest in absolute terms (de +100 pp, sv_FI +80 pp).
- **Iteration-2 single-run carries a discipline footnote, not a flaw.** Sonnet's executor output varies between runs (verbosity, choice of vocabulary in the transcript). The v0.5.5 assertions that survived two rounds of reformulation now name their evidence forms broadly enough that the grader does not depend on Sonnet writing a specific phrase. A future iteration with `--runs 3` would quantify residual variance; one isn't required for release certification because the assertion language was hardened in iteration-2 specifically to remove the brittleness.

## How to refresh this baseline

1. Re-run the pipeline per the *Running the suite* section in `evals/README.md` for each of the four skills, from a terminal where `claude` is authenticated (not from inside a Claude Code session). `uv run evals/workspace/_runner.py --iteration <N> --runs <R>` drives the full suite; `--skill <name>` and `--case-ids <list>` scope down for partial sweeps.
2. Aggregate the per-skill grading outputs and refresh the tables above.
3. Update the front-matter note with the new ISO date and the plugin version being baselined.
4. Commit the refreshed `baseline.md`. From that point on, regressions are measured against the new baseline; any drop in the with-skill pass rate is a release blocker until investigated.
