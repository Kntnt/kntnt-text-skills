# kntnt-text-skills

[![License](https://img.shields.io/github/license/Kntnt/kntnt-text-skills)](LICENSE)
[![Latest release](https://img.shields.io/github/v/release/Kntnt/kntnt-text-skills)](https://github.com/Kntnt/kntnt-text-skills/releases/latest)
[![Audit](https://github.com/Kntnt/kntnt-text-skills/actions/workflows/audit.yml/badge.svg)](https://github.com/Kntnt/kntnt-text-skills/actions/workflows/audit.yml)

A plugin for Claude Code and Cowork that turns a house writing style into installable rules and protocols, then exposes eight skills for writing, reviewing, editing and proofreading text in Swedish, British English or American English – and can be taught any further language by adding one file.

## Description

The plugin embodies the house style of [Kntnt](https://kntnt.com), but every skill-internal text addresses *the user* rather than the author, so it works for anyone who wants to write in the same vein. Universal rules – punctuation, structure, the global bans – are kept separate from language-specific realisations: typography, address, AI-tell manifestations and interference patterns live in per-language files under `lib/languages/`, so the same rule set produces idiomatic output across languages.

The skills come in three groups: four task skills that do the work (`/proofread`, `/redline`, `/edit`, `/write`), three context loaders that bring the rule set into a session for ad-hoc writing (`/writing-rules`, `/abt`, `/pac`) and a help command (`/kntnt-text-skills:help`).

### Key features

- Eight skills in three groups: four task skills, three context loaders and a help command.
- A strict review hierarchy – `proofread ⊂ redline ⊂ edit` – where each deeper skill is the previous one plus a phase, with no duplicated logic.
- Per-language conventions split into a mechanics layer (proofread scope) and a style layer (redline / edit scope), shipping with Swedish, British English and American English plus an international fallback.
- Ten content types – article, case study, press release, web copy, teaser, report, column, opinion piece, GitHub README and a general fallback – each with its own genre file.
- Two structural techniques, ABT and PAC, applied only from installed files.
- An opt-in subagent loop for deeper polish, off by default and bounded to three iterations.
- Plugin-anchored triggers: skills activate only on explicit invocation, never on a bare action word.
- Self-contained: no external libraries or MCP servers required.

### The problem

Text written with a general-purpose assistant tends to drift. AI-tell phrases creep in, typography and punctuation wander between conventions, sources get invented, and the structure flattens into something recognisably machine-made. Ad-hoc prompting does not enforce a consistent house style, and the conventions that matter – how British English differs from American, when an attribution takes a speech dash, which abbreviations need spelling out – are easy to state once and hard to apply every time.

### How this plugin helps

The plugin encodes a house style as installable rules and protocols, then applies them through skills that follow a fixed protocol. Proofreading corrects only what is objectively wrong; the redline and edit passes review against the full style, content-type and language rule set; the write skill produces a draft from a brief and polishes it through the same machinery. Per-language files carry the conventions so the output reads as though written by someone fluent in that variety, and the global bans keep the plugin from inventing sources, metaphors or rhetorical questions.

### Limitations

Ad copy, Google Ads copy and bare social-media posts without a teaser purpose are out of scope. A narrative technique is applied only when an installed file defines it – a technique named in a prompt but not installed is refused rather than improvised. The plugin needs a host that supports the features listed under [Requirements](#requirements).

## Requirements

The plugin runs in Claude Code or Cowork and needs support for slash commands, YAML frontmatter (including `disable-model-invocation`) and subagents. No external libraries or MCP servers are required; the plugin is self-contained.

Subagents drive the opt-in `--max-iterations=N` loop in `/edit`, `/write` and `/redline`, and the automatic one-round floor when the redline pass surfaces a last-resort finding. Contributors who run the audit hook also need [`uv`](https://docs.astral.sh/uv/) – see [Development](#development).

## Installation

The plugin ships as a Claude Code marketplace. In Claude Code or Cowork, run:

```
/plugin marketplace add Kntnt/kntnt-text-skills
/plugin install kntnt-text-skills@kntnt-text-skills
```

The first line registers the marketplace from the GitHub repository; the second installs the plugin from it. Restart the session if the slash commands do not appear immediately.

To verify the installation, run `/writing-rules` in a fresh session. If Claude confirms that the rules are loaded, the plugin is working.

**Manual install (fallback).** If your client does not yet support the `/plugin` flow, clone the repository into the plugin directory directly:

```bash
git clone git@github.com:Kntnt/kntnt-text-skills.git ~/.claude/plugins/kntnt-text-skills
```

Restart the session and the slash commands become available.

## Usage

Each skill is invoked by its slash command. A language argument, where the skill accepts one, comes first; the text or file reference follows.

### `/proofread`

Conservative proofreading: corrects only what is objectively wrong – spelling, grammar, punctuation, the conventions in the loaded mechanics file – and never touches word choice, word order, structure, tone or argumentation. Type the command with the text, or `/proofread` alone to operate on the most recent text in the conversation. An optional language argument fixes the language; without one the skill detects it.

```
/proofread Det här ä en testtext med några konstigheter
/proofread sv Det här ä en testtext med några konstigheter
/proofread en_GB Here's a proofreading sample with a few mistakes
```

Formatting (line breaks, headings, lists, code blocks) is preserved exactly. When nothing is wrong, the reply is *No errors found.* / *Inga fel hittade.* in the input language, and no text is returned.

### `/redline`

Critical editorial review with you in the loop. A silent proofread pass runs first, then a critical-review pass against the full rule set, then each finding is presented one at a time as a four-part proposal – marking, problem, solution and prompt – to which you respond *accept*, *reject*, *counter* or *delegate*.

```
/redline @draft.md
/redline sv @draft.md
```

Scope runs from proofreading up to and including line editing. When the text sits below what line editing can fix, the pass raises a single last-resort finding describing what to do instead rather than rewriting at the developmental level. Pass `--max-iterations=N` to switch the delegation tail to an opt-in subagent loop with that ceiling.

### `/edit`

The away-from-keyboard variant of `/redline`: the same proofread and critical-review passes, but no question-by-question dialogue. The main agent applies the finding list and delivers the polished text.

```
/edit @draft.md
/edit en_GB @draft.md
/edit --max-iterations=2 @draft.md
```

The default is a single direct pass. `--max-iterations=1`, `=2` or `=3` – or a natural-language equivalent such as *deep review*, *two rounds max* or *one round* – opts into a subagent loop with that ceiling (clamped to three).

### `/write`

Content creation from a brief or from source material, in four phases: brief acquisition over nine fields, an idea for structure, tone, technique and address, the draft and an automatic polish through the redline machinery. A language argument is required; without one, `/write` proposes a language from the prompt and asks you to confirm.

```
/write Skriv ett kundcase om hur Ystadbostäder gick över till digitala lås. Källmaterial: @intervju.md
/write en_GB Draft a column on the agency market consolidation
```

Pass `--max-iterations=N` on the invocation to opt the polish into a subagent loop. You can override the content type's default technique in the prompt – *use ABT*, *force PAC*, *no technique* – and a technique with no installed file is refused with the alternatives named.

### Context loaders: `/writing-rules`, `/abt`, `/pac`

These do no work of their own; they load rule modules into the session so later ad-hoc writing follows the rule set without going through `/write`, `/redline` or `/edit`. `/writing-rules` loads the writing rules, the general style guide and the language file (every installed language with no argument, or one named language). `/abt` and `/pac` load the narrative and analytical arcs.

```
/writing-rules
/writing-rules sv
/abt
/pac
```

### `/kntnt-text-skills:help`

A short overview of the plugin and its skills. Bare invocation lists every skill with its intro paragraph; passing a skill name shows that skill's intro on its own. It is a slash command backed by a small rendering script, so the version, author and per-skill text are read live from `plugin.json` and the individual `SKILL.md` files – there is no parallel help text to maintain.

```
/kntnt-text-skills:help
/kntnt-text-skills:help write
```

## Frequently asked questions (FAQ)

#### How do `/proofread`, `/redline` and `/edit` differ?

They form a strict hierarchy: `proofread ⊂ redline ⊂ edit`. `/proofread` corrects only objective errors. `/redline` adds a critical-review pass and walks you through each finding interactively. `/edit` runs the same passes but applies the findings for you, with no dialogue. See [`docs/architecture.md`](docs/architecture.md) for the full layering.

#### Why doesn't saying ‘edit this’ trigger `/edit`?

By design. Every skill uses plugin-anchored triggers: it activates only on its slash command, the qualified form `/kntnt-text-skills:<skill>` or natural-language phrasing that names this plugin together with the skill. Bare action words such as *edit*, *write* or *redline* fire nothing. `/proofread` is the one documented exception – it also responds to clear proofreading requests aimed at a specific text – because its scope is conservative and broad triggering is safe.

#### Which languages are supported?

Swedish, British English and American English ship as full language files. Any other language falls back to an international baseline (`default-mechanics.md`), and the plugin tells you it has done so. Adding a language is a single file – see [`docs/languages.md`](docs/languages.md) and [`docs/extending.md`](docs/extending.md).

#### Does the plugin need any external services?

No. It is self-contained – no external libraries, no MCP servers, no network access.

## Questions, bugs, and feature requests

Have a usage question or something to discuss? Please use [Discussions](https://github.com/Kntnt/kntnt-text-skills/discussions).

Found a bug or want to request a feature? Please [open an issue](https://github.com/Kntnt/kntnt-text-skills/issues). Search the existing issues first to avoid duplicates.

## Extending

Three things can be added without touching any `SKILL.md`, each a single file (plus, for a genre, a row in the index):

- **A new content type** – a genre file under `lib/genres/` plus a matching block in `lib/genres/_index.md`.
- **A new technique** – a file under `lib/techniques/`, described in parallel with ABT and PAC.
- **A new language** – one file under `lib/languages/`, carrying a mechanics layer and an optional style layer.

The full procedure, including the frontmatter patterns and the territorial-variant overlay, is in [`docs/extending.md`](docs/extending.md). For the content types and techniques already installed, see [`docs/content-types.md`](docs/content-types.md); for the language model, [`docs/languages.md`](docs/languages.md).

## Development

### Build from source

There is nothing to compile – the plugin is a set of Markdown rule files and two small Python helper scripts. To work on it, clone the repository:

```bash
git clone git@github.com:Kntnt/kntnt-text-skills.git
cd kntnt-text-skills
```

Install the pre-commit hook so the audit runs before each commit:

```bash
pip install pre-commit && pre-commit install
```

The audit ([`scripts/audit.py`](scripts/audit.py)) is a self-contained PEP 723 script, run with `uv run scripts/audit.py`; [`uv`](https://docs.astral.sh/uv/) provisions its single dependency automatically. The same script is the hard gate in CI.

### Run tests

The eval suite under [`evals/`](evals/) exercises the four task skills against the rule set and is wired to the [skill-creator](https://github.com/anthropics/skills/tree/main/skill-creator) pipeline. See [`evals/README.md`](evals/README.md) for the layout, the scaling rule for new languages and how to run it.

### Technical documentation

The deeper record lives under [`docs/`](docs/):

- [`docs/architecture.md`](docs/architecture.md) – the review hierarchy, the three layers, the file structure and the design principles.
- [`docs/languages.md`](docs/languages.md) – the language model: mechanics and style layers, the default fallback, resolution and the territorial-variant overlay.
- [`docs/content-types.md`](docs/content-types.md) – the ten content types, the ABT and PAC techniques and the global bans.
- [`docs/extending.md`](docs/extending.md) – adding a content type, technique or language, and the eval suite.
- [`docs/authoring.md`](docs/authoring.md) – the authoring rules and the pre-commit audit checklist for anyone editing `skills/` or `lib/`.
- [`docs/versioning.md`](docs/versioning.md) – the Semantic Versioning policy adapted to a rules-driven plugin.

## How you can contribute

Contributions are welcome, small or large – reporting a bug, requesting a feature, fixing a rule, adding a language file or improving the documentation. New language files that follow the existing template are especially welcome. Before editing anything under `skills/` or `lib/`, read [`docs/authoring.md`](docs/authoring.md); for which kinds of change are likely to be merged and how inbound licensing works, see [`CONTRIBUTING.md`](CONTRIBUTING.md).

## License

Licensed under the Apache License 2.0. The full licence text is in [`LICENSE`](LICENSE), and the copyright and attribution notice is in [`NOTICE`](NOTICE). Contributions are accepted under the same terms by virtue of Apache 2.0 §5.

## Changelog

Release notes for each version live in [`CHANGELOG.md`](CHANGELOG.md); the policy that decides each release's version class is in [`docs/versioning.md`](docs/versioning.md).

The project follows [Keep a Changelog](https://keepachangelog.com/) and [Semantic Versioning](https://semver.org/).
