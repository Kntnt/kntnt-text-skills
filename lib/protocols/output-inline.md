# Output protocol — inline input

Where the result of a task skill goes when the input was inline text in the prompt.

## Rule

Inline input maps to inline output. Deliver the result directly in the conversation.

## No-op behaviour

When the skill's procedure produces no changes — typically because the input contains no errors the procedure was looking for — the output protocol does not apply. The calling skill returns a short status message defined in its own procedure and writes nothing.
