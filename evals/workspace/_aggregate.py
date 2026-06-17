# /// script
# requires-python = ">=3.12"
# ///
"""Aggregate grading.json files into baseline tables with variance.

Reads all `run-N/grading.json` files under `iteration-<N>/` for each case
and configuration, computes pass-rate mean ± stddev across the runs, and
prints a markdown report suitable for inserting into `baseline.md`.

Iteration and runs can be selected via flags; defaults pick the natural
post-v0.5.5 layout (iteration-2 with 3 runs).
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys
from collections import defaultdict
from statistics import mean, stdev

# Default repository root, resolved from this file's location. The suite and
# workspace are read relative to it at run time (overridable via --repo) so the
# module imports without touching the filesystem.
REPO = pathlib.Path(__file__).resolve().parents[2]

# The three scoring dimensions split into two reported numbers: the hard
# release gate pools protocol and mechanics; register is the tracked
# improvement target, reported separately with its assertion count.
GATE_DIMENSIONS = ("protocol", "mechanics")
REGISTER_DIMENSION = "register"


def build_dim_by_text(suite: dict) -> dict[str, str]:
    """Map each assertion's verbatim text to its dimension from the suite file.

    The grader prompt grades a flat list of strings and writes each result
    back under the same verbatim `text`, so re-joining the dimension by text
    is exact. Flat-string assertions (an un-migrated suite) carry no
    dimension and are skipped, which leaves them out of the sub-scores rather
    than guessing.
    """
    dim_by_text: dict[str, str] = {}
    for case in suite["evals"]:
        for exp in case["expectations"]:
            if isinstance(exp, dict) and "dimension" in exp:
                dim_by_text[exp["text"]] = exp["dimension"]
    return dim_by_text


def split_by_dimension(
    graded: list[dict], dim_by_text: dict[str, str]
) -> dict[str, dict[str, int]]:
    """Tally graded assertions into `{dimension: {passed, total}}` by text.

    `graded` is a flat list of grading.json expectation entries (`text`,
    `passed`); `dim_by_text` joins each back to its dimension. Assertions
    whose text is not in the map are ignored so a stray grading entry cannot
    distort a sub-score.
    """
    by_dim: dict[str, dict[str, int]] = defaultdict(lambda: {"passed": 0, "total": 0})
    for entry in graded:
        dimension = dim_by_text.get(entry["text"])
        if dimension is None:
            continue
        by_dim[dimension]["total"] += 1
        if entry["passed"]:
            by_dim[dimension]["passed"] += 1
    return dict(by_dim)


def gate_score(by_dim: dict[str, dict[str, int]]) -> dict[str, int]:
    """Pool the hard-gate dimensions (protocol + mechanics) into one count."""
    passed = sum(by_dim.get(d, {}).get("passed", 0) for d in GATE_DIMENSIONS)
    total = sum(by_dim.get(d, {}).get("total", 0) for d in GATE_DIMENSIONS)
    return {"passed": passed, "total": total}


def register_score(by_dim: dict[str, dict[str, int]]) -> dict[str, int]:
    """Return the register sub-score and its n, the improvement target."""
    register = by_dim.get(REGISTER_DIMENSION, {"passed": 0, "total": 0})
    return {"passed": register["passed"], "total": register["total"]}


def collect_records(iteration: int, runs: int, ws: pathlib.Path, suite: dict) -> list[dict]:
    """Read every run's grading.json into a list of records.

    Alongside the per-run pass-rate summary, each record carries the flat
    list of graded `{text, passed}` expectation entries so the dimension
    breakout can be tallied downstream without re-reading the files.
    """
    records = []
    for case in suite["evals"]:
        base = (
            ws
            / case["skill_name"]
            / f"iteration-{iteration}"
            / f"eval-{case['id']:03d}-{case['name']}"
        )
        for cfg in ("with_skill", "without_skill"):
            run_rates = []
            run_passed = []
            run_total = []
            graded: list[dict] = []
            for run_n in range(1, runs + 1):
                g_path = base / cfg / f"run-{run_n}" / "grading.json"
                if not g_path.exists():
                    continue
                g = json.loads(g_path.read_text())
                summ = g["summary"]
                run_passed.append(summ["passed"])
                run_total.append(summ["total"])
                run_rates.append(summ["pass_rate"])
                graded.extend(g.get("expectations", []))
            if not run_rates:
                continue
            records.append(
                {
                    "id": case["id"],
                    "name": case["name"],
                    "skill": case["skill_name"],
                    "language": case["language"],
                    "config": cfg,
                    "n_runs": len(run_rates),
                    "passed_total": sum(run_passed),
                    "total_total": sum(run_total),
                    "mean_rate": mean(run_rates),
                    "stddev_rate": stdev(run_rates) if len(run_rates) > 1 else 0.0,
                    "graded": graded,
                }
            )
    return records


def fmt_rate(passed: int, total: int) -> str:
    """Format a pass count as `passed / total (pct%)`."""
    pct = round(100 * passed / total) if total else 0
    return f"{passed} / {total} ({pct}%)"


def fmt_mean_stddev(records: list[dict]) -> str:
    """Mean ± stddev of per-case pass rates, weighted equally per case."""
    rates = [r["mean_rate"] for r in records]
    sds = [r["stddev_rate"] for r in records]
    if not rates:
        return "n/a"
    m = mean(rates)
    # Pooled stddev across cases — simple average of per-case stddevs (a
    # rough but informative proxy; not a formal pooled variance).
    pooled = mean(sds) if any(s > 0 for s in sds) else 0.0
    return f"{m * 100:.1f}% ± {pooled * 100:.1f}pp"


def write_per_skill(records: list[dict], out: list[str]) -> None:
    """Append the per-skill pass-rate table (with-skill vs. without-skill, plus delta) to `out`."""
    out.append("\n## Per-skill")
    out.append("| Skill | With-skill | Without-skill | Delta |")
    out.append("|---|---|---|---|")
    by_skill = defaultdict(lambda: {"w": [], "wo": []})
    for r in records:
        side = "w" if r["config"] == "with_skill" else "wo"
        by_skill[r["skill"]][side].append(r)
    for skill in ("proofread", "redline", "edit", "write"):
        if skill not in by_skill:
            continue
        w_recs = by_skill[skill]["w"]
        wo_recs = by_skill[skill]["wo"]
        w_passed = sum(r["passed_total"] for r in w_recs)
        w_total = sum(r["total_total"] for r in w_recs)
        wo_passed = sum(r["passed_total"] for r in wo_recs)
        wo_total = sum(r["total_total"] for r in wo_recs)
        delta = (
            100 * w_passed / w_total - 100 * wo_passed / wo_total
            if (w_total and wo_total)
            else 0
        )
        out.append(
            f"| {skill} | {fmt_rate(w_passed, w_total)} "
            f"({fmt_mean_stddev(w_recs)}) | "
            f"{fmt_rate(wo_passed, wo_total)} "
            f"({fmt_mean_stddev(wo_recs)}) | {delta:+.0f} pp |"
        )


def write_dimension_breakout(
    records: list[dict], dim_by_text: dict[str, str], out: list[str]
) -> None:
    """Append the two-sub-score breakout (hard gate vs. register) to `out`.

    Only the with-skill configuration is scored here — the split exists to
    separate the protocol/mechanics release gate from the register
    improvement target on the side the skill drives. Each skill row and the
    overall row carry the pooled gate score and the register score with its
    assertion count (its n), so a register value below 100 % reads as a
    tracked target rather than a blocker.
    """
    out.append("\n## Sub-score breakout (with-skill)")
    out.append(
        "Protocol/mechanics is the hard release gate (any regression blocks). "
        "Register is a tracked improvement target — reported with its n, where "
        "only a regression against the prior register baseline is flagged."
    )
    out.append("\n| Skill | Protocol/mechanics gate | Register (improvement) |")
    out.append("|---|---|---|")
    by_skill = defaultdict(list)
    for r in records:
        if r["config"] == "with_skill":
            by_skill[r["skill"]].append(r)
    overall_graded: list[dict] = []
    for skill in ("proofread", "redline", "edit", "write"):
        if skill not in by_skill:
            continue
        graded = [e for r in by_skill[skill] for e in r["graded"]]
        overall_graded.extend(graded)
        by_dim = split_by_dimension(graded, dim_by_text)
        gate = gate_score(by_dim)
        register = register_score(by_dim)
        out.append(
            f"| {skill} | {fmt_rate(gate['passed'], gate['total'])} | "
            f"{fmt_register(register)} |"
        )
    overall_by_dim = split_by_dimension(overall_graded, dim_by_text)
    overall_gate = gate_score(overall_by_dim)
    overall_register = register_score(overall_by_dim)
    out.append(
        f"| **overall** | "
        f"**{fmt_rate(overall_gate['passed'], overall_gate['total'])}** | "
        f"**{fmt_register(overall_register)}** |"
    )


def fmt_register(register: dict[str, int]) -> str:
    """Format the register sub-score as `passed / n (pct%)`, carrying its n explicitly."""
    n = register["total"]
    if not n:
        return "n/a (n=0)"
    pct = round(100 * register["passed"] / n)
    return f"{register['passed']} / {n} ({pct}%, n={n})"


def write_per_language(records: list[dict], out: list[str]) -> None:
    """Append the per-language pass-rate table to `out`."""
    out.append("\n## Per-language")
    out.append("| Language | With-skill | Without-skill | Delta |")
    out.append("|---|---|---|---|")
    by_lang = defaultdict(lambda: {"w": [], "wo": []})
    for r in records:
        side = "w" if r["config"] == "with_skill" else "wo"
        by_lang[r["language"]][side].append(r)
    for lang in ("sv", "en_GB", "en_US", "sv_FI", "de"):
        if lang not in by_lang:
            continue
        w_recs = by_lang[lang]["w"]
        wo_recs = by_lang[lang]["wo"]
        w_passed = sum(r["passed_total"] for r in w_recs)
        w_total = sum(r["total_total"] for r in w_recs)
        wo_passed = sum(r["passed_total"] for r in wo_recs)
        wo_total = sum(r["total_total"] for r in wo_recs)
        delta = (
            100 * w_passed / w_total - 100 * wo_passed / wo_total
            if (w_total and wo_total)
            else 0
        )
        label = (
            lang
            if lang not in ("sv_FI", "de")
            else f"{lang} ({'overlay' if lang == 'sv_FI' else 'fallback'})"
        )
        out.append(
            f"| {label} | {fmt_rate(w_passed, w_total)} "
            f"({fmt_mean_stddev(w_recs)}) | "
            f"{fmt_rate(wo_passed, wo_total)} "
            f"({fmt_mean_stddev(wo_recs)}) | {delta:+.0f} pp |"
        )


def write_required_cases(records: list[dict], out: list[str]) -> None:
    """Append the status table for the contract-required cases to `out`."""
    required = {
        401: "fallback-default-mechanics-on-german-text",
        402: "overlay-loader-sv_FI-territorial-variant",
        403: "fast-path-hit-short-unsignalled-sv-text",
        404: "fast-path-standard-flow-on-structured-article",
        405: "max-iterations-natural-language-redline",
        406: "max-iterations-natural-language-edit",
        407: "max-iterations-natural-language-write",
        408: "last-resort-floor-raises-to-one-when-flag-zero",
        409: "phase-3-dialogue-mixed-accept-reject-counter",
        410: "phase-3-dialogue-delegate-with-max-iterations",
        411: "phase-3-dialogue-counter-defended",
    }
    out.append("\n## Per-required-case status")
    out.append("| Case | id | With-skill (mean ± stddev) | Without-skill | n_runs |")
    out.append("|---|---|---|---|---|")
    for rid in sorted(required):
        w = next(
            (r for r in records if r["id"] == rid and r["config"] == "with_skill"), None
        )
        wo = next(
            (r for r in records if r["id"] == rid and r["config"] == "without_skill"),
            None,
        )
        if not w or not wo:
            out.append(f"| {required[rid]} | {rid} | n/a | n/a | 0 |")
            continue
        out.append(
            f"| {required[rid]} | {rid} | "
            f"{w['mean_rate'] * 100:.0f}% ± {w['stddev_rate'] * 100:.1f}pp | "
            f"{wo['mean_rate'] * 100:.0f}% ± {wo['stddev_rate'] * 100:.1f}pp | "
            f"{w['n_runs']} |"
        )


def write_overall(records: list[dict], out: list[str]) -> None:
    """Append the overall pooled and per-case-averaged summary to `out`."""
    w_recs = [r for r in records if r["config"] == "with_skill"]
    wo_recs = [r for r in records if r["config"] == "without_skill"]
    w_passed = sum(r["passed_total"] for r in w_recs)
    w_total = sum(r["total_total"] for r in w_recs)
    wo_passed = sum(r["passed_total"] for r in wo_recs)
    wo_total = sum(r["total_total"] for r in wo_recs)
    out.append("\n## Overall")
    out.append(
        f"- With-skill aggregate (all runs pooled): {fmt_rate(w_passed, w_total)}"
    )
    out.append(f"- With-skill mean ± stddev across cases: {fmt_mean_stddev(w_recs)}")
    out.append(
        f"- Without-skill aggregate (all runs pooled): {fmt_rate(wo_passed, wo_total)}"
    )
    out.append(
        f"- Without-skill mean ± stddev across cases: {fmt_mean_stddev(wo_recs)}"
    )
    delta = (
        100 * w_passed / w_total - 100 * wo_passed / wo_total
        if (w_total and wo_total)
        else 0
    )
    out.append(f"- Delta: {delta:+.1f} pp")


def main() -> int:
    """Parse CLI args, collect grading records, and print the aggregated markdown report."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--iteration", type=int, default=2)
    parser.add_argument("--runs", type=int, default=3)
    parser.add_argument(
        "--repo",
        type=pathlib.Path,
        default=REPO,
        help="Repository root to read evals/evals.json and evals/workspace/ from "
        "(defaults to the checkout this script lives in; overridable for tests)",
    )
    args = parser.parse_args()

    # Resolve the suite and workspace from the chosen repo so the breakout can
    # be exercised against a synthetic tree without touching the real checkout.
    repo = args.repo.resolve()
    suite = json.loads((repo / "evals" / "evals.json").read_text())
    ws = repo / "evals" / "workspace"
    dim_by_text = build_dim_by_text(suite)

    records = collect_records(args.iteration, args.runs, ws, suite)
    if not records:
        print(
            f"No grading.json data found for iteration {args.iteration}",
            file=sys.stderr,
        )
        return 1
    n_with = sum(1 for r in records if r["config"] == "with_skill")
    n_without = sum(1 for r in records if r["config"] == "without_skill")
    out: list[str] = [
        f"# Aggregated baseline — iteration-{args.iteration}",
        f"\nCases graded: with_skill={n_with}, without_skill={n_without}; "
        f"target runs per config: {args.runs}.",
    ]
    write_per_skill(records, out)
    write_dimension_breakout(records, dim_by_text, out)
    write_per_language(records, out)
    write_required_cases(records, out)
    write_overall(records, out)
    print("\n".join(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
