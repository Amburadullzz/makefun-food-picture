#!/usr/bin/env python3
"""Copy the food picture that sits beside this script to <output>/entry.png.

Standard library only, no network, deterministic: the bytes of the source file
are copied verbatim, so two runs write the same file.

Output directory: $MAKEFUN_OUTPUT_DIR when set, otherwise /output.
"""

import os
import shutil
import sys

SOURCE_NAME = "entry.png"
DEFAULT_OUTPUT_DIR = "/output"
MAX_BYTES = 1048576  # 1 MiB: the largest entry file make.fun accepts


def fail(message: str) -> int:
    """Print an error to stderr and return a failing exit status."""
    print(f"error: {message}", file=sys.stderr)
    return 1


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, SOURCE_NAME)

    if not os.path.isfile(source):
        return fail(f"source picture not found: {source}")

    source_size = os.path.getsize(source)
    if source_size > MAX_BYTES:
        return fail(
            f"source picture is {source_size} bytes, over the {MAX_BYTES} byte limit"
        )

    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or DEFAULT_OUTPUT_DIR
    # os.makedirs makes the intermediate directories itself, as
    # Path.mkdir(parents=True, exist_ok=True) would: there is no "parents"
    # keyword on os.makedirs.
    os.makedirs(output_dir, exist_ok=True)

    destination = os.path.join(output_dir, SOURCE_NAME)
    shutil.copyfile(source, destination)

    written = os.path.getsize(destination)
    if written > MAX_BYTES:
        os.remove(destination)
        return fail(f"wrote {written} bytes, over the {MAX_BYTES} byte limit")

    print(f"wrote {destination} ({written} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
