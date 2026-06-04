# I/O protocol

How a task skill detects the form of its input and routes its output. The file is loaded whenever a skill handles user-supplied text; the calling skill applies the relevant section based on what the user actually provided. The mechanics (which tool to call, how to read directories, how to handle URLs) are left to the calling agent, which solves them with the standard file tools (Glob, Grep, Read) and web-fetch tools.

<!-- form: input -->
## Input

A task skill that operates on user-supplied text accepts the input in several modes. This section describes the modes and the expected outcome at each ambiguity point.

### Input modes

The user can provide input in any of these forms:

- **Inline text in the prompt.** The text to operate on is included directly in the user's message, often after the slash command. Use it as-is.
- **File referenced via `@`-notation.** The user explicitly attaches a file path with `@`-notation. Read the file and operate on its contents.
- **File described by name.** The user mentions a filename or describes a file in natural language ("rätta artikeln om vitvaror", "the report I just saved"). The agent finds the file in the workspace.
- **URL.** The user supplies a URL. Fetch the content and operate on it. The output protocol applies – URLs are read-only, so the output goes elsewhere than back to the source.
- **Upload.** A file appears in the uploads area of the session. Read it from there.

### Search domain when a file is described by name

The agent searches the user's workspace folder recursively and the uploads folder if present. Matching is on filename and on text features the user mentioned (a working title, a topic phrase, a date).

### Outcomes for file-by-name input

- **Zero candidates.** Ask the user which file is meant. Do not guess.
- **One candidate.** Use it. Report in the response which file was read so the user can confirm.
- **Multiple candidates.** List them with their paths and ask the user which is meant.

### Bare slash command

When the calling skill is invoked with no following text and no file reference, operate on the most recent text in the conversation – typically the previous assistant message or the text that the conversation was just working on. A skill that creates new content rather than revising an existing text treats a bare invocation as a new request, starting from the most recent prompt or material in the conversation as context.

### Multiple files in one prompt

When the user references several files in one prompt, run the skill per file in a loop. The output protocol applies to each file separately.

<!-- form: output-inline -->
## Output – inline input

Where the result of a task skill goes when the input was inline text in the prompt.

### Rule

Inline input maps to inline output. Deliver the result directly in the conversation.

### No-op behaviour

When the skill's procedure produces no changes – typically because the input contains no errors the procedure was looking for – the output protocol does not apply. The calling skill returns a short status message defined in its own procedure and writes nothing.

<!-- form: output-files -->
## Output – file and URL input

Where the result of a task skill goes when the input was a file or a URL – depending on input source and runtime environment. The agent detects the case using its tools (a write-probe on the workspace folder, an Edit-availability check on the target file) and selects the matching outcome.

### Cases

| Input | Environment | Output |
|---|---|---|
| File in writable workspace folder | n/a (writable by definition) | Edit in place |
| Read-only file or URL | Workspace folder available (Cowork / Claude Code with selected folder) | Write new file to workspace folder; link via `computer://` |
| Read-only file or URL | No workspace folder (Claude Chat without workspace) | Create the file as a conversation attachment |

### User override

The user can override the case with an explicit phrase ("write inline", "create a new file", "edit in place", "skriv direkt", "skapa en ny fil"). Honour the override.

### Multiple files

When the user references multiple files in one prompt, the skill loops per file. The output protocol is evaluated separately for each file.

### No-op behaviour

When the skill's procedure produces no changes – typically because the input contains no errors the procedure was looking for – the output protocol does not apply. The calling skill returns a short status message defined in its own procedure and writes nothing.

### Multi-phase output

When the calling skill runs several phases (e.g., a silent corrective pass followed by a critical-review pass followed by a settling step), only the final polished text is routed through this protocol. Intermediate phase outputs are not separately delivered – the user sees the result of all phases combined.

### Content-creation defaults

When the calling skill produces new content rather than revising an existing text (no input file, only a brief), the default output is a new file in the workspace folder, named after the working title. Inline delivery is available on explicit user request.
