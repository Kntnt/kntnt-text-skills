---
name: edit
description: AFK (away-from-keyboard) variant of /redline — proofread ⊂ redline ⊂ edit, this is the deepest skill. Same Phase 1 and Phase 2 as /redline (silent proofread, then critical review per protocols/redline.md). Phase 3 settles findings via an internal subagent per protocols/subagent.md — no question-by-question dialogue with the user. Use when the user writes "/edit" — alone or followed by text, a file reference, or a URL. An optional language argument (e.g. `/edit sv`, `/edit en_GB`) can be supplied. Also triggers on natural-language redaction phrases that imply a specific text exists to edit ("edit my text", "redigera den här texten", "polera utkastet", "redaktörsgranska den här texten", "polish this draft"), in which case the skill confirms the AFK intent before running. Does not trigger on generic uses of "edit" or "redigera" with no text in context. Scope is from proofreading up to and including line editing; substantive or developmental editing is raised only as a single last-resort note.
---

# /edit

Three-phase critical editorial review settled by an internal subagent.

## Trigger logic and confirmation

How `/edit` was invoked governs whether the skill confirms before running.

- **Slash invocation.** If the user's most recent message starts with the literal string `/edit` (with or without following text, language argument, or a file reference), proceed directly to language determination and then Phase 1. No confirmation is asked.
- **Natural-language invocation.** If the skill was triggered by a natural-language phrase (*redigera den här texten*, *polera utkastet*, *edit my text*, *redaktörsgranska den här*, etc.), confirm intent before language determination with an `AskUserQuestion` along the lines of:

  > Run AFK editing on the text? It iterates with an internal editorial colleague for up to three rounds and delivers polished text without asking about individual changes. To review each change yourself, run `/redline` instead.
  >
  > Options: *Yes, run AFK* / *Run `/redline` instead* / *Cancel*.

  - Yes → proceed.
  - `/redline` → hand over to `/redline`.
  - Cancel → done, no further action.

  Address the user in the language they wrote in, even though the skill text above is in English.

- **Generic mention with no text context.** If the skill description happens to fire on a generic mention of *edit* or *redigera* without an identifiable text to operate on (no shared text, no file reference, no obvious previous assistant text as target), do not ask the confirmation question. Reply briefly that the skill needs a text to operate on and offer how the user can supply one (inline, `@`-reference, file in the workspace, URL).

The skill description is written tight so this last case should be rare in practice, but the body must handle it gracefully when it occurs.

## Language determination

If the user passed a language argument (e.g. `sv`, `sv_SE`, `en`, `en_GB`, `en_US`), use it. Otherwise determine language in two steps:

1. **Detect** the language of the input text.
2. **Inventory** the matching files in `../../lib/languages/`:
   - If multiple files exist for the detected language, ask the user which to use.
   - If a single file exists, use it without asking.
   - If no file exists for the detected language, fall back to `../../lib/languages/default.md` and mention this in the reply (in English):
     > No language file found for [language]. Baseline conventions from `default.md` apply. Add `lib/languages/<code>.md` for stricter control.

Phase 1 (proofread) applies only the *Mechanics* section of the loaded file. Phase 2 (redline) applies both *Mechanics* and *Style*. When `default.md` is in use, only *Mechanics* exists — Phase 2 still runs but without language-specific style overlays (the universal style foundation in `rules/style.md` carries the pass).

## Phase 1 — silent proofread

Apply `../../lib/protocols/proofread.md` against `../../lib/rules/writing.md` and the loaded language file. The corrected text flows directly into Phase 2 — it is not delivered as a separate intermediate output.

## Phase 2 — critical review

Apply `../../lib/protocols/redline.md` against `../../lib/rules/style.md`, the loaded language file, the applicable file in `../../lib/genres/`, and the applicable file in `../../lib/techniques/`. The pass produces a finding list.

## Phase 3 — subagent settling

Settle the finding list via `../../lib/protocols/subagent.md` — main agent and subagent iterate as colleagues for up to three rounds, early consensus preferred. The polished text is delivered via `../../lib/protocols/output.md`. No user-facing summary of the internal dialogue is produced.

The single exception is the last-resort finding from `protocols/redline.md` — when the text is so far from publication that line editing cannot fix it, or when it is structured as one content type but the material wants another. That single decision is escalated to the user as a closing note.

## Files to read

Read in this order:

1. `../../lib/protocols/proofread.md`, `../../lib/rules/writing.md`, and the language file determined above (specific `lib/languages/<lang>.md`, otherwise `lib/languages/default.md`) — Phase 1.
2. `bin/list-frontmatter.sh lib/genres/` — to identify the content type.
3. The matching `../../lib/genres/<type>.md` and `../../lib/techniques/<technique>.md`.
4. `../../lib/rules/style.md`, `../../lib/protocols/redline.md`, and `../../lib/protocols/finding-format.md` — Phase 2.
5. `../../lib/protocols/subagent.md` — Phase 3.
6. `../../lib/protocols/input.md` and `../../lib/protocols/output.md` — as needed.

## Output

The output protocol routes the polished final text after Phase 3 completes.
