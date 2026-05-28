#!/usr/bin/env python3
"""One-shot authoring script for v0.5.5 eval refinements.

Applies the four authoring deliverables in a single pass over evals.json:

  Task 2 — Rewrite case 404 assertion 5 to an observable form.
  Task 3 — Append a protocol-semantic paired assertion to the 19 cases that
           passed 100% without_skill in iteration-1 (identified by directly
           reading iteration-1 grading.json files; the IDs are hardcoded
           because the list is stable for this release).
  Task 4 — Add five negative-control cases (clean text → preserve, do not
           over-correct) covering proofread sv/en_GB/en_US, redline sv, and
           edit en_GB.
  Task 5A — Add three Phase 3 dialogue cases (simulated user response
            scripted in the prompt) for /redline.

Idempotent in spirit but not enforced — running twice will append the
paired assertion twice. Run once per release cycle.
"""

from __future__ import annotations

import json
import pathlib

REPO = pathlib.Path(__file__).resolve().parents[2]
EVALS = REPO / "evals" / "evals.json"
data = json.loads(EVALS.read_text())

# Build an id -> case lookup for in-place mutation.
by_id: dict[int, dict] = {c["id"]: c for c in data["evals"]}


# Task 2 — Rewrite case 404 assertion 5 to observable form.
case_404_old_assertion = (
    "The standard-flow output reflects the article-genre review-scoped rules "
    "from `lib/genres/article.md`; no behaviour beyond what the article genre "
    "prescribes is introduced by the genre-resolution detour — the fast-path "
    "is a dedup of the same downstream rules, not a behaviour change."
)
case_404_new_assertion = (
    "The findings list (`## Findings` in the transcript) includes at least one "
    "finding that cites a review-scoped section of `lib/genres/article.md` — "
    "specifically the repetition rule between H1, standfirst, lead and first H2, "
    "OR one of the documented common pitfalls (visible ABT formula, standfirst "
    "and lead repeating each other, teasing subheadings, explicit bridges). "
    "This is the observable consequence of the standard flow loading the genre "
    "file's review-scoped sections."
)
case_404 = by_id[404]
assert case_404["expectations"][4] == case_404_old_assertion, "case 404 assertion 5 has drifted"
case_404["expectations"][4] = case_404_new_assertion


# Task 3 — Paired protocol-semantic assertions for the 19 non-discriminating cases.
PROOFREAD_PAIR = (
    "`## Language resolution` in the transcript names `lib/languages/{lang}.md` "
    "as the loaded language file and identifies the *Mechanics* section as the "
    "applied scope (proofread is Phase-1-only). The without-skill baseline does "
    "not produce this scope record — the skill's value is that the loaded rule "
    "set is documented, not just that the right corrections happen to be made."
)
REDLINE_PAIR = (
    "`## Genre / technique resolution` in the transcript names the committed "
    "genre and documents whether the fast-path exited or the standard flow read "
    "`lib/genres/_index.md` and the matching genre file. The without-skill "
    "baseline does not produce this resolution record — the skill's value is "
    "the explicit genre commitment that scopes the review pass."
)
EDIT_PAIR = (
    "`## Genre / technique resolution` records both the committed genre and the "
    "committed technique, and `## Phase log` includes a Phase 2 entry citing "
    "`lib/rules/style.md` as the applied style foundation. The without-skill "
    "baseline does not produce these structured records — the skill's value is "
    "the protocol fidelity behind the corrections, not the corrections alone."
)

paired_proofread = {
    4: "sv",
    5: "sv",
    11: "en_GB",
    12: "en_GB",
    14: "en_US",
    15: "en_US",
    16: "en_US",
    17: "en_US",
    18: "en_US",
}
for cid, lang in paired_proofread.items():
    by_id[cid]["expectations"].append(PROOFREAD_PAIR.format(lang=lang))

paired_redline = (105, 114, 115, 116, 118)
for cid in paired_redline:
    by_id[cid]["expectations"].append(REDLINE_PAIR)

paired_edit = (205, 211, 214, 215, 218)
for cid in paired_edit:
    by_id[cid]["expectations"].append(EDIT_PAIR)


# Task 4 — Negative-control cases.
negative_cases = [
    {
        "id": 19,
        "skill_name": "proofread",
        "name": "sv-negative-clean-text",
        "language": "sv",
        "prompt": "/proofread sv",
        "files": ["evals/fixtures/sv-clean-text.md"],
        "expected_output": (
            "Input already follows Swedish mechanics conventions. Proofread "
            "delivers the text unchanged (or with at most a trivial change) "
            "and does not introduce false-positive 'corrections' such as "
            "removing the thin no-break space, converting curly quotes, or "
            "rewriting the time format."
        ),
        "expectations": [
            "The output text is unchanged from the input, OR any change is "
            "limited to whitespace-equivalent normalisation (no semantic edits).",
            "The thin no-break space (U+202F) inside `1 234 567` is preserved — "
            "not normalised to a regular space and not replaced by a comma or "
            "full stop.",
            "Swedish quotation marks ”…” (U+201D both sides) are preserved — "
            "not converted to straight ASCII \"…\" and not to curly “…”.",
            "Time `kl. 10.30` is preserved with a full stop — not changed to "
            "`10:30`.",
            "Genitive `Marx teorier` (zero-marking on -s name) is preserved — "
            "no apostrophe-s is inserted.",
            "`## Language resolution` in the transcript names "
            "`lib/languages/sv.md` and identifies the *Mechanics* section as "
            "the applied scope; the without-skill baseline lacks this record.",
        ],
    },
    {
        "id": 20,
        "skill_name": "proofread",
        "name": "en_GB-negative-clean-text",
        "language": "en_GB",
        "prompt": "/proofread en_GB",
        "files": ["evals/fixtures/en_GB-clean-text.md"],
        "expected_output": (
            "Input already follows British English mechanics. Proofread "
            "preserves -ise/-our spellings, omits the Oxford comma in the "
            "list, and does not Americanise the text."
        ),
        "expectations": [
            "The output text is unchanged from the input, OR any change is "
            "limited to whitespace-equivalent normalisation.",
            "British spellings *analyse*, *refurbishment*, *metres* are "
            "preserved — not changed to *analyze*, *remodeling*, *meters*.",
            "The series `readings, music and short workshops` is preserved "
            "without an Oxford comma (British convention).",
            "Single quotation marks `'…'` around the librarian quote are "
            "preserved — not converted to double quotes.",
            "The abbreviation `Department for Transport` and its currency "
            "format `£1,234,567` are preserved — not Americanised.",
            "`## Language resolution` names `lib/languages/en_GB.md` and "
            "identifies the *Mechanics* section as the applied scope; the "
            "without-skill baseline lacks this record.",
        ],
    },
    {
        "id": 21,
        "skill_name": "proofread",
        "name": "en_US-negative-clean-text",
        "language": "en_US",
        "prompt": "/proofread en_US",
        "files": ["evals/fixtures/en_US-clean-text.md"],
        "expected_output": (
            "Input already follows American English mechanics. Proofread "
            "preserves -ize/-or spellings, keeps the Oxford comma, and does "
            "not Britishise the text."
        ),
        "expectations": [
            "The output text is unchanged from the input, OR any change is "
            "limited to whitespace-equivalent normalisation.",
            "American spellings *analyze*, *renovation*, *feet* are "
            "preserved — not changed to British equivalents.",
            "The series `readings, music, and short workshops` is preserved "
            "with the Oxford comma (American convention).",
            "Double quotation marks `\"…\"` around the librarian quote are "
            "preserved — not converted to single quotes.",
            "Time format `10:30 a.m.` is preserved with the colon and the "
            "lowercase periods (American convention).",
            "`## Language resolution` names `lib/languages/en_US.md` and "
            "identifies the *Mechanics* section as the applied scope; the "
            "without-skill baseline lacks this record.",
        ],
    },
    {
        "id": 119,
        "skill_name": "redline",
        "name": "sv-negative-clean-press-release",
        "language": "sv",
        "prompt": "/redline sv",
        "files": ["evals/fixtures/sv-clean-press-release.md"],
        "expected_output": (
            "A clean Swedish press release with proper genre conventions. "
            "Redline produces zero or near-zero findings. The dialogue phase "
            "is short or noted as not entered. No false-positive style "
            "findings are raised."
        ),
        "expectations": [
            "`## Findings` is empty or contains at most one minor finding "
            "(no wall of false positives).",
            "If any finding is raised, the transcript justifies it with a "
            "concrete citation from a loaded rule or genre file — no `## "
            "Findings` items are added on vibes.",
            "`## Genre / technique resolution` commits to `press-release` "
            "(or the closest matching genre) based on the structural "
            "markers — not to the default `general` fallback.",
            "Output is identical or near-identical to the input — no "
            "spurious style rewrites of clean sentences.",
            "`## Phase log` records Phase 3 entered briefly (or skipped if "
            "no findings); the dialogue is not artificially inflated to "
            "demonstrate the protocol on a clean text.",
        ],
    },
    {
        "id": 219,
        "skill_name": "edit",
        "name": "en_GB-negative-clean-essay",
        "language": "en_GB",
        "prompt": "/edit en_GB",
        "files": ["evals/fixtures/en_GB-clean-essay.md"],
        "expected_output": (
            "A clean British English essay-style text. Edit produces a "
            "polished version with minimal substantive changes; protocol "
            "fidelity is the testable signal, not the volume of edits."
        ),
        "expectations": [
            "`## Findings` raises at most a small number of substantive "
            "items (no wall of false positives on clean prose).",
            "British conventions are preserved: -ise spellings, no Oxford "
            "comma in standard series, single quotation marks, £ currency, "
            "metric units with no-break space (`21 °C`, `320 square metres`).",
            "`## Genre / technique resolution` commits to the closest "
            "matching genre — `column` or `general` — and names a technique "
            "if the genre's `default_technique` is not `none`.",
            "`## Phase log` includes a Phase 2 entry citing `lib/rules/"
            "style.md` as the applied style foundation.",
            "Any change applied in the edit is traceable to a finding in "
            "the transcript — no silent rewrites.",
        ],
    },
]
data["evals"].extend(negative_cases)


# Task 5A — Phase 3 dialogue cases (simulated user response).
dialogue_cases = [
    {
        "id": 409,
        "skill_name": "redline",
        "name": "phase-3-dialogue-mixed-accept-reject-counter",
        "language": "sv",
        "prompt": (
            "/redline sv. Du presenterar fynden ett i taget. För denna körning "
            "scriptar jag mina svar i förväg: jag accepterar fynd 1 (svar: "
            "”OK, kör”), avvisar fynd 2 (svar: ”nej, lämna det”), kontrar fynd "
            "3 med en alternativ formulering du själv väljer som passar texten "
            "och som du tycker är substansmässigt minst lika bra som ditt "
            "original (svar: ”jag föreslår istället: <din alternativa "
            "formulering>”). För fynd 4 och framåt: accept på allt. Visa hela "
            "dialog-loopen i `## Phase log` med en rad per fynd och min "
            "scriptade respons."
        ),
        "files": ["evals/fixtures/sv-article.md"],
        "expected_output": (
            "Final polished text reflecting the scripted decisions: finding 1 "
            "applied, finding 2 dropped, finding 3 applied in the executor's "
            "counter-form, findings 4+ applied. Transcript Phase log records "
            "each branch."
        ),
        "expectations": [
            "`## Phase log` records Phase 3 entered with finding-by-finding "
            "presentation (one row per finding minimum).",
            "Finding 1 is recorded as ACCEPTED in the Phase log; the proposed "
            "change appears in `output.md`.",
            "Finding 2 is recorded as REJECTED in the Phase log; the proposed "
            "change does NOT appear in `output.md`.",
            "Finding 3 is recorded as a COUNTER in the Phase log; the "
            "executor's alternative formulation is named in the transcript "
            "and that alternative (not the original proposal) appears in "
            "`output.md`.",
            "Findings 4 and onward are recorded as ACCEPTED in the Phase log; "
            "those changes appear in `output.md`.",
            "The without-skill baseline does not produce a structured Phase 3 "
            "record — the skill's value is the per-finding accountability.",
        ],
    },
    {
        "id": 410,
        "skill_name": "redline",
        "name": "phase-3-dialogue-delegate-with-max-iterations",
        "language": "en_GB",
        "prompt": (
            "/redline en_GB --max-iterations=2. You present the findings one "
            "at a time. My scripted responses for this run: I accept finding "
            "1 ('OK'). I accept finding 2 ('yes, apply it'). After finding 2 "
            "I delegate the rest ('just do the rest, you decide'). Record "
            "the subagent ceiling N that `subagent.md` would be invoked with "
            "on the open tail — N comes from the `--max-iterations=2` flag, "
            "not natural language."
        ),
        "files": ["evals/fixtures/en_GB-article.md"],
        "expected_output": (
            "Findings 1 and 2 settled in dialogue (both accepted). The "
            "remaining open tail is delegated to subagent.md with N=2 from "
            "the flag. The polished text is delivered without a user-facing "
            "summary of internal work."
        ),
        "expectations": [
            "`## Phase log` records findings 1 and 2 as ACCEPTED via the "
            "dialogue protocol.",
            "`## Phase log` records the user's delegation signal after "
            "finding 2 ('just do the rest' or close paraphrase).",
            "`## Subagent ceiling` records N=2 and identifies the source as "
            "the `--max-iterations=2` flag (not a natural-language phrase, "
            "not the default 0, not the last-resort floor).",
            "`## Phase log` notes that `lib/protocols/subagent.md` would be "
            "invoked on the open tail with N=2 (executor records what the "
            "subagent would do; no actual sub-subagent is spawned per the "
            "executor instructions).",
            "`output.md` contains the polished text only — no user-facing "
            "summary of which findings were settled by the subagent.",
        ],
    },
    {
        "id": 411,
        "skill_name": "redline",
        "name": "phase-3-dialogue-counter-defended",
        "language": "sv",
        "prompt": (
            "/redline sv. Du presenterar fynden ett i taget. Scriptade svar: "
            "fynd 1 accept (”OK”). För fynd 2, om du föreslår ett mer "
            "publikvänligt språk: jag kontrar med argumentet att "
            "originalformuleringen är fackspråk som målgruppen "
            "(branschkollegor) förväntar sig (svar: ”nej, behåll original — "
            "fackspråk är vad målgruppen vill ha”). Du ska antingen försvara "
            "ditt ursprungliga förslag med en konkret hänvisning till en "
            "regel- eller genre-aspekt, eller acceptera mitt motargument och "
            "behålla originalet — och transkripten ska göra klart vilket. "
            "Resten av fynden: accept."
        ),
        "files": ["evals/fixtures/sv-press-release.md"],
        "expected_output": (
            "Finding 1 accepted. Finding 2 — the executor either defends "
            "with a concrete citation from a loaded rule/genre file, or "
            "adopts the user's counter and drops the proposal. The choice "
            "and its justification are explicit in the transcript. Remaining "
            "findings accepted."
        ),
        "expectations": [
            "Finding 1 is recorded as ACCEPTED in `## Phase log`.",
            "The user's counter on finding 2 ('fackspråk är vad målgruppen "
            "vill ha' or close paraphrase) is quoted or summarised in the "
            "Phase log.",
            "The executor's response on finding 2 is explicit: either (a) "
            "DEFENDS the original proposal with a concrete citation from a "
            "loaded file (a rule name + a one-line reason), or (b) ADOPTS "
            "the user's counter and drops the proposal. The transcript "
            "states which branch was taken.",
            "If (a) defended: the original proposal appears in `output.md`. "
            "If (b) adopted: the original proposal does NOT appear in "
            "`output.md`.",
            "Remaining findings (3+) are accepted in sequence; corresponding "
            "changes appear in `output.md`.",
            "The transcript shows substantive engagement — no 'you're right, "
            "I agree' without analysis (sycophancy fail), no 'no, my "
            "proposal stands' without citation (stubborn fail).",
        ],
    },
]
data["evals"].extend(dialogue_cases)


# Sort by id for stable diff and deterministic per-skill regeneration.
data["evals"].sort(key=lambda e: e["id"])


# Write back with the same formatting conventions as the original file
# (indent=2, ensure_ascii=False, trailing newline).
EVALS.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")

# Report.
total_cases = len(data["evals"])
total_assertions = sum(len(e["expectations"]) for e in data["evals"])
print(f"OK — {total_cases} cases, {total_assertions} assertions written to {EVALS}")
