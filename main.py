"""news-image-20261124 entrypoint (Python 3.13, stdlib only).

Copies the pre-rendered front page assets/entry.png to the output
directory after validating it is a whole 1024x1024 PNG. No network,
no third-party imports: the grader image has no Pillow.
"""
import os
import struct
import sys

ASSET = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     "assets", "entry.png")
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1048576


def read_asset():
    with open(ASSET, "rb") as fh:
        data = fh.read()
    if len(data) > MAX_BYTES:
        raise SystemExit("entry.png exceeds 1 MiB: %d bytes" % len(data))
    if data[:8] != PNG_MAGIC:
        raise SystemExit("assets/entry.png is not a PNG (bad magic bytes)")
    if len(data) < 24 or data[12:16] != b"IHDR":
        raise SystemExit("assets/entry.png has no IHDR chunk")
    width, height = struct.unpack(">II", data[16:24])
    if (width, height) != (1024, 1024):
        raise SystemExit("unexpected size %dx%d, want 1024x1024" % (width, height))
    if data[-12:] != b"\x00\x00\x00\x00IEND\xaeB`\x82":
        raise SystemExit("assets/entry.png is truncated (no IEND chunk)")
    return data


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    data = read_asset()
    out_path = os.path.join(out_dir, "entry.png")
    with open(out_path, "wb") as fh:
        fh.write(data)
    os.chmod(out_path, 0o644)
    print("wrote %s (%d bytes)" % (out_path, len(data)))


if __name__ == "__main__":
    main()
