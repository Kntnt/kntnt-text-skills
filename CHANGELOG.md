# Changelog

All notable changes to this project are documented here. The format follows [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/) and the versioning policy described in the project README.

History starts at **0.3.0** — the first version with a documented baseline. Earlier versions (0.1.0, 0.2.0) are not reconstructed here; the git log is the source for that prehistory.

## [Unreleased]

## [0.6.1] — 2026-05-29

### Changed

- **Help command rendering extracted into a standalone script.** `commands/help.md` no longer renders the help block in the model at invocation; it runs `scripts/help.py` (a PEP 723 script invoked via `uv run`) and prints the result verbatim inside a single fenced block. The script is the single source of truth — it reads `.claude-plugin/plugin.json` and every `skills/<name>/SKILL.md` and resolves the intro paragraphs, 80-character wrapping, column alignment, and single-space separator lines in code. Output is unchanged: bare invocation → overview, known skill name → detail, unknown argument → the one-line error. The command frontmatter gains `model: sonnet` and narrows `allowed-tools` to `Bash(uv:*)`. The change makes the layout deterministic (no model-rendering drift) at the cost of a `uv` dependency for the help command.
- **All project scripts brought onto the uv + PEP 723 runtime** per the coding standard. `scripts/audit.py` declares its only dependency (PyYAML) in PEP 723 inline metadata and runs via `uv run`; the `audit` CI job drops `actions/setup-python` + `pip install pyyaml` for `astral-sh/setup-uv` + `uv run scripts/audit.py`, and `.pre-commit-config.yaml` invokes it the same way. The four eval-harness scripts (`_setup.py`, `_runner.py`, `_prompts.py`, `_aggregate.py`) gain `requires-python` PEP 723 headers, lose their `#!/usr/bin/env python3` shebangs (they are internal scripts, not `bin/` commands), and their run instructions in `evals/README.md` / `evals/baseline.md` move to `uv run`. Every script gains full per-function docstrings; a one-off ruff pass (not wired into the project) removed two unused imports and one unused variable and formatted the files. Behaviour-neutral — the audit and eval pipelines produce identical results.
- **README refreshed** to match: the file-structure tree corrects `commands/kntnt-text-skills.md` → `commands/help.md` and lists `scripts/help.py`; the help-command and audit-checklist sections describe the `uv run` / PEP 723 mechanism; the eval-suite summary now names the Phase 3 dialogue and negative-control cases.

### Removed

- `evals/workspace/_author_055.py` — the one-shot authoring script that applied the v0.5.5 eval refinements (negative-control cases, Phase 3 dialogue cases, the case-404 rewrite, the paired assertions). Its mutations have been part of `evals/evals.json` since 0.5.5 and nothing references it; it remains recoverable from git history.

## [0.6.0] — 2026-05-29

### Changed

- **Skills now auto-invoke on natural language.** `disable-model-invocation: true` removed from every `SKILL.md`. The flag was previously blocking inter-skill invocation; with it gone, one skill can activate another from inside its body, and the model can route a user's natural-language request to the right skill without the slash command. Each skill's frontmatter `description` is rewritten as a precise trigger spec — slash command, qualified form `/kntnt-text-skills:<skill>`, or plugin-anchored natural-language phrasings (e.g. *kntnt text skills edit*, *text-edit-skill*, *edit X with Kntnt's skill*) — and explicitly rejects bare action words. The slash-command interface is unchanged; this only adds a second, gated triggering path.
- **`/proofread` is the documented exception to the plugin-anchored trigger rule.** Its description accepts clear natural-language proofreading requests aimed at a specific text — *proofread this*, *fix the typos in this paragraph*, *spell-check this draft*, *korrekturläs det här* — because the skill's scope is conservative (mechanical errors only, never style or word order) and broad triggering is safe. Bare mentions of the word, questions about proofreading, or passing references must not activate the skill.
- **Each `SKILL.md`'s body opens with a declarative, human-readable description** of what the skill does, how to invoke it, and what arguments it takes. The opener replaces the prior terse imperative ("Apply the procedure in …", "Three-phase critical editorial review settled by an internal subagent") with prose that serves Claude on activation and a human reader via `/kntnt-text-skills:help`. Operational imperatives that need to survive live in a follow-up paragraph below the opener for the three loaders and `/proofread`.
- **Help command renders the plugin's `description` from `plugin.json`** in the overview header above the skill list, making use of a field that was already being read but not surfaced. Detail view skips `plugin.json` entirely and renders just `/<skill>` plus the skill's body intro paragraph — no version, no repo, no plugin name in the detail header.
- **Help command emits single-space separator lines** instead of fully empty lines. Claude.app's code-fence renderer was collapsing fully empty lines; lines containing exactly one space are treated as non-empty and stay visible. In a terminal the single space is indistinguishable from a fully empty line, so the trick is free.
- **README restructured.** Skill groups collapsed from four ("Automatically-triggered task skill", "Slash-only task skills", "Slash-only context loaders", "Slash-only help") to three (Task skills, Context loaders, Help) — the auto-trigger / slash-only distinction is no longer the discriminator. Added a trigger-doctrine paragraph after the group list. Authoring rule #7 (*Progressive disclosure in SKILL.md*) rewritten to allow a human-readable opening paragraph in the body and to document the conservative-skill exception. Help command's description in both the intro section and the Usage section updated to describe the new render behaviour.
- **CI workflow** bumped `actions/checkout@v4` → `@v6` and `actions/setup-python@v5` → `@v6`. The previous pins ran on Node 20, which GitHub deprecates after 2026-06-02 and removes after 2026-09-16. The new pins are on Node 24-compatible majors.

### Fixed

- YAML parse error in the frontmatter `description` of every task skill: the `: ` (colon-space) inside *…this plugin's edit skill: `/edit`, …* was being parsed as a nested mapping, breaking the file. Replaced with ` — ` (em dash) in every affected description — same visual cadence, no YAML ambiguity.

## [0.5.7] — 2026-05-29

### Changed

- `/kntnt-text-skills` command renamed to `/kntnt-text-skills:help`. `commands/kntnt-text-skills.md` moves to `commands/help.md`; invocation becomes the qualified `/kntnt-text-skills:help [skill-name]`. The bare `/kntnt-text-skills` short form no longer resolves to this command — it would only do so if no other plugin had taken that namespace, and the qualified form is what the harness surfaces in practice anyway. README and the internal references inside the command body updated to match.
- Help command render layout reworked. Overview block collapses the header to one line (`kntnt-text-skills <version>  ·  <repo>`, dropping the separate author line), wraps each skill's intro paragraph at word boundaries with continuation lines aligned to the description column, separates entries with blank lines, and enforces a hard 80-character ceiling on every rendered line. Detail block applies the same 80-char wrap to the frontmatter description and the intro paragraph, and drops the author line from its header. The render still happens entirely in the model at invocation — no script, no separate man-page source, no token-heavy template additions.

## [0.5.6] — 2026-05-28

### Added

- `commands/kntnt-text-skills.md` — slash-command implementation of the plugin's help. At invocation it lists `skills/` via `ls`, reads `plugin.json` for version / author / repository, and reads each skill's `SKILL.md` frontmatter `description` and body intro paragraph live. There is no parallel, hand-maintained help text anywhere in the plugin.
- `.claude-plugin/plugin.json` now declares the two recommended manifest fields `homepage` and `repository` (both `https://github.com/Kntnt/kntnt-text-skills`). Audit against the `plugin-structure` skill flagged them as missing.

### Changed

- `/kntnt-text-skills` migrated from a slash-only skill to a slash command. The slash interface is unchanged — bare invocation renders an overview; passing a skill name renders that skill's detail view; an unknown name returns `Unknown skill: X. Known: …`. The overview is simpler than the v0.5.0 manpage: it lists `/<skill>` plus the intro paragraph for every skill, and drops the previously hand-maintained `LANGUAGES`, `INPUT MODES`, and `FLAGS` blocks. Languages, input modes, and flags are documented in README.md and per-`SKILL.md`; the help command no longer duplicates that surface. The detail view shows the skill's frontmatter `description` plus its body intro paragraph.
- `CONTRIBUTING.md` point 6 simplified — adding a new skill no longer requires a separate help-text edit; the command auto-discovers from `skills/` and reads the new `SKILL.md` live. Contributors are reminded to give the new `SKILL.md` a clear frontmatter `description` and a short intro paragraph, since those are what the help command shows.
- README *What the plugin does* and *Usage* `/kntnt-text-skills` subsection rewritten to describe the command implementation and the live-read behaviour. *File structure* tree now lists `commands/kntnt-text-skills.md` instead of `skills/kntnt-text-skills/SKILL.md`. The post-list note about `disable-model-invocation: true` clarified to cover task and context-loader skills; the new help command shares the explicit-invocation property by construction.

### Removed

- `skills/kntnt-text-skills/SKILL.md` — replaced by the command above. The handcrafted manpage blocks it carried (one Overview + seven Detail blocks) are not ported; the command derives equivalent overview lines from each skill's intro paragraph instead, eliminating the drift risk where the parallel help text could fall behind real skill behaviour.

## [0.5.5] — 2026-05-28

### Added

- `evals/workspace/_runner.py` — headless orchestrator that drives the full `(case × config × run)` sweep through `claude -p` subprocesses. Resumable (skips runs whose `output.md` / `grading.json` already exist), parallelisable (`--parallel N`), budget-capped (`--executor-budget`, `--grader-budget`), and scopable by skill (`--skill`) or individual cases (`--case-ids 11,205,…`). Pre-flight parses `claude -p`'s JSON envelope to surface auth failures early — the script cannot be run from inside a Claude Code session because nested invocations strip auth and return 401, and the runner says so up front. Model is pinned through `--model` (default `claude-sonnet-4-6`) so iteration-to-iteration numbers stay comparable while leaving room to bump Sonnet on the next major.
- Five negative-control cases (ids 19, 20, 21, 119, 219) supply clean-text fixtures in sv, en_GB, and en_US for `/proofread`, `/redline`, and `/edit`, with assertions that pin the false-positive rate: no wall of corrections, no spurious style rewrites, genre / language resolution still recorded. With-skill 28 / 28; without-skill 16 / 28.
- Three Phase 3 dialogue cases (ids 409, 410, 411) exercise the `/redline` accept / reject / counter / delegate protocol via scripted user responses in the executor prompt. The executor simulates the dialogue in-transcript (the same pattern `--max-iterations` already uses); the grader reads the transcript for the documented branches. With-skill 17 / 17; without-skill 11 / 17. End-to-end Phase 3 with an interactive user cannot be driven by the skill-creator pipeline's one-shot `claude -p`; that limitation is documented as a known gap rather than treated as a defect.

### Changed

- Paired protocol-semantic assertions appended to the 19 v0.5.4 cases that scored 100 % without-skill in iteration-1 (ids 4, 5, 11, 12, 14–18, 105, 114–116, 118, 205, 211, 214, 215, 218). Each augmented case now also records the genre commit, the technique commit, or the file-citation evidence that distinguishes a skilled run from a baseline LLM run. The new dimensions widened the suite from 80 cases / 299 assertions to 88 cases / 363 assertions.
- Case 11 (en_GB) reframed from "American spellings corrected" — which the plugin's en_GB.md correctly classifies as Style-layer and therefore out of `/proofread` scope — to `en_GB-proofread-respects-style-scope-on-spellings`. The case now verifies the plugin's scope discipline: `/proofread` must *not* touch -ize / -ise, -or / -our, traveler / traveller drift in en_GB text, and the transcript must record the layer choice. Was a Mechanics-vs-Style framing mistake in the original eval, not a plugin behaviour question.
- Case 404 assertion 5 rewritten to an observable form. Previously a process invariant ("no behaviour beyond what the article genre prescribes is introduced") that a single executor transcript could not falsify; now requires the findings list to cite an article-genre review-scoped rule from `lib/genres/article.md`.
- Cases 205, 211, 218 had two assertions reformulated to remove a grader-LLM literalism dependency: the style-layer-pass evidence assertion now enumerates three valid evidence forms (file-path citation, layer-naming phrase, or category enumeration of `lib/rules/style.md`'s sections); the body-text-stability assertion now requires findings-traceability rather than literal "body text under each heading remains unchanged" (which conflicted with the legitimate ABT-technique restructuring that `/edit` performs).
- Case 219 assertion 3 broadened to accept `article` alongside `column` / `general` as a defensible genre commit for the structural markers in the negative-clean-essay fixture — the plugin's trigger set commits to `article` on H1 + standfirst, and that is correct.
- Case 410 assertion 5 broadened to allow a brief editorial trailer in `output.md` when the subagent has processed delegated findings; what the assertion bans is the polished text being subordinated to a verbose user-facing summary, not any acknowledgement at all.
- `evals/evals.json` is now the source of truth for 88 cases / 363 assertions; the per-skill `evals/<skill>/evals.json` mirrors are regenerated from it (proofread 22, redline 26, edit 21, write 19).
- `evals/baseline.md` refreshed against version 0.5.5 with hybrid iteration-1 + iteration-2 numbers: aggregate with-skill 363 / 363 (100.0 %), without-skill 170 / 363 (46.8 %), delta +53.2 pp. Every skill at 100 % with-skill; every language at 100 %; every required case, every negative-control case, and every Phase 3 dialogue case at 100 %. Methodology section documents the hybrid construction, the orchestrator, and the Sonnet-tur dependency that was hardened away.

## [0.5.4] — 2026-05-28

### Changed

- Three eval fixtures gained one sentence each so every assertion has an observable trigger in the input: `evals/fixtures/en_GB-typography-errors.md` now contains `£12,450.75` and `3.5%`; `evals/fixtures/en_US-typography-errors.md` now contains `CEO`, `FY`, `$12,450.75`, and `3.5%`; `evals/fixtures/en_US-style-errors.md` now contains the previously-absent AI-tells *next-generation*, *touch base*, *strategic*, *proactive*, *synergies*, plus the concrete series *usability, performance, and accessibility* used by the Oxford-comma-in-output check. No existing case content changed; only added sentences.
- Four conjunction-style assertions in `evals/evals.json` were split into per-term sub-assertions so future regressions point at the exact term that dropped instead of "the conjunction did not fully pass": en_GB-12 and en_US-18 decimal/thousands split (2 sub-assertions each); en_US-115 #3 split into 3 American AI-tell terms; en_US-115 #4 split into 6 management-jargon terms. Per-skill mirrors regenerated. Total assertion count: 290 → 299.
- `evals/baseline.md` refreshed against version 0.5.4: aggregate with-skill 299 / 299 (100 %), without-skill 152 / 299 (50.8 %), delta +49.2 pp. Every skill and every language at 100 % with-skill. README scaffold line updated.

## [0.5.3] — 2026-05-28

### Changed

- `evals/baseline.md` now carries real numbers from the skill-creator eval pipeline run against 0.5.2 (Sonnet executor and grader, one run per configuration). Aggregate with-skill 282 / 290 (97.2 %), without-skill 132 / 290 (45.5 %), delta +51.7 pp. All eight required cases pass every with-skill expectation. The README scaffold line is updated to point at the populated baseline.
- Three test assertions in `evals/evals.json` (403 #4, 404 #5, 405 #2 and #3) were reworded from invariant or counterfactual claims that could not be verified from a single executor transcript, to transcript-content claims that a single run can demonstrate. The protocol intent is preserved — the fast-path is documented as a downstream-rule dedup, and subagent invocation remains delegation-gated — only the verification framing changes. Original wording is preserved in git history. Per-skill `evals/redline/evals.json` mirror regenerated.

## [0.5.2] — 2026-05-27

### Changed

- The `--max-iterations` natural-language parity list now lives in a single authoritative section, `## Natural-language parity` in `lib/protocols/subagent.md`. The four bullets that were duplicated verbatim across `skills/write/SKILL.md`, `skills/redline/SKILL.md`, and `skills/edit/SKILL.md` are replaced by a one-line reference to that section, removing the drift risk where adding, removing, or rewording a phrase silently diverged the three skills. Closes [#37](https://github.com/Kntnt/kntnt-text-skills/issues/37).

## [0.5.1] — 2026-05-27

### Fixed

- README *What the plugin does* now reflects the eight-skill, four-group reality after `/kntnt-text-skills` landed in 0.5.0. The opener, the group enumeration, and the post-list note about `disable-model-invocation: true` are updated; a new *Slash-only help* group lists the help command alongside the existing *task skill*, *task skills*, and *context loaders* groups.
- README *File structure* tree now lists `skills/kntnt-text-skills/SKILL.md`.
- README *Usage* section gains a `/kntnt-text-skills` subsection with examples, matching the per-skill structure used by the surrounding entries.

## [0.5.0] — 2026-05-27

### Added

- `/kntnt-text-skills` — manpage-style help command. Bare invocation renders an overview of every skill in the plugin (commands, arguments, flags, input modes, language list). Passing a skill name (e.g. `/kntnt-text-skills write`) renders a detail view for that skill. The version is read live from `plugin.json`; the rest of the help text is static and maintained by hand. Marked `disable-model-invocation: true` — manual trigger only.
- CONTRIBUTING.md point 6 reminds contributors to update `skills/kntnt-text-skills/SKILL.md` when adding a new skill or language file so `/kntnt-text-skills` keeps showing accurate help.

## [0.4.2] — 2026-05-27

### Changed

- Plugin descriptions in `plugin.json` and `marketplace.json` now attribute the writing style to *Kntnt* rather than to *Thomas Barregren* personally — the plugin is a company artefact, not a personal one.
- Swedish press-release fixture (`evals/fixtures/sv-press-release.md`) no longer quotes Thomas Barregren by name; the fictional spokesperson is now Anna Lindberg, keeping the fixture free of real-person attributions.

## [0.4.1] — 2026-05-27

### Fixed

- README *Authoring rules* point 8 now lists all four shared protocols (`protocols/proofread.md`, `protocols/redline.md`, `protocols/language-resolution.md`, `protocols/genre-resolution.md`) rather than only the original two. The two protocols added in 0.4.0 capture real abstractions in the same anda; the rule's example list had not caught up.
- README *Audit checklist* — the trigger-list-duplication bullet no longer describes its `_index.md`-cites-exemption as *slated for removal*; the exemption is reframed as a forward-compat safety net, which reflects what the check in `scripts/audit.py` actually does after the fast-path-dedup landed in 0.4.0.
- README *File structure* tree now lists every top-level repo artefact: `.github/` (issue template + audit workflow), `scripts/audit.py`, the `evals/` suite, `.pre-commit-config.yaml`, `.gitignore`, `CHANGELOG.md`, `CONTRIBUTING.md`, `LICENSE`, and `NOTICE`. Previously the tree only depicted the plugin core (`skills/`, `lib/`, `.claude-plugin/plugin.json`, `README.md`).

## [0.4.0] — 2026-05-27

### Added

- Eval suite under `evals/` wired to the skill-creator pipeline. Aggregated `evals/evals.json` (80 cases) covers `/proofread`, `/redline`, `/edit`, and `/write` in Swedish, British English, and American English (≥6 cases per shipped language per skill), with the required fallback, overlay, fast-path parity, per-skill natural-language `--max-iterations`, and last-resort-floor cases. Per-skill `evals/<skill>/evals.json` files mirror the aggregated source for runners that expect the canonical per-skill schema. Fixtures live under `evals/fixtures/` (committed); `evals/workspace/` is gitignored. `evals/README.md` documents the layout, run instructions, and scaling rule for new languages. `evals/baseline.md` is the structural baseline scaffold for 0.3.0 — populate the numbers by running the pipeline locally.
- `lib/protocols/language-resolution.md` — shared language-resolution protocol covering the argument step, source mode (*detect* / *propose*), file inventory, the overlay loader for territorial variants (`inherits: "@<base>.md"`), and fallback reporting. Inline `## Language determination` sections in `/proofread`, `/redline`, `/edit`, `/write`, and `/writing-rules` are replaced by a short reference to the protocol. Overlay semantics: H2 sections under `<!-- layer: mechanics -->` and `<!-- layer: style -->` are the unit of override; H3 sub-sections cannot be overridden in isolation; no partial within-section merges; one step deep only. The current shipped language files declare no `inherits` field, so the protocol is a no-op for them until the first territorial variant lands.
- Automated audit pipeline (`scripts/audit.py`) wired to pre-commit and CI. The script runs every scriptable item from the README *Audit checklist*: skill `../../lib/...` path resolution, genre file ↔ `_index.md` symmetry and frontmatter sync, single-default-genre invariant, language-file layer markers, genre scope markers, skill slash names in execution-context lib files, `plugin.json` shape with version-matches-CHANGELOG-heading coupling, `inherits` validation (forward-compat for territorial variants), and trigger-list duplication outside `_index.md` (forward-compat for the fast-path-dedup slice). The same script is the source of truth for `.pre-commit-config.yaml` and `.github/workflows/audit.yml`; CI is the hard gate.

### Changed

- License changed from proprietary to Apache 2.0.
- README *Authoring rules* and *Audit checklist* updated to remove the prior exception for inline language resolution. Resolution is now treated like any other shared procedure: the protocol lives in `lib/protocols/`, and each consuming `SKILL.md` references it.
- README *Audit checklist* now carries `(auto)` / `(manual)` markers per item and a brief note on installing the pre-commit hook.
- `lib/protocols/proofread.md` rephrased to remove the prior naming of sibling skills (the previous line referred to *the redline / edit passes*); the protocol now speaks generically of *deeper review passes*, restoring caller-agnosticism per authoring rule 1.
- Extracted the genre fast-path into `lib/protocols/genre-resolution.md` (behaviour-neutral refactor). The inline *Genre fast-path* section in `skills/redline/SKILL.md` and `skills/edit/SKILL.md` — including the duplicated trigger-word enumeration — is replaced by a short reference to the protocol; Files-to-read marks `_index.md`, the matched genre file, and the matched technique file as conditional per the protocol's fast-path exit.

## [0.3.0] — 2026-05-25

### Added

- Seven slash skills covering the writing-and-review surface: `/proofread` (auto-triggered conservative proofreading), `/redline` (human-in-the-loop critical editorial review), `/edit` (AFK variant of `/redline`), `/write` (four-phase content creation), and the three context loaders `/writing-rules`, `/abt`, and `/pac`.
- Strict inheritance hierarchy `proofread ⊂ redline ⊂ edit`, enforced by shared protocol files rather than copied prose. `/write` Phase 4 reuses the same redline procedure so the post-draft polish inherits from the same base.
- Three shipped languages under `lib/languages/`: Swedish (`sv.md`), British English (`en_GB.md`), and American English (`en_US.md`), each split into a `<!-- layer: mechanics -->` section (proofread scope) and a `<!-- layer: style -->` section (redline / edit scope). Plus a standalone `default-mechanics.md` fallback for languages with no shipped file.
- Nine genre files under `lib/genres/`: article, case study, press release, web copy, teaser, report, column, opinion, and a general fallback (`default: true`). Each carries `<!-- scope: write -->` and `<!-- scope: review -->` section markers so write and review passes load only what they need. A hand-maintained `_index.md` mirrors the frontmatter for discovery.
- Two technique files under `lib/techniques/`: ABT (narrative arc) and PAC (analytical arc). Techniques are installed artefacts only — the plugin refuses to apply techniques it does not ship as files.
- Protocol files under `lib/protocols/`: `proofread.md`, `redline.md`, `dialogue.md` (one-at-a-time human-in-the-loop settling), `subagent.md` (opt-in iterative settling capped at three rounds), and `io.md` (input detection plus inline-vs-file output routing). Protocols are caller-agnostic — they speak of *the loaded rule files*, never of specific skills or rule-file names.
- Rule files under `lib/rules/`: `writing.md` (universal writing principles), `constructions.md` (four construction-scoped sections — quotation, abbreviation, headed-text, lists — applied cognitively when the matching construction is in the input), and `style.md` (the substantive style foundation).
- Opt-in subagent loop in `/edit`, `/write` Phase 4, and `/redline`'s delegation tail via `--max-iterations=N` (and natural-language equivalents in English and Swedish). Last-resort developmental findings raise the floor to one round automatically.
- Genre fast-path in `/edit` and `/redline`: when the input shows no structural markers and the prompt contains no genre word, the skills commit to `general` directly and skip both the index read and the matched-genre file read.
- Authoring rules and audit checklist in the README — ten rules plus a pre-commit checklist that codify the architectural constraints established over earlier cleanup rounds.
- Marketplace metadata (`.claude-plugin/marketplace.json`) and `/plugin marketplace add` / `/plugin install` instructions for installation via the modern Claude Code plugin flow.
- Keep a Changelog 1.1.0 changelog (this file) and a versioning-policy section in the README that adapts SemVer to a rules-driven plugin.

