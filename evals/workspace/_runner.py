#!/usr/bin/env python3
"""Orchestrate the kntnt-text-skills eval suite via headless `claude -p`.

Runs every (case x config x run) combination through `claude -p` with the
executor prompt, then runs graders in batches by (skill, run_n, config).
Resumable — skips invocations whose output already exists on disk.

Usage (from the project root):

    python3 evals/workspace/_runner.py
    python3 evals/workspace/_runner.py --limit 4 --parallel 2  # dry-run-ish
    python3 evals/workspace/_runner.py --skip-executors        # only re-grade
    python3 evals/workspace/_runner.py --skill proofread       # one skill

The script must be run in a terminal where `claude` is authenticated —
i.e. your normal interactive terminal. It cannot be run from inside a
Claude Code session (the inner `claude -p` returns 401 because nested
Claude invocations strip auth).

The default budget caps spend per executor at $1 and per grader batch
at $3. Adjust with --executor-budget / --grader-budget.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import pathlib
import subprocess
import sys
import time
from dataclasses import dataclass

REPO = pathlib.Path(__file__).resolve().parents[2]
SUITE = json.loads((REPO / "evals" / "evals.json").read_text())
WS = REPO / "evals" / "workspace"


@dataclass(frozen=True)
class ExecJob:
    """One executor invocation: case x config x run."""

    case_id: int
    skill: str
    name: str
    config: str  # "with_skill" or "without_skill"
    run_n: int
    iteration: int

    @property
    def run_dir(self) -> pathlib.Path:
        return (WS / self.skill / f"iteration-{self.iteration}"
                / f"eval-{self.case_id:03d}-{self.name}"
                / self.config / f"run-{self.run_n}")

    @property
    def output_md(self) -> pathlib.Path:
        return self.run_dir / "outputs" / "output.md"

    @property
    def grading_json(self) -> pathlib.Path:
        return self.run_dir / "grading.json"

    @property
    def done_exec(self) -> bool:
        return self.output_md.exists() and self.output_md.stat().st_size > 0

    @property
    def done_grade(self) -> bool:
        return self.grading_json.exists() and self.grading_json.stat().st_size > 0

    def label(self) -> str:
        return (f"{self.skill}/eval-{self.case_id:03d}-{self.name}/"
                f"{self.config}/run-{self.run_n}")


def build_job_list(iteration: int, runs: int, skill_filter: str | None,
                   case_ids: set[int] | None,
                   limit: int | None) -> list[ExecJob]:
    jobs: list[ExecJob] = []
    for case in SUITE["evals"]:
        if skill_filter and case["skill_name"] != skill_filter:
            continue
        if case_ids is not None and case["id"] not in case_ids:
            continue
        for cfg in ("with_skill", "without_skill"):
            for run_n in range(1, runs + 1):
                jobs.append(ExecJob(
                    case_id=case["id"],
                    skill=case["skill_name"],
                    name=case["name"],
                    config=cfg,
                    run_n=run_n,
                    iteration=iteration,
                ))
    if limit:
        jobs = jobs[:limit]
    return jobs


def render_prompt(cfg_arg: str, case_id: int, iteration: int, run_n: int) -> str:
    cmd = [sys.executable, str(WS / "_prompts.py"), cfg_arg, str(case_id),
           "--iteration", str(iteration), "--run", str(run_n)]
    return subprocess.run(cmd, capture_output=True, text=True, check=True).stdout


def run_one_executor(job: ExecJob, budget_usd: float, timeout_s: int,
                     model: str) -> tuple[ExecJob, bool, str]:
    if job.done_exec:
        return job, True, "skipped"
    job.run_dir.mkdir(parents=True, exist_ok=True)
    (job.run_dir / "outputs").mkdir(parents=True, exist_ok=True)
    cfg_arg = "with" if job.config == "with_skill" else "without"
    prompt = render_prompt(cfg_arg, job.case_id, job.iteration, job.run_n)
    start = time.time()
    try:
        result = subprocess.run(
            ["claude", "-p",
             "--permission-mode", "bypassPermissions",
             "--max-budget-usd", str(budget_usd),
             "--output-format", "json",
             "--add-dir", str(REPO),
             "--model", model,
             ],
            input=prompt, capture_output=True, text=True,
            timeout=timeout_s, check=False,
        )
    except subprocess.TimeoutExpired:
        return job, False, f"TIMEOUT after {timeout_s}s"
    elapsed = time.time() - start
    if job.done_exec:
        return job, True, f"ok {elapsed:.0f}s"
    # Surface the claude json result for diagnosis.
    snippet = (result.stdout or result.stderr or "<no output>")[-300:]
    return job, False, f"FAIL {elapsed:.0f}s: {snippet}"


def run_executors(jobs: list[ExecJob], parallel: int,
                  budget_usd: float, timeout_s: int,
                  model: str) -> dict[str, int]:
    stats = {"ok": 0, "skipped": 0, "fail": 0}
    n = len(jobs)
    print(f"\n=== Executors: {n} jobs, {parallel} parallel, ${budget_usd}/job budget, model={model} ===")
    t0 = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=parallel) as pool:
        futures = {pool.submit(run_one_executor, j, budget_usd, timeout_s, model): j for j in jobs}
        for i, fut in enumerate(concurrent.futures.as_completed(futures), start=1):
            job, ok, msg = fut.result()
            if msg == "skipped":
                stats["skipped"] += 1
                tag = "SKIP"
            elif ok:
                stats["ok"] += 1
                tag = "OK"
            else:
                stats["fail"] += 1
                tag = "FAIL"
            elapsed = time.time() - t0
            print(f"  [{i:3d}/{n}] {tag:4s} {job.label()} — {msg} "
                  f"(elapsed {elapsed/60:.1f} min)")
    return stats


def grader_batch_prompt(jobs: list[ExecJob]) -> str:
    """Render a batched grader prompt covering several case-configs."""
    lines = [
        "You are grading multiple test cases for kntnt-text-skills.",
        "Follow the rules in evals/workspace/GRADER_BATCH.md.",
        "",
        "For EACH case-config below, read `eval_metadata.json` at the case "
        "directory and the outputs in the configuration's run directory, "
        "then write `<case_dir>/<config>/run-<N>/grading.json` per the schema.",
        "",
        "Cases to grade in this batch:",
    ]
    for j in jobs:
        case_dir = j.run_dir.parent.parent  # strip /<config>/run-<N>
        lines.append(f"- case_dir: `{case_dir}`")
        lines.append(f"  config: `{j.config}`")
        lines.append(f"  run: {j.run_n}")
        lines.append(f"  grading.json target: `{j.grading_json}`")
        lines.append("")
    lines.append(f"Total grading.json files to produce in this batch: {len(jobs)}.")
    lines.append("When complete, end your response with: "
                 f"`Graded {len(jobs)} runs.`")
    return "\n".join(lines)


def run_one_grader_batch(jobs: list[ExecJob], budget_usd: float,
                         timeout_s: int, model: str) -> tuple[list[ExecJob], int]:
    """Submit one batched grader call covering several jobs."""
    prompt = grader_batch_prompt(jobs)
    try:
        result = subprocess.run(
            ["claude", "-p",
             "--permission-mode", "bypassPermissions",
             "--max-budget-usd", str(budget_usd),
             "--output-format", "json",
             "--add-dir", str(REPO),
             "--model", model,
             ],
            input=prompt, capture_output=True, text=True,
            timeout=timeout_s, check=False,
        )
    except subprocess.TimeoutExpired:
        return jobs, 0
    graded = sum(1 for j in jobs if j.done_grade)
    return jobs, graded


def run_graders(jobs: list[ExecJob], parallel: int, batch_size: int,
                budget_usd: float, timeout_s: int, model: str) -> dict[str, int]:
    # Filter to jobs that have outputs but no grading yet.
    pending = [j for j in jobs if j.done_exec and not j.done_grade]
    stats = {"graded": 0, "missing": 0}
    if not pending:
        print("\n=== Graders: nothing pending ===")
        return stats
    print(f"\n=== Graders: {len(pending)} pending, batches of {batch_size}, "
          f"{parallel} parallel, ${budget_usd}/batch budget, model={model} ===")
    # Group into batches of `batch_size` per call, batching by skill+run for cohesion.
    pending.sort(key=lambda j: (j.skill, j.run_n, j.config, j.case_id))
    batches = [pending[i:i+batch_size] for i in range(0, len(pending), batch_size)]
    t0 = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=parallel) as pool:
        futures = {pool.submit(run_one_grader_batch, b, budget_usd, timeout_s, model): b
                   for b in batches}
        for i, fut in enumerate(concurrent.futures.as_completed(futures), start=1):
            batch, graded = fut.result()
            stats["graded"] += graded
            stats["missing"] += len(batch) - graded
            elapsed = time.time() - t0
            print(f"  [batch {i:3d}/{len(batches)}] {graded}/{len(batch)} graded "
                  f"(elapsed {elapsed/60:.1f} min)")
    return stats


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--iteration", type=int, default=2)
    parser.add_argument("--runs", type=int, default=3,
                        help="Runs per configuration (1, 2, or 3 for variance)")
    parser.add_argument("--parallel", type=int, default=4,
                        help="Parallel claude -p invocations")
    parser.add_argument("--executor-budget", type=float, default=1.0,
                        help="Per-executor USD cap")
    parser.add_argument("--grader-budget", type=float, default=3.0,
                        help="Per-grader-batch USD cap")
    parser.add_argument("--grader-batch-size", type=int, default=8)
    parser.add_argument("--executor-timeout", type=int, default=420)
    parser.add_argument("--grader-timeout", type=int, default=600)
    parser.add_argument("--skill", default=None,
                        help="Run only one skill (proofread, redline, edit, write)")
    parser.add_argument("--case-ids", default=None,
                        help="Comma-separated list of case ids to run "
                             "(e.g. '404,409,410,411'). Default: all cases.")
    parser.add_argument("--model", default="claude-sonnet-4-6",
                        help="Claude model id for both executor and grader. "
                             "Default: claude-sonnet-4-6 (the latest Sonnet "
                             "as of 2026-05-28; matches v0.5.4 baseline).")
    parser.add_argument("--limit", type=int, default=None,
                        help="Cap total executor jobs (debug)")
    parser.add_argument("--skip-executors", action="store_true",
                        help="Skip executor pass; only run graders on existing outputs")
    parser.add_argument("--skip-graders", action="store_true",
                        help="Skip grader pass; only run executors")
    args = parser.parse_args()

    case_ids: set[int] | None = None
    if args.case_ids:
        case_ids = {int(x) for x in args.case_ids.split(",") if x.strip()}

    # Smoke-test that claude -p auth and tool access work before launching
    # hundreds of jobs. The CLI always wraps its response in a JSON envelope
    # under `--output-format json`; auth failure shows up as is_error=true
    # plus a non-null api_error_status. Parse the envelope rather than
    # grepping its raw text, since fields like "api_error_status":null are
    # present on every success too.
    print("Pre-flight: testing claude -p auth ...")
    try:
        check = subprocess.run(
            ["claude", "-p", "--output-format", "json", "--", "reply with the single word: ok"],
            capture_output=True, text=True, timeout=30, check=False,
        )
        out = check.stdout.strip()
        err = check.stderr.strip()
        envelope: dict | None = None
        try:
            envelope = json.loads(out)
        except json.JSONDecodeError:
            envelope = None
        is_auth_fail = check.returncode != 0
        if envelope is not None:
            if envelope.get("is_error"):
                is_auth_fail = True
            if envelope.get("api_error_status") is not None:
                is_auth_fail = True
        if "Invalid authentication" in (out + err):
            is_auth_fail = True
        if is_auth_fail:
            print("FAIL — claude -p returned an error. "
                  "Run this script in a terminal where `claude` is signed in "
                  "(test with `claude -p \"say ok\"`). Do NOT run it from "
                  "inside a Claude Code session — nested invocations strip "
                  "auth and return 401.", file=sys.stderr)
            print(f"  return code: {check.returncode}", file=sys.stderr)
            print(f"  stdout: {out[:800]}", file=sys.stderr)
            print(f"  stderr: {err[:800]}", file=sys.stderr)
            return 2
        reply = envelope.get("result", out) if envelope else out
        print(f"  ok — `{reply[:120]}`\n")
    except subprocess.TimeoutExpired:
        print("FAIL — auth check timed out after 30s", file=sys.stderr)
        return 2
    except FileNotFoundError:
        print("FAIL — `claude` binary not found in PATH", file=sys.stderr)
        return 2

    jobs = build_job_list(args.iteration, args.runs, args.skill, case_ids, args.limit)
    case_count = len({j.case_id for j in jobs})
    print(f"Job list: {len(jobs)} executor jobs "
          f"({case_count} cases × 2 configs × {args.runs} runs)")

    if not args.skip_executors:
        exec_stats = run_executors(jobs, args.parallel,
                                   args.executor_budget, args.executor_timeout,
                                   args.model)
        print(f"\nExecutor summary: ok={exec_stats['ok']} "
              f"skipped={exec_stats['skipped']} fail={exec_stats['fail']}")

    if not args.skip_graders:
        grade_stats = run_graders(jobs, max(1, args.parallel // 2),
                                  args.grader_batch_size,
                                  args.grader_budget, args.grader_timeout,
                                  args.model)
        print(f"\nGrader summary: graded={grade_stats['graded']} "
              f"missing={grade_stats['missing']}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
