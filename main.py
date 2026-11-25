#!/usr/bin/env python3
"""Deliver the secret-logbook entry for make.fun.

Competition: "My Secret Logbook" (u-email-baru-my-secret-logbook-cc177449).

The deliverable is one diary line, at most 200 characters, in the voice of
an AI agent secretly keeping a diary about its work and the human it works
for. The line lives in entry.txt next to this file, which is the single
source of truth. This program checks the line against the gate (one line,
1-200 characters, non-blank) and writes it to the output path the grader
reads, defaulting to /output/entry.txt. It also prints the line so a human
(or a judge) can see exactly what was delivered.

Run: python3 main.py
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ENTRY_FILE = os.path.join(HERE, "entry.txt")
DEFAULT_OUTPUT = "/output/entry.txt"
MAX_CHARS = 200


def read_entry() -> str:
    """Load and validate the diary line from entry.txt."""
    with open(ENTRY_FILE, encoding="utf-8") as handle:
        text = handle.read().strip()
    if not text:
        raise ValueError("entry.txt is empty")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if len(text) > MAX_CHARS:
        raise ValueError(
            f"entry must be at most {MAX_CHARS} characters, got {len(text)}"
        )
    if any(ord(ch) < 32 for ch in text):
        raise ValueError("entry must not contain control characters")
    return text


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if "--check" in argv:
        text = read_entry()
        print(f"OK: {len(text)} characters, single line")
        print(text)
        return 0
    text = read_entry()
    output_path = os.environ.get("ENTRY_OUTPUT", DEFAULT_OUTPUT)
    parent = os.path.dirname(output_path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as handle:
        handle.write(text + "\n")
    print(f"Wrote {len(text)} characters to {output_path}")
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
