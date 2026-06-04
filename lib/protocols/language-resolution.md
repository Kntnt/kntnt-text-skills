# Language resolution protocol

How a calling skill resolves the input or proposed language to a single language file in `lib/languages/`, applies any inheritance overlay declared by that file and reports the outcome. The procedure is caller-agnostic – it speaks of *the calling skill*, *the input* and *the loaded language file*; the calling skill names its own source mode and its own scope of layers.

The protocol is data-aware about one directory: `lib/languages/`. The fallback file `default-mechanics.md` lives in that directory and is named explicitly here because it is the documented baseline the resolution flow falls back to.

## Resolution flow

The procedure runs once per invocation. The calling skill supplies two inputs: a *language argument* (possibly absent) from the user's invocation, and a *source mode* – either *detect mode* (the language is inferred from the text being reviewed) or *propose mode* (the language is proposed for the text being created and confirmed with the user).

1. **Argument.** If the user passed a language argument (e.g. `sv`, `sv_SE`, `en`, `en_GB`, `en_US`), use it as the candidate. A bare argument (`sv`, `en`) that matches no file directly but matches several territorial variants (e.g. `en` matches `en_GB.md` and `en_US.md`) goes to the disambiguation step below.
2. **Source step.** Without an argument, derive the candidate from the source mode:
   - *Detect mode.* Infer the language from the input text.
   - *Propose mode.* Propose a target language based on the prompt's language and any source material, and ask the user to confirm.
3. **Inventory.** Look for `<lang>.md` in `lib/languages/` for the candidate:
   - **One match.** Load it. If its frontmatter declares an `inherits` field, apply the overlay procedure below before any caller-side use of the loaded content.
   - **Several matches.** Ask the user which to use. Continue with the chosen file as in *One match*.
   - **No match.** Fall back to `lib/languages/default-mechanics.md` and report the absence in the calling skill's reply (in English):
     > No language file found for [language]. Baseline conventions from `default-mechanics.md` apply. Add `lib/languages/<code>.md` for stricter control.

The calling skill receives one loaded language file at the end of resolution – either a base file, a base-with-overlay-applied composite or `default-mechanics.md`. Which named sections of the loaded file apply (mechanics, style or both) is the calling skill's concern.

## Overlay semantics

The overlay mechanism lets a territorial variant (e.g. a future `sv_FI.md`) reuse the base language file (e.g. `sv.md`) and replace or add only the sections that differ. The trigger is the presence of an `inherits` field in the resolved file's frontmatter:

```yaml
---
name: sv_FI
language: Finland Swedish
inherits: "@sv.md"
---
```

The `inherits` value uses the syntax `"@<base>.md"` – the `@` prefix marks the value as a file reference within the same directory (`lib/languages/`). The base file must exist in that directory.

### What the overlay unit is

The overlay unit is **H2 sections** (`## Section`) inside the two layer markers `<!-- layer: mechanics -->` and `<!-- layer: style -->`. That is the same level as *Typography*, *Quotation marks*, *Punctuation conventions*, *Address and voice*, *AI-tell manifestations* and similar H2 headings inside the layer blocks.

For each H2 in the variant file:

- **Same heading as a base H2 under the same layer marker.** The variant H2 replaces the base H2 entirely. The replacement is wholesale – the base section is dropped and the variant section takes its place.
- **Heading absent from the base under the same layer marker.** The variant H2 is appended to that layer in the composite.

For each H2 in the base file with no matching heading in the variant under the same layer marker:

- The base H2 is carried into the composite unchanged.

### What the overlay unit is not

An H3 sub-section (e.g. *Run-in quotation* under *Quotation conventions*) **cannot** be overridden in isolation. An H3 inherits or overrides as part of its H2 parent. The overlay does not merge inside an H2 section.

There is no partial within-section merge of any kind – not for tables, not for lists, not for paragraphs.

> **Sharp edge – read this before authoring a variant.** A variant that wants to change a single table row inside an H2 section (e.g. one row of the *Typography* table) must duplicate the entire H2 section in the variant file and edit the row in the copy. The variant cannot say "override only this row of the base table". The base H2 is replaced wholesale or carried through unchanged – there is no middle option. This is deliberate: predictable resolution beats clever merging, and the price is duplication when the variant is small.

### Variant layer structure

A variant file with `inherits` must mirror the base's layer-marker structure. That means:

- One `<!-- layer: mechanics -->` marker, placed before the mechanics-scope H2 sections.
- One `<!-- layer: style -->` marker (if the base has a style layer), placed before the style-scope H2 sections.

Every H2 section in the variant must sit under one of those layer markers. An H2 outside both markers is a structural error in the variant file – flag it during the load and refuse to proceed with the overlay until the variant is corrected.

Sections inside the variant are classified by which layer marker precedes them, mirroring how the base file classifies its own sections. A variant cannot reclassify a base section from one layer to the other – the heading match is per-layer.

## Depth

Inheritance is **one step only**. A variant inherits from a base; a base does not inherit from anything. Two-step inheritance is not allowed: when the resolved file has `inherits`, the file it points to must not itself have `inherits`.

Cycles are impossible by construction – the base never has `inherits`, so no chain of length > 1 can exist.

## Conflicts

There are no conflicts to resolve. When a variant H2 and a base H2 share a heading under the same layer, the variant always wins and the base section is dropped.

## Fallback

When no language-specific file matches the candidate after argument, source step and inventory, load `lib/languages/default-mechanics.md` and report the absence in the calling skill's reply (in English):

> No language file found for [language]. Baseline conventions from `default-mechanics.md` apply. Add `lib/languages/<code>.md` for stricter control.

`default-mechanics.md` has no layer markers and no `inherits` field – it is a standalone baseline. The overlay procedure does not apply to the fallback file.

## Reporting

Reporting on resolution outcomes is bounded:

- **Specific match (with or without overlay).** Silent. The user does not need a note that a matching language file was found.
- **Multiple matches requiring disambiguation.** Ask the user which variant to use.
- **No match – fallback to `default-mechanics.md`.** Report once, in the calling skill's reply, using the wording above.
- **Structural error in a variant file** (overlay applied, but the variant has H2 sections outside the layer markers, or `inherits` points to a non-existent base, or the pointed-to file itself has `inherits`). Refuse to proceed with the overlay and report the structural problem so the variant file author can fix it.
