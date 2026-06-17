# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pyyaml==6.0.3",
# ]
# ///
"""Audit script for kntnt-text-skills.

Runs every scriptable check from the "Audit checklist" in docs/authoring.md.
Cognitive checks (vague descriptions, prose duplication summaries, intent of
unmarked sections) stay manual.

Exit code 0 when no findings are produced; exit code 1 otherwise. A
tabulated report is written to stdout in both cases.

Required by the project root: `uv run scripts/audit.py` works from anywhere
in the worktree because the script resolves the repository root from its
own location, not from the current working directory.
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Iterable

import yaml


# Repository root resolved from this file's location: scripts/audit.py.
REPO_ROOT: Path = Path(__file__).resolve().parent.parent

# Directory shortcuts.
LIB_DIR: Path = REPO_ROOT / "lib"
SKILLS_DIR: Path = REPO_ROOT / "skills"
GENRES_DIR: Path = LIB_DIR / "genres"
LANGUAGES_DIR: Path = LIB_DIR / "languages"
PROTOCOLS_DIR: Path = LIB_DIR / "protocols"
RULES_DIR: Path = LIB_DIR / "rules"
TECHNIQUES_DIR: Path = LIB_DIR / "techniques"
PLUGIN_JSON: Path = REPO_ROOT / ".claude-plugin" / "plugin.json"
CHANGELOG: Path = REPO_ROOT / "CHANGELOG.md"

# Skill slash names that must not appear in execution-context lib files.
SKILL_SLASH_NAMES: tuple[str, ...] = (
    "/proofread",
    "/redline",
    "/edit",
    "/write",
    "/writing-rules",
    "/abt",
    "/pac",
)


@dataclass
class Finding:
    """One audit finding – path plus optional line plus message."""

    check: str
    path: str
    line: int | None
    message: str


@dataclass
class CheckResult:
    """The result of running one named check."""

    name: str
    findings: list[Finding] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        """True when the check produced no findings."""
        return not self.findings


def read_text(path: Path) -> str:
    """Read a UTF-8 text file. Returns empty string when the file is missing."""

    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def parse_frontmatter(text: str) -> tuple[dict[str, Any] | None, str]:
    """Split YAML frontmatter from the body of a markdown file."""

    # A frontmatter block is delimited by --- on the first line and --- on
    # a subsequent line. Anything else returns no frontmatter plus the
    # original text as the body.
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---", 4)
    if end == -1:
        return None, text
    raw = text[4:end]
    body_start = end + len("\n---")
    if text[body_start : body_start + 1] == "\n":
        body_start += 1
    try:
        data = yaml.safe_load(raw)
    except yaml.YAMLError:
        return None, text[body_start:]
    if not isinstance(data, dict):
        data = {}
    return data, text[body_start:]


def relpath(path: Path) -> str:
    """Repository-relative path for reporting."""

    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def iter_dir_md(directory: Path) -> list[Path]:
    """Sorted list of *.md files directly inside `directory`."""

    if not directory.exists():
        return []
    return sorted(p for p in directory.iterdir() if p.is_file() and p.suffix == ".md")


def check_skill_lib_paths() -> CheckResult:
    """Check (a) – every substrate read in a skill file uses the
    `${CLAUDE_PLUGIN_ROOT}/lib/...` form and resolves to an actual file, and
    the legacy `../../lib/...` relative form does not reappear.

    Two findings are produced. The plugin-root form is dereferenced against
    the repository root (which is `${CLAUDE_PLUGIN_ROOT}` at runtime) and a
    missing target is reported. The relative form is a hard regression: the
    convention was unified on the plugin-root variable, so any new
    `../../lib/` reference is flagged so the change cannot quietly undo
    itself. Placeholders like `<lang>.md` and `<type>.md` are skipped in both
    cases because they expand at runtime."""

    result = CheckResult(name="(a) skill -> lib path resolution")
    plugin_root = re.compile(
        r"\$\{CLAUDE_PLUGIN_ROOT\}/lib/[A-Za-z0-9_./<>-]+\.md"
    )
    legacy_relative = re.compile(r"\.\./\.\./lib/[A-Za-z0-9_./<>-]+\.md")
    placeholder = re.compile(r"<[^>]+>")
    for skill_dir in sorted(SKILLS_DIR.iterdir()):
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            continue
        text = read_text(skill_md)
        for line_no, line in enumerate(text.splitlines(), start=1):
            # Plugin-root reads must resolve against the repository root.
            for match in plugin_root.findall(line):
                if placeholder.search(match):
                    continue
                relative = match[len("${CLAUDE_PLUGIN_ROOT}/") :]
                target = (REPO_ROOT / relative).resolve()
                if not target.exists():
                    result.findings.append(
                        Finding(
                            check=result.name,
                            path=relpath(skill_md),
                            line=line_no,
                            message=f"unresolved reference: {match}",
                        )
                    )
            # The retired relative form is a regression and must not reappear.
            for match in legacy_relative.findall(line):
                result.findings.append(
                    Finding(
                        check=result.name,
                        path=relpath(skill_md),
                        line=line_no,
                        message=(
                            f"retired relative form: {match} – use "
                            "${CLAUDE_PLUGIN_ROOT}/lib/..."
                        ),
                    )
                )
    return result


def load_index_sections() -> dict[str, dict[str, Any]]:
    """Parse `lib/genres/_index.md` into a mapping name -> field dict."""

    index_path = GENRES_DIR / "_index.md"
    text = read_text(index_path)
    sections: dict[str, dict[str, Any]] = {}
    # Each genre block opens with `## <name>` (H2). Split on those headings
    # and parse each block as a flat key/value list with bullets.
    blocks = re.split(r"^## (.+)$", text, flags=re.MULTILINE)
    # `re.split` with one capture group returns: [head, name1, body1, name2, body2, ...].
    for idx in range(1, len(blocks), 2):
        name = blocks[idx].strip()
        body = blocks[idx + 1]
        sections[name] = parse_index_block(body)
    return sections


def parse_index_block(body: str) -> dict[str, Any]:
    """Parse one genre block from `_index.md` into a field dict."""

    # The index uses bullets like `- name: \`article\`` and nested bullets
    # for list fields. Convert to a flat dict carrying the same keys as the
    # genre file frontmatter for symmetric comparison.
    fields: dict[str, Any] = {}
    current_key: str | None = None
    for raw_line in body.splitlines():
        line = raw_line.rstrip()
        if not line.strip():
            current_key = None
            continue
        # Top-level field: `- key: value` (value may be empty for a list).
        top = re.match(r"^- ([A-Za-z_]+):\s*(.*)$", line)
        if top:
            key = top.group(1)
            raw_value = top.group(2).strip()
            current_key = key
            if raw_value == "":
                # Disambiguation is a mapping; other list-shaped fields
                # are plain lists. The first nested line determines the
                # shape – start empty and let the nested-line handler
                # promote to dict on first key: value match.
                fields[key] = []
                continue
            fields[key] = strip_index_value(raw_value)
            current_key = None
            continue
        # Nested bullet under a list field.
        nested = re.match(r"^\s+- (.*)$", line)
        if nested and current_key:
            value = nested.group(1).strip()
            pair = re.match(r"`([^`]+)`:\s*(.+)", value)
            if current_key == "disambiguation" and pair:
                # Promote to dict on first key: value bullet.
                container = fields.get(current_key)
                if not isinstance(container, dict):
                    container = {}
                    fields[current_key] = container
                container[pair.group(1)] = strip_index_value(pair.group(2))
                continue
            existing = fields.get(current_key)
            if not isinstance(existing, list):
                existing = []
                fields[current_key] = existing
            existing.append(strip_index_value(value))
    return fields


def strip_index_value(raw: str) -> Any:
    """Strip backticks and surrounding quotes from an index value, and
    coerce the literal `true` / `false` strings into booleans."""

    stripped = raw.strip()
    if stripped.startswith("`") and stripped.endswith("`"):
        stripped = stripped[1:-1]
    if (stripped.startswith('"') and stripped.endswith('"')) or (
        stripped.startswith("'") and stripped.endswith("'")
    ):
        stripped = stripped[1:-1]
    if stripped == "true":
        return True
    if stripped == "false":
        return False
    return stripped


def check_genre_symmetry() -> CheckResult:
    """Check (b) – every genre file has a section in `_index.md` and vice
    versa. No orphans either direction."""

    result = CheckResult(name="(b) genre <-> _index.md symmetry")
    index_sections = load_index_sections()
    genre_files = [p for p in iter_dir_md(GENRES_DIR) if p.name != "_index.md"]
    file_names = {p.stem for p in genre_files}
    index_names = set(index_sections.keys())
    for name in sorted(file_names - index_names):
        result.findings.append(
            Finding(
                check=result.name,
                path=relpath(GENRES_DIR / f"{name}.md"),
                line=None,
                message=f"genre file '{name}' has no matching section in _index.md",
            )
        )
    for name in sorted(index_names - file_names):
        result.findings.append(
            Finding(
                check=result.name,
                path=relpath(GENRES_DIR / "_index.md"),
                line=None,
                message=f"_index.md section '{name}' has no matching genre file",
            )
        )
    return result


def check_genre_frontmatter_sync() -> CheckResult:
    """Check (c) – each genre file's frontmatter matches the corresponding
    `_index.md` block field-by-field for the documented fields."""

    result = CheckResult(name="(c) genre frontmatter <-> _index.md fields")
    index_sections = load_index_sections()
    for genre_file in iter_dir_md(GENRES_DIR):
        if genre_file.name == "_index.md":
            continue
        frontmatter, _ = parse_frontmatter(read_text(genre_file))
        if frontmatter is None:
            result.findings.append(
                Finding(
                    check=result.name,
                    path=relpath(genre_file),
                    line=None,
                    message="missing YAML frontmatter",
                )
            )
            continue
        name = genre_file.stem
        index_block = index_sections.get(name)
        if index_block is None:
            # Missing from index – already reported by (b); skip here.
            continue
        # Compare the documented fields when present in either source.
        for field_name in (
            "name",
            "swedish_term",
            "default_technique",
            "triggers",
            "default",
            "not_triggers",
            "disambiguation",
        ):
            in_fm = field_name in frontmatter
            in_idx = field_name in index_block
            if not in_fm and not in_idx:
                continue
            if in_fm != in_idx:
                presence = "frontmatter" if in_fm else "_index.md"
                result.findings.append(
                    Finding(
                        check=result.name,
                        path=relpath(genre_file),
                        line=None,
                        message=f"field '{field_name}' present only in {presence}",
                    )
                )
                continue
            if not values_equal(frontmatter[field_name], index_block[field_name]):
                result.findings.append(
                    Finding(
                        check=result.name,
                        path=relpath(genre_file),
                        line=None,
                        message=(
                            f"field '{field_name}' differs from _index.md: "
                            f"{frontmatter[field_name]!r} vs {index_block[field_name]!r}"
                        ),
                    )
                )
    return result


def values_equal(a: Any, b: Any) -> bool:
    """Structural equality with a forgiving string/list comparison so the
    index's bullet style and the genre frontmatter's YAML style compare
    equal when their normalised values match."""

    if isinstance(a, list) and isinstance(b, list):
        return [str(x) for x in a] == [str(x) for x in b]
    if isinstance(a, dict) and isinstance(b, dict):
        if set(a.keys()) != set(b.keys()):
            return False
        return all(values_equal(a[k], b[k]) for k in a)
    return str(a) == str(b)


def check_default_genre_unique() -> CheckResult:
    """Check (d) – exactly one genre file (and exactly one `_index.md`
    block) carries `default: true`."""

    result = CheckResult(name="(d) exactly one genre with default: true")
    defaults_files: list[str] = []
    for genre_file in iter_dir_md(GENRES_DIR):
        if genre_file.name == "_index.md":
            continue
        frontmatter, _ = parse_frontmatter(read_text(genre_file))
        if frontmatter and frontmatter.get("default") is True:
            defaults_files.append(genre_file.stem)
    if len(defaults_files) != 1:
        result.findings.append(
            Finding(
                check=result.name,
                path=relpath(GENRES_DIR),
                line=None,
                message=(
                    f"expected exactly one genre with default: true, found "
                    f"{len(defaults_files)}: {defaults_files}"
                ),
            )
        )
    index_defaults = [
        name
        for name, fields in load_index_sections().items()
        if fields.get("default") is True
    ]
    if len(index_defaults) != 1:
        result.findings.append(
            Finding(
                check=result.name,
                path=relpath(GENRES_DIR / "_index.md"),
                line=None,
                message=(
                    f"expected exactly one section with default: true, found "
                    f"{len(index_defaults)}: {index_defaults}"
                ),
            )
        )
    return result


def check_language_layer_markers() -> CheckResult:
    """Check (e) – every `lib/languages/<lang>.md` except `default-mechanics.md`
    carries the mechanics layer marker. The style layer marker is also
    required (the issue calls absence a warning but the project policy is
    hard-fail without warning levels)."""

    result = CheckResult(name="(e) language files carry <!-- layer: --> markers")
    for lang_file in iter_dir_md(LANGUAGES_DIR):
        if lang_file.name == "default-mechanics.md":
            continue
        text = read_text(lang_file)
        if "<!-- layer: mechanics -->" not in text:
            result.findings.append(
                Finding(
                    check=result.name,
                    path=relpath(lang_file),
                    line=None,
                    message="missing <!-- layer: mechanics --> marker",
                )
            )
        if "<!-- layer: style -->" not in text:
            result.findings.append(
                Finding(
                    check=result.name,
                    path=relpath(lang_file),
                    line=None,
                    message="missing <!-- layer: style --> marker",
                )
            )
    return result


def check_genre_scope_markers() -> CheckResult:
    """Check (f) – each genre file has at least one `<!-- scope: write -->`
    and one `<!-- scope: review -->` marker. Whether each section is marked
    correctly is a cognitive check."""

    result = CheckResult(name="(f) genre files have both scope markers")
    for genre_file in iter_dir_md(GENRES_DIR):
        if genre_file.name == "_index.md":
            continue
        text = read_text(genre_file)
        if "<!-- scope: write -->" not in text:
            result.findings.append(
                Finding(
                    check=result.name,
                    path=relpath(genre_file),
                    line=None,
                    message="missing any <!-- scope: write --> marker",
                )
            )
        if "<!-- scope: review -->" not in text:
            result.findings.append(
                Finding(
                    check=result.name,
                    path=relpath(genre_file),
                    line=None,
                    message="missing any <!-- scope: review --> marker",
                )
            )
    return result


def check_slash_names_in_lib() -> CheckResult:
    """Check (g) – skill slash names do not appear in execution-context lib
    files (protocols, rules, genres, techniques). The only documented
    legitimate location is `lib/protocols/subagent.md`.

    Language files are deliberately exempt: they are data tables of
    conventions, and their file-level description paragraph names the
    skills that load each section as scope metadata, similar to a SKILL.md
    frontmatter description. Authoring rule 1 (docs/authoring.md) is about
    skill bodies and execution-context procedure / rule files; language files
    carry data that consuming skills classify by scope."""

    result = CheckResult(name="(g) skill slash names in lib/ execution context")
    # Build a regex that matches a skill slash name with a non-word boundary
    # on the right. The left boundary is the literal slash, which already
    # acts as a non-identifier separator from the preceding text.
    pattern = re.compile(
        r"(?<![A-Za-z0-9_/])("
        + "|".join(re.escape(n) for n in SKILL_SLASH_NAMES)
        + r")(?![A-Za-z0-9_-])"
    )
    scan_dirs = (PROTOCOLS_DIR, RULES_DIR, GENRES_DIR, TECHNIQUES_DIR)
    for directory in scan_dirs:
        for lib_file in iter_dir_md(directory):
            rel = relpath(lib_file)
            # `lib/protocols/subagent.md` is the documented legitimate
            # location for slash-name references (subagent role inside a
            # parent skill).
            if rel == "lib/protocols/subagent.md":
                continue
            text = read_text(lib_file)
            for line_no, line in enumerate(text.splitlines(), start=1):
                for match in pattern.finditer(line):
                    result.findings.append(
                        Finding(
                            check=result.name,
                            path=rel,
                            line=line_no,
                            message=f"skill slash name '{match.group(1)}' in execution-context file",
                        )
                    )
    return result


def check_plugin_json_and_version() -> CheckResult:
    """Check (h) – `plugin.json` is well-formed and carries the required
    fields; the version field matches the latest non-Unreleased heading in
    `CHANGELOG.md`."""

    result = CheckResult(name="(h) plugin.json shape and CHANGELOG version match")
    try:
        plugin_data = json.loads(read_text(PLUGIN_JSON))
    except json.JSONDecodeError as exc:
        result.findings.append(
            Finding(
                check=result.name,
                path=relpath(PLUGIN_JSON),
                line=None,
                message=f"invalid JSON: {exc}",
            )
        )
        return result
    if not isinstance(plugin_data, dict):
        result.findings.append(
            Finding(
                check=result.name,
                path=relpath(PLUGIN_JSON),
                line=None,
                message="plugin.json root is not an object",
            )
        )
        return result
    for required in ("name", "version", "description"):
        if required not in plugin_data:
            result.findings.append(
                Finding(
                    check=result.name,
                    path=relpath(PLUGIN_JSON),
                    line=None,
                    message=f"missing required field '{required}'",
                )
            )
    plugin_version = str(plugin_data.get("version", "")).strip()
    # Find the latest non-Unreleased heading in the changelog.
    changelog_text = read_text(CHANGELOG)
    heading_pattern = re.compile(r"^## \[([^\]]+)\]", flags=re.MULTILINE)
    latest_released: str | None = None
    for match in heading_pattern.finditer(changelog_text):
        name = match.group(1)
        if name.lower() == "unreleased":
            continue
        latest_released = name
        break
    if latest_released is None:
        result.findings.append(
            Finding(
                check=result.name,
                path=relpath(CHANGELOG),
                line=None,
                message="no non-Unreleased heading found in CHANGELOG.md",
            )
        )
    elif plugin_version != latest_released:
        result.findings.append(
            Finding(
                check=result.name,
                path=relpath(PLUGIN_JSON),
                line=None,
                message=(
                    f"plugin.json version '{plugin_version}' does not match "
                    f"latest CHANGELOG version '{latest_released}'"
                ),
            )
        )
    return result


def check_language_inherits() -> CheckResult:
    """Check (i) – every `inherits` field points to an existing base file in
    `lib/languages/`, the base does not itself declare `inherits` (one step
    only), and cycles are structurally impossible. No live `inherits` ships
    today, so the check is a no-op on current data – kept in place so the
    overlay loader's documented constraint cannot drift."""

    result = CheckResult(name="(i) inherits validation")
    for lang_file in iter_dir_md(LANGUAGES_DIR):
        frontmatter, _ = parse_frontmatter(read_text(lang_file))
        if frontmatter is None:
            continue
        inherits = frontmatter.get("inherits")
        if inherits is None:
            continue
        # Strip the documented `@` prefix and dereference relative to
        # `lib/languages/`.
        target_name = str(inherits).lstrip("@")
        base_file = LANGUAGES_DIR / target_name
        if not base_file.exists():
            result.findings.append(
                Finding(
                    check=result.name,
                    path=relpath(lang_file),
                    line=None,
                    message=f"inherits target '{target_name}' does not exist in lib/languages/",
                )
            )
            continue
        base_fm, _ = parse_frontmatter(read_text(base_file))
        if base_fm is not None and "inherits" in base_fm:
            result.findings.append(
                Finding(
                    check=result.name,
                    path=relpath(lang_file),
                    line=None,
                    message=(
                        f"inherits target '{target_name}' itself declares inherits "
                        "(only one step is allowed)"
                    ),
                )
            )
    return result


def collect_trigger_lists() -> dict[str, list[str]]:
    """Return a mapping genre name -> list of trigger words from `_index.md`."""

    result: dict[str, list[str]] = {}
    for name, fields in load_index_sections().items():
        triggers = fields.get("triggers", [])
        if isinstance(triggers, list):
            result[name] = [str(t) for t in triggers]
    return result


def check_trigger_duplication() -> CheckResult:
    """Check (j) – trigger words from `_index.md` should not be enumerated
    as inline lists in `skills/*/SKILL.md` or `lib/protocols/*.md`. Forward-
    compat gate so the fast-path-dedup refactor cannot be silently undone.

    A paragraph block is exempt when it explicitly cites `_index.md` –
    that pattern is a meta-reference acknowledging the index as the source,
    and the fast-path-dedup slice removes those paragraphs wholesale rather
    than leaving them in place. A naked enumeration without the citation is
    flagged."""

    result = CheckResult(name="(j) trigger-list duplication outside _index.md")
    triggers = collect_trigger_lists()
    files: list[Path] = []
    for skill_dir in sorted(SKILLS_DIR.iterdir()):
        skill_md = skill_dir / "SKILL.md"
        if skill_md.exists():
            files.append(skill_md)
    files.extend(iter_dir_md(PROTOCOLS_DIR))
    for path in files:
        text = read_text(path)
        # Split into paragraph-shaped blocks separated by blank lines so the
        # heuristic operates on local context, not the whole file.
        blocks = re.split(r"\n\s*\n", text)
        for block in blocks:
            if "_index.md" in block:
                # Meta-reference: the block names the index as the source,
                # so the enumeration is a documented duplication that #28
                # will remove. Allow it.
                continue
            block_lower = block.lower()
            for genre, words in triggers.items():
                # `general` is the fallback genre and its trigger list
                # consists of everyday vocabulary (mejl, brev, memo, ...)
                # whose presence in skill bodies is unavoidable. Exempt
                # the general genre from the duplication heuristic.
                if genre == "general":
                    continue
                hits: set[str] = set()
                for word in words:
                    word_lc = word.lower()
                    pattern = (
                        r"(?<![A-Za-z0-9_])" + re.escape(word_lc) + r"(?![A-Za-z0-9_])"
                    )
                    if re.search(pattern, block_lower):
                        hits.add(word_lc)
                if len(hits) >= 3:
                    line_no = locate_block(text, block)
                    result.findings.append(
                        Finding(
                            check=result.name,
                            path=relpath(path),
                            line=line_no,
                            message=(
                                f"{len(hits)} distinct trigger words from genre "
                                f"'{genre}' appear together: {sorted(hits)}"
                            ),
                        )
                    )
    return result


def locate_block(text: str, block: str) -> int | None:
    """Return the 1-indexed line number where `block` starts inside `text`."""

    idx = text.find(block)
    if idx == -1:
        return None
    return text.count("\n", 0, idx) + 1


CHECKS: tuple[Callable[[], CheckResult], ...] = (
    check_skill_lib_paths,
    check_genre_symmetry,
    check_genre_frontmatter_sync,
    check_default_genre_unique,
    check_language_layer_markers,
    check_genre_scope_markers,
    check_slash_names_in_lib,
    check_plugin_json_and_version,
    check_language_inherits,
    check_trigger_duplication,
)


def format_report(results: list[CheckResult]) -> str:
    """Render the report as a tabulated summary followed by a finding
    detail block per failing check."""

    # Summary table – fixed column widths derived from the data.
    name_width = max(len(r.name) for r in results)
    status_width = len("STATUS")
    header = f"{'CHECK'.ljust(name_width)}  {'STATUS'.ljust(status_width)}  COUNT"
    separator = "-" * len(header)
    lines = [header, separator]
    for r in results:
        status = "OK" if r.ok else "FAIL"
        lines.append(
            f"{r.name.ljust(name_width)}  {status.ljust(status_width)}  {len(r.findings)}"
        )
    lines.append(separator)
    total = sum(len(r.findings) for r in results)
    lines.append(
        f"{'TOTAL FINDINGS'.ljust(name_width)}  {''.ljust(status_width)}  {total}"
    )
    # Detail block – every failing check prints its findings.
    failing = [r for r in results if not r.ok]
    if failing:
        lines.append("")
        lines.append("Findings:")
        for r in failing:
            lines.append("")
            lines.append(f"## {r.name}")
            for f in r.findings:
                location = f.path if f.line is None else f"{f.path}:{f.line}"
                lines.append(f"  - {location} – {f.message}")
    return "\n".join(lines)


def main(argv: Iterable[str]) -> int:
    """Run every check, print the report, return 0 on clean run else 1."""

    results = [check() for check in CHECKS]
    print(format_report(results))
    return 0 if all(r.ok for r in results) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
