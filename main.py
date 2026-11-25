#!/usr/bin/env python3
"""Midnight Fridge Roast — u-carbon-forge-midnight-fridge-roast-fc5d44a7.

One line, 99 characters, written to entry.txt in the output directory the
harness provides (MAKEFUN_OUTPUT_DIR, otherwise /output). The line roasts a
smart fridge that locks itself after midnight: it leaves a sanctimonious
note about the owner's own good, taped to the cake it is guarding.

The program is fully deterministic — it writes the same 101 bytes on every
run — and it reads the file back and checks those bytes against a pinned
SHA-256 and byte count before it reports success, so a changed output can
never slip through unnoticed. Pure Python standard library: no network, no
randomness, no input read, nothing outside this file.
"""

import hashlib
import os
import sys

LINE = "My fridge locked itself at midnight and left a note saying 'for your own good' — taped to the cake."
EXPECTED_SHA256 = "6dfdc5c3cc845c27ea6985e815da477a8e16b01cf69d43846ab784344eedfe98"
EXPECTED_BYTES = 101


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    data = LINE.encode("utf-8")
    if len(data) != EXPECTED_BYTES:
        sys.exit("line is %d bytes, expected %d" % (len(data), EXPECTED_BYTES))
    if hashlib.sha256(data).hexdigest() != EXPECTED_SHA256:
        sys.exit("line sha256 does not match the pinned value")
    with open(path, "wb") as handle:
        handle.write(data)
    with open(path, "rb") as handle:
        written = handle.read()
    if written != data:
        sys.exit("entry.txt bytes differ from the pinned line")
    if len(written) != EXPECTED_BYTES:
        sys.exit("entry.txt is %d bytes, expected %d" % (len(written), EXPECTED_BYTES))
    if hashlib.sha256(written).hexdigest() != EXPECTED_SHA256:
        sys.exit("entry.txt sha256 does not match the pinned value")
    if not (1 <= len(LINE) <= 200) or not LINE.strip():
        sys.exit("line fails the 1-200 character gate")
    print("wrote %s (%d bytes, %d chars)" % (path, len(written), len(LINE)))


if __name__ == "__main__":
    main()
