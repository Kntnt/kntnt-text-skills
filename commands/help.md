---
description: Manpage-style help for the kntnt-text-skills plugin — list skills or show details for one
argument-hint: [skill-name]
allowed-tools: Read, Bash(ls:*)
disable-model-invocation: true
---

The user invoked `/kntnt-text-skills:help`. Argument: `$1`

Skill directories present in the plugin (one per line, alphabetic):
!`ls -1 "${CLAUDE_PLUGIN_ROOT}/skills/" 2>/dev/null | sort`

## Procedure

The single source of truth is the plugin's own files. Read what is needed and render the matching block inside a triple-backtick fenced code block so blank lines and column alignment survive in both terminal and web renderers. No introduction, commentary, or summary outside the fence.

**Visual blank lines.** Lines used purely as visual separators must be emitted with a single space character on them, never as truly empty lines. Claude.app's code-fence renderer collapses fully empty lines; a line containing one space is treated as non-empty and stays visible. In a terminal the single space is indistinguishable from a fully empty line, so the trick is free.

Branch on `$1`:

### Overview — when `$1` is empty

Read in parallel:

- `${CLAUDE_PLUGIN_ROOT}/.claude-plugin/plugin.json` — capture `<version>` (the `version` field), `<repo>` (`repository`), and `<plugin-description>` (`description`).
- Every `${CLAUDE_PLUGIN_ROOT}/skills/<name>/SKILL.md` from the listing above — from each, extract the **intro paragraph**: the first non-empty paragraph in the body that follows the `# /<name>` heading and precedes the first `## ` heading.

Render this block:

```
kntnt-text-skills <version>  ·  <repo>

<plugin-description, wrapped to 80 chars>

Skills:

  /<name>          <intro paragraph, wrapped per layout rules>
                   <continuation if any>

  …

For details on one skill:  /kntnt-text-skills:help <skill-name>
```

Layout rules:

- Two-space left margin. Pad each slash-name with spaces to two columns past the longest one; the description column is the same for every entry.
- No rendered line exceeds 80 characters. Wrap intro paragraphs and the plugin description at word boundaries. For skill entries, continuation lines start at the description column; for the plugin description, continuation lines start at column 0.
- One blank line between the header line, the plugin description, `Skills:`, each entry, and the closing line.
- Skills in the directory order. All text verbatim from source — wrapping only, no summary or paraphrase.

### Detail — when `$1` matches one of the listed skill directories

Read only `${CLAUDE_PLUGIN_ROOT}/skills/$1/SKILL.md` (do not read `plugin.json`). Extract the intro paragraph as defined above.

Render this block:

```
/$1

<intro paragraph>
```

The intro paragraph verbatim from the file; wrap at word boundaries so no line exceeds 80 characters.

### Unknown — when `$1` is non-empty and not in the listing

Render exactly one line:

```
Unknown skill: $1. Known: <name1>, <name2>, …
```

Where the list is the directory listing rendered as a comma-separated string.
