# Contributing to kntnt-text-skills

Thanks for considering a contribution. The plugin is open source under the Apache License 2.0, which means anyone is free to fork it and modify it for their own purposes. This document describes the *project norm* – what kinds of contributions are likely to be welcomed into the upstream repository at [Kntnt/kntnt-text-skills](https://github.com/Kntnt/kntnt-text-skills). It is not a legal restriction on what you may do with the code; it is editorial guidance on what is likely to be merged.

## Contribution scope

The plugin embodies a specific house style. Decisions about what enters the upstream repository follow that voice. The table below describes how different kinds of contributions are likely to be received.

| Category | Examples | Reception |
|---|---|---|
| Welcomed without question | New language files under `lib/languages/` that follow the existing template; bug reports; bug fixes against existing rules; corrections to broken examples; typo and grammar fixes in prose; clarifications that do not alter rule semantics. | Open a PR. If the change is small and self-evidently correct, it is usually merged quickly. |
| Accepted but discussed first | New genres under `lib/genres/`; new techniques under `lib/techniques/`; adjustments to existing rules; changes to default behaviour; tightening or loosening of an existing rule. | Open an issue first to align on intent before writing code. A PR without prior discussion may still land, but expect feedback rounds. |
| Unlikely to be merged but free to fork | Fundamental style changes that alter the plugin's voice; a new style-bearer competing with the house voice; restructuring the architecture in a way that conflicts with the authoring rules in `docs/authoring.md`. | The Apache 2.0 licence makes forking explicit and lawful. If you want a different voice, build it in your fork. |

## Inbound licensing

By submitting a contribution, you agree it is licensed under Apache 2.0 by virtue of Apache License 2.0 §5 *Submission of Contributions*, which states that any contribution intentionally submitted for inclusion in the work shall be under the terms of that licence unless you explicitly state otherwise. No separate contributor licence agreement is required.

## How to contribute

1. **Open an issue first** for anything in the *discussed* row of the table above. For *welcomed* items, you can open a PR directly. Use the issue tracker at <https://github.com/Kntnt/kntnt-text-skills/issues>.
2. **Bug reports** should follow the template under `.github/ISSUE_TEMPLATE/bug.md` – which rule, which language file, which input, observed versus expected outcome.
3. **Read the authoring rules** in [`docs/authoring.md`](docs/authoring.md) (the authoring rules and the audit checklist beneath them) before editing files under `skills/` or `lib/`. The rules exist to prevent recurring architectural drift.
4. **Keep prose in British English** outside `lib/languages/`. Language-specific examples and conventions live in the matching language file.
5. **One concern per PR.** Smaller PRs land faster.
6. **When adding a new skill**, give the new `SKILL.md` a clear frontmatter `description` and a short intro paragraph beneath the `# /name` heading. The `/kntnt-text-skills` help command auto-discovers skills from `skills/` and reads those two fields live – no separate help text needs updating.

## Style and language conventions

- All identifiers and comments in English.
- British English in all prose outside `lib/languages/`.
- Per-language realisations belong in `lib/languages/<lang>.md` with the mechanics and style sections in their canonical places.
- Follow the layer boundary: proofread-scope conventions go under `<!-- layer: mechanics -->`, redline / edit-scope conventions under `<!-- layer: style -->`.

## Questions

Open an issue. Discussion happens in the open.
