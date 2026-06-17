# /// script
# requires-python = ">=3.12"
# ///
"""Tests for the eval register-dimension breakout (issue #44).

A plain-assert harness rather than pytest, matching the project's no-pytest
convention: every check raises `AssertionError` on failure and the runner
prints a one-line pass/fail summary, exiting non-zero on the first failure.
Run with `uv run evals/tests/test_register_dimension.py`.

The tests cover the three pieces of genuine logic the slice introduces:
the per-assertion classifier, the migrated suite file's shape, the
aggregator's dimension split, and the setup step's plain-string extraction
with a parallel dimensions list.
"""

from __future__ import annotations

import importlib.util
import json
import pathlib
import subprocess
import sys
import tempfile

REPO = pathlib.Path(__file__).resolve().parents[2]
EVALS = REPO / "evals"
WS = EVALS / "workspace"


def _load(name: str, path: pathlib.Path):
    """Import a hyphen-free module from an explicit path (the workspace scripts are not a package)."""
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_classifier_tags_the_three_dimensions() -> None:
    """The classifier maps anglicism/AI-tell/style to register, protocol behaviour to protocol, typography/spelling to mechanics."""
    classify = _load("classify_dimensions", EVALS / "classify_dimensions.py").classify

    # Register: anglicism interference, AI-tell removal, address/voice.
    assert classify(
        "*adressera* becomes *ta upp* or *behandla*; *navigera* becomes *hantera*."
    ) == "register"
    assert classify(
        "*delve into*, *leverage* (as a verb), *tapestry* are flagged as AI vocabulary tells."
    ) == "register"
    assert classify(
        "*Det är värt att notera att…* is flagged as an AI-tell calque of *It's worth noting that…*."
    ) == "register"

    # Protocol: genre commit, fast-path, max-iterations, subagent, fallback, overlay, phase ordering.
    assert classify(
        "The fast-path exits before reading `lib/genres/_index.md`."
    ) == "protocol"
    assert classify(
        "The natural-language phrase *kör djupt* is parsed to 3 — the same value as the `--max-iterations=3` flag."
    ) == "protocol"
    assert classify(
        "Genre commits to `general` (the genre with `default: true`)."
    ) == "protocol"

    # Mechanics: typography, spelling, quotation marks, genitive.
    assert classify(
        "Thousands separator uses thin no-break space (U+202F), not comma: 1 234 567."
    ) == "mechanics"
    assert classify(
        "*Marx's teorier* is corrected to *Marx teorier* (zero-marking)."
    ) == "mechanics"
    assert classify(
        "Outer quotation marks use ”…” (U+201D on both sides), not \"…\" straight ASCII."
    ) == "mechanics"


def test_suite_file_is_object_form_with_valid_dimensions() -> None:
    """Every assertion in the aggregated suite carries a dimension drawn from the three-value vocabulary."""
    suite = json.loads((EVALS / "evals.json").read_text())
    valid = {"protocol", "mechanics", "register"}
    seen = set()
    for case in suite["evals"]:
        for exp in case["expectations"]:
            assert isinstance(exp, dict), f"assertion not object-form in case {case['id']}"
            assert set(exp.keys()) >= {"text", "dimension"}, exp
            assert isinstance(exp["text"], str) and exp["text"], exp
            assert exp["dimension"] in valid, exp
            seen.add(exp["dimension"])
    # The slice's whole point is that register is now scored as its own thing.
    assert "register" in seen, "no register assertions found after migration"
    assert "protocol" in seen and "mechanics" in seen


def test_per_skill_files_are_flattened_plain_strings() -> None:
    """The per-skill exports must stay flat string lists so they validate against the stock skill-creator schema."""
    for skill in ("proofread", "redline", "edit", "write"):
        data = json.loads((EVALS / skill / "evals.json").read_text())
        for case in data["evals"]:
            for exp in case["expectations"]:
                assert isinstance(exp, str), (
                    f"{skill} case {case['id']} has non-string expectation: {exp!r}"
                )


def test_aggregator_splits_by_dimension() -> None:
    """`split_by_dimension` partitions graded assertions into a hard gate and a register sub-score with its n."""
    agg = _load("_aggregate", WS / "_aggregate.py")

    graded = [
        {"text": "typo rule", "passed": True},
        {"text": "spelling rule", "passed": False},
        {"text": "genre commit", "passed": True},
        {"text": "anglicism flagged", "passed": True},
        {"text": "ai-tell flagged", "passed": False},
    ]
    dim_by_text = {
        "typo rule": "mechanics",
        "spelling rule": "mechanics",
        "genre commit": "protocol",
        "anglicism flagged": "register",
        "ai-tell flagged": "register",
    }

    by_dim = agg.split_by_dimension(graded, dim_by_text)
    assert by_dim["mechanics"] == {"passed": 1, "total": 2}
    assert by_dim["protocol"] == {"passed": 1, "total": 1}
    assert by_dim["register"] == {"passed": 1, "total": 2}

    # The hard gate pools protocol + mechanics; register stays separate with its n.
    gate = agg.gate_score(by_dim)
    register = agg.register_score(by_dim)
    assert gate == {"passed": 2, "total": 3}
    assert register == {"passed": 1, "total": 2}


def test_aggregator_dry_run_emits_a_register_sub_score() -> None:
    """A dry run of the aggregator over a synthetic graded tree prints both sub-scores, the register line carrying its n."""
    suite = {
        "suite_name": "t",
        "evals": [
            {
                "id": 1,
                "skill_name": "redline",
                "name": "synthetic-case",
                "language": "sv",
                "prompt": "p",
                "files": [],
                "expected_output": "",
                "expectations": [
                    {"text": "genre commits to general", "dimension": "protocol"},
                    {"text": "thin space used", "dimension": "mechanics"},
                    {"text": "anglicism adressera flagged", "dimension": "register"},
                ],
            }
        ],
    }
    grading = {
        "expectations": [
            {"text": "genre commits to general", "passed": True, "evidence": "e"},
            {"text": "thin space used", "passed": True, "evidence": "e"},
            {"text": "anglicism adressera flagged", "passed": False, "evidence": "e"},
        ],
        "summary": {"passed": 2, "failed": 1, "total": 3, "pass_rate": 2 / 3},
    }

    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        (root / "evals").mkdir()
        (root / "evals" / "evals.json").write_text(
            json.dumps(suite, ensure_ascii=False)
        )
        ws = root / "evals" / "workspace"
        case = (
            ws
            / "redline"
            / "iteration-2"
            / "eval-001-synthetic-case"
            / "with_skill"
            / "run-1"
        )
        case.mkdir(parents=True)
        (case / "grading.json").write_text(json.dumps(grading, ensure_ascii=False))

        # Run the aggregator against the synthetic tree via the --repo override.
        out = subprocess.run(
            [
                sys.executable,
                str(WS / "_aggregate.py"),
                "--repo",
                str(root),
                "--iteration",
                "2",
                "--runs",
                "1",
            ],
            capture_output=True,
            text=True,
        )
        report = out.stdout
        assert "register" in report.lower(), f"no register sub-score in report:\n{report}\n{out.stderr}"
        # The register line must carry its assertion count (its n).
        assert "n=" in report.lower() or "/ 1" in report or "(1)" in report, (
            f"register line lacks its n:\n{report}"
        )


def _run() -> int:
    """Run every test function in definition order, printing a terse pass/fail line each."""
    tests = [
        test_classifier_tags_the_three_dimensions,
        test_suite_file_is_object_form_with_valid_dimensions,
        test_per_skill_files_are_flattened_plain_strings,
        test_aggregator_splits_by_dimension,
        test_aggregator_dry_run_emits_a_register_sub_score,
    ]
    failures = 0
    for test in tests:
        try:
            test()
            print(f"PASS {test.__name__}")
        except Exception as exc:  # noqa: BLE001 — a test harness reports any failure
            failures += 1
            print(f"FAIL {test.__name__}: {exc}")
    print(f"\n{len(tests) - failures}/{len(tests)} passed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(_run())
