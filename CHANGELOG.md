# Changelog

All notable changes to this project are documented here. The format follows [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/) and the versioning policy described in the project README.

History starts at **0.3.0** — the first version with a documented baseline. Earlier versions (0.1.0, 0.2.0) are not reconstructed here; the git log is the source for that prehistory.

## [Unreleased]

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

