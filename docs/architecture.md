# Architecture

How the plugin is built: the hierarchy that relates the review skills, the three layers that hold the rule set, the file structure on disk and the principles that govern every change. For how to add a content type, technique or language, see [`extending.md`](extending.md); for the constraints on editing the files, see [`authoring.md`](authoring.md).

## Review hierarchy: proofread ⊂ redline ⊂ edit

The three review skills form a strict inheritance hierarchy. Each deeper skill is the previous skill plus an additional phase. No logic is duplicated – phases are shared at the file level.

| Skill | Phase 1 (silent) | Phase 2 (critical review) | Phase 3 (settling) |
|---|---|---|---|
| `/proofread` | `protocols/proofread.md` against `rules/writing.md` (plus the matching sections of `rules/constructions.md`) + the *Mechanics* section of the loaded `<lang>.md` (or `default-mechanics.md`) | – | – |
| `/redline` | same as `/proofread` | `protocols/redline.md` against `rules/style.md` + the *Style* section of the loaded `<lang>.md` + applicable `genres/<type>.md` + applicable `techniques/<technique>.md` | `protocols/dialogue.md` (one finding at a time, you decide); on delegation the main agent applies directly, or – with `--max-iterations=N` – invokes `protocols/subagent.md` with that ceiling |
| `/edit` | same as `/proofread` | same as `/redline` | Default: main agent applies directly. Opt-in via `--max-iterations=N`: `protocols/subagent.md` runs with that ceiling. Last-resort finding raises the floor to 1 |

`/write` Phase 4 invokes the same Phase 2 and Phase 3 directly – so the inheritance also covers the post-draft polish of newly written text.

## The three layers

The procedure and rule files are arranged in three layers with distinct responsibilities:

| Layer | File | Content |
|---|---|---|
| Rules – what | `lib/rules/writing.md`, `lib/rules/constructions.md`, `lib/rules/style.md`, `lib/languages/<lang>.md`, `lib/genres/*.md`, `lib/techniques/*.md` | The universal punctuation rules, the construction-scoped rules (quotation, abbreviation, headed-text, lists) whose sections are applied only when the matching construction is in the input, the substantive style foundation, the per-language realisations split into mechanics and style sections inside a single file, the content-type-specific rules and the narrative or analytical arcs. |
| Procedure – how | `lib/protocols/proofread.md`, `lib/protocols/redline.md`, `lib/protocols/dialogue.md`, `lib/protocols/subagent.md`, `lib/protocols/io.md`, `lib/protocols/language-resolution.md`, `lib/protocols/genre-resolution.md` | The proofread pass procedure, the redline pass procedure (including the shared finding format), the human-in-the-loop settling procedure, the subagent settling procedure, the I/O protocol (input detection plus inline-output and file/URL-output routing), the language-resolution procedure (argument, source step, inventory, overlay loader, fallback reporting) and the genre-resolution procedure (fast-path exit to the fallback genre when the input has no structural markers and the prompt no genre word; standard flow against `_index.md` otherwise). |
| Skill – entry | `skills/proofread/SKILL.md`, `skills/redline/SKILL.md`, `skills/edit/SKILL.md` | Each composes one or more procedure files and supplies the caller-side bits the protocols cannot know (source mode for language resolution, scope of layers applied). No skill duplicates rule content or pass procedure; rules and pass procedures are by reference. |

Changing a rule requires editing exactly one place. Adding a new content type, technique or language requires no `SKILL.md` change. The inheritance is enforced by composition – `/redline` and `/edit` reference the same `protocols/proofread.md` and `protocols/redline.md` files that `/proofread` and `/redline` use respectively.

## File structure

```
kntnt-text-skills/
├── .claude-plugin/
│   ├── plugin.json
│   └── marketplace.json
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   └── bug.md
│   └── workflows/
│       └── audit.yml
├── commands/
│   └── help.md
├── docs/
│   ├── architecture.md
│   ├── languages.md
│   ├── content-types.md
│   ├── extending.md
│   ├── authoring.md
│   └── versioning.md
├── skills/
│   ├── write/SKILL.md
│   ├── edit/SKILL.md
│   ├── redline/SKILL.md
│   ├── proofread/SKILL.md
│   ├── writing-rules/SKILL.md
│   ├── abt/SKILL.md
│   └── pac/SKILL.md
├── lib/
│   ├── languages/
│   │   ├── default-mechanics.md
│   │   ├── sv.md
│   │   ├── en_GB.md
│   │   └── en_US.md
│   ├── rules/
│   │   ├── writing.md
│   │   ├── constructions.md
│   │   └── style.md
│   ├── protocols/
│   │   ├── proofread.md
│   │   ├── redline.md
│   │   ├── dialogue.md
│   │   ├── subagent.md
│   │   ├── io.md
│   │   ├── language-resolution.md
│   │   └── genre-resolution.md
│   ├── genres/
│   │   ├── _index.md
│   │   ├── article.md
│   │   ├── case-study.md
│   │   ├── press-release.md
│   │   ├── web-copy.md
│   │   ├── teaser.md
│   │   ├── report.md
│   │   ├── column.md
│   │   ├── opinion.md
│   │   ├── readme-github.md
│   │   └── general.md
│   └── techniques/
│       ├── abt.md
│       └── pac.md
├── scripts/
│   ├── audit.py
│   └── help.py
├── evals/
│   ├── README.md
│   ├── baseline.md
│   ├── evals.json
│   ├── proofread/evals.json
│   ├── redline/evals.json
│   ├── edit/evals.json
│   ├── write/evals.json
│   └── fixtures/
├── .pre-commit-config.yaml
├── .gitignore
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
├── NOTICE
└── README.md
```

Each `SKILL.md` is a short entry point that references the shared modules via relative paths. Rules, language files, content types and techniques live in `lib/` so every skill can share the same rule set without duplication. All files outside `lib/languages/` are written in British English; language-specific conventions and examples live in the matching language layer files.

## Design principles

- **DRY.** Shared rules live in one place. The proofread pass is described once across three layers. Language-specific conventions live only in the language layer files. No trigger keywords are duplicated between `SKILL.md` and content-type frontmatter.
- **Modular.** New content type = one new file (plus a row in `lib/genres/_index.md`). New technique = one new file. New language = one new file (`<lang>.md` with `<!-- layer: mechanics -->` and optionally `<!-- layer: style -->` sections). No `SKILL.md` needs to change.
- **Plugin-anchored triggers.** Every skill activates only on plugin-anchored invocation: slash command, qualified form `/kntnt-text-skills:<skill>` or natural-language phrasing that names this plugin together with the skill. Bare action words do not fire any skill. The `description` field in each `SKILL.md`'s frontmatter defines that trigger boundary.
- **Tools, not algorithms.** The skill files describe outcomes and rules. They do not specify matching algorithms or file-search heuristics – the plugin solves the mechanics with standard tools (Glob, Grep, Read, Edit, Write, Bash).
- **The user, not the author.** All skill-internal text addresses *the user*. The plugin is generic; the house voice it embodies is documented in metadata, not embedded in the skill text.
- **English baseline, language layer for the rest.** Everything outside `lib/languages/` is written in British English. Per-language conventions, examples and overrides live in `lib/languages/<lang>.md` (with mechanics and style as named sections).
- **Token-aware.** The subagent is opt-in by default – `/edit` Phase 3, `/write` Phase 4 and `/redline`'s delegation tail all apply findings directly unless the user passes `--max-iterations=N` (or an equivalent natural-language phrase) on the invocation. A last-resort developmental finding from the redline pass raises the floor to one round automatically; otherwise no subagent fires. The protocol ceiling is three iterations, early termination preferred. Skills load one language file per run (`/proofread` applies only its *Mechanics* section; `/redline`, `/edit` and `/write` apply both sections); a territorial variant pulls in its base file as well so the overlay can be applied, still bounded to two files at most. Plus `rules/constructions.md`, whose four sections are applied cognitively only when the matching construction appears in the input. `/edit` and `/redline` additionally take a genre fast-path documented in [`../lib/protocols/genre-resolution.md`](../lib/protocols/genre-resolution.md): when the input has no structural markers (no H1, standfirst, byline or attributed-quote pattern) and the prompt contains no genre word, the skills commit to the fallback genre directly and skip both the `_index.md` and the matched-genre reads. Files-to-read batches are issued in parallel where dependencies allow.
