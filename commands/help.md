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

The single source of truth is the plugin's own files. Read what is needed and render the matching block verbatim. No introduction, no commentary, no summary before or after the rendered block.

**Step 1.** Read `${CLAUDE_PLUGIN_ROOT}/.claude-plugin/plugin.json`. Capture three values:

- `<version>` — the `version` field.
- `<author>` — the `author.name` field.
- `<repo>` — the `repository` field.

**Step 2.** Branch on `$1`:

### Overview — when `$1` is empty

Read every `${CLAUDE_PLUGIN_ROOT}/skills/<name>/SKILL.md` from the listing above, in a single parallel batch. From each file, extract the **intro paragraph** — the first non-empty paragraph in the body that follows the `# /<name>` heading and precedes the first `## ` heading.

Render exactly this block, with placeholders substituted:

```
kntnt-text-skills <version>  ·  <author>
<repo>

Skills:
  /<name>          <intro paragraph>
  …

For details on one skill:  /kntnt-text-skills:help <skill-name>
```

Left-align the slash-name column, padded to two spaces past the longest name. List skills in the same order as the directory listing. Use the intro paragraphs verbatim — do not re-flow, summarise, or rewrite.

### Detail — when `$1` matches one of the listed skill directories

Read `${CLAUDE_PLUGIN_ROOT}/skills/$1/SKILL.md`. From its YAML frontmatter, capture the `description` field. From its body, capture the intro paragraph as defined above.

Render exactly this block:

```
/$1 — kntnt-text-skills <version>  ·  <author>
<repo>

<frontmatter description>

<intro paragraph>
```

Both fields verbatim from the file — no edits, no wrapping changes.

### Unknown — when `$1` is non-empty and not in the listing

Render exactly one line:

```
Unknown skill: $1. Known: <name1>, <name2>, …
```

Where the list is the directory listing rendered as a comma-separated string.
