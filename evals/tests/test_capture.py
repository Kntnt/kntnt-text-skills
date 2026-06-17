# /// script
# requires-python = ">=3.12"
# ///
"""Tests for the /eval capture command's deterministic core (issue #45).

A plain-assert harness rather than pytest, matching the project's no-pytest
convention (see test_register_dimension.py): every check raises
`AssertionError` on failure and the runner prints a one-line pass/fail summary,
exiting non-zero on the first failure. Run with
`uv run evals/tests/test_capture.py`.

The interactive propose-and-ratify flow itself is a human-in-the-loop step the
SKILL.md prose drives and no test can stand in for. What these tests lock is
the mechanically verifiable core the flow calls: parsing a synthetic
transcript, proposing dimension-tagged assertions traced to the feedback,
shaping them per skill, anonymising names, the no-write contract of propose,
and the commit round-trip into the object-form suite plus flattened per-skill
files.
"""

from __future__ import annotations

import importlib.util
import json
import pathlib
import sys
import tempfile

REPO = pathlib.Path(__file__).resolve().parents[2]
EVALS = REPO / "evals"
FIXTURES = EVALS / "fixtures"
EDIT_TRANSCRIPT = FIXTURES / "capture-transcript-edit.md"
WRITE_TRANSCRIPT = FIXTURES / "capture-transcript-write.md"


def _load(name: str, path: pathlib.Path):
    """Import a hyphen-free module from an explicit path (the eval scripts are not a package)."""
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


capture = _load("capture", EVALS / "capture.py")


def test_propose_reads_the_edit_transcript_into_a_well_formed_case() -> None:
    """An /edit transcript yields a case carrying the skill, language, prompt and an input fixture, with assertions present."""
    case = capture.propose(EDIT_TRANSCRIPT)
    assert case["skill_name"] == "edit"
    assert case["language"] == "sv"
    assert case["prompt"] == "/edit sv"
    # An edit case grades a correction of an input, so it must carry input text.
    assert case["input_text"].strip(), "edit case must propose input text to edit"
    assert len(case["expectations"]) >= 3, "expected several assertions from the planted feedback"
    for exp in case["expectations"]:
        assert set(exp) >= {"text", "dimension", "source"}, (
            f"each assertion must carry text, dimension and its traced source: {exp}"
        )
        assert exp["dimension"] in {"protocol", "mechanics", "register"}


def test_each_assertion_is_traced_to_the_feedback_it_came_from() -> None:
    """Every proposed assertion records the verbatim maintainer remark it derives from, and that remark is one of the transcript's feedback bullets."""
    case = capture.propose(EDIT_TRANSCRIPT)
    feedback = capture.parse_transcript(EDIT_TRANSCRIPT.read_text())["feedback"]
    for exp in case["expectations"]:
        assert exp["source"] in feedback, (
            f"assertion source {exp['source']!r} is not one of the transcript's feedback remarks"
        )


def test_edit_assertions_are_deterministic_catch_or_apply_shape() -> None:
    """For edit/redline, assertions read as deterministic 'must catch / must apply fault X', not negative draft assertions."""
    case = capture.propose(EDIT_TRANSCRIPT)
    texts = [e["text"].lower() for e in case["expectations"]]
    # At least one assertion uses the deterministic catch/apply phrasing.
    assert any("corrected to" in t or "flagged" in t or "applied" in t or "becomes" in t for t in texts), (
        f"edit assertions should be deterministic catch/apply shape: {texts}"
    )
    # No edit assertion should be phrased as a negative-draft 'must not contain'.
    assert not any("a fresh draft must not contain" in t for t in texts), (
        "edit assertions must not use the write-style negative-draft shape"
    )


def test_register_faults_are_tagged_register_and_mechanics_faults_mechanics() -> None:
    """The anglicism faults classify as register; the typography/genitive faults classify as mechanics."""
    case = capture.propose(EDIT_TRANSCRIPT)
    by_register = [e for e in case["expectations"] if e["dimension"] == "register"]
    by_mechanics = [e for e in case["expectations"] if e["dimension"] == "mechanics"]
    register_text = " ".join(e["text"].lower() for e in by_register)
    mechanics_text = " ".join(e["text"].lower() for e in by_mechanics)
    assert "adressera" in register_text or "leverera" in register_text, (
        f"anglicism faults should be register: {register_text!r}"
    )
    assert "1 234 567" in mechanics_text or "marx" in mechanics_text, (
        f"typography/genitive faults should be mechanics: {mechanics_text!r}"
    )


def test_write_assertions_are_negative_or_structural_shape() -> None:
    """A /write case shapes assertions as negative ('a fresh draft must not contain X') or structural ('reaches substance by sentence N'), never edit-style 'corrected to'."""
    case = capture.propose(WRITE_TRANSCRIPT)
    assert case["skill_name"] == "write"
    # A write case has no input to correct — its source is a brief.
    assert case.get("brief", "").strip(), "write case must propose a brief"
    assert not case.get("input_text", "").strip(), "write case must not carry input text"
    texts = [e["text"].lower() for e in case["expectations"]]
    assert any("must not contain" in t for t in texts), (
        f"write assertions should include a negative-draft shape: {texts}"
    )
    assert any("sentence" in t and ("reaches" in t or "by sentence" in t) for t in texts), (
        f"write assertions should include a structural opening shape: {texts}"
    )
    assert not any("corrected to" in t for t in texts), (
        "write assertions must not use the edit-style 'corrected to' shape"
    )


def test_names_are_anonymised_in_the_proposed_fixture() -> None:
    """People, companies and products from the transcript do not survive verbatim into the proposed fixture or assertions."""
    edit_case = capture.propose(EDIT_TRANSCRIPT)
    write_case = capture.propose(WRITE_TRANSCRIPT)
    edit_blob = json.dumps(edit_case, ensure_ascii=False)
    write_blob = json.dumps(write_case, ensure_ascii=False)
    for name in ("Anna Lindqvist", "Volvo", "Spotify"):
        assert name not in edit_blob, f"name {name!r} survived into the edit proposal"
    for name in ("Erik Svensson", "Ericsson"):
        assert name not in write_blob, f"name {name!r} survived into the write proposal"


def test_anonymiser_scrubs_names_but_keeps_anglicism_terms() -> None:
    """The anonymiser replaces capitalised proper-name spans, leaving the lowercase fault vocabulary that assertions need."""
    scrubbed = capture.anonymise("Anna Lindqvist på Volvo missade adressera och leverera.")
    assert "Anna Lindqvist" not in scrubbed
    assert "Volvo" not in scrubbed
    assert "adressera" in scrubbed and "leverera" in scrubbed


def test_propose_writes_nothing_to_disk() -> None:
    """propose() is pure: it returns a candidate without touching evals.json or any per-skill file."""
    before = (EVALS / "evals.json").read_text()
    capture.propose(EDIT_TRANSCRIPT)
    capture.propose(WRITE_TRANSCRIPT)
    after = (EVALS / "evals.json").read_text()
    assert before == after, "propose() must not modify evals.json"


def test_commit_appends_object_form_case_and_regenerates_flattened_per_skill() -> None:
    """commit() into a temp suite copy appends the case in object form and regenerates flattened plain-string per-skill files (the round-trip smoke test)."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = pathlib.Path(tmp)
        suite_path = tmp_path / "evals.json"
        # Seed a minimal object-form suite with one pre-existing edit case.
        suite_path.write_text(
            json.dumps(
                {
                    "suite_name": "kntnt-text-skills",
                    "schema_version": "skill-creator/evals.json",
                    "evals": [
                        {
                            "id": 1,
                            "skill_name": "edit",
                            "name": "seed-case",
                            "language": "sv",
                            "prompt": "/edit sv",
                            "files": [],
                            "expected_output": "seed",
                            "expectations": [
                                {"text": "seed assertion", "dimension": "mechanics"}
                            ],
                        }
                    ],
                },
                indent=2,
                ensure_ascii=False,
            )
            + "\n"
        )
        case = capture.propose(EDIT_TRANSCRIPT)
        new_id = capture.commit(case, suite_path=suite_path, skill_root=tmp_path)

        suite = json.loads(suite_path.read_text())
        ids = [c["id"] for c in suite["evals"]]
        assert new_id in ids and new_id != 1, "commit must assign a fresh id"
        appended = next(c for c in suite["evals"] if c["id"] == new_id)
        # The appended case is object-form: every expectation is {text, dimension}.
        for exp in appended["expectations"]:
            assert isinstance(exp, dict) and set(exp) == {"text", "dimension"}, (
                f"committed assertion must be flattened to {{text, dimension}}: {exp}"
            )

        # The per-skill edit file regenerates as flat plain strings.
        per_skill = json.loads((tmp_path / "edit" / "evals.json").read_text())
        new_in_per_skill = next(c for c in per_skill["evals"] if c["id"] == new_id)
        for exp in new_in_per_skill["expectations"]:
            assert isinstance(exp, str), (
                f"per-skill expectation must be a flattened plain string: {exp!r}"
            )


def test_commit_strips_the_propose_only_source_trace() -> None:
    """The 'source' trace is a proposal-time aid; the committed object-form assertion carries only text and dimension."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = pathlib.Path(tmp)
        suite_path = tmp_path / "evals.json"
        suite_path.write_text(
            json.dumps(
                {"suite_name": "x", "evals": []}, indent=2, ensure_ascii=False
            )
            + "\n"
        )
        case = capture.propose(WRITE_TRANSCRIPT)
        new_id = capture.commit(case, suite_path=suite_path, skill_root=tmp_path)
        suite = json.loads(suite_path.read_text())
        appended = next(c for c in suite["evals"] if c["id"] == new_id)
        for exp in appended["expectations"]:
            assert "source" not in exp, "committed assertions must not carry the propose-only source trace"


def _run() -> int:
    """Run every test function in definition order, printing a terse pass/fail line each."""
    tests = [
        test_propose_reads_the_edit_transcript_into_a_well_formed_case,
        test_each_assertion_is_traced_to_the_feedback_it_came_from,
        test_edit_assertions_are_deterministic_catch_or_apply_shape,
        test_register_faults_are_tagged_register_and_mechanics_faults_mechanics,
        test_write_assertions_are_negative_or_structural_shape,
        test_names_are_anonymised_in_the_proposed_fixture,
        test_anonymiser_scrubs_names_but_keeps_anglicism_terms,
        test_propose_writes_nothing_to_disk,
        test_commit_appends_object_form_case_and_regenerates_flattened_per_skill,
        test_commit_strips_the_propose_only_source_trace,
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
