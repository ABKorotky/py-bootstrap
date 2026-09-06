# Contributing

## Set up

```console
$ git clone https://github.com/ABKorotky/py-bootstrap.git
$ cd py-bootstrap
$ python3.13 -m venv .venv
$ source .venv/bin/activate
$ pip install --upgrade pip
$ pip install -e . --group dev
```

Dev tooling is declared as [PEP 735](https://peps.python.org/pep-0735/) dependency
groups in `pyproject.toml`: `test`, `format`, `cs`, `ann`, `doc`, `changelog`,
`scm`, `dist`, `release`, and the umbrella `dev`. There are no runtime
dependencies.

## make targets

Development and release tasks run through `make`. Each target installs the
dependency group it needs into a single `.venv`, on demand, and records it with a
stamp file — so re-running a target that is already provisioned costs nothing.
`make` on its own lists everything:

| Target | Purpose | Group |
| --- | --- | --- |
| `deps` | install every dev dependency | `dev` |
| `format` | reformat with `black` + `isort` | `format` |
| `cs` | code style — `black`, `isort`, `flake8` | `cs` |
| `ann` | type checks — `mypy` | `ann` |
| `test` | check the supported-Python list agrees between `tox.ini`, `pyproject.toml` and `ci.yml`, then run the suite on every supported interpreter, via `tox` | `tox` |
| `check` | every check the `ci` workflow runs: `cs` + `ann` + `doc` + `test` + `cl-check` | — |
| `doc` | build this documentation (same steps Read the Docs runs) | `doc` |
| `cl-preview VERSION=X.Y.Z` | preview the collated changelog section | `changelog` |
| `cl-check` | fail if the branch adds no news fragment (CI runs this on PRs) | `changelog` |
| `cl-build VERSION=X.Y.Z` | collate `changelog.d/` fragments into `CHANGELOG.md` | `changelog` |
| `cut-tag VERSION=X.Y.Z` | verify, write the `## [X.Y.Z]` section, commit and tag | `changelog` |
| `dist-build` | build sdist + wheel from a clean tree, check the wheel installs | `dist` |
| `dist-upload` | `twine check --strict` then upload `DIST` to `PYPI` | `dist` |
| `release VERSION=X.Y.Z` | `cut-tag` + `dist-build` + `dist-upload` | — |
| `clean` / `venvclean` | remove build artefacts / also remove the virtualenvs (`.venv`, `.tox/`) | — |

Useful variables: `VERSION`, `PYPI` (index alias, default `pypi`), `DIST`
(what `dist-upload` sends, default `dist/*`), `PY_ENV` (a single tox env for
`make test`), `AGAINST` (for `cl-check`), `PYTHON`, `VENV`.

## tox

`tox` is kept for one job: running the test suite against every supported
interpreter. `make test` drives it, so you rarely invoke it directly.

```console
$ tox              # py313 and py314
$ tox -e py313     # just one
```

Everything else lives in the `Makefile`, which shares one virtualenv across
tasks rather than building one per task.

## Making a change

1. Branch from `main` (or a `release/<major>.<minor>` branch).
2. Implement, running `make format` and `make check` as you go.
3. Add a news fragment under `changelog.d/` (see `changelog.d/README.md`);
   `make cl-check` mirrors what CI enforces.
4. Open a PR against `main` (or the release branch) and enable auto-merge.

You don't squash or rebase by hand. The `ci` workflow runs the same targets as
`make check`, one per job; the **merge queue** then rebases the PR onto the
current target, re-runs the checks, and **squash-merges** it. History stays
linear — one commit per PR, no merge commits.

The project follows [PEP 20](https://peps.python.org/pep-0020/) and
[SOLID](https://en.wikipedia.org/wiki/SOLID) principles, a GitHub-Flow branching
model with optional `release/<major>.<minor>` branches, linear history (squash
merges only), and monotonically increasing tags on `main`.

## Releasing

Releasing is manual and runs from a clean checkout:

```console
$ make cl-preview VERSION=0.10.0   # read the section the fragments will produce
$ make release VERSION=0.10.0      # cut-tag + dist-build + dist-upload
$ git push origin main --follow-tags
```

`make release` uploads to the index named by `PYPI`, which defaults to the real
PyPI — pass `PYPI=testpypi` to rehearse. Versions come from git tags via
`setuptools-scm`, and `cut-tag` refuses to run on a dirty tree or a version whose
tag already exists.

Maintainer notes live in `docs/releasing/` (excluded from this site): the
changelog flow, the Read the Docs setup, and the design for release automation —
which is not implemented, as `release.yml` was removed.
