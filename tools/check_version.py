"""Fail unless the version is releasable and its tag is still free.

Usage::

    python tools/check_version.py 0.10.0
    python tools/check_version.py 0.10.0rc1 --remote upstream
    python tools/check_version.py --help

Checks:

* the version is a PEP 440 release or pre-release - never ``.dev``, which
  cannot be published;
* no ``vX.Y.Z`` tag exists locally;
* no such tag exists on the remote either, so a release is not cut twice from
  two clones.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys

PEP440 = re.compile(r"^\d+\.\d+\.\d+(?:(?:a|b|rc)\d+)?$")


def git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], capture_output=True, text=True)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="check_version.py",
        description="Verify a release version is well formed and unused.",
    )
    parser.add_argument("version", help="release version, e.g. 0.10.0")
    parser.add_argument(
        "--remote",
        default="origin",
        help="remote to check for an existing tag (default: origin)",
    )
    args = parser.parse_args()

    version = args.version.removeprefix("v")
    if not PEP440.match(version):
        sys.exit(
            f"check-version: {version!r} is not a releasable version "
            "(expected X.Y.Z or X.Y.ZrcN)"
        )

    tag = f"v{version}"
    if git("rev-parse", "-q", "--verify", f"refs/tags/{tag}").returncode == 0:
        sys.exit(
            f"check-version: tag {tag} already exists locally "
            f"(drop it with `git tag -d {tag}`)"
        )

    remote = git("ls-remote", "--tags", args.remote, f"refs/tags/{tag}")
    if remote.returncode:
        sys.exit(
            f"check-version: cannot reach remote {args.remote!r}\n"
            f"{remote.stderr.strip()}"
        )
    if remote.stdout.strip():
        sys.exit(
            f"check-version: tag {tag} is already published on {args.remote!r}"
        )

    print(f"check-version: ok - {version} is releasable and {tag} is free")


if __name__ == "__main__":
    main()
