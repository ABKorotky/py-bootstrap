# Py Bootstrap Changelog

<!-- towncrier release notes start -->

## [0.9.4] - 2026-09-07
### Added
- Added `tools/check_matrix.py`, which fails when the supported-Python list drifts apart. The interpreters are declared three times with nothing linking them — `tox.ini` `env_list`, the `pyproject.toml` classifiers and the `ci.yml` test matrix — so adding a version in one place and forgetting the others used to pass silently. `make test` runs it before handing over to `tox`.
- Added a `CLAUDE.md` at the repository root describing the project for Claude Code: the `make`-driven command set, the mandatory `changelog.d/` news fragment, the operation-object and entry-point discovery architecture, the templating rules that are easy to get wrong (rendered destination paths, the `.tmpl` suffix, the `{empty}` dotfile placeholder), and the test fixture layout. It also sets a 200-line limit on every `CLAUDE.md` in the repository.
- Added coverage reporting to Codecov. The suite now writes `coverage.xml` alongside the existing terminal and HTML reports, and the `ci` workflow uploads it once per interpreter. The coverage gate itself is unchanged — `fail_under = 95` still fails `make test` locally and in CI, so the upload is reporting only and a Codecov outage cannot turn the build red.
- Declared support for Python 3.14 with a `Programming Language :: Python :: 3.14` classifier. The test suite already ran on `py314` through `tox`, but the package metadata advertised only 3.13.

### Changed
- Corrected the maintainer release docs after `release.yml` was removed. `docs/releasing/configure-github-actions.md` and `configure-pypi.md` described a release pipeline that no longer exists and listed `tools/` scripts that were never written; both now open with a "not implemented" admonition and read as a design record. The contributing guide documents the actual flow, which is `make release` from a clean checkout.
- Extended the code style and annotation checks to `tools/`. `make format`, `make cs` and `make ann` previously covered only `py_bootstrap/` and `tests/`, leaving the release and check scripts unchecked.
- Folded the separate `changelog` workflow into `.github/workflows/ci.yml` as another `make cl-check` leg, and dropped the `skip-changelog` label bypass. The `ci` workflow is now exactly `make check` split across parallel jobs, so a check either fails in both places or neither — `make check` also runs `doc`, which previously only ran on GitHub.
- Switched the default release index to the real PyPI. `make dist-upload` and `make release` now upload to `pypi` instead of `testpypi`; pass `PYPI=testpypi` to rehearse a release against the sandbox index.
- Upgraded the `ci` workflow to `actions/checkout@v7` and `actions/setup-python@v7`. The previous major versions target Node.js 20, which GitHub has deprecated, so every job emitted a warning and was silently forced onto Node.js 24.

### Fixed
- Corrected the Read the Docs setup guide on two settings that silently stop automatic builds: the project must use a **Connected repository** rather than a manually configured repository URL, which leaves it with no GitHub integration at all, so no push or tag event ever reaches Read the Docs; and the `.readthedocs.yaml` path field takes a path relative to the repository root, not a URL. Also clarified that a version being *Hidden* and being *Active* are independent settings.
- Fixed the `ci` GitHub Actions workflow, which invoked `tox` environments (`cs`, `ann`, `utc`, `doc`) that `tox.ini` does not define, so every run failed. The checks now go through `make`, matching how they are documented and run locally, and the suite runs once per supported interpreter with only that interpreter installed.

## [0.9.3] - 2026-09-06
### Added
- Added `docs/static/rtd-flyout.js`, which removes the "On Read the Docs" section (Project Home, Builds) from the Read the Docs flyout menu. Read the Docs offers no setting for this and the flyout exposes no CSS hooks, so it is done with a small script loaded through `html_js_files`.

### Changed
- Documented building the published documentation from release tags: `stable` as the default Read the Docs version, activating `v*` tag versions, and hiding `latest` so readers are offered documentation matching a released artefact. The README badge and link now point at `stable`.

## [0.9.2] - 2026-09-06
### Added
- Added `docs/releasing/configure-readthedocs.md`, a setup guide for hosting the documentation on Read the Docs: creating the project, verifying the first build, the version and automation-rule settings, pull request previews, and troubleshooting.
- Added a `make apidoc` target that regenerates the `docs/modules/` API stubs. `make doc` depends on it and Read the Docs calls it with `VENV=$READTHEDOCS_VIRTUALENV_PATH`, so the `sphinx-apidoc` flags are defined once instead of being duplicated in `.readthedocs.yaml`, and Read the Docs no longer needs a second virtualenv.

### Changed
- Changed the `towncrier` output template so generated `CHANGELOG.md` sections match the compact style of the hand-written history: no blank line after the version or category headings, one blank line between categories.

### Fixed
- Fixed the Read the Docs build: `.readthedocs.yaml` installed a `docs` dependency group, but the group in `pyproject.toml` is named `doc`. Every build failed at the `pre_build` step with `Dependency group 'docs' not found`.

## [0.9.1] - 2026-09-06
### Added
- Added GitHub Actions workflows: `ci` (style, types, tests and docs on every pull request), `changelog` (fails a pull request that adds no news fragment) and `release` (builds and publishes to PyPI through Trusted Publishing on a `v*` tag, then creates the GitHub Release).
- Added a `Makefile` as the task runner for development and release work. Targets install the PEP 735 dependency group they need on demand into a single virtualenv, so the toolchain is no longer duplicated per task. Run `make` for the full list.
- Added release tooling under `tools/`, driven by the `Makefile`: `check_version.py` rejects a version that is not PEP 440 or whose tag already exists locally or on the remote, `check_no_diff.py` refuses to release from a dirty working tree, and `smoke.py` installs the freshly built wheel into a throwaway virtualenv and exercises the console script. `make release VERSION=X.Y.Z` chains the tag, build and upload steps; `make dist-build` and `make dist-upload` are usable on their own.
- Adopted `towncrier` for changelog management. Document user-facing changes by adding a news fragment under `changelog.d/` (see `changelog.d/README.md`); the release flow collates them into `CHANGELOG.md`.

### Changed
- Project version is now derived from git tags via `setuptools-scm`. The hand-maintained `NAME`, `TITLE`, `DESCRIPTION`, `VERSION`, `PY_VERSION`, `AUTHOR` and `AUTHOR_EMAIL` constants were removed from `py_bootstrap/__init__.py`; consumers read `importlib.metadata` instead.
- Reduced `tox.ini` to the interpreter matrix (`py313`, `py314`) running the test suite. Every other task moved to the `Makefile`.
- Reworked the documentation: the Sphinx site is now MyST Markdown with installation, quickstart, guides, concepts and API reference sections, published on Read the Docs via `.readthedocs.yaml`. The hand-written `docs/modules/*.rst` stubs are generated by `sphinx-apidoc` at build time instead of being committed.

### Removed
- Removed `requirements.txt` and `requirements-dev.txt`. Dependencies are declared in `pyproject.toml` as PEP 735 dependency groups; install them with `pip install -e . --group dev` or `make deps`.

## [0.9.0] - 2025-11-02
### Changed
- Move `name` and `description` CLI arguments processing from `BaseBuildBootstrapOperation` to `DefaultBuildBootstrapOperation`. See `py_bootstrap/operations/build_bootstrap.py` file for details.

## [0.8.0] - 2025-09-13
### Added
- Add `tox.ini` to `application` bootstrap. See `py_bootstrap/templates/application/tox.ini` file for details.
- Add `tox.ini` to `package` bootstrap. See `py_bootstrap/templates/package/tox.ini` file for details.

### Changed
- `underscored_name` placeholder is replaced to `python_name` in all templates and corresponding builders. see `py_bootstrap/templates/` directory for details.

## [0.7.0] - 2025-06-24
### Changed
- Convert `templates` directory into a Python package. See `py_bootstrap/templates/__init__.py` file for details.
- Implement getting a list of bootstraps from setuptools plugins. See `py_bootstrap/operations/base.py` file for details.

## [0.6.1] - 2025-06-24
### Changed
- Refactor `README.md` files in `application`, `package`. See `py_bootastrap/templates/` directory for details.
- Refactor project's `README.md` file. See `README.md` for details.

## [0.6.0] - 2025-06-24
### Added
- Actualize `README.md` file. Prepare `Using` and `For Development` sections.
- Refactor implemented bootstraps for unification, fix small bugs and actualize help data. See `py_bootstrap/templates` directory for details.
- Implement `bootstrap` template for developing bootstraps from scratches. See `py_bootstrap/templates/bootstrap/` directory for details.
- Implement exporting bootstraps templates operation. See `py_bootstrap/operations/export_bootstrap.py` file for details.

## [0.5.0] - 2025-06-23
### Added
- Implement `FilesProcessors` functionality. See `py_bootstrap/files_processors/` directory for details.

### Changed
- Refactor operations functionality. See `py_bootstrap/operations/` directory for details.
- Rename `BaseOperationsDispatcher` to `BaseRecursiveOperationsContainer`, move it in a separated file. See `/py_bootstrap/base/operations/recursive_container.py` file for details.

## [0.4.0] - 2025-06-02
### Added
- Implement `RegisterBootstrapOperation` class for registering new customer's bootstraps. See `/py_bootstrap/operations/register_bootstrap.py` file for details.
- Prepare `template` bootstrap structure. See `/py_bootstrap/templates/template/` directory for details.

## [0.3.0] - 2025-06-01
### Added
- Prepare `application` bootstrap structure. See `/py_bootstrap/templates/application/` directory for details.

## [0.2.0] - 2025-06-01
### Added
- Prepare `package` bootstrap structure. See `/py_bootstrap/templates/package/` directory for details.
- Implement `BuildBootstrapOperation` class for generating a given bootstrap. See `/py_bootstrap/operations/build_bootstraps.py` file for details.
- Implement `ListBootstrapsOperation` class for printing enabled bootstraps. See `/py_bootstrap/operations/list_bootstraps.py` file for details.
- Implement the main script for running bootstrap operations. See `/py_bootstrap/scripts/bootstrap.py` file for details.
- Implement base functionality for operations. See `/py_bootstrap/base/operations.py` file for details.
- Implement the main CLI entrypoint. See `/py_bootstrap/cli_entrypoint.py` file for details.

## [0.1.0] - 2024-06-08
### Added
- Prepare a common skeleton based on tox automation.
