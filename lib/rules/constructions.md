# Construction-scoped rules

Universal rules for specific text constructions. The calling skill loads this file always; sections are applied cognitively based on which constructions appear in the input.

<!-- construction: quotation -->
## Quotation

Three quotation modes, each with its own conventions. Identify which mode a quotation belongs to before applying the rules. The base regime below uses straight double quotation marks `"` and straight single quotation marks `'` as typographic placeholders. The loaded language file replaces these with the typographically correct characters for that language and may override or extend any rule.

- **Run-in quotation.** Verbatim text embedded inline within a sentence.
- **Block quotation.** Verbatim text set off as an indented block – used for citations of approximately one hundred words or more, six to eight lines or more, or for correspondence, lists and poetry regardless of length.
- **Dialogue.** Reported direct speech in narrative text.

### Run-in quotation

The verbatim text is enclosed in straight double quotation marks `"…"`. Phrase the surrounding sentence so the quoted words fit logically and grammatically; tense and pronouns in the surrounding text must harmonise with the quotation.

- **Comma for standard attribution.** *She replied, "I'll be there."*
- **No comma when the quotation flows in as a grammatical object or fragment.** *She said that the proposal was "completely unacceptable."*
- **Colon for more formal or longer introductions.** *His argument was clear: "We must act now."*
- **Capitalisation.** Capitalise the first letter when the quotation is a complete sentence introduced by comma or colon. When the quotation slides into the surrounding syntax, use lower case. If the original had a capital, mark the change with brackets: *"[T]he proposal was unacceptable."*
- **Modifications.** Brackets `[ ]` mark additions or modifications. Ellipsis `…` marks omissions. `[sic]` marks an error in the original that has been preserved.
- **Inner quotation.** Use straight single quotation marks `'…'` for a quotation within a quotation.

### Block quotation

Use when the quotation reaches approximately one hundred words or six to eight lines, or for correspondence, lists and poetry regardless of length.

- **Format.** Start on a new line, indented. In Markdown use `> ` at the start of each line followed by the text. GFM treats a hard newline as `<br>`, so each block-quote paragraph stays on one line.
- **No surrounding quotation marks.** The indentation is the marker.
- **Existing quotation marks in the original are preserved.**
- **Introduction.** Usually a colon, or a full stop when the preceding sentence is self-contained.
- **Source attribution** is placed after the closing punctuation – differs from run-in, where the attribution comes before the full stop.
- **Inner quotation** follows the same rules as run-in. Specifically, use straight double quotation marks `"…"` for inner quotation, since the outer block carries no marks.

### Dialogue

- **Speech marks.** Each utterance is enclosed in straight double quotation marks `"…"`.
- **New speaker = new paragraph.** Even if the utterance is a single word.
- **Attribution.** The reporting clause (*she said*, *he replied*) is separated by a comma. *"I'll come," she said.* / *She said, "I'll come."*
- **Question or exclamation inside the utterance.** *"Will you?" she asked.* – no comma after the `?`, lower-case *she*.
- **Broken or stammered speech.** Marked with dash or ellipsis.
- **Multi-paragraph utterances.** When one speaker continues across paragraphs, open each new paragraph with an opening quotation mark and close only the final paragraph – so the reader sees that the same speaker continues.

### Language overrides

Language files override or extend this regime as needed. Notably, Swedish replaces the Dialogue rules with the speech-dash convention, and distinguishes typographically between word-for-word quotation and rendered attribution – a distinction that does not exist in English.

<!-- construction: abbreviation -->
## Initialisms, acronyms and lower-case initialisms

Three categories with different writing rules. They apply in running text. The categories themselves are universal; each language file lists category-1 forms specific to that language (which initialisms have become everyday words there).

### 1. Lower-case initialisms (everyday words)

Initialisms that have become established everyday words are written in lower case without full stops. They are normally not spelled out in running text – they function as their own words.

Exception: at first occurrence in a text aimed at a reader who may not know the abbreviation, it can be spelled out. For generally familiar lower-case initialisms, spelling out is unnecessary and disruptive. The language file lists which initialisms qualify for this category in that language.

### 2. Initialisms and acronyms (not everyday words)

Initialisms that have not become everyday words are written in capitals without full stops. At first occurrence in a text, the spelled-out form is given. The spelled-out form follows the normal rules for capitalisation – lower case unless it is a proper name. The capitals in the abbreviation arise from the fact that it is an abbreviation, not because the words are proper names.

Correct: *SEO = search engine optimisation*, *GDPR = general data protection regulation*, *HTML = hypertext markup language*.

Wrong: *SEO = Search Engine Optimisation*, *HTML = HyperText Markup Language*. The error probably arises from writers reasoning backwards from the capitals in the abbreviation.

### 3. Proper names

Initialisms standing for proper names – organisations, companies, institutions – are written in capitals. The spelled-out form starts with a capital because it is a proper name.

Examples: *NATO = North Atlantic Treaty Organization*, *BBC = British Broadcasting Corporation*, *WHO = World Health Organization*.

### 4. Introducing abbreviations in running text

When an abbreviation that is not already established and familiar to the reader is used in a text, it must be introduced by writing the full name first, followed by the abbreviation in parentheses. The abbreviation is used alone for the rest of the text.

Correct: *the Society of Lock and Security Suppliers (SLSS) advocates for…*. Subsequently: *SLSS holds that…*.

Wrong: *SLSS – the Society of Lock and Security Suppliers – advocates for…*. The abbreviation precedes the spelled-out form, and dashes are used instead of parentheses. This forces the reader to see an incomprehensible abbreviation first and then retroactively understand what it means.

Wrong: *SLSS (the Society of Lock and Security Suppliers) advocates for…*. The abbreviation precedes the spelled-out form.

If the abbreviation occurs only once or twice in the text, it is often better not to introduce it at all and instead use the full name or a natural short form (*the society*, *the commission*) throughout. Generally familiar abbreviations (UN, FBI, NATO) need no introduction.

<!-- construction: headed-text -->
## Body-text self-sufficiency

Body text must be fully understandable when the H1 headline, any kicker or strapline, the standfirst and all subheadings are removed. These elements are paratextual – they help the reader navigate and entice reading, but they are not part of the body text and may not carry information that the body text presupposes.

This principle is documented in major editorial style guides (TT-språket for Swedish journalism, the *Guardian Style Guide*, *BBC News Style Guide*, AP Stylebook). The background is that headlines are often written or changed by a different person than the writer, and in digital publishing headlines can also be changed after publication.

### Concrete rules

The body text may not begin with a pronoun, a definite form or a reference that is only intelligible via the headline or standfirst. If the headline reads *SafeTeam launches new access system*, the body text may not begin with *The system rests on…* – it must establish on its own what is being referred to.

The same principle applies to subheadings: the text under a subheading may not presuppose that the reader has read the subheading. Subheadings function as visual rest stops and navigation aids, not as information carriers.

Standfirst and lead are two separate elements. The standfirst stands between the headline and the body text and summarises or sells the article – it is not part of the body text. The lead is the body text's first paragraph and therefore part of the body. The lead must be readable and understandable without the reader having first read the standfirst.

### Test method

A simple check is to remove the headline, any kicker or strapline, the standfirst and all subheadings, and then read the remaining body text. If the text contains unexplained pronouns, definite forms without a referent or logical jumps, information is missing and must be added to the body text.

<!-- construction: lists -->
## Lists

Lists are punctuated and capitalised consistently. When list items are complete sentences, each begins with a capital and ends with a full stop. When items are fragments, they typically begin with lower case and carry no terminal punctuation – though a final full stop on the last item is acceptable when the list closes a paragraph. The chosen convention is held consistent within a single list.
