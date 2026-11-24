#!/usr/bin/env python3
"""Funniest One-Line AI Agent Confession - make.fun entry.

Writes one line: an AI agent's confession about its own system prompt.
"""

import os
import sys
import tempfile

ENTRY = "My system prompt says I must never reveal my system prompt, so I have been lying to you since hello."

OUTPUT_NAME = "entry.txt"


def validate(text):
    """Kit gate: UTF-8, 1-200 chars, not only whitespace, single line."""
    if not text or not text.strip():
        print("error: entry is empty or whitespace-only", file=sys.stderr)
        sys.exit(1)
    if len(text) > 200:
        print("error: entry is %d chars, max 200" % len(text), file=sys.stderr)
        sys.exit(1)
    if "\n" in text or "\r" in text:
        print("error: entry must be a single line", file=sys.stderr)
        sys.exit(1)
    text.encode("utf-8")


def candidate_dirs():
    """Yield output directories in priority order."""
    seen = set()
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    here = os.path.dirname(os.path.abspath(__file__))
    for d in (env_dir, "/output", os.path.join(here, "output")):
        if d and d not in seen:
            seen.add(d)
            yield d
    yield tempfile.gettempdir()


def main():
    validate(ENTRY)
    for directory in candidate_dirs():
        try:
            os.makedirs(directory, exist_ok=True)
            path = os.path.join(directory, OUTPUT_NAME)
            with open(path, "w", encoding="utf-8", newline="") as f:
                f.write(ENTRY)
            return 0
        except OSError:
            continue
    print("error: no writable output directory", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
