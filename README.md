# kntnt-text-skills

A plugin for Claude Code and Cowork that provides seven interconnected skills for writing, reviewing, editing, and proofreading text. The plugin embodies Kntnt's house style but is built generically — every skill-internal text addresses *the user*, so the plugin works for anyone who wants to write in the same vein. Language-specific conventions (typography, punctuation, address, AI-tell manifestations, interference patterns) live in per-language files under `lib/languages/`; the plugin ships with Swedish, British English, and American English and can be extended with one file per additional language.

## What the plugin does

The plugin exposes seven skills, organised in three groups.

**Automatically-triggered task skill:**

- `/proofread` — conservative proofreading. Corrects only what is objectively wrong (spelling, grammar, punctuation, the conventions in the loaded mechanics file). Never changes word choice, word order, structure, tone, or argumentation. The lightest of three review skills: `proofread ⊂ redline ⊂ edit`. Triggers on the `/proofread` slash command and on natural-language proofreading requests.

**Slash-only task skills:**

- `/redline` — critical editorial review with human-in-the-loop. Runs the same silent proofread pass as `/proofread`, then performs a critical-review pass against the full rule set (style, content type, technique, language) and presents each finding one at a time as a four-part proposal (marking, problem, solution, prompt). You accept, reject, counter, or delegate. Scope is from proofreading up to and including line editing.
- `/edit` — AFK (away-from-keyboard) variant of `/redline`. Same proofread and critical-review passes, but findings are settled by an internal subagent — no question-by-question dialogue with you. The main agent and subagent iterate as colleagues for up to three rounds and deliver the polished text directly.
- `/write` — four-phase content creation. Phase 1 acquires a brief over nine fields. Phase 2 presents the idea for structure, tone, technique, and address. Phase 3 writes the draft. Phase 4 applies the redline protocol with subagent settling — the same procedure `/edit` runs — so you receive only the polished final result.

**Slash-only context loaders:**

- `/writing-rules` — loads the writing rules, the general style guide, and the language file(s) into the session, so later ad-hoc writing follows the rule set without going through `/write` or `/edit`.
- `/abt` — loads the ABT technique (And, But, Therefore — narrative arc).
- `/pac` — loads the PAC technique (Premise, Analysis, Conclusion — analytical arc).

The slash-only skills (both task skills and context loaders) carry `disable-model-invocation: true` in their frontmatter and therefore activate only on the exact slash command — never through the model deciding on its own that they would be useful.

## Languages

The plugin separates universal rules from language-specific realisations. Files in `lib/rules/`, `lib/genres/`, `lib/techniques/`, and `lib/protocols/` are language-agnostic (all examples in British English). Per-language conventions live in `lib/languages/` as one file per language. Each file carries both layers in named sections — a `<!-- layer: mechanics -->` section with the proofread-scope conventions and a `<!-- layer: style -->` section with the redline / edit-scope conventions. The ship set:

- `default-mechanics.md` — international baseline (fallback when no language-specific file exists)
- `sv.md` — Swedish
- `en_GB.md` — British English
- `en_US.md` — American English

Naming follows the POSIX locale form `language_TERRITORY`. Both bare language codes (`sv`, `en`) and territorial variants (`sv_SE`, `sv_FI`, `en_GB`, `en_US`) are accepted as skill arguments. The resolver maps a language code `<lang>` to the single file `<lang>.md`; skills decide which section they apply (mechanics, style, or both) based on the pass they run.

A territorial variant is reserved to declare an inheritance relationship with its base — for a future `sv_FI.md` the frontmatter would read:

```yaml
---
name: sv_FI
language: Finland Swedish
inherits: "@sv.md"
---
```

The overlay loader is not implemented today (no territorial variant ships yet). When the first real variant lands, the loader is added with that variant as the test case for the overlay rules.

### Mechanics and Style sections

The two-section layout enforces the split between layers within a single file. The *Mechanics* section carries proofread-scope conventions (typography, quotation, punctuation, grammar, greetings); the *Style* section carries redline / edit-scope conventions (address and voice, AI-tell manifestations, interference patterns, genre adjustments).

`/proofread` applies only the *Mechanics* section. `/redline`, `/edit`, and `/write` apply both. The proofread pass cannot drift into stylistic touch-ups because the *Style* section is explicitly out of its scope.

### Default fallback

When no language-specific file exists for the determined language, skills fall back to `lib/languages/default-mechanics.md`. It carries international-standard typography (ISO 8601 dates, SI unit conventions) plus internationally neutral defaults for ambiguous cases (straight ASCII quotation marks, EN-dash with spaces for parentheticals, no Oxford comma, British-style punctuation relative to quotes). There is no companion `default-style.md` because address, AI-tell manifestations, interference, and genre adjustments are inherently language-and-culture-bound and have no meaningful baseline.

Loading is either-or: a skill loads the specific language file if it exists, otherwise `default-mechanics.md`. They are not mixed.

When `default-mechanics.md` is used, the skill mentions in its reply (in English):

> No language file found for [language]. Baseline conventions from `default-mechanics.md` apply. Add `lib/languages/<code>.md` for stricter control.

### Language determination flow

The resolution procedure lives inline in each consuming SKILL.md. In summary:

1. **Argument.** If the user passes a language argument (e.g. `/proofread sv`, `/edit en_GB`), use it. A bare argument that matches no file directly but matches several territorial variants (e.g. `en` matches both `en_GB.md` and `en_US.md`) triggers a disambiguation question.
2. **Source step.** Without an argument, the skill picks a source mode: *detect mode* (`/proofread`, `/redline`, `/edit` — source from the input text) or *propose mode* (`/write` — propose from the prompt's language and confirm).
3. **Inventory.** Check `lib/languages/` for matching files. If multiple language matches arise, ask the user which to use. If a single language matches, load the file and apply the section(s) the pass requires. If none, fall back to `default-mechanics.md` and report the absence.

The manual context loader `/writing-rules` loads either the specified language's file or every installed language file.

## Installation

Copy the plugin root — the directory containing `.claude-plugin/plugin.json` — into `~/.claude/plugins/` (Claude Code) or the equivalent location for Cowork. Restart the session. The slash commands above should now be available.

To verify the installation, run `/writing-rules` in a fresh session. If Claude confirms that the rules are loaded, the plugin is working.

## Usage

### `/proofread`

Proofreading without commentary or explanations — only the corrected text comes back. Type the slash command followed by the text, or `/proofread` alone (in which case it operates on the most recent text in the conversation). An optional language argument fixes the language; without one the skill detects.

```
/proofread Det här ä en testtext med några konstigheter
/proofread sv Det här ä en testtext med några konstigheter
/proofread en_GB Here's a proofreading sample with a few mistakes
```

Original formatting (line breaks, headings, lists, code blocks) is preserved exactly. When no errors are found, the plugin replies with *No errors found.* / *Inga fel hittade.* (in the input language) and does not return the unchanged text.

Style matters — interference from other languages, AI-tell constructions, weak verbs — are explicitly *out of scope* for `/proofread`. They are handled in `/redline`, `/edit`, and `/write` Phase 4.

### `/redline`

Critical editorial review with human-in-the-loop. Use it when a text exists, you want an editorial reading beyond plain proofreading, and you want to control each change yourself.

```
/redline @draft.md
/redline sv @draft.md
```

Phase 1 runs silently — the technical corrections are baked into the final result and are not shown separately. Phase 2 produces a list of findings against the full rule set (`rules/style.md`, the loaded mechanics and style files, the applicable content-type file, the applicable technique file). Phase 3 presents the findings one at a time in a four-part format: marking (the offending span or location), problem (what is wrong, with rule reference), solution (a concrete proposal), and a prompt to which you respond in one of four ways:

- **Accept** — the proposal is applied.
- **Reject** — the proposal is dropped.
- **Counter** — the plugin evaluates your objection against the rule set and either stands its ground with motivation or accepts your counter.
- **Delegate** (*just do it*, *gör vad du tycker är bäst*) — the plugin activates its subagent protocol on the remaining open findings and delivers the polished result without reporting the internal dialogue. From that point the run is `/edit`-like for the tail of the list.

Scope is from proofreading up to and including line editing. When the text is so far from publication that line editing cannot fix it, `/redline` raises a single last-resort finding describing what the writer should do instead, rather than silently rewriting at the developmental level.

### `/edit`

AFK (away-from-keyboard) variant of `/redline`. Same proofread and critical-review passes, but findings are settled by an internal subagent — no question-by-question dialogue with you.

```
/edit @draft.md
/edit en_GB @draft.md
```

Phase 1 and Phase 2 are identical to `/redline`. Phase 3 settles the findings via the subagent protocol: the main agent points out, the subagent improves, for up to three rounds, early consensus preferred. You receive only the polished final text. The single exception is the last-resort finding described under `/redline` — if the text requires developmental work, the plugin surfaces that single decision to you as a closing note.

### `/write`

Content creation from scratch or from source material. The plugin walks you through four phases.

```
/write Skriv ett kundcase om hur Ystadbostäder gick över till digitala lås. Källmaterial: @intervju.md
/write sv_SE Skriv ett kundcase om hur Ystadbostäder gick över till digitala lås. Källmaterial: @intervju.md
/write en_GB Draft a column on the agency market consolidation
```

If no language argument is given, `/write` proposes a target language based on the prompt and asks for confirmation.

**Phase 1 — brief acquisition.** The plugin proposes values for nine fields (working title, target audience, sender purpose, reader takeaway, angle, hook, channel, length, content type) based on your prompt. You go through them one at a time and accept, modify, or discuss. You can also answer *accept all* as blanket acceptance.

**Phase 2 — idea.** The plugin presents a short plan for structure, tone, ABT or PAC usage, address, and language. The default is to wait for your approval before the draft is written. Bypass: if you have pre-authorised in the original prompt that the plugin should proceed without asking (*just produce the draft*, *no need to wait*), the plugin presents the idea and continues to Phase 3 immediately.

**Phase 3 — draft.** The plugin writes the draft per the content-type file, the technique file, and the loaded language files.

**Phase 4 — redline review with subagent settling.** The plugin applies the same procedure `/edit` runs — `protocols/redline.md` plus `protocols/subagent.md` — to the draft. Main agent and subagent iterate for up to three rounds, early consensus encouraged. You see only the polished final result — the internal dialogue is not reported.

`/write` has no follow-up user-facing dialogue. If you want to review the delivered text yourself, run `/redline` separately. If you want another AFK pass, run `/edit`.

**Technique override.** You can tell the plugin to use a technique other than the content type's default in the prompt: *use ABT*, *force PAC*, *without ABT*, *no technique*. If you name a technique that is not installed in `lib/techniques/` (e.g., *PAS*), the plugin refuses and proposes the installed alternatives.

### `/writing-rules`, `/abt`, `/pac`

Context loaders. They do no work of their own — they only load the relevant rule modules into the active session so later ad-hoc writing has them in context. Useful when you want to write or revise freely without going through `/write`, `/redline`, or `/edit`, but still want the rule set to apply.

```
/writing-rules
/writing-rules sv
/abt
/pac
```

`/writing-rules` without an argument loads all installed language files so any subsequent ad-hoc writing in any language is covered. With an argument it loads only that language.

The plugin briefly confirms that the module is loaded. The rules then apply for the rest of the session's output.

## File structure

```
kntnt-text-skills/
├── .claude-plugin/
│   └── plugin.json
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
│   │   └── io.md
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
│   │   └── general.md
│   └── techniques/
│       ├── abt.md
│       └── pac.md
└── README.md
```

Each `SKILL.md` is a short entry point that references the shared modules via relative paths. Rules, language files, content types, and techniques live in `lib/` so every skill can share the same rule set without duplication. All files outside `lib/languages/` are written in British English; language-specific conventions and examples live in the matching language layer files.

## Review architecture: proofread ⊂ redline ⊂ edit

The three review skills form a strict inheritance hierarchy. Each deeper skill is the previous skill plus an additional phase. No logic is duplicated — phases are shared at the file level.

| Skill | Phase 1 (silent) | Phase 2 (critical review) | Phase 3 (settling) |
|---|---|---|---|
| `/proofread` | `protocols/proofread.md` against `rules/writing.md` (plus the matching sections of `rules/constructions.md`) + the *Mechanics* section of the loaded `<lang>.md` (or `default-mechanics.md`) | — | — |
| `/redline` | same as `/proofread` | `protocols/redline.md` against `rules/style.md` + the *Style* section of the loaded `<lang>.md` + applicable `genres/<type>.md` + applicable `techniques/<technique>.md` | `protocols/dialogue.md` (one finding at a time, you decide) |
| `/edit` | same as `/proofread` | same as `/redline` | `protocols/subagent.md` (AFK, max three iterations) |

`/write` Phase 4 invokes the same Phase 2 + Phase 3 directly — so the inheritance also covers the post-draft polish of newly written text.

The procedure and rule files are arranged in three layers with distinct responsibilities:

| Layer | File | Content |
|---|---|---|
| Rules — what | `lib/rules/writing.md`, `lib/rules/constructions.md`, `lib/rules/style.md`, `lib/languages/<lang>.md`, `lib/genres/*.md`, `lib/techniques/*.md` | The universal punctuation rules, the construction-scoped rules (quotation, abbreviation, headed-text, lists) whose sections are applied only when the matching construction is in the input, the substantive style foundation, the per-language realisations split into mechanics and style sections inside a single file, the content-type-specific rules, and the narrative or analytical arcs. |
| Procedure — how | `lib/protocols/proofread.md`, `lib/protocols/redline.md`, `lib/protocols/dialogue.md`, `lib/protocols/subagent.md`, `lib/protocols/io.md` | The proofread pass procedure, the redline pass procedure (including the shared finding format), the human-in-the-loop settling procedure, the subagent settling procedure, the I/O protocol (input detection plus inline-output and file/URL-output routing). The language-resolution procedure is inlined into each consuming SKILL.md. |
| Skill — entry | `skills/proofread/SKILL.md`, `skills/redline/SKILL.md`, `skills/edit/SKILL.md` | Each composes one or more procedure files and carries its own language-resolution logic. No skill duplicates rule content or pass procedure; rules and pass procedures are by reference. |

Changing a rule requires editing exactly one place. Adding a new content type, technique, or language requires no `SKILL.md` change. The inheritance is enforced by composition — `/redline` and `/edit` reference the same `protocols/proofread.md` and `protocols/redline.md` files that `/proofread` and `/redline` use respectively.

## Content types

The plugin covers nine content types — the last is a fallback:

| Content type | Swedish term | Default technique |
|---|---|---|
| Article / reportage / blog post | artikel | ABT |
| Case study | kundcase | ABT |
| Press release | pressmeddelande | none |
| Web copy | webbcopy | ABT (outer arc plus iterative microstructure) |
| Teaser | puff | mini-ABT (microstructure) |
| Report / whitepaper | rapport | PAC |
| Column | krönika | ABT (drawing, freely visible) |
| Opinion piece | opinionstext | ABT (pushing, explicit-argumentative) |
| General (fallback) | allmän text | none |

Each content type has its own file in `lib/genres/` describing its purpose and context, stylistic nuance (tone, length, structure, headline conventions, address), default technique, and common pitfalls. The files are compact — only what distinguishes the type from the general rules. Language-specific realisations (e.g., which mark renders attribution in a particular language) come from the loaded language files. Sections within each genre file are annotated with `<!-- scope: write -->` or `<!-- scope: review -->` markers so write-only sections are skipped during review passes and vice versa; sections relevant to both phases are left unmarked.

Maximum headline length is 60 characters for every H1, H2, H3, and below across all content types.

**Blog post.** *Blog post* / *blogginlägg* is not a content type of its own. When you ask for a blog post, the plugin asks whether it should be written as article or column.

**E-book.** E-books are handled chapter by chapter. The plugin asks per chapter which content type fits (article, case study, or report are the most common).

**Out of scope.** Ad copy, Google Ads copy, and bare social-media copy without a teaser purpose are explicitly outside the plugin's coverage.

## Techniques

Two techniques are installed out of the box:

- **ABT (And, But, Therefore)** — narrative arc. Sets the scene, introduces an obstacle or question, delivers the resolution. Default for article, case study, web copy, teaser, column, and opinion piece. The structure should be invisible to the reader — if the text feels formulaic, the technique has failed.
- **PAC (Premise, Analysis, Conclusion)** — analytical arc. Establishes the underlying material, analyses what it means, draws the conclusion. Default for report. Tolerates and even welcomes being visible at the section level — the reader of a report expects to see the path from data to conclusion.

Each technique file describes the arc concretely with variants (nesting, iteration, in medias res for ABT; nesting and partial PAC for PAC) and concrete examples.

**Techniques are not applied from training data.** If a user asks the plugin to use a technique that does not exist as an installed file in `lib/techniques/` (e.g., *PAS*), the plugin refuses and points to the alternatives. This is deliberate: techniques are installed artefacts, not claimed capabilities.

## Global rules

Three global rules apply across all content types wherever the redline pass runs — `/redline` Phase 2, `/edit` Phase 2, and `/write` Phase 4:

- **Source fabrication ban.** Every source cited — book, article, study, author, interview subject, dataset, statistic with attribution — must exist and be verified. The only exception is when the user explicitly requests a fictional source (e.g., a hypothetical interview subject as part of a thought experiment).
- **AI metaphor ban.** The plugin does not invent metaphors. If a metaphor exists in the source material, it can be used and deepened — by staying with that one metaphor. Invented metaphors are typically flat and undermine the text.
- **Rhetorical question rule.** The plugin does not invent rhetorical questions. If they appear in the source material, they can be kept and improved. Strict in report; looser in column and opinion where rhetorical address is part of the genre — but never as filler.

## Extending the plugin

The plugin is deliberately modular. New content types, techniques, and languages can be added without modifying any `SKILL.md`.

**New content type.** Create a file `lib/genres/<name>.md` with YAML frontmatter matching the pattern:

```yaml
---
name: your-type-name
swedish_term: swedish-term
default_technique: abt
triggers:
  - canonical-term-english
  - idiosyncratic-other-language-term
not_triggers:
  - phrase-that-would-otherwise-match-but-should-not
disambiguation:
  ambiguous-phrase: "ask type-A-or-type-B"
---
```

`triggers` lists the canonical terms that should fire this content type. `not_triggers` lists exceptions — phrases that would otherwise match but should not. `disambiguation` lists phrases that match this type but require asking the user before committing (e.g., *blogginlägg* maps to article or column). Use `lib/genres/article.md` as the working template.

A single genre is flagged as the fallback by adding `default: true` to its frontmatter — `lib/genres/general.md` currently carries this flag. When no trigger matches and no semantic likeness lands cleanly, skills fall back to the genre whose frontmatter has `default: true`. Exactly one genre must carry the flag.

Then describe the type's purpose, stylistic nuance, default technique, and common pitfalls following the pattern in the existing content-type files. Annotate each section heading with `<!-- scope: write -->` (sections relevant only to drafting — typically address, structure, length, headings, format conventions, default technique) or `<!-- scope: review -->` (sections relevant only to critical review — typically common pitfalls and review-only checks). Sections relevant to both phases (purpose, trigger keywords) are left unmarked. The review skills (`/redline`, `/edit`) skip write-scoped sections; the write skill (`/write`) skips review-scoped sections.

Finally, add a matching block for the new genre to `lib/genres/_index.md` so the skills can discover it without reading every genre file in full.

**New technique.** Create a file `lib/techniques/<name>.md` with the corresponding frontmatter. Describe the technique in parallel with ABT and PAC: the carrying parts, variants, where it applies, concrete examples.

**New language.** Create one file: `lib/languages/<lang>.md`. The file carries both layers in named sections — a `<!-- layer: mechanics -->` section for proofread scope (typography, quotation marks, quotation conventions, punctuation conventions, grammar specifics, greetings and closings) and a `<!-- layer: style -->` section for redline / edit scope (address and voice, AI-tell manifestations, interference from other languages, genre adjustments). Name the language part per the POSIX locale form (`sv`, `sv_SE`, `nb_NO`, `de_DE`, etc.). Use the existing language files as a template. The *Mechanics* section must always exist; the *Style* section is optional (a language with no meaningful style layer can ship mechanics only, as `default-mechanics.md` does). For territorial variants, see the inheritance note under *Languages* above — the overlay loader is not yet implemented.

`/write`, `/redline`, and `/edit` resolve content types through `lib/genres/_index.md` — a static, hand-maintained index that mirrors the frontmatter of every file in `lib/genres/`. When you add, rename, or remove a genre file, update `_index.md` to match. The skills read the index directly; they do not regenerate it. Languages are still discovered automatically through directory inventory of `lib/languages/`.

Before editing any files under `skills/` or `lib/`, read the **Authoring rules** section below — it captures the architectural constraints that earlier rounds of cleanup have established and that future changes must preserve.

## Design principles

- **DRY.** Shared rules live in one place. The proofread pass is described once across three layers. Language-specific conventions live only in the language layer files. No trigger keywords are duplicated between `SKILL.md` and content-type frontmatter.
- **Modular.** New content type = one new file (plus a row in `lib/genres/_index.md`). New technique = one new file. New language = one new file (`<lang>.md` with `<!-- layer: mechanics -->` and optionally `<!-- layer: style -->` sections). No `SKILL.md` needs to change.
- **Manual context loaders.** `/writing-rules`, `/abt`, `/pac` fire only on explicit slash commands. Their descriptions document what they do — not when to invoke them.
- **Tools, not algorithms.** The skill files describe outcomes and rules. They do not specify matching algorithms or file-search heuristics — the plugin solves the mechanics with standard tools (Glob, Grep, Read, Edit, Write, Bash).
- **The user, not the author.** All skill-internal text addresses *the user*. The plugin is generic; the house voice it embodies is documented in metadata, not embedded in the skill text.
- **English baseline, language layer for the rest.** Everything outside `lib/languages/` is written in British English. Per-language conventions, examples, and overrides live in `lib/languages/<lang>.md` (with mechanics and style as named sections).
- **Token-aware.** The subagent is invoked once per `/write` (Phase 4, auto), once per `/edit` (Phase 3, auto), and once per `/redline` invocation when the user delegates an open finding. Maximum three iterations per invocation, early termination preferred. Skills load one language file per run (`/proofread` applies only its *Mechanics* section; `/redline`, `/edit`, and `/write` apply both sections) plus `rules/constructions.md`, whose four sections are applied cognitively only when the matching construction appears in the input.

## Authoring rules

These rules govern how to edit the files in this plugin. They exist to prevent a recurring failure mode where well-meaning changes reintroduce architectural drift — duplicated prose between skill files, cross-references that read like helpful documentation, protocols that quietly bind themselves to one specific caller. The rules apply to anyone (human or AI) modifying anything under `skills/` or `lib/`.

**1. No skill cross-references in execution context.** A skill's body — the markdown below the frontmatter, loaded *after* the skill triggers — must not name or describe other skills. By the time Claude reads the body, it has already chosen the skill; knowing what siblings do adds noise without operational value. The exception is the frontmatter `description`, which is always in context and drives trigger decisions. Cross-references there are fine when they serve *differentiation* (*AFK variant of /redline*); they are not fine when they merely document architecture.

**2. Files don't know each other without an operational reason.** A rule file describes its own rules and does not advertise sibling rule files. A protocol file describes its own procedure and does not name specific callers or specific rule files it expects. The architectural map — who calls what, how the layers stack — lives in this README, not in the artefacts. The artefacts are self-contained.

**3. Procedure and data are separate, and they don't merge.** Protocol files (`lib/protocols/*.md`) describe *how*. Rule files (`lib/rules/*.md`, `lib/languages/*.md`, `lib/genres/*.md`, `lib/techniques/*.md`) describe *what*. Merging them — even when one protocol seems to be the only consumer of a particular rule file — breaks reusability for skills that need the data without the procedure.

**4. Protocols are agnostic about their callers.** A procedure file does not say *the user invoked /proofread*; it says *the user wants…*. It does not name which rule files are applied; it says *the loaded rule files*. Each calling skill loads its own rule files in its `Files to read` list and applies the protocol against them. This is what makes the same procedure usable across skills with different scope.

**5. Universal rules in `lib/rules/`, language rules in `lib/languages/`.** A rule that holds across languages (the principle of avoiding AI-tell, the body-text-self-sufficiency rule, the PAC visibility tolerance) goes in `rules/` or in a content-type file. A rule whose realisation depends on the language (which character renders an attribution, which substitutions to make against training-language interference) goes in the language layer files. When a universal rule references a language-specific realisation, it does so by saying *see the loaded language file*.

**5a. Mechanics vs style as named sections inside one language file.** Each language is represented by a single file `<lang>.md` carrying both layers in named sections: a `<!-- layer: mechanics -->` section (proofread scope — typography, quotation marks, quotation conventions, punctuation, grammar specifics, greetings) and a `<!-- layer: style -->` section (redline / edit scope — address and voice, AI-tell manifestations, interference patterns, genre adjustments). The proofread protocol applies only the *Mechanics* section; the redline and edit protocols apply both. Place each new language rule under the section that matches its scope. A language with no meaningful style layer (the international baseline) can ship mechanics only — `default-mechanics.md` retains its standalone-file name and has no `<!-- layer: -->` markers because no companion style layer exists for it. The construction-scoped universal rules live in a single file `rules/constructions.md` with four `<!-- construction: -->` sections (quotation, abbreviation, headed-text, lists); the file is always loaded and the sections are applied cognitively when the matching construction appears in the input.

**6. No false equivalence claims.** If two skills differ in scope, behaviour, or settling mechanism, they are not *the same thing with one difference*. Describe each honestly. *Phase 1 identical to /proofread* is false if /proofread loads one rule file and Phase 1 loads two — even if both follow the same protocol.

**7. Progressive disclosure in SKILL.md.** Frontmatter is always in context — put the full description and trigger logic there. The body is loaded when the skill triggers — keep it lean: one or two imperative sentences plus the file list. Body prose should not duplicate the frontmatter or the file list.

**8. DRY where the abstraction is real, duplicate where it isn't.** A shared file is justified when multiple callers genuinely follow the same procedure or apply the same rules. The current shared protocols (`protocols/proofread.md`, `protocols/redline.md`) capture real abstractions — both are followed identically by their callers, varying only in which rule files are loaded. Do not introduce shared files for accidental similarity; do not duplicate when the shared abstraction is real.

**9. Lean prose, imperative with whys.** Four sentences saying the same thing differently is overwork. Prefer one imperative followed by a short explanation of why, rather than ALL-CAPS, MUSTs, or stacked redundant clauses. Today's models do better with reasoning than with commands.

**10. No vague descriptions.** Phrases like *conservative error correction* without specifying *what* is conserved invite the model to fill the gap with its own interpretation. Either specify (*fix what is objectively wrong, leave style alone*) or omit and let the protocol carry the definition.

### Audit checklist before committing changes

- Search for skill names (`/proofread`, `/redline`, `/edit`, `/write`, `/writing-rules`, `/abt`, `/pac`) in `lib/protocols/*.md`. The only legitimate match is in `lib/protocols/subagent.md`, which describes the subagent role within a parent skill.
- Search for skill names in another skill's *body* (not just file references like `protocols/proofread.md`, but `/proofread` itself).
- Compare `skills/redline/SKILL.md` and `skills/edit/SKILL.md` — Phase 1 and Phase 2 sections should not be duplicated verbatim. Shared procedure belongs in a shared protocol file.
- Search for specific rule-file names (`rules/writing.md`, `rules/constructions.md`, `rules/style.md`, the language files) inside protocol files. They should not appear; protocols speak of *the loaded rule files* and *the loaded language file*.
- Confirm `lib/languages/` contains a `<lang>.md` per installed language, each with `<!-- layer: mechanics -->` and (where the language has a meaningful style layer) `<!-- layer: style -->` section markers. The default fallback ships as `default-mechanics.md` — a standalone mechanics-only file with no `<!-- layer: -->` markers. Place a new convention under the section that matches its layer.
- Confirm `lib/genres/_index.md` lists every genre file in `lib/genres/` with matching frontmatter (`name`, `swedish_term`, `default_technique`, `triggers`, plus `default`, `not_triggers`, and `disambiguation` where set). Exactly one genre carries `default: true`.
- Open each genre file and confirm sections are annotated with `<!-- scope: write -->` or `<!-- scope: review -->` markers where the section is relevant to only one phase. Sections relevant to both (purpose, trigger keywords) stay unmarked.
- Search for Swedish-only or English-only prose outside `lib/languages/`. All files outside the language directory should be in British English with no embedded Swedish examples (canonical Swedish triggers in genre frontmatter, which are user-input matchers, are the documented exception).
- Read each skill body. If it summarises content also covered in a referenced file, pick one location and remove the duplicate. The language-resolution procedure is the documented exception — it lives inline in every consuming SKILL.md by design.
- Read each frontmatter description. Does it overstate equivalence between skills? Does it differentiate this skill from siblings clearly enough that Claude knows when to pick it?

## Requirements

The plugin requires Claude Code or Cowork with support for slash commands, YAML frontmatter with `disable-model-invocation`, and subagents (for `/write` Phase 4, `/edit` Phase 3, and `/redline` when the user delegates). No external libraries or MCP servers are required — the plugin is self-contained.

## License

Proprietary. See `.claude-plugin/plugin.json`.

## About

Made by [Kntnt](https://kntnt.com).
