# /// script
# requires-python = ">=3.12"
# ///
"""Deterministic core of the /eval capture command (issue #45) — stub.

The implementation lands in the green commit. This stub exists so the test
harness imports and every test fails for its own reason rather than the suite
crashing on a missing module.
"""

from __future__ import annotations

import pathlib


def parse_transcript(text: str) -> dict:
    """Parse a capture transcript into header fields, feedback and diff. Unimplemented."""
    raise NotImplementedError


def anonymise(text: str) -> str:
    """Scrub proper-name spans from a piece of text. Unimplemented."""
    raise NotImplementedError


def propose(transcript_path: pathlib.Path) -> dict:
    """Read a transcript and propose a candidate eval case. Unimplemented."""
    raise NotImplementedError


def commit(case: dict, *, suite_path: pathlib.Path, skill_root: pathlib.Path) -> int:
    """Append a ratified case to the suite and regenerate per-skill files. Unimplemented."""
    raise NotImplementedError
