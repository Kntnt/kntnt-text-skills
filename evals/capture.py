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


# The maintainer wraps each feedback remark in an outer pair of quotes — a
# straight `"` or a smart left/right double quote (U+201C / U+201D). The opening
# and closing classes hold each character once, and the capture is greedy so the
# match runs from the first opening quote to the LAST closing quote on the line:
# a remark that itself contains an inner smart-quoted span ("the phrase ”as
# such” is filler") is then kept whole rather than truncated at the first inner
# quote. A non-greedy capture would stop at that inner quote and silently drop
# any fault named after it.
_OUTER_QUOTE = re.compile(r"[\"“”](.+)[\"“”]")


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
        quote = _OUTER_QUOTE.search(bullet)
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

# Ordinary capitalised prose words that are not names: pronouns, articles and
# connectives that legitimately open a sentence in Swedish or English. These are
# kept in place so a sentence-initial capital is not mistaken for a company. The
# set holds GENUINE prose words only — never a proper name from a fixture: a name
# placed here would leak whenever it stood alone, which is exactly the failure a
# real capture must avoid. It is necessarily incomplete (a capitalised real word
# this list misses still over-scrubs, and a real name that happens to be a
# sentence-opener here would slip through), so the heuristic is a first pass the
# maintainer reviews in Phase 2, not a robust named-entity recogniser.
_NAME_STOPWORDS = frozenset(
    {
        # Swedish sentence-openers, pronouns and connectives.
        "Vi", "Du", "Det", "Den", "De", "Han", "Hon", "Jag", "Ni",
        "Bra", "Och", "Men", "Att", "Som", "Här", "Där", "Detta",
        # English sentence-openers, articles, pronouns and connectives.
        "In", "It", "The", "A", "An", "We", "I", "You", "They", "He",
        "She", "This", "That", "These", "Those", "And", "But", "Here",
        "There", "District",
    }
)


def anonymise(text: str) -> str:
    """Replace proper-name spans (people, companies, products) with placeholders.

    A name is a capitalised single word or multi-word run. A multi-word span
    reads as a person and scrubs as one unit (*Anna Lindqvist* → *[Person 1]*);
    a single-word span whose token is not an ordinary capitalised prose word
    reads as a company or product (*Volvo* → *[Company 1]*). Single first names
    that stand alone (*Erik*) scrub the same way, because the stopword set holds
    only genuine prose words, never fixture names. Lowercase fault vocabulary
    that assertions depend on — *adressera*, *leverera* — is never touched
    because it is not capitalised. A single pass over the original text rules out
    re-scanning emitted placeholders, and distinct spans map to stable, numbered
    placeholders so a span used twice scrubs to the same token.

    The heuristic is capitalisation plus a prose-word allowlist, not robust NER:
    a capitalised real word the allowlist misses can over-scrub, and a real name
    coinciding with an allowlisted opener can slip through. That is why `/eval`
    proposes — the maintainer reviews the scrubbed fixture line by line in Phase
    2 before anything is committed (see the eval SKILL.md), so a residual leak is
    human-catchable rather than silently shipped.
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


# Connectives that introduce a correction target after a flagged fault, in the
# Swedish and English the maintainer's remarks use ("ska bli", "måste bli", "byt
# till", "becomes", "→", …). A connective is honoured only when an *emphasised*
# target follows it: an incidental connective word in ordinary prose ("needs to
# go") then captures nothing, so no fabricated correction is invented.
_TARGET_CONNECTIVE = (
    r"(?:ska\s+(?:bli|vara)|m[åa]ste\s+bli|byt(?:\s+\w+)?\s+till|"
    r"[äa]ndra(?:\s+\w+)?\s+till|ers[äa]tt(?:\s+\w+)?\s+med|"
    r"blir|→|->|becomes?|should\s+(?:become|be)|corrected\s+to|"
    r"chang(?:e[ds]?|ing)(?:\s+\w+)?\s+to|replace[ds]?\s+with)"
)

# An emphasised correction target, optionally one of several alternatives the
# maintainer offered (joined by a coordinating "eller"/"or"/"och"/"and"), e.g.
# "byt till *ta upp* eller *behandla*". All listed alternatives are corrections,
# not faults. Only conjunctions join alternatives — a comma or semicolon usually
# separates independent clauses (a second fault), so they are deliberately not
# alternative separators, keeping "…*ge värde*; *leverera*…" as two faults.
_ALT_SEP = r"\s*(?:eller|or|och|and)\s+"
# A fault that names its correction may put ordinary words between the fault span
# and the connective ("*utilise* is jargon, change to *use*"), so non-emphasised
# filler is allowed there. The filler is `[^*]*?` — it stops at the next `*`, so
# an intervening emphasised span (a second fault) is never swallowed into this
# pairing; that span pairs on its own match or stands alone as its own fault.
_FAULT_TO_TARGETS = re.compile(
    rf"\*([^*]+)\*[^*]*?{_TARGET_CONNECTIVE}\s*"
    rf"\*([^*]+)\*(?:{_ALT_SEP}\*([^*]+)\*)*",
    re.IGNORECASE,
)
_EMPHASISED_AFTER_CONNECTIVE = re.compile(
    rf"{_TARGET_CONNECTIVE}\s*\*([^*]+)\*(?:{_ALT_SEP}\*([^*]+)\*)*",
    re.IGNORECASE,
)


def _faults_from_remark(remark: str) -> list[dict]:
    """Derive zero or more assertion seeds from one maintainer feedback remark.

    A seed is `{term, target}` where `term` is the flagged fault and `target` is
    the correction the maintainer named (empty when none). Affirmations — "good
    that you kept X, no change needed" — yield nothing, because a case asserts
    faults to catch, not things already correct.

    A single remark may flag several distinct faults ("*leverera värde* ska bli
    *ge värde*; *leverera* metaforiskt är en anglicism" names two), so every
    emphasised span that is *not* itself a named correction becomes its own seed
    rather than collapsing the bullet to one fault. Correction targets — the
    emphasised spans after a "ska bli" / "byt till" / "becomes" connective, and
    any alternatives the maintainer listed — are excluded from the fault set; a
    fault that names its correction carries that target as its `target`.
    """

    lower = remark.lower()
    # Affirmations carry no fault: an explicit "no change needed" / "bra att du
    # behöll" remark is praise, not a planted fault, so it seeds no assertion.
    if "inga ändringar" in lower or "no change" in lower or (
        "bra att" in lower and "behöll" in lower
    ):
        return []

    # Resolve which emphasised spans are correction targets (after a connective,
    # including listed alternatives) so a target is never proposed as a fault,
    # and pair each fault that names its correction with that first target.
    targets: set[str] = set()
    for match in _EMPHASISED_AFTER_CONNECTIVE.finditer(remark):
        targets.update(group.strip() for group in match.groups() if group)
    pair_target: dict[str, str] = {}
    for match in _FAULT_TO_TARGETS.finditer(remark):
        pair_target[match.group(1).strip()] = match.group(2).strip()

    # Every emphasised span that is not itself a correction target is a fault;
    # each becomes its own seed so several faults in one bullet are all kept.
    terms = [term.strip() for term in re.findall(r"\*([^*]+)\*", remark)]
    faults = [term for term in terms if term not in targets]

    if not faults:
        # No emphasised fault term: fall back to the remark itself as the fault
        # description so a numeric/structural remark still seeds an assertion.
        return [{"term": "", "target": "", "raw": remark}]
    return [
        {"term": term, "target": pair_target.get(term, ""), "raw": remark}
        for term in faults
    ]


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


def _classify_assertion(skill: str, shaped: str, remark: str) -> str:
    """Classify an assertion's dimension from the right source for its skill.

    For a correction skill the shaped text is "*fault* is corrected to *target*"
    — a template that discards every word the maintainer used to name the fault,
    so the maintainer's own classification (an "anglicism", a "thousands
    separator") would be lost and the assertion would mis-tag as the mechanics
    fallback. Classifying from the source remark together with the shaped text
    keeps the maintainer's explicit register/mechanics signal while still seeing
    the emphasised terms. Draft skills already shape the fault verbatim into the
    assertion, so the shaped text alone classifies them faithfully.
    """

    if skill in CORRECTION_SKILLS:
        return classify(f"{remark} {shaped}")
    return classify(shaped)


def _diff_before(diff: str) -> str:
    """Reconstruct the 'before' side of a unified diff (removed and context lines).

    Every unified-diff line is a one-char marker (`-` removed, `+` added, space
    context) followed by a single separating space and the text. Added lines are
    dropped; for the rest the marker and its one separating space are stripped so
    the reconstructed text matches the source verbatim — keeping the space would
    leave a stray leading blank on every committed input line.
    """
    lines: list[str] = []
    for line in diff.splitlines():
        if line.startswith("+"):
            continue
        # Strip the marker plus its single separating space; a context line's
        # marker is itself a space, so the same two-char slice applies.
        lines.append(line[2:] if line[:1] in "- " else line)
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

    # Build the dimension-tagged assertions. The assertion `text` is the part
    # that lands in the committed suite (commit() keeps only {text, dimension}),
    # so it is anonymised: a name the maintainer cites inside a fault remark —
    # *Marx's teorier*, an *Acme delivers value* phrase — otherwise survives
    # verbatim into evals.json, the one leak the fixture-body scrub never reached.
    # The `source` trace stays verbatim: it is a proposal-only aid the maintainer
    # reads during ratification to recognise their own remark and is dropped on
    # commit, so scrubbing it would only blur provenance without protecting the
    # committed object. Classification keys off the unscrubbed shaped text and
    # remark, where the lowercase fault vocabulary anonymisation never touches
    # still carries the register/mechanics signal.
    expectations: list[dict] = []
    for remark in parsed["feedback"]:
        for seed in _faults_from_remark(remark):
            shaped = _shape_assertion(skill, seed, remark)
            if shaped is None:
                continue
            expectations.append(
                {
                    "text": anonymise(shaped),
                    "dimension": _classify_assertion(skill, shaped, remark),
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
