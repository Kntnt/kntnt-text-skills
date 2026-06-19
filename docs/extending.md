# Extending the plugin

The plugin is deliberately modular. New content types, techniques and languages can be added without modifying any `SKILL.md`. Before editing any files under `skills/` or `lib/`, read [`authoring.md`](authoring.md) – it captures the architectural constraints that earlier rounds of cleanup have established and that future changes must preserve.

## New content type

Create a file `lib/genres/<name>.md` with YAML frontmatter matching the pattern:

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

`triggers` lists the canonical terms that should fire this content type. `not_triggers` lists exceptions – phrases that would otherwise match but should not. `disambiguation` lists phrases that match this type but require asking the user before committing (e.g. *blogginlägg* maps to article or column). Use `lib/genres/article.md` as the working template.

A single genre is flagged as the fallback by adding `default: true` to its frontmatter – `lib/genres/general.md` currently carries this flag. When no trigger matches and no semantic likeness lands cleanly, skills fall back to the genre whose frontmatter has `default: true`. Exactly one genre must carry the flag.

Then describe the type's purpose, stylistic nuance, default technique and common pitfalls following the pattern in the existing content-type files. Annotate each section heading with `<!-- scope: write -->` (sections relevant only to drafting – typically address, structure, length, headings, format conventions, default technique) or `<!-- scope: review -->` (sections relevant only to critical review – typically common pitfalls and review-only checks). Sections relevant to both phases (purpose, trigger keywords) are left unmarked. The review skills (`/redline`, `/edit`) skip write-scoped sections; the write skill (`/write`) skips review-scoped sections.

Finally, add a matching block for the new genre to `lib/genres/_index.md` so the skills can discover it without reading every genre file in full.

## New technique

Create a file `lib/techniques/<name>.md` with the corresponding frontmatter. Describe the technique in parallel with ABT and PAC: the carrying parts, variants, where it applies, concrete examples.

## New language

Create one file: `lib/languages/<lang>.md`. The file carries both layers in named sections – a `<!-- layer: mechanics -->` section for proofread scope (typography, quotation marks, quotation conventions, punctuation conventions, grammar specifics, greetings and closings) and a `<!-- layer: style -->` section for redline / edit scope (address and voice, AI-tell manifestations, interference from other languages, genre adjustments). Name the language part per the POSIX locale form (`sv`, `sv_SE`, `nb_NO`, `de_DE`, etc.). Use the existing language files as a template. The *Mechanics* section must always exist; the *Style* section is optional (a language with no meaningful style layer can ship mechanics only, as `default-mechanics.md` does). For territorial variants, declare `inherits: "@<base>.md"` in the frontmatter and follow the overlay semantics in [`../lib/protocols/language-resolution.md`](../lib/protocols/language-resolution.md) – H2 sections under the layer markers are the unit of override; H3 sub-sections cannot be overridden in isolation; one step deep only.

## How the skills discover what you add

`/write`, `/redline` and `/edit` resolve content types through `lib/genres/_index.md` – a static, hand-maintained index that mirrors the frontmatter of every file in `lib/genres/`. When you add, rename or remove a genre file, update `_index.md` to match. The skills read the index directly; they do not regenerate it. Languages are still discovered automatically through directory inventory of `lib/languages/`.
