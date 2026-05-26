# Genre resolution protocol

How a calling skill resolves the input it received into a single genre file in `lib/genres/` and the technique file declared by that genre, with a fast-path that lets unmarked everyday text commit to the fallback genre without reading the index. The procedure is caller-agnostic — it speaks of *the calling skill*, *the input*, and *the user's prompt*; the calling skill names its own review pass and its own scope of layers.

The protocol is data-aware about one file: `lib/genres/_index.md`. The index lives in that directory and is named explicitly here because it is the trigger catalogue the standard flow matches against. The protocol does not enumerate the catalogue's contents — it points at the index as the single source.

## Inputs and outputs

The procedure takes two inputs from the calling skill: the *input text* being reviewed and the *user's prompt* that invoked the calling skill. It produces two outputs: a committed *genre* (one of the `name` values in `_index.md` — `general` when the fast-path exits) and a committed *technique* (the genre's `default_technique` from `_index.md`, which may be `none`).

The procedure runs once per invocation, before the calling skill issues its Files-to-read batches. The committed genre and technique determine which files the calling skill loads.

## Fast-path

Before consulting `_index.md`, check two conditions against the input text and the user's prompt:

1. **No structural markers in the input.** No H1 heading, no standfirst, no byline, no attributed-quote pattern.
2. **No genre word in the user's prompt.** None of the trigger terms catalogued in `lib/genres/_index.md` for any non-fallback genre. Reference the catalogue; do not enumerate it here.

**Both conditions hold.** Commit to the fallback genre — the one whose `_index.md` block carries `default: true`. Skip the `_index.md` read and skip the matched-genre read entirely. Commit to the fallback genre's `default_technique`; when that value is `none`, no technique file is loaded.

**Either condition is broken.** Continue with the standard flow below.

## Standard flow

When the fast-path does not exit:

1. **Read `_index.md`.** The index carries one block per genre with the `name`, `swedish_term`, `default_technique`, optional `default: true`, `triggers`, `not_triggers`, and `disambiguation` fields.
2. **Match.** Test the input's structural markers and the prompt's genre words against the trigger lists in the index. A trigger word landing inside a `not_triggers` exception does not match.
3. **Disambiguate.** When multiple genres match, apply the `disambiguation` logic from `_index.md` — typically a question to the user ("article or column?") for shared phrases like *blogginlägg* / *blog post*.
4. **Fallback.** When no trigger matches and no semantic likeness lands cleanly, commit to the genre whose block carries `default: true`.
5. **Read the matched files.** Read the matched `<genre>.md` for the full rules and, when the genre's `default_technique` is not `none`, read the matching `<technique>.md`.

## Last-resort floor

Misclassification is caught by the subsequent review pass's last-resort-finding mechanism — see the corresponding protocol that the calling skill loads. When the resolved genre is wrong for the material, the review pass surfaces it as a single last-resort developmental finding rather than silently rewriting. The detection logic lives in the review-pass protocol; this resolution protocol is concerned only with picking a genre and a technique to start from.
