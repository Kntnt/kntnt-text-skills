---
name: kntnt-text-skills
description: Manpage-style help for the kntnt-text-skills plugin. Renders version, repository link, and a quick reference for every skill in the plugin — commands, arguments, flags, input modes, language behaviour. Activates only via the explicit `/kntnt-text-skills` slash command. Run without arguments for the overview; pass a skill name (e.g. `/kntnt-text-skills write`) for the detail view of one skill.
disable-model-invocation: true
---

# /kntnt-text-skills

Manual help command. Renders plugin metadata and a quick reference for the skills in this plugin. Never invoked automatically.

## Procedure

1. Read `../../.claude-plugin/plugin.json` and extract the `version` field. This is the only live value; everything else below is static and is updated by hand when skills or languages change.
2. If the user passed no argument (or only the bare slash command), output the **Overview** block verbatim, substituting `<version>` with the value just read.
3. If the user passed exactly one argument matching one of `abt`, `edit`, `pac`, `proofread`, `redline`, `write`, `writing-rules`, output the matching **Detail** block verbatim, substituting `<version>` in the same way.
4. If the argument does not match any known skill, output one line: `Unknown skill: <arg>. Known: abt, edit, pac, proofread, redline, write, writing-rules.` Then stop.
5. Do not read any other files. Do not summarise. Do not add commentary before or after the rendered block.

## Output: Overview

````
kntnt-text-skills <version>  ·  Thomas Barregren
https://github.com/Kntnt/kntnt-text-skills

REVIEW SKILLS  (proofread ⊂ redline ⊂ edit)
  /proofread [lang] [input]    Mechanics only. Auto-detects language from the input.
                               Conservative — fixes objective errors only, never touches
                               style, structure, or voice.
  /redline   [input]           Three phases: silent proofread, finding list, then settle
                               each finding with the user one at a time
                               (accept / reject / counter / delegate).
  /edit      [input]           Same three phases as /redline, but settled by an internal
                               subagent without dialogue. AFK variant.

CREATION SKILL
  /write     [prompt]          Four phases: brief acquisition (nine fields) → idea
                               presentation → draft → automatic redline polish.

CONTEXT LOADERS  (no operation on input — they just load reference material into the session)
  /abt                         Loads the And-But-Therefore narrative arc.
  /pac                         Loads the Premise-Analysis-Conclusion analytical arc.
  /writing-rules [lang]        Loads the plugin's writing/style rules. With a language
                               argument, scoped to that language; without, loads all
                               languages.

LANGUAGES
  sv      Swedish
  en_GB   British English
  en_US   American English
  (fallback: default-mechanics)

INPUT MODES  (review and write skills)
  - Inline text after the command
  - File via @-notation:   /redline @path/to/file.md
  - File described by name: "rätta artikeln om vitvaror"
  - URL — fetched, treated as read-only
  - Upload in the session

FLAGS
  --max-iterations=N    /redline, /edit, /write. N in 0..3. Caps the subagent polish loop.
                        Default 0 (no subagent). Natural-language equivalents recognised
                        ("iterera max tre gånger", "deep review", "skip subagent", etc.).

Run  /kntnt-text-skills <skill>  for the detail view of one skill.
````

## Output: Detail — proofread

````
/proofread — conservative proofreading (kntnt-text-skills <version>)

SYNOPSIS
  /proofread [lang] [input]

DESCRIPTION
  The lightest of the three review skills. Corrects only objectively wrong things —
  spelling, grammar, punctuation, duplicated or missing words, wrong-word errors, and
  the loaded language file's mechanics. Never changes style, word order, structure,
  voice, or argumentation; those belong to /redline and /edit.

  Hierarchy:  proofread ⊂ redline ⊂ edit

ARGUMENTS
  lang     Optional language code (sv, en_GB, en_US). Without it, language is
           auto-detected from the input.
  input    Inline text, @file, file by name, URL, or upload. If no input is given,
           operates on the most recent text in the conversation.

FLAGS
  (none)

OUTPUT
  Corrected text. Original formatting preserved.
````

## Output: Detail — redline

````
/redline — three-phase editorial review with dialogue (kntnt-text-skills <version>)

SYNOPSIS
  /redline [--max-iterations=N] [input]

DESCRIPTION
  Three phases:
    1. Silent proofread (mechanics) feeds directly into phase 2.
    2. Critical review against style, genre, and technique — produces a finding list.
    3. Dialogue settling — accept / reject / counter / delegate, one finding at a time.

  Human-in-the-loop counterpart of /edit. Use /redline when you want to shape the
  review interactively; use /edit when you want a polished result without dialogue.

ARGUMENTS
  input    Inline text, @file, file by name, URL, or upload.

FLAGS
  --max-iterations=N    N in 0..3 (>3 clamped to 3). Default 0.
                        0 = on delegation, main agent applies remaining findings directly.
                        1..3 = on delegation, hand to subagent with that ceiling.
                        Natural-language parity: "iterera max tre gånger" → 3,
                        "två rundor" → 2, "en runda räcker" → 1, "skip subagent" → 0.

LANGUAGE
  Auto-detected from the input (detect mode).

OUTPUT
  Polished final text after phase 3 completes.
````

## Output: Detail — edit

````
/edit — three-phase editorial review, AFK (kntnt-text-skills <version>)

SYNOPSIS
  /edit [--max-iterations=N] [input]

DESCRIPTION
  Same three phases as /redline (silent proofread → critical review → settling), but
  settled by an internal subagent without user dialogue. Use when you want a polished
  result without sitting at the keyboard.

ARGUMENTS
  input    Inline text, @file, file by name, URL, or upload.

FLAGS
  --max-iterations=N    N in 0..3 (>3 clamped to 3). Default 0.
                        Same semantics and natural-language parity as /redline.

LANGUAGE
  Auto-detected from the input (detect mode).

OUTPUT
  Polished final text.
````

## Output: Detail — write

````
/write — content creation, four phases (kntnt-text-skills <version>)

SYNOPSIS
  /write [--max-iterations=N] [prompt]

DESCRIPTION
  Content creation from scratch or from source material. Four phases gate the run so
  the user shapes the brief and idea before drafting begins:
    1. Brief acquisition — nine fields are proposed and confirmed.
    2. Idea presentation — agreed before drafting.
    3. Draft.
    4. Automatic redline polish.

ARGUMENTS
  prompt   What you want written. Source material can be referenced inline, by @file,
           by name, or by URL.

FLAGS
  --max-iterations=N    N in 0..3 (>3 clamped to 3). Default 0. Caps the polish-loop
                        subagent in phase 4. Same natural-language parity as /redline.

LANGUAGE
  Proposed from the prompt (and source material if any) and confirmed with the user
  before drafting begins (propose mode).

OUTPUT
  Finished text in the chosen language.
````

## Output: Detail — abt

````
/abt — load the ABT narrative arc (kntnt-text-skills <version>)

SYNOPSIS
  /abt

DESCRIPTION
  Manual context loader. Loads the ABT technique (And, But, Therefore — narrative arc)
  into the current session. Does not operate on input, does not produce output beyond
  a short confirmation that ABT is ready.

  Use before /write or before discussing narrative structure when you want ABT
  guidance available in the session.

ARGUMENTS
  (none)

FLAGS
  (none)
````

## Output: Detail — pac

````
/pac — load the PAC analytical arc (kntnt-text-skills <version>)

SYNOPSIS
  /pac

DESCRIPTION
  Manual context loader. Loads the PAC technique (Premise, Analysis, Conclusion —
  analytical arc) into the current session. Does not operate on input, does not
  produce output beyond a short confirmation that PAC is ready.

  Use before /write or before discussing analytical structure when you want PAC
  guidance available in the session.

ARGUMENTS
  (none)

FLAGS
  (none)
````

## Output: Detail — writing-rules

````
/writing-rules — load writing and style rules (kntnt-text-skills <version>)

SYNOPSIS
  /writing-rules [lang]

DESCRIPTION
  Manual context loader. Loads the plugin's writing and style rules into the current
  session so they are available to subsequent ad-hoc writing in the same session.
  Does not operate on input, does not produce output beyond a short confirmation.

ARGUMENTS
  lang     Optional language code (sv, en_GB, en_US). With an argument, scopes the
           load to that language. Without an argument, loads every language file in
           lib/languages/ plus default-mechanics for full coverage.

FLAGS
  (none)
````
