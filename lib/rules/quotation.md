# Quotation

Three quotation modes, each with its own conventions. Identify which mode a quotation belongs to before applying the rules. The base regime below uses straight double quotation marks `"` and straight single quotation marks `'` as typographic placeholders. The loaded language file replaces these with the typographically correct characters for that language and may override or extend any rule.

- **Run-in quotation.** Verbatim text embedded inline within a sentence.
- **Block quotation.** Verbatim text set off as an indented block — used for citations of approximately one hundred words or more, six to eight lines or more, or for correspondence, lists, and poetry regardless of length.
- **Dialogue.** Reported direct speech in narrative text.

## Run-in quotation

The verbatim text is enclosed in straight double quotation marks `"…"`. Phrase the surrounding sentence so the quoted words fit logically and grammatically; tense and pronouns in the surrounding text must harmonise with the quotation.

- **Comma for standard attribution.** *She replied, "I'll be there."*
- **No comma when the quotation flows in as a grammatical object or fragment.** *She said that the proposal was "completely unacceptable."*
- **Colon for more formal or longer introductions.** *His argument was clear: "We must act now."*
- **Capitalisation.** Capitalise the first letter when the quotation is a complete sentence introduced by comma or colon. When the quotation slides into the surrounding syntax, use lower case. If the original had a capital, mark the change with brackets: *"[T]he proposal was unacceptable."*
- **Modifications.** Brackets `[ ]` mark additions or modifications. Ellipsis `…` marks omissions. `[sic]` marks an error in the original that has been preserved.
- **Inner quotation.** Use straight single quotation marks `'…'` for a quotation within a quotation.

## Block quotation

Use when the quotation reaches approximately one hundred words or six to eight lines, or for correspondence, lists, and poetry regardless of length.

- **Format.** Start on a new line, indented. In Markdown use `> ` at the start of each line followed by the text. GFM treats a hard newline as `<br>`, so each block-quote paragraph stays on one line.
- **No surrounding quotation marks.** The indentation is the marker.
- **Existing quotation marks in the original are preserved.**
- **Introduction.** Usually a colon, or a full stop when the preceding sentence is self-contained.
- **Source attribution** is placed after the closing punctuation — differs from run-in, where the attribution comes before the full stop.
- **Inner quotation** follows the same rules as run-in. Specifically, use straight double quotation marks `"…"` for inner quotation, since the outer block carries no marks.

## Dialogue

- **Speech marks.** Each utterance is enclosed in straight double quotation marks `"…"`.
- **New speaker = new paragraph.** Even if the utterance is a single word.
- **Attribution.** The reporting clause (*she said*, *he replied*) is separated by a comma. *"I'll come," she said.* / *She said, "I'll come."*
- **Question or exclamation inside the utterance.** *"Will you?" she asked.* — no comma after the `?`, lower-case *she*.
- **Broken or stammered speech.** Marked with dash or ellipsis.
- **Multi-paragraph utterances.** When one speaker continues across paragraphs, open each new paragraph with an opening quotation mark and close only the final paragraph — so the reader sees that the same speaker continues.

## Language overrides

Language files override or extend this regime as needed. Notably, Swedish (`sv-mechanics.md`) replaces the Dialogue rules with the speech-dash convention, and distinguishes typographically between word-for-word quotation and rendered attribution — a distinction that does not exist in English.
