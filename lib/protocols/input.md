# Input detection

A task skill that operates on user-supplied text accepts the input in several modes. This file describes the modes and the expected outcome at each ambiguity point. The mechanics (which tool to call, how to read directories, how to handle URLs) are left to the calling agent, which solves them with the standard file tools (Glob, Grep, Read) and web-fetch tools.

## Input modes

The user can provide input in any of these forms:

- **Inline text in the prompt.** The text to operate on is included directly in the user's message, often after the slash command. Use it as-is.
- **File referenced via `@`-notation.** The user explicitly attaches a file path with `@`-notation. Read the file and operate on its contents.
- **File described by name.** The user mentions a filename or describes a file in natural language ("rätta artikeln om vitvaror", "the report I just saved"). The agent finds the file in the workspace.
- **URL.** The user supplies a URL. Fetch the content and operate on it. The output protocol applies — URLs are read-only, so the output goes elsewhere than back to the source.
- **Upload.** A file appears in the uploads area of the session. Read it from there.

## Search domain when a file is described by name

The agent searches the user's workspace folder recursively and the uploads folder if present. Matching is on filename and on text features the user mentioned (a working title, a topic phrase, a date).

## Outcomes for file-by-name input

- **Zero candidates.** Ask the user which file is meant. Do not guess.
- **One candidate.** Use it. Report in the response which file was read so the user can confirm.
- **Multiple candidates.** List them with their paths and ask the user which is meant.

## Bare slash command

When the calling skill is invoked with no following text and no file reference, operate on the most recent text in the conversation — typically the previous assistant message or the text that the conversation was just working on. A skill that creates new content rather than revising an existing text treats a bare invocation as a new request, starting from the most recent prompt or material in the conversation as context.

## Multiple files in one prompt

When the user references several files in one prompt, run the skill per file in a loop. The output protocol applies to each file separately.
