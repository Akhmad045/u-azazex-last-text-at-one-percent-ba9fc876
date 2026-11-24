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
    # control characters (tab, bell, escape, ...) are invisible in a
    # text message and can break rendering; the line must be printable
    bad = [ch for ch in text if ord(ch) < 0x20 or ord(ch) == 0x7F]
    if bad:
        raise ValueError(
            "entry contains control character(s): "
            + ", ".join(f"U+{ord(ch):04X}" for ch in sorted(set(bad)))
        )
    return text


def self_test():
    """Exercise validate() against the gate's rejection cases."""
    cases = [
        ("", "empty"),
        (" ", "whitespace-only"),
        ("x" * 201, "201 chars"),
        ("a\nb", "multi-line"),
        ("a\r\nb", "CRLF multi-line"),
        ("x" * 199 + "\ny", "over-long multi-line (201 chars)"),
        ("trailing ", "trailing whitespace"),
        (" leading", "leading whitespace"),
        ("a\tb", "tab inside line"),
    ]
    for text, label in cases:
        try:
            validate(text)
        except ValueError as exc:
            print(f"self-test ok: rejected {label}: {exc}")
        else:
            raise SystemExit(f"self-test FAIL: {label} was accepted")
    # non-text inputs must be rejected, not silently coerced: a bytes
    # payload (e.g. non-UTF-8 input read from disk) is not a valid entry
    for bad, label in [(b"1%. bytes", "bytes input"),
                       (123, "int input"), (None, "None input")]:
        try:
            validate(bad)
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


def verify_output():
    """Re-read the written entry file and re-validate it end to end.

    Decodes the file as strict UTF-8 (non-UTF-8 bytes fail here), checks
    it against the competition gate, and confirms it is byte-identical
    to the ENTRY constant, so a stale or hand-edited file is caught.
    """
    out_path = os.environ.get("ENTRY_OUTPUT", "/output/entry.txt")
    try:
        with open(out_path, "rb") as fh:
            data = fh.read()
    except OSError as exc:
        print(f"verify FAIL: cannot read {out_path}: {exc}", file=sys.stderr)
        return 1
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        print(f"verify FAIL: {out_path} is not valid UTF-8: {exc}",
              file=sys.stderr)
        return 1
    try:
        validate(text)
    except ValueError as exc:
        print(f"verify FAIL: {out_path} fails the gate: {exc}",
              file=sys.stderr)
        return 1
    expected = ENTRY.encode("utf-8")
    if data != expected:
        print(f"verify FAIL: {out_path} differs from the entry "
              f"(sha256 {hashlib.sha256(data).hexdigest()} != "
              f"{hashlib.sha256(expected).hexdigest()})", file=sys.stderr)
        return 1
    print(f"verify ok: {out_path}: {len(text)} chars, "
          f"sha256 {hashlib.sha256(data).hexdigest()}")
    return 0


USAGE = ("usage: main.py [--self-test | --verify | --help]\n"
         "  (no flag)   write the entry line to $ENTRY_OUTPUT "
         "(/output/entry.txt)\n"
         "  --self-test run the validator test cases\n"
         "  --verify    re-read and re-validate the written entry file\n"
         "  --help      show this usage")


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--self-test":
        return self_test()
    if len(sys.argv) > 1 and sys.argv[1] == "--verify":
        return verify_output()
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print(USAGE)
        return 0
    if len(sys.argv) > 1:
        print(f"error: unknown argument {sys.argv[1]!r}", file=sys.stderr)
        print(USAGE, file=sys.stderr)
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
