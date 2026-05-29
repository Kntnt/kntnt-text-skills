# /// script
# requires-python = ">=3.12"
# ///
"""Scaffold evals/workspace/<skill>/iteration-<N>/eval-<id>-<name>/ tree.

Creates per-case directories with eval_metadata.json under the iteration
directory passed via --iteration (default: latest). When --runs is set
greater than 1, also creates per-config run-<k> subdirectories with their
outputs/ trees, ready for the executor.

Not part of the plugin; just a one-shot helper for the baseline / variance
run pipeline.
"""

from __future__ import annotations

import argparse
import json
import pathlib

REPO = pathlib.Path(__file__).resolve().parents[2]
SUITE = json.loads((REPO / "evals" / "evals.json").read_text())
WS = REPO / "evals" / "workspace"


def main() -> None:
    """Parse CLI args and scaffold the per-case iteration tree for the requested runs."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--iteration",
        type=int,
        default=2,
        help="Iteration number; iteration-<N> subdir is created",
    )
    parser.add_argument(
        "--runs",
        type=int,
        default=3,
        help="Number of runs per configuration to scaffold",
    )
    args = parser.parse_args()

    created = 0
    for case in SUITE["evals"]:
        skill = case["skill_name"]
        case_dir = (
            WS
            / skill
            / f"iteration-{args.iteration}"
            / f"eval-{case['id']:03d}-{case['name']}"
        )
        case_dir.mkdir(parents=True, exist_ok=True)
        meta = {
            "eval_id": case["id"],
            "eval_name": case["name"],
            "skill_name": case["skill_name"],
            "language": case["language"],
            "prompt": case["prompt"],
            "files": case.get("files", []),
            "expected_output": case.get("expected_output", ""),
            "assertions": case.get("expectations", []),
        }
        (case_dir / "eval_metadata.json").write_text(
            json.dumps(meta, indent=2, ensure_ascii=False) + "\n"
        )
        for cfg in ("with_skill", "without_skill"):
            for run_n in range(1, args.runs + 1):
                (case_dir / cfg / f"run-{run_n}" / "outputs").mkdir(
                    parents=True, exist_ok=True
                )
        created += 1

    print(
        f"Scaffolded {created} case directories under "
        f"{WS} (iteration-{args.iteration}, runs=1..{args.runs})."
    )


if __name__ == "__main__":
    main()
