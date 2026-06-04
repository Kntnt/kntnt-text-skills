# Versioning

The plugin follows Semantic Versioning, adapted to a domain where a *change* is usually a rule or a procedure rather than executable code. The outcome of a run – what the plugin would say about a given draft – is the unit that determines the bump class. Each release is recorded in [`../CHANGELOG.md`](../CHANGELOG.md) using Keep a Changelog 1.1.0.

**Major (X.0.0).** A change that alters the outcome of a category of prior runs without being a bug fix. Examples: `default-mechanics.md` switching from British to logical-American punctuation, the default genre `general` being swapped out or a protocol tightening its procedure so prior findings would have been treated differently. Users need to know that re-running an old draft will yield new output.

**Minor (0.X.0).** A new language, genre, technique or skill – or an extension of an existing rule or procedure that does not change the outcome of prior runs. Examples: adding a new AI-tell to `sv.md`'s smell test, or shipping a variant-inheritance mechanic that no existing file uses. Users should feel free to update without worrying about retroactive change.

**Patch (0.0.X).** Bug fixes, documentation changes, prose clarifications that do not change the rule set and refactors that are behaviour-neutral – for example extracting the genre fast-path into a shared procedure file without changing its semantics.

**Borderline cases.** When an existing rule or procedure is tightened or loosened, it is a major bump if the outcome for a typical text plausibly changes, otherwise a minor bump. Uncertainty resolves to major – the safer side. This test applies equally to rule files and protocol files; procedure is just as outcome-determining as data.

**External language contributions.** When a contributor adds a new `lib/languages/<lang>.md`, the merge bumps the minor version. A bug fix in an existing language file is a patch. The contributor does not handle the version bump themselves – it happens at merge.

**License change.** The transition from proprietary to Apache 2.0 is a distinct and significant event that deserves its own line in the CHANGELOG block for the release that lands it – typically phrased *License changed from proprietary to Apache 2.0* under *Changed*. The licence change does not itself alter the outcome of any run, so it does not force a major bump by the outcome test; it is recorded as a *Changed* event in whichever release ships it. Because it marks the end of the proprietary phase, it is a natural part of the 1.0 release if that lands close in time; if it merges before 1.0, it is noted in whichever minor or patch release it ships with.

**Version-bump moment.** A release is one commit that does three things together: (1) bump the `version` field in `.claude-plugin/plugin.json`, (2) move the `[Unreleased]` block in `CHANGELOG.md` to a concrete version heading with an ISO date and (3) set a matching git tag. The audit script verifies that `plugin.json`'s version matches the latest non-*Unreleased* heading in the changelog; tag consistency is a manual responsibility at release time.
