"""Fail unless the working tree and index are clean.

Usage::

    python tools/check_no_diff.py

setuptools-scm derives the version from the *working tree*, not from HEAD, so a
dirty tree silently ships local edits and stamps the version with a
``.dYYYYMMDD`` local segment. Untracked files are ignored - they are neither
committed by the release flow nor packaged - which matches `git describe
--dirty`.
"""

from __future__ import annotations

import subprocess
import sys

CMD = ["git", "status", "--porcelain", "--untracked-files=no"]


def main() -> None:
    result = subprocess.run(CMD, capture_output=True, text=True)
    if result.returncode:
        sys.exit(
            f"check-no-diff: not a git repository\n{result.stderr.strip()}"
        )
    changes = result.stdout.strip()
    if changes:
        sys.exit(
            "check-no-diff: working tree has uncommitted changes - commit or "
            f"stash them first:\n{changes}"
        )
    print("check-no-diff: ok - working tree is clean")


if __name__ == "__main__":
    main()
