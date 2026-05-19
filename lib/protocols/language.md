# Language determination

The procedure for choosing which language file a skill loads. The calling skill picks one of two source modes for the no-argument case; the rest of the procedure is shared.

## Source modes

The calling skill names one of two modes:

- **Detect mode** — source the language from the input text. Used by skills that process an existing text.
- **Propose mode** — propose a target language from the prompt's language (and any source material) and ask the user to confirm. Used by skills that create new text.

## Resolution

1. **Argument.** If the user passed a language argument (e.g. `sv`, `sv_SE`, `en`, `en_GB`, `en_US`), use it as the candidate. A bare language argument (`sv`, `en`) that matches no file directly but matches several territorial variants (e.g. `en` matches `en_GB.md` and `en_US.md`) is treated as an ambiguous candidate and goes to the disambiguation question below.
2. **Source step.** Without an argument, apply the calling skill's chosen mode (detect or propose) to determine the candidate.
3. **Inventory.** Check `lib/languages/` for files matching the candidate:
   - If a single file matches, use it.
   - If several files match (e.g. `en.md`, `en_GB.md`, `en_US.md` all exist for the candidate `en`), ask the user which to use.
   - If no file matches, fall back to `lib/languages/default.md` and mention this in the reply (in English):
     > No language file found for [language]. Baseline conventions from `default.md` apply. Add `lib/languages/<code>.md` for stricter control.

The same disambiguation question covers both routes — an ambiguous bare argument and an ambiguous detection or proposal go through the same path.
