# Languages

The plugin separates universal rules from language-specific realisations. Files in `lib/rules/`, `lib/genres/`, `lib/techniques/` and `lib/protocols/` are language-agnostic (all examples in British English). Per-language conventions live in `lib/languages/` as one file per language. Each file carries both layers in named sections – a `<!-- layer: mechanics -->` section with the proofread-scope conventions and a `<!-- layer: style -->` section with the redline / edit-scope conventions. The ship set:

- `default-mechanics.md` – international baseline (fallback when no language-specific file exists)
- `sv.md` – Swedish
- `en_GB.md` – British English
- `en_US.md` – American English

Naming follows the POSIX locale form `language_TERRITORY`. Both bare language codes (`sv`, `en`) and territorial variants (`sv_SE`, `sv_FI`, `en_GB`, `en_US`) are accepted as skill arguments. The resolver maps a language code `<lang>` to the single file `<lang>.md`; skills decide which section they apply (mechanics, style or both) based on the pass they run.

A territorial variant declares an inheritance relationship with its base – for a future `sv_FI.md` the frontmatter would read:

```yaml
---
name: sv_FI
language: Finland Swedish
inherits: "@sv.md"
---
```

The overlay loader is documented in [`../lib/protocols/language-resolution.md`](../lib/protocols/language-resolution.md) and active. The overlay unit is the H2 section inside the `<!-- layer: mechanics -->` and `<!-- layer: style -->` markers – a variant H2 with the same heading as a base H2 under the same layer replaces it wholesale; an absent-in-base H2 is appended. H3 sub-sections cannot be overridden in isolation, and there is no partial within-section merge: a variant that wants to change a single table row must duplicate the entire H2 section. Inheritance is one step only – a base never has `inherits`, so cycles are impossible. No territorial variant ships yet; the protocol is a no-op for the current language files because none of them carries an `inherits` field.

## Mechanics and Style sections

The two-section layout enforces the split between layers within a single file. The *Mechanics* section carries proofread-scope conventions (typography, quotation, punctuation, grammar, greetings); the *Style* section carries redline / edit-scope conventions (address and voice, AI-tell manifestations, interference patterns, genre adjustments).

`/proofread` applies only the *Mechanics* section. `/redline`, `/edit` and `/write` apply both. The proofread pass cannot drift into stylistic touch-ups because the *Style* section is explicitly out of its scope.

## Default fallback

When no language-specific file exists for the determined language, skills fall back to `lib/languages/default-mechanics.md`. It carries international-standard typography (ISO 8601 dates, SI unit conventions) plus internationally neutral defaults for ambiguous cases (straight ASCII quotation marks, EN-dash with spaces for parentheticals, no Oxford comma, British-style punctuation relative to quotes). There is no companion `default-style.md` because address, AI-tell manifestations, interference and genre adjustments are inherently language-and-culture-bound and have no meaningful baseline.

Loading is either-or: a skill loads the specific language file if it exists, otherwise `default-mechanics.md`. They are not mixed.

When `default-mechanics.md` is used, the skill mentions in its reply (in English):

> No language file found for [language]. Baseline conventions from `default-mechanics.md` apply. Add `lib/languages/<code>.md` for stricter control.

## Language determination flow

The resolution procedure lives in [`../lib/protocols/language-resolution.md`](../lib/protocols/language-resolution.md). Each consuming `SKILL.md` references the protocol and supplies its own source mode. In summary:

1. **Argument.** If the user passes a language argument (e.g. `/proofread sv`, `/edit en_GB`), use it. A bare argument that matches no file directly but matches several territorial variants (e.g. `en` matches both `en_GB.md` and `en_US.md`) triggers a disambiguation question.
2. **Source step.** Without an argument, the calling skill picks a source mode: *detect mode* (`/proofread`, `/redline`, `/edit` – source from the input text) or *propose mode* (`/write` – propose from the prompt's language and confirm).
3. **Inventory.** Check `lib/languages/` for matching files. If multiple language matches arise, ask the user which to use. If a single language matches, load the file (and apply the overlay procedure when the file declares `inherits`). If none, fall back to `default-mechanics.md` and report the absence.

The manual context loader `/writing-rules` loads either the specified language's file or every installed language file.
