"""news-image-20261124 final round entrypoint (Python 3.13, stdlib only).

Writes the pre-rendered front page assets/entry.png to the output
directory. The PNG is validated chunk by chunk (signature, IHDR size,
IEND terminator) before it is copied, and the copy is streamed so the
two grader runs produce identical bytes. No network, no third-party
imports: the grader image has no Pillow.
"""
import os
import struct

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "assets", "entry.png")
SIGNATURE = b"\x89PNG\r\n\x1a\n"
WANT_W, WANT_H = 1024, 1024
LIMIT = 1048576


def fail(msg):
    raise SystemExit("entry.png rejected: " + msg)


def check_png(blob):
    if len(blob) > LIMIT:
        fail("too large (%d bytes, limit 1 MiB)" % len(blob))
    if blob[:8] != SIGNATURE:
        fail("bad magic bytes, not a PNG")
    pos = 8
    seen_ihdr = False
    seen_iend = False
    size = None
    while pos + 8 <= len(blob):
        length = struct.unpack(">I", blob[pos:pos + 4])[0]
        kind = blob[pos + 4:pos + 8]
        if kind == b"IHDR":
            if length != 13 or pos + 8 + 13 > len(blob):
                fail("broken IHDR chunk")
            size = struct.unpack(">II", blob[pos + 8:pos + 16])
            depth, colour = blob[pos + 16], blob[pos + 17]
            if depth != 8 or colour not in (2, 6):
                fail("unexpected IHDR depth %d colour %d" % (depth, colour))
            seen_ihdr = True
        if kind == b"IEND":
            seen_iend = True
            break
        pos += 12 + length
    if not seen_ihdr:
        fail("no IHDR chunk")
    if size != (WANT_W, WANT_H):
        fail("size is %dx%d, want 1024x1024" % size)
    if not seen_iend:
        fail("truncated, no IEND chunk")


def copy_entry():
    with open(SOURCE, "rb") as src:
        blob = src.read()
    check_png(blob)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    with open(target, "wb") as dst:
        dst.write(blob)
    os.chmod(target, 0o644)
    print("wrote %s (%d bytes)" % (target, len(blob)))


if __name__ == "__main__":
    copy_entry()
