# Proofread protocol

The procedure for conservative error correction in a text. Only what is objectively wrong is touched. Stylistic decisions are out of scope here — they require separate, more substantive editorial work.

## Scope

Correct on every invocation:

- Spelling and typos
- Grammar
- Punctuation
- Duplicated or missing words
- Wrong-word errors that are objectively wrong (preposition, article, language-specific agreement)
- Conventions in the loaded rule files and the mechanics section of the loaded language file (or the default mechanics file when no language-specific file is loaded), matched to the determined language

Leave everything else untouched, even when an improvement seems obvious. Stylistic word choice, word order, structure, voice, tone, argumentation, language-interference patterns, AI-tell constructions, weak verbs — all of these can be improved, but doing so crosses the line from objective correction into substantive editing. The language style layer is **not** in scope for this pass; it belongs to the redline / edit passes. The user invoked this pass precisely to avoid stylistic interference; making those calls violates the contract.

## Application

Silent — no commentary, no list of changes, no preamble. The user wants clean text back, not a discussion.

The calling skill determines the language and loads the matching language file (applying only its mechanics section) before invoking this protocol. When a language-specific file exists, use it; when none exists for the determined language, the calling skill falls back to the default mechanics file and reports the absence in its reply.

Preserve formatting exactly — line breaks, paragraphs, headings, lists, code blocks, blockquotes, tables. Correct the language inside the formatting, never the formatting itself.

## GFM convention

The plugin produces GitHub-Flavoured Markdown. In GFM a hard newline within a paragraph renders as `<br>`. When the input uses one paragraph per line — the typical convention — preserve that. Do not introduce hard line breaks inside paragraphs; they will show up as visible breaks in the rendered output.

## No-op behaviour

When the input contains no errors, the procedure produces no changes. Do not return the unchanged text. Skills that deliver output directly to the user return a short status message in the language of the input (*No errors found.* in English, *Inga fel hittade.* in Swedish, equivalent phrasings in other languages) and write nothing. Skills that pass the result into a later phase simply proceed with the unchanged input.

## Input source

Inline text: operate on it. Bare invocation with no text or file reference: operate on the most recent text in the conversation — typically the previous assistant message or the text just being worked on. See the *Input* section of `protocols/io.md` for file and URL inputs.
