#!/usr/bin/env python3
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
import math
import pathlib
import sys
from collections import defaultdict
from statistics import mean, stdev

REPO = pathlib.Path(__file__).resolve().parents[2]
SUITE = json.loads((REPO / "evals" / "evals.json").read_text())
WS = REPO / "evals" / "workspace"


def collect_records(iteration: int, runs: int) -> list[dict]:
    """Read every run's grading.json into a list of records."""
    records = []
    for case in SUITE["evals"]:
        base = (WS / case["skill_name"] / f"iteration-{iteration}"
                / f"eval-{case['id']:03d}-{case['name']}")
        for cfg in ("with_skill", "without_skill"):
            run_rates = []
            run_passed = []
            run_total = []
            for run_n in range(1, runs + 1):
                g_path = base / cfg / f"run-{run_n}" / "grading.json"
                if not g_path.exists():
                    continue
                g = json.loads(g_path.read_text())
                summ = g["summary"]
                run_passed.append(summ["passed"])
                run_total.append(summ["total"])
                run_rates.append(summ["pass_rate"])
            if not run_rates:
                continue
            records.append({
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
            })
    return records


def fmt_rate(passed: int, total: int) -> str:
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
    return f"{m*100:.1f}% ± {pooled*100:.1f}pp"


def write_per_skill(records: list[dict], out: list[str]) -> None:
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
        delta = 100 * w_passed / w_total - 100 * wo_passed / wo_total if (w_total and wo_total) else 0
        out.append(f"| {skill} | {fmt_rate(w_passed, w_total)} "
                   f"({fmt_mean_stddev(w_recs)}) | "
                   f"{fmt_rate(wo_passed, wo_total)} "
                   f"({fmt_mean_stddev(wo_recs)}) | {delta:+.0f} pp |")


def write_per_language(records: list[dict], out: list[str]) -> None:
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
        delta = 100 * w_passed / w_total - 100 * wo_passed / wo_total if (w_total and wo_total) else 0
        label = lang if lang not in ("sv_FI", "de") else f"{lang} ({'overlay' if lang == 'sv_FI' else 'fallback'})"
        out.append(f"| {label} | {fmt_rate(w_passed, w_total)} "
                   f"({fmt_mean_stddev(w_recs)}) | "
                   f"{fmt_rate(wo_passed, wo_total)} "
                   f"({fmt_mean_stddev(wo_recs)}) | {delta:+.0f} pp |")


def write_required_cases(records: list[dict], out: list[str]) -> None:
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
        w = next((r for r in records if r["id"] == rid and r["config"] == "with_skill"), None)
        wo = next((r for r in records if r["id"] == rid and r["config"] == "without_skill"), None)
        if not w or not wo:
            out.append(f"| {required[rid]} | {rid} | n/a | n/a | 0 |")
            continue
        out.append(f"| {required[rid]} | {rid} | "
                   f"{w['mean_rate']*100:.0f}% ± {w['stddev_rate']*100:.1f}pp | "
                   f"{wo['mean_rate']*100:.0f}% ± {wo['stddev_rate']*100:.1f}pp | "
                   f"{w['n_runs']} |")


def write_overall(records: list[dict], out: list[str]) -> None:
    w_recs = [r for r in records if r["config"] == "with_skill"]
    wo_recs = [r for r in records if r["config"] == "without_skill"]
    w_passed = sum(r["passed_total"] for r in w_recs)
    w_total = sum(r["total_total"] for r in w_recs)
    wo_passed = sum(r["passed_total"] for r in wo_recs)
    wo_total = sum(r["total_total"] for r in wo_recs)
    out.append("\n## Overall")
    out.append(f"- With-skill aggregate (all runs pooled): {fmt_rate(w_passed, w_total)}")
    out.append(f"- With-skill mean ± stddev across cases: {fmt_mean_stddev(w_recs)}")
    out.append(f"- Without-skill aggregate (all runs pooled): {fmt_rate(wo_passed, wo_total)}")
    out.append(f"- Without-skill mean ± stddev across cases: {fmt_mean_stddev(wo_recs)}")
    delta = 100 * w_passed / w_total - 100 * wo_passed / wo_total if (w_total and wo_total) else 0
    out.append(f"- Delta: {delta:+.1f} pp")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--iteration", type=int, default=2)
    parser.add_argument("--runs", type=int, default=3)
    args = parser.parse_args()
    records = collect_records(args.iteration, args.runs)
    if not records:
        print(f"No grading.json data found for iteration {args.iteration}", file=sys.stderr)
        return 1
    n_with = sum(1 for r in records if r["config"] == "with_skill")
    n_without = sum(1 for r in records if r["config"] == "without_skill")
    out: list[str] = [f"# Aggregated baseline — iteration-{args.iteration}",
                      f"\nCases graded: with_skill={n_with}, without_skill={n_without}; "
                      f"target runs per config: {args.runs}."]
    write_per_skill(records, out)
    write_per_language(records, out)
    write_required_cases(records, out)
    write_overall(records, out)
    print("\n".join(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
