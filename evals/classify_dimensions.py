# /// script
# requires-python = ">=3.12"
# ///
"""Classify each eval assertion into a scoring dimension.

The eval suite scores three dimensions (issue #44): `protocol` (the hard
release gate — genre commit, fast-path, fallback, overlay, max-iterations,
last-resort, phase ordering), `mechanics` (typography, spelling, quotation
marks, genitive — also part of the hard gate), and `register` (anglicism
interference, AI-tell removal, address and voice — the improvement target
reported separately).

`classify` encodes the editorial judgement for the migration of
`evals/evals.json` from flat strings to `{text, dimension}` objects. The
rules are tuned so the classifier output matches that judgement directly:
where a real assertion was found mis-tagged, the fix is a marker here, not a
one-off override on the committed file. The committed suite is verified to
match this classifier (re-running `classify` over it must report zero
divergences); a divergence means either the suite or a rule here needs
attention. Keeping the rules in code makes a re-classification reproducible
if assertions change, and documents why each assertion carries the dimension
it does.

Run `uv run evals/classify_dimensions.py` to print a classification of the
current suite (text, proposed dimension) without writing anything;
`--write` migrates `evals/evals.json` in place, preserving assertion order
and text verbatim and leaving any assertion already in object form
untouched.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
SUITE_PATH = REPO / "evals" / "evals.json"

# Protocol-discipline overrides: false-positive restraint and dialogue
# discipline read like register at the substring level (they mention style
# rewrites, "you", or stance) but assert a *behaviour* the hard gate must
# hold — the negative-control restraint and the Phase 3 counter-defence — not
# a property of the produced prose. They win first so the broad register and
# regex cues below do not pull them into the improvement score. The baseline
# doc groups these with the negative-control and dialogue protocol records.
PROTOCOL_OVERRIDE_MARKERS = (
    "false positive",
    "no wall of",
    "on vibes",
    "spurious style rewrite",
    "no spurious",
    "identical or near-identical",
    "substantive engagement",
    "sycophancy",
    "stubborn",
    "canonical section order",
    "section order and heading",
    # The fast-path short-text restraint check ("findings ... are short and
    # reflect the everyday-text register") is a false-positive / negative-
    # control assertion: clean everyday prose must yield few findings. It
    # names the everyday-text register only to describe the input, not to
    # score the produced prose, so it belongs with the protocol restraint
    # records — not the register improvement target. It wins ahead of the
    # register markers below for that reason.
    "short and reflect",
    # The genre/technique-resolution record asserts that the Phase log
    # documents the committed genre and that the style-layer pass ran — a
    # protocol record, even though its evidence list enumerates style.md's
    # AI-tell and address/voice categories as acceptable proof.
    "genre / technique resolution",
    "## phase log",
    # The fast-path negative-control discriminator and the flow-load
    # consequence in the structured-article case. "Either condition broken …"
    # is the discriminator proving the standard flow ran rather than the
    # fast-path; "… the observable consequence of the standard flow loading
    # the genre file's review-scoped sections" names that flow-load outcome.
    # Both assert the protocol path, not an output-form property, and would
    # otherwise drop to the mechanics fallback.
    "condition broken",
    "observable consequence",
    # The proofread-scope and output-unchanged restraint checks: clean input
    # must come back unchanged save for mechanics normalisation. Like the
    # "no spurious style rewrites" record they are negative-control restraint
    # on the skill's scope discipline, not a property of produced prose, so
    # they belong with the protocol restraint records rather than the mechanics
    # fallback they previously dropped to.
    "proofread scope only",
    "unchanged from the input",
)

# Mechanics-discipline overrides: a structural assertion whose graded
# content is a verbatim line, a badge-row shape or a section layout reads as
# register only through a trailing "no AI-tell openings" clause. The dominant
# graded content is structural, so it scores in the hard gate, not the
# improvement target. Checked before the register markers for that reason.
MECHANICS_OVERRIDE_MARKERS = (
    "verbatim line",
    # A "British conventions are preserved" assertion grades spelling,
    # quotation marks and the genitive — mechanics — and only tacks the
    # no-silent-rewrite traceability restraint on as a trailing clause. The
    # dominant graded content is the convention set, so it stays in the hard
    # gate. This override is what keeps such an assertion mechanics where its
    # near-twin — a bare "traceable to a finding … no silent rewrites" line
    # with no convention lead — classifies protocol via the restraint cue
    # below, because the override is checked before that cue is reached.
    "british conventions are preserved",
)

# Register: the substitution and AI-tell vocabulary that the style layer
# targets. Matching any of these marks the assertion as a register concern —
# the thing the suite now tracks as a separate, unblocking improvement score.
REGISTER_MARKERS = (
    "anglicism",
    "ai-tell",
    "ai vocabulary",
    "ai tell",
    "calque",
    "interference",
    "jargon",
    "cliché",
    "cliche",
    "opening cliché",
    "formulaic",
    "crutch",
    # Canonical AI-tell openers and conclusion clichés named by their bare
    # phrasing. Some assertions list these tells without using a category word
    # like "ai-tell" or "calque" (e.g. "*In a world where…*, *It's worth
    # noting that…* are flagged"), so they would otherwise fall through to the
    # mechanics default despite naming the exact same register concern their
    # near-identical siblings tag register. Matching the phrases themselves
    # keeps that concern in the register score.
    "in a world where",
    "i en värld där",
    "it's worth noting",
    "det är värt att notera",
    "let me be perfectly clear",
    "sammanfattningsvis",
    "to summarize",
    "to summarise",
    "dyk djupare",
    "delve",
    "leverage",
    "multifaceted",
    "tapestry",
    "robust",
    "comprehensive",
    "streamline",
    "game-changer",
    "paradigm shift",
    "next-generation",
    "circle back",
    "touch base",
    "holistic",
    "synergies",
    "proactive",
    "going forward",
    "reach out",
    "adressera",
    "navigera",
    "leverera",
    "metrik",
    "regulator",
    "false balance",
    "free language is permitted",
)

# Protocol: the procedural behaviour the hard gate must hold. These name a
# path the skill takes (which genre it commits to, whether the fast-path
# exited, how a natural-language iteration count parsed) rather than a
# property of the output text.
PROTOCOL_MARKERS = (
    "fast-path",
    "fast path",
    "max-iterations",
    "max iterations",
    "subagent",
    "last-resort",
    "last resort",
    "fallback",
    "overlay",
    "genre resolves",
    "genre commits",
    "genre is committed",
    "genre is still committed",
    "genre / technique resolution",
    "genre still committed",
    "default_technique",
    "default technique",
    "technique file",
    "technique override",
    "ceiling of",
    "iteration",
    "convergence",
    "phase 1",
    "phase 2",
    "phase 3",
    "phase 4",
    "phase log",
    "dialogue protocol",
    "bypass behaviour",
    "propose mode",
    "language resolves",
    "language resolution",
    "scope record",
    "scope; the without-skill",
    "applied scope",
    "loaded language file",
    "briefing fields",
    "audience layering",
    "settles the finding",
    "settle each finding",
    "main agent",
    "no subagent",
    "fast-path exits",
    "no technique file",
    "is parsed to",
    "honoured",
    "no field is silently filled",
    "no post-draft",
    "no user dialogue",
    "delegate",
    # Procedural assertions whose phrasing carries no protocol keyword above
    # and would otherwise drop to the mechanics fallback. Each names a path or
    # rule the hard gate must hold: the overlay inheritance depth and the
    # style-layer carry-through (overlay protocol); the genre-resolution read
    # and trigger-match; the flag-versus-phrase precedence and the
    # max-iterations clamp; the AFK no-dialogue contract; and the Phase 3
    # defend-or-adopt counter-defence with its acceptance sequence.
    "inheritance is one step",
    "does not itself inherit",
    "style h2 sections",
    "is read and trigger-matched",
    "the flag wins",
    "clamped to",
    "protocol maximum",
    "no user-facing dialogue",
    "afk variant",
    "which branch was taken",
    "if (a) defended",
    "accepted in sequence",
    # The no-silent-rewrite traceability discipline: every applied change
    # traces to a finding, nothing is rewritten silently. This is the same
    # negative-control restraint as the Phase-2-traceable records already
    # tagged protocol (#205/#211/#218); a bare line carrying only this cue
    # would otherwise drop to the mechanics fallback. It sits in the regular
    # protocol bucket rather than the override above so the mechanics override
    # still wins for a convention-led assertion that merely appends the clause.
    "no silent rewrites",
)

# Mechanics: objectively verifiable output form — typography, spelling,
# quotation marks, genitive. These are the proofread-scope conventions and
# also part of the hard gate.
MECHANICS_MARKERS = (
    "thousands separator",
    "decimal separator",
    "no-break space",
    "thin space",
    "en-dash",
    "em-dash",
    "en dash",
    "em dash",
    "quotation mark",
    "curly quote",
    "straight ascii",
    "speech dash",
    "talstreck",
    "genitive",
    "zero-marking",
    "zero marking",
    "apostrophe-s",
    "apostrophe",
    "oxford comma",
    "full stop",
    "initialism",
    "compound",
    "split-compound",
    "spelling",
    "-ize",
    "-ise",
    "-our",
    "-or ",
    "typography",
    "date format",
    "dates are",
    "time format",
    "time uses",
    "12-hour",
    "24-hour",
    "currency",
    "temperature",
    "degree sign",
    "percent in figures",
    "procent",
    "comma placement",
    "punctuation",
    "spellings",
)


def classify(text: str) -> str:
    """Return the scoring dimension for one assertion's text.

    Protocol-discipline overrides win first: a false-positive-restraint or
    dialogue-discipline assertion asserts a behaviour the hard gate holds,
    even though it mentions style rewrites or *you*. A mechanics override
    follows for assertions whose graded body is structural (a verbatim line,
    a badge row) or a preserved-conventions set, and whose only other-dimension
    cue is a trailing clause — a register AI-tell mention, or a no-silent-rewrite
    restraint addendum — that must not pull the dominant graded content out of
    the hard gate. Register wins next: an
    anglicism or AI-tell finding is a register concern even inside a
    phase-numbered sentence, because the substitution is the thing being
    scored. Protocol wins after that: a genre commit or iteration-parse
    assertion is procedural even when it names the conventions the committed
    genre will apply. Mechanics is the remaining typography / spelling /
    quotation / genitive bucket, and also the final fallback so every
    assertion is classified. The address-and-voice regex sits last because
    its cues (*you*, *stance*, *voice*) are weak on their own and must not
    outrank an explicit mechanics or protocol marker.
    """
    lowered = text.lower()
    if _matches(lowered, PROTOCOL_OVERRIDE_MARKERS):
        return "protocol"
    if _matches(lowered, MECHANICS_OVERRIDE_MARKERS):
        return "mechanics"
    if _matches(lowered, REGISTER_MARKERS):
        return "register"
    if _matches(lowered, PROTOCOL_MARKERS):
        return "protocol"
    if _matches(lowered, MECHANICS_MARKERS):
        return "mechanics"
    # Address-and-voice register cues that are awkward as bare substrings.
    if re.search(r"\b(address|voice|first-person|third-person|register)\b", lowered):
        return "register"
    return "mechanics"


def _matches(lowered: str, markers: tuple[str, ...]) -> bool:
    """True when any marker appears as a substring of the lowered assertion text."""
    return any(marker in lowered for marker in markers)


def migrate(suite: dict) -> int:
    """Rewrite every flat-string assertion to `{text, dimension}` in place; return the count migrated."""
    migrated = 0
    for case in suite["evals"]:
        new_expectations = []
        for exp in case["expectations"]:
            if isinstance(exp, dict):
                new_expectations.append(exp)
                continue
            new_expectations.append({"text": exp, "dimension": classify(exp)})
            migrated += 1
        case["expectations"] = new_expectations
    return migrated


def main() -> int:
    """Print or write the classification of the current suite per the CLI flags."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--write",
        action="store_true",
        help="Migrate evals/evals.json in place instead of printing the classification",
    )
    args = parser.parse_args()

    suite = json.loads(SUITE_PATH.read_text())
    if args.write:
        migrated = migrate(suite)
        SUITE_PATH.write_text(
            json.dumps(suite, indent=2, ensure_ascii=False) + "\n"
        )
        print(f"Migrated {migrated} assertions to object form in {SUITE_PATH}.")
        return 0

    for case in suite["evals"]:
        for exp in case["expectations"]:
            text = exp["text"] if isinstance(exp, dict) else exp
            print(f"{classify(text)}\t{case['skill_name']}\t{case['id']}\t{text}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
