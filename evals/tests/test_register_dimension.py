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


def test_committed_suite_matches_the_classifier() -> None:
    """Every committed dimension equals the classifier's output — the suite is kept in sync, not hand-patched.

    The README and the classifier docstring promise the committed suite tracks
    the classifier's editorial rules. A divergence here means a mis-tag was
    left in the file (or a rule drifted) instead of being fixed at the rule —
    exactly the gap that let the AI-tell / restraint / protocol mis-tags ship.
    """
    cd = _load("classify_dimensions", EVALS / "classify_dimensions.py")
    suite = json.loads((EVALS / "evals.json").read_text())
    divergences = [
        (case["id"], exp["dimension"], cd.classify(exp["text"]), exp["text"])
        for case in suite["evals"]
        for exp in case["expectations"]
        if exp["dimension"] != cd.classify(exp["text"])
    ]
    assert not divergences, (
        f"{len(divergences)} committed dimension(s) diverge from the classifier; "
        f"first: case {divergences[0][0]} committed={divergences[0][1]!r} "
        f"classifier={divergences[0][2]!r} :: {divergences[0][3]!r}"
    )


def test_known_ai_tell_and_restraint_assertions_are_tagged_correctly() -> None:
    """The previously mis-tagged AI-tell, restraint and protocol assertions carry the editorially correct dimension.

    Locks the specific corrections: bare-phrased AI-tell / opening-cliché
    assertions are register (matching their near-identical siblings); the
    fast-path short-text restraint checks are protocol (a negative control,
    not a register property); and the procedural assertions that previously
    dropped to the mechanics fallback are protocol.
    """
    suite = json.loads((EVALS / "evals.json").read_text())
    by_id_text = {
        (case["id"], exp["text"]): exp["dimension"]
        for case in suite["evals"]
        for exp in case["expectations"]
    }
    expected = {
        # Bare-phrased AI-tells / opening clichés -> register (Finding 1).
        (115, "*In a world where…*, *It's worth noting that…*, *Let me be perfectly clear* are flagged."): "register",
        (208, "*To summarize* opening a conclusion is rewritten."): "register",
        # Fast-path short-text restraint -> protocol (Finding 2).
        (112, "Finding list (if any) is short and reflects the everyday-text register."): "protocol",
        (117, "Findings (if any) are short and reflect everyday-text register."): "protocol",
        # Procedural assertions that fell to the mechanics fallback -> protocol (Finding 3).
        (216, "Values above 3 would be clamped to 3 (protocol maximum)."): "protocol",
        (404, "`lib/genres/_index.md` is read and trigger-matched."): "protocol",
        (405, "If the flag and the natural-language phrase conflict, the flag wins; if ambiguous, ask the user."): "protocol",
        (406, "Output is the polished text, with no user-facing dialogue (the AFK variant)."): "protocol",
        (402, "Inheritance is one step only — the base `sv.md` does not itself inherit."): "protocol",
    }
    for key, want in expected.items():
        assert key in by_id_text, f"assertion not found in suite: {key}"
        assert by_id_text[key] == want, (
            f"case {key[0]} expected {want}, got {by_id_text[key]}: {key[1]!r}"
        )


def test_negative_control_restraint_assertions_are_protocol() -> None:
    """Negative-control and no-silent-rewrite restraint assertions classify protocol, not the mechanics fallback.

    Locks the second wave of corrections. The fast-path discriminator and the
    flow-load consequence in redline #404 assert a behaviour the standard flow
    ran (protocol), not an output-form property. The proofread-scope and
    output-unchanged restraint checks (proofread #5/#8/#14/#17, #19/#20/#21)
    and the bare no-silent-rewrite traceability line in edit #219 are the same
    negative-control discipline as their protocol-tagged siblings (#119,
    #205/#211/#218) and must classify alike. The boundary holds in the other
    direction too: edit #220's twin clause stays mechanics because its
    assertion is led by a British-conventions-preserved mechanics body, so the
    restraint clause is a trailing addendum rather than the graded content.
    """
    suite = json.loads((EVALS / "evals.json").read_text())
    by_id_text = {
        (case["id"], exp["text"]): exp["dimension"]
        for case in suite["evals"]
        for exp in case["expectations"]
    }
    expected = {
        # #404 fast-path discriminator and flow-load consequence -> protocol.
        (404, "Either condition broken: structural markers present (H1, standfirst, byline, attributed quote)."): "protocol",
        (404, "The findings list (`## Findings` in the transcript) includes at least one finding that cites a review-scoped section of `lib/genres/article.md` — specifically the repetition rule between H1, standfirst, lead and first H2, OR one of the documented common pitfalls (visible ABT formula, standfirst and lead repeating each other, teasing subheadings, explicit bridges). This is the observable consequence of the standard flow loading the genre file's review-scoped sections."): "protocol",
        # Proofread-scope and output-unchanged restraint -> protocol.
        (5, "No style or word-order changes are made — proofread scope only."): "protocol",
        (8, "No other word-order or content changes are made — proofread scope only."): "protocol",
        (14, "No other word-order or content changes are made — proofread scope only."): "protocol",
        (17, "No other word-order or content changes are made — proofread scope only."): "protocol",
        (19, "The output text is unchanged from the input, OR any change is limited to whitespace-equivalent normalisation (no semantic edits)."): "protocol",
        (20, "The output text is unchanged from the input, OR any change is limited to whitespace-equivalent normalisation."): "protocol",
        (21, "The output text is unchanged from the input, OR any change is limited to whitespace-equivalent normalisation."): "protocol",
        # Bare no-silent-rewrite traceability -> protocol, matching #205/#211/#218.
        (219, "Any change applied in the edit is traceable to a finding in the transcript — no silent rewrites."): "protocol",
        # The mechanics-led twin keeps its trailing restraint clause in mechanics.
        (220, "British conventions are preserved (-ise spellings, single quotation marks, *Licence*); every applied change is traceable to a finding in the transcript — no silent rewrites."): "mechanics",
    }
    for key, want in expected.items():
        assert key in by_id_text, f"assertion not found in suite: {key}"
        assert by_id_text[key] == want, (
            f"case {key[0]} expected {want}, got {by_id_text[key]}: {key[1]!r}"
        )


def test_aggregator_warns_on_unmatched_graded_text() -> None:
    """A graded assertion whose text does not join to a dimension is surfaced, not dropped silently."""
    agg = _load("_aggregate", WS / "_aggregate.py")
    graded = [
        {"text": "joins fine", "passed": True},
        {"text": "drifted text not in suite", "passed": False},
    ]
    dim_by_text = {"joins fine": "mechanics"}

    unmatched = agg.unmatched_texts(graded, dim_by_text)
    assert unmatched == ["drifted text not in suite"], unmatched
    # The matched entry still scores; only the drifted one is excluded.
    by_dim = agg.split_by_dimension(graded, dim_by_text)
    assert by_dim["mechanics"] == {"passed": 1, "total": 1}


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
        test_committed_suite_matches_the_classifier,
        test_known_ai_tell_and_restraint_assertions_are_tagged_correctly,
        test_negative_control_restraint_assertions_are_protocol,
        test_aggregator_warns_on_unmatched_graded_text,
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
