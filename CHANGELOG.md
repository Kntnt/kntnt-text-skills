# Changelog

All notable changes to this project are documented here. The format follows [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/) and the versioning policy described in the project README.

History starts at **0.3.0** — the first version with a documented baseline. Earlier versions (0.1.0, 0.2.0) are not reconstructed here; the git log is the source for that prehistory.

## [Unreleased]

### Changed

- License changed from proprietary to Apache 2.0.

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

