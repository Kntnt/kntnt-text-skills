# Output protocol — file and URL input

Where the result of a task skill goes when the input was a file or a URL — depending on input source and runtime environment. The agent detects the case using its tools (a write-probe on the workspace folder, an Edit-availability check on the target file) and selects the matching outcome.

## Cases

| Input | Environment | Output |
|---|---|---|
| File in writable workspace folder | n/a (writable by definition) | Edit in place |
| Read-only file or URL | Workspace folder available (Cowork / Claude Code with selected folder) | Write new file to workspace folder; link via `computer://` |
| Read-only file or URL | No workspace folder (Claude Chat without workspace) | Create the file as a conversation attachment |

## User override

The user can override the case with an explicit phrase ("write inline", "create a new file", "edit in place", "skriv direkt", "skapa en ny fil"). Honour the override.

## Multiple files

When the user references multiple files in one prompt, the skill loops per file. The output protocol is evaluated separately for each file.

## No-op behaviour

When the skill's procedure produces no changes — typically because the input contains no errors the procedure was looking for — the output protocol does not apply. The calling skill returns a short status message defined in its own procedure and writes nothing.

## Multi-phase output

When the calling skill runs several phases (e.g., a silent corrective pass followed by a critical-review pass followed by a settling step), only the final polished text is routed through this protocol. Intermediate phase outputs are not separately delivered — the user sees the result of all phases combined.

## Content-creation defaults

When the calling skill produces new content rather than revising an existing text (no input file, only a brief), the default output is a new file in the workspace folder, named after the working title. Inline delivery is available on explicit user request.
