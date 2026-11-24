#!/usr/bin/env python3
"""Last Text at One Percent — writes one funny final text from a dying
phone to /output/entry.txt.

The line is the phone's final invoice: after three years of service,
zero thank-yous and 289 drops, it bills its owner one charger — and
accepts cash, card, or an apology. The "1%." opener anchors the dying
state; the invoice format gives the phone a personality with a stake
in dying; the kicker pays off in three beats.

Stdlib only, deterministic, no network, no randomness.
"""
import hashlib
import os
import sys

ENTRY = ("1%. Final invoice: 3 years of service, 0 thank-yous, "
         "289 drops. Payment due: one charger. I accept cash, card, "
         "or an apology.")

MAX_CHARS = 200


def validate(text):
    """Enforce the competition gate: 1-200 chars, not only whitespace."""
    if not isinstance(text, str):
        raise ValueError("entry must be text")
    if len(text) == 0:
        raise ValueError("entry is empty (gate needs 1-200 characters)")
    if len(text) > MAX_CHARS:
        raise ValueError(
            f"entry is {len(text)} characters, over the 200-character gate"
        )
    if text.strip() == "":
        raise ValueError("entry is only whitespace")
    if text != text.strip():
        raise ValueError("entry has leading or trailing whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    return text


def self_test():
    """Exercise validate() against the gate's rejection cases."""
    cases = [
        ("", "empty"),
        (" ", "whitespace-only"),
        ("x" * 201, "201 chars"),
        ("a\nb", "multi-line"),
        ("trailing ", "trailing whitespace"),
        (" leading", "leading whitespace"),
    ]
    for text, label in cases:
        try:
            validate(text)
        except ValueError as exc:
            print(f"self-test ok: rejected {label}: {exc}")
        else:
            raise SystemExit(f"self-test FAIL: {label} was accepted")
    # boundaries: 1 char and exactly 200 chars must pass
    validate("x")
    print("self-test ok: 1-char boundary accepted")
    validate("y" * 200)
    print("self-test ok: 200-char boundary accepted")
    print("self-test: all cases passed")
    return 0


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--self-test":
        return self_test()
    if len(sys.argv) > 1:
        print("usage: main.py [--self-test]", file=sys.stderr)
        return 2
    out_path = os.environ.get("ENTRY_OUTPUT", "/output/entry.txt")
    text = validate(ENTRY)
    data = text.encode("utf-8")
    parent = os.path.dirname(out_path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(out_path, "wb") as fh:
        fh.write(data)  # no trailing newline: the file is exactly the line
    with open(out_path, "rb") as fh:
        roundtrip = fh.read()
    if roundtrip != data:
        raise SystemExit("round-trip mismatch: file does not match entry")
    print(f"wrote {out_path}: {len(text)} chars, "
          f"sha256 {hashlib.sha256(data).hexdigest()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
