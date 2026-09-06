"""Check that the built distribution is actually installable and works.

Usage::

    python tools/smoke.py
    python tools/smoke.py --dist-dir dist

Run as the last step of ``make dist-build``. Installs the freshly built wheel
into a throwaway virtualenv containing nothing else and drives the installed
console script. That clean room is the point: it catches the failures the
source tree cannot show - a ``package-data`` glob that missed the templates, a
broken console script, a missing entry point, an undeclared third-party import.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = ("application", "package", "bootstrap")


def run(*args: str) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(args, capture_output=True, text=True)
    if result.returncode:
        sys.exit(
            f"smoke: `{' '.join(args)}` exited {result.returncode}\n"
            f"{result.stdout}{result.stderr}"
        )
    return result


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="smoke.py", description="Install the built wheel and exercise it."
    )
    parser.add_argument(
        "--dist-dir", default="dist", help="where the build put the artefacts"
    )
    args = parser.parse_args()

    dist_dir = ROOT / args.dist_dir
    wheels = sorted(dist_dir.glob("*.whl"))
    if not wheels:
        sys.exit(f"smoke: no wheel found in {dist_dir}/ - run the build first")
    if len(wheels) > 1:
        # Never guess which one the build just produced.
        found = "\n".join(f"  {path.name}" for path in wheels)
        sys.exit(
            f"smoke: {len(wheels)} wheels in {dist_dir}/ - cannot tell which "
            f"one to test:\n{found}\nclear the directory and rebuild"
        )
    wheel = wheels[0]

    with tempfile.TemporaryDirectory(prefix="py-bootstrap-smoke-") as tmp:
        venv = Path(tmp) / "venv"
        run(sys.executable, "-m", "venv", str(venv))
        python = venv / "bin" / "python"
        run(str(python), "-m", "pip", "install", "--quiet", str(wheel))

        listed = run(str(venv / "bin" / "bootstrap"), "list").stdout
        missing = [name for name in EXPECTED if f"{name}:" not in listed]
        if missing:
            sys.exit(
                f"smoke: `bootstrap list` is missing {', '.join(missing)}\n"
                f"--- output ---\n{listed}"
            )

        installed = run(
            str(python),
            "-c",
            "from importlib.metadata import version;"
            "print(version('ak-py-bootstrap'))",
        ).stdout.strip()

    print(f"smoke: ok - {wheel.name} installs and lists {', '.join(EXPECTED)}")
    print(f"smoke: installed version reports {installed}")


if __name__ == "__main__":
    main()
