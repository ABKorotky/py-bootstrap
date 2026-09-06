"""Fail unless the supported-Python list agrees everywhere it is declared.

Usage::

    python tools/check_matrix.py

The set of interpreters this project supports is written down three times, and
nothing links them:

* ``tox.ini`` - ``env_list``, the interpreters the suite actually runs on;
* ``pyproject.toml`` - the ``Programming Language :: Python :: X.Y``
  classifiers, which PyPI and the README badge read, plus ``requires-python``;
* ``.github/workflows/ci.yml`` - the ``test`` job matrix.

Adding an interpreter in one place and forgetting the others fails silently:
the badge understates what is supported, or CI quietly stops testing a version
that the package still advertises. This compares the three declarations and
exits non-zero when they disagree.
"""

from __future__ import annotations

import configparser
import re
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOX_INI = ROOT / "tox.ini"
PYPROJECT = ROOT / "pyproject.toml"
WORKFLOW = ROOT / ".github" / "workflows" / "ci.yml"

Version = tuple[int, int]

# `- python: "3.13"` immediately followed by `toxenv: py313`, the shape of the
# ci.yml test-job matrix. Anchored on both keys so a reshaped matrix is caught
# as "found nothing" rather than silently passing.
MATRIX_ENTRY = re.compile(
    r'-\s+python:\s*"(?P<major>\d+)\.(?P<minor>\d+)"\s*\n\s*toxenv:\s*(?P<toxenv>\S+)'
)
TOX_ENV = re.compile(r"^py(?P<major>\d)(?P<minor>\d+)$")
CLASSIFIER = re.compile(
    r"^Programming Language :: Python :: (?P<major>\d+)\.(?P<minor>\d+)$"
)


def fmt(versions: set[Version]) -> str:
    return ", ".join(f"{major}.{minor}" for major, minor in sorted(versions))


def from_tox() -> set[Version]:
    parser = configparser.ConfigParser(interpolation=None)
    parser.read(TOX_INI)
    raw = parser.get("tox", "env_list", fallback="")

    versions = set()
    for env in raw.split():
        matched = TOX_ENV.match(env)
        if matched:
            versions.add((int(matched["major"]), int(matched["minor"])))

    if not versions:
        sys.exit(
            f"check-matrix: no pyXY environments found in {TOX_INI.name} "
            "[tox] env_list"
        )
    return versions


def from_pyproject() -> tuple[set[Version], str]:
    data = tomllib.loads(PYPROJECT.read_text())
    project = data["project"]

    versions = set()
    for classifier in project.get("classifiers", []):
        matched = CLASSIFIER.match(classifier)
        if matched:
            versions.add((int(matched["major"]), int(matched["minor"])))

    if not versions:
        sys.exit(
            f"check-matrix: no 'Programming Language :: Python :: X.Y' "
            f"classifiers found in {PYPROJECT.name}"
        )
    return versions, project.get("requires-python", "")


def from_workflow() -> set[Version]:
    if not WORKFLOW.exists():
        sys.exit(f"check-matrix: {WORKFLOW} does not exist")

    versions = set()
    mismatched = []
    for matched in MATRIX_ENTRY.finditer(WORKFLOW.read_text()):
        major, minor = int(matched["major"]), int(matched["minor"])
        versions.add((major, minor))
        if matched["toxenv"] != f"py{major}{minor}":
            mismatched.append(
                f"python {major}.{minor} is paired with "
                f"toxenv {matched['toxenv']!r}, expected 'py{major}{minor}'"
            )

    if not versions:
        sys.exit(
            f"check-matrix: no 'python:'/'toxenv:' matrix entries found in "
            f"{WORKFLOW.name} - has the test job been reshaped?"
        )
    if mismatched:
        sys.exit(
            "check-matrix: ci.yml matrix pairs an interpreter with the wrong "
            "tox env:\n  " + "\n  ".join(mismatched)
        )
    return versions


def main() -> None:
    tox = from_tox()
    classifiers, requires_python = from_pyproject()
    workflow = from_workflow()

    problems = []
    if tox != classifiers:
        problems.append(
            f"tox.ini env_list ({fmt(tox)}) and pyproject.toml classifiers "
            f"({fmt(classifiers)}) disagree"
        )
    if tox != workflow:
        problems.append(
            f"tox.ini env_list ({fmt(tox)}) and the ci.yml test matrix "
            f"({fmt(workflow)}) disagree"
        )

    # requires-python is the floor consumers install against; it must not claim
    # support below the oldest interpreter anything is actually tested on.
    floor = re.search(r">=\s*(\d+)\.(\d+)", requires_python)
    if floor:
        declared = (int(floor[1]), int(floor[2]))
        oldest = min(tox)
        if declared != oldest:
            problems.append(
                f"requires-python {requires_python!r} declares a floor of "
                f"{declared[0]}.{declared[1]}, but the oldest tested "
                f"interpreter is {oldest[0]}.{oldest[1]}"
            )

    if problems:
        sys.exit(
            "check-matrix: the supported-Python list has drifted:\n  "
            + "\n  ".join(problems)
            + "\n\nUpdate tox.ini, the pyproject.toml classifiers and the "
            "ci.yml test matrix together."
        )

    print(f"check-matrix: ok - {fmt(tox)} declared consistently")


if __name__ == "__main__":
    main()
