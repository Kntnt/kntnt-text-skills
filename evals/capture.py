# /// script
# requires-python = ">=3.12"
# ///
"""Deterministic core of the /eval capture command (issue #45).

The `/eval` capture command turns a real worked-on writing/editing session into
a dimension-tagged eval case. It lives entirely under `evals/` and never reads
or modifies the skills under `lib/`. The interactive propose-and-ratify flow —
showing the candidate, taking accept/edit/reject per assertion and a
commit-or-skip decision — is driven by the SKILL.md prose alongside this file.
This module is the part of that flow a test can pin down:

- `parse_transcript` splits a capture transcript into its header (skill,
  language, prompt), the maintainer's running feedback, and the before/after
  diff;
- `anonymise` scrubs proper-name spans (people, companies, products) from a
  fixture so a real session's names never reach the committed suite;
- `propose` reads a transcript and returns a candidate case — a brief (for a
  `/write` case) or input text plus expected findings (for `/edit` / `/redline`)
  and a list of dimension-tagged assertions, each traced to the feedback remark
  it came from. It writes nothing;
- `commit` is invoked only after the maintainer ratifies: it appends the case
  to the aggregated suite in object form (`{text, dimension}`) and regenerates
  the per-skill files, flattened to plain strings.

The dimension tag itself is not re-decided here. `classify_dimensions.classify`
already encodes that editorial judgement for issue #44, so this module reuses
it rather than inventing a parallel classifier.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import pathlib
import re
import sys

# Repository and suite anchors, resolved from this file's location so the tool
# works from any working directory.
REPO = pathlib.Path(__file__).resolve().parents[1]
EVALS = REPO / "evals"
SUITE_PATH = EVALS / "evals.json"
PER_SKILL = ("proofread", "redline", "edit", "write")

# Skills whose assertions are deterministic catch/apply checks against an input,
# versus skills whose assertions are negative/structural checks on a fresh draft.
CORRECTION_SKILLS = ("edit", "redline")
DRAFT_SKILLS = ("write",)


def _load_classifier():
    """Import the issue #44 dimension classifier from its explicit path.

    The eval scripts are standalone files, not a package, so the classifier is
    loaded the same way the test harness loads modules. Reusing it keeps the
    register/mechanics/protocol judgement in one place.
    """
    path = EVALS / "classify_dimensions.py"
    spec = importlib.util.spec_from_file_location("classify_dimensions", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.classify


classify = _load_classifier()


def parse_transcript(text: str) -> dict:
    """Split a capture transcript into header fields, feedback remarks and diff.

    The transcript wire format is a frontmatter-style header (`skill:`,
    `language:`, `prompt:` lines before the first `#` heading), a `## Maintainer
    feedback` section of quoted bullet remarks, and a `## Diff` fenced block.
    The maintainer's running feedback is the primary fault source; the diff
    corroborates it.
    """

    # Pull the leading header lines (key: value) that precede the first heading.
    header: dict[str, str] = {}
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            break
        match = re.match(r"^([A-Za-z_]+):\s*(.+)$", stripped)
        if match:
            header[match.group(1)] = match.group(2).strip()

    # Collect the maintainer's feedback: each bullet under the feedback heading,
    # taking the quoted remark when the bullet quotes one, else the whole bullet.
    feedback = _extract_section_bullets(text, "Maintainer feedback")
    quoted: list[str] = []
    for bullet in feedback:
        quote = re.search(r"[\"“””“](.+?)[\"“””“]", bullet)
        quoted.append(quote.group(1).strip() if quote else bullet)

    # Capture the diff body from the fenced block under the Diff heading.
    diff = ""
    diff_match = re.search(r"##\s+Diff\s*\n+```[a-z]*\n(.*?)```", text, re.DOTALL)
    if diff_match:
        diff = diff_match.group(1)

    return {"header": header, "feedback": quoted, "diff": diff}


def _extract_section_bullets(text: str, heading: str) -> list[str]:
    """Return the bullet lines under a `## <heading>` section, up to the next heading."""

    pattern = re.compile(
        rf"##\s+{re.escape(heading)}\s*\n(.*?)(?=\n##\s|\Z)", re.DOTALL
    )
    match = pattern.search(text)
    if not match:
        return []
    bullets: list[str] = []
    for line in match.group(1).splitlines():
        stripped = line.strip()
        if stripped.startswith("- "):
            bullets.append(stripped[2:].strip())
    return bullets


# Proper-name spans are capitalised runs of one or more words. The anonymiser
# replaces each distinct span with a stable placeholder so a span used twice
# scrubs to the same token, keeping the fixture readable.
_NAME_SPAN = re.compile(r"\b[A-ZÅÄÖ][\wÅÄÖåäö]+(?:\s+[A-ZÅÄÖ][\wÅÄÖåäö]+)*\b")

# Capitalised words that open a sentence or a fixed phrase are not names; keep
# them so the anonymiser does not maul ordinary prose. Swedish and English
# sentence openers and connectives that appear in the fixtures live here.
_NAME_STOPWORDS = frozenset(
    {
        "Vi", "Du", "Det", "Bra", "Anna", "Erik",
        "In", "It", "The", "District", "Phase", "Mechanics", "Style",
        "Marx", "Session", "Maintainer", "Diff", "Range", "Time",
        "Temperature", "Percent", "Thousands", "A", "An",
    }
)


def anonymise(text: str) -> str:
    """Replace proper-name spans (people, companies, products) with placeholders.

    A name is a capitalised single word or multi-word run. A multi-word span
    reads as a person and scrubs as one unit (*Anna Lindqvist* → *[Person 1]*);
    a single-word span whose token is not a known sentence opener or prose word
    reads as a company or product (*Volvo* → *[Company 1]*). Lowercase fault
    vocabulary that assertions depend on — *adressera*, *leverera* — is never
    touched because it is not capitalised. A single pass over the original text
    rules out re-scanning emitted placeholders, and distinct spans map to
    stable, numbered placeholders so a span used twice scrubs to the same token.
    """

    replacements: dict[str, str] = {}
    person_n = company_n = 0

    def _replace(match: re.Match[str]) -> str:
        nonlocal person_n, company_n
        span = match.group(0)
        # A single capitalised token that is a sentence opener or known prose
        # word is left in place; a multi-word span is always treated as a name.
        if " " not in span and span in _NAME_STOPWORDS:
            return span
        if span in replacements:
            return replacements[span]
        if " " in span:
            person_n += 1
            token = f"[Person {person_n}]"
        else:
            company_n += 1
            token = f"[Company {company_n}]"
        replacements[span] = token
        return token

    return _NAME_SPAN.sub(_replace, text)


def _emphasise(term: str) -> str:
    """Wrap a fault term in markdown emphasis the way the existing assertions do."""
    return f"*{term.strip('*')}*"


def _faults_from_remark(remark: str) -> list[dict]:
    """Derive zero or more assertion seeds from one maintainer feedback remark.

    A seed is `{term, target}` where `term` is the flagged fault and `target` is
    the correction the maintainer named (empty when none). Affirmations — "good
    that you kept X, no change needed" — yield nothing, because a case asserts
    faults to catch, not things already correct.
    """

    lower = remark.lower()
    # Affirmations carry no fault: an explicit "no change needed" / "bra att du
    # behöll" remark is praise, not a planted fault, so it seeds no assertion.
    if "inga ändringar" in lower or "no change" in lower or (
        "bra att" in lower and "behöll" in lower
    ):
        return []

    # Pull the emphasised terms the maintainer named and any explicit correction
    # target introduced by "bli", "vara", "blir", "→", "to", or "ska bli".
    terms = re.findall(r"\*([^*]+)\*", remark)
    target_match = re.search(
        r"(?:ska (?:bli|vara)|ska\s|bli|blir|vara|→|->|to|become[s]?)\s+\*?([^*.,;]+)\*?",
        remark,
    )
    target = target_match.group(1).strip() if target_match else ""

    if not terms:
        # No emphasised fault term: fall back to the remark itself as the fault
        # description so a numeric/structural remark still seeds an assertion.
        return [{"term": "", "target": target, "raw": remark}]
    return [{"term": term, "target": target, "raw": remark} for term in terms[:1]]


def _shape_assertion(skill: str, seed: dict, remark: str) -> str | None:
    """Shape a fault seed into an assertion text appropriate for the skill.

    edit/redline assertions are deterministic — *fault* is corrected to *target*
    (or flagged when no target is named). write assertions are negative or
    structural — a fresh draft must not contain the fault, or the opening must
    reach substance by a named sentence. Returns None when the remark cannot be
    shaped (an empty seed for a correction skill).
    """

    term = seed.get("term", "")
    target = seed.get("target", "")
    lower = remark.lower()

    if skill in DRAFT_SKILLS:
        # A structural opening remark ("substance by sentence N", "buries the
        # lede") becomes a positional assertion rather than a negative one.
        sentence = re.search(r"sentence (\w+)", lower)
        if "lede" in lower or "substance" in lower or sentence:
            n = sentence.group(1) if sentence else "two"
            return f"The opening reaches substance by sentence {n}, not later."
        if term:
            return f"A fresh draft must not contain {_emphasise(term)} (flagged in the source session as a register fault)."
        return None

    # Correction skills: name the fault and, when given, the correction.
    if not term:
        return None
    if target:
        return f"{_emphasise(term)} is corrected to {_emphasise(target)}."
    return f"{_emphasise(term)} is flagged and corrected."


def _diff_before(diff: str) -> str:
    """Reconstruct the 'before' side of a unified diff (removed and context lines)."""
    lines: list[str] = []
    for line in diff.splitlines():
        if line.startswith("+"):
            continue
        lines.append(line[1:] if line.startswith("-") else line)
    return "\n".join(line for line in lines if line.strip())


def propose(transcript_path: pathlib.Path) -> dict:
    """Read a transcript and propose a candidate eval case without writing anything.

    The maintainer's running feedback is the primary fault source; each remark
    becomes a dimension-tagged assertion shaped for the skill and traced back to
    its remark. For a correction skill the diff's 'before' side becomes the
    input fixture; for a draft skill the prompt is the brief. All proposed text
    is anonymised.
    """

    text = pathlib.Path(transcript_path).read_text(encoding="utf-8")
    parsed = parse_transcript(text)
    header = parsed["header"]
    skill = header.get("skill", "")
    language = header.get("language", "")
    prompt = header.get("prompt", "")

    # Build the dimension-tagged assertions, each carrying the verbatim remark it
    # traces to so the ratification step can show provenance.
    expectations: list[dict] = []
    for remark in parsed["feedback"]:
        for seed in _faults_from_remark(remark):
            shaped = _shape_assertion(skill, seed, remark)
            if shaped is None:
                continue
            expectations.append(
                {
                    "text": shaped,
                    "dimension": classify(shaped),
                    "source": remark,
                }
            )

    case: dict = {
        "skill_name": skill,
        "language": language,
        "prompt": anonymise(prompt),
        "expected_output": "",
        "expectations": expectations,
    }

    # A correction skill grades a fix of an input; a draft skill works from a
    # brief and produces a fresh draft with no input to correct.
    if skill in CORRECTION_SKILLS:
        case["input_text"] = anonymise(_diff_before(parsed["diff"]))
        case["brief"] = ""
    else:
        case["input_text"] = ""
        case["brief"] = anonymise(prompt)

    return case


def commit(case: dict, *, suite_path: pathlib.Path = SUITE_PATH, skill_root: pathlib.Path = EVALS) -> int:
    """Append a ratified case to the suite and regenerate the per-skill files.

    Invoked only after the maintainer ratifies. The case is appended to the
    aggregated suite in object form — each assertion flattened to `{text,
    dimension}`, dropping the proposal-only `source` trace — under a fresh id.
    The per-skill files are then regenerated, flattening each assertion to its
    plain text so the exports still validate against the stock skill-creator
    schema. Returns the id assigned to the committed case.
    """

    suite = json.loads(pathlib.Path(suite_path).read_text(encoding="utf-8"))
    evals = suite.setdefault("evals", [])

    # Assign the next free id above the current maximum.
    new_id = (max((c.get("id", 0) for c in evals), default=0)) + 1

    # Flatten each proposed assertion to object form, dropping the source trace.
    object_expectations = [
        {"text": exp["text"], "dimension": exp["dimension"]}
        for exp in case["expectations"]
    ]

    record = {
        "id": new_id,
        "skill_name": case["skill_name"],
        "name": case.get("name") or f"captured-{case['skill_name']}-{new_id}",
        "language": case["language"],
        "prompt": case["prompt"],
        "files": case.get("files", []),
        "expected_output": case.get("expected_output", ""),
        "expectations": object_expectations,
    }
    evals.append(record)
    pathlib.Path(suite_path).write_text(
        json.dumps(suite, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    _regenerate_per_skill(suite, skill_root)
    return new_id


def _regenerate_per_skill(suite: dict, skill_root: pathlib.Path) -> None:
    """Write the per-skill `<skill>/evals.json` files, flattening to plain strings.

    Mirrors the regeneration one-liner in `evals/README.md`: each `{text,
    dimension}` assertion collapses to its text so the per-skill exports match
    the stock skill-creator schema (a flat list of strings). A still-flat
    assertion (a plain string) passes through unchanged.
    """

    for skill in PER_SKILL:
        cases = []
        for case in suite["evals"]:
            if case.get("skill_name") != skill:
                continue
            flat = dict(case)
            flat["expectations"] = [
                exp["text"] if isinstance(exp, dict) else exp
                for exp in case.get("expectations", [])
            ]
            cases.append(flat)
        out = skill_root / skill / "evals.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(
            json.dumps({"skill_name": skill, "evals": cases}, indent=2, ensure_ascii=False)
            + "\n",
            encoding="utf-8",
        )


def main(argv: list[str]) -> int:
    """CLI surface for the propose step (the ratify-and-commit step is interactive).

    `propose <transcript>` prints the candidate case as JSON so the SKILL.md
    flow can show it for line-by-line ratification. Committing is deliberately
    not a bare CLI flag: nothing is persisted until the maintainer ratifies, so
    the commit path is exercised by the harness and invoked by the flow only
    after ratification.
    """

    parser = argparse.ArgumentParser(description="Propose an eval case from a session transcript.")
    parser.add_argument("transcript", type=pathlib.Path, help="Path to the capture transcript.")
    args = parser.parse_args(argv)

    case = propose(args.transcript)
    print(json.dumps(case, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
