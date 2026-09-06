# Versioning and compatibility

## Scheme

`py-bootstrap` follows [Semantic Versioning](https://semver.org/) and
[PEP 440](https://peps.python.org/pep-0440/). The version is derived from the git
tag by `setuptools-scm` — there is no version constant in the source.

- `X.Y.Z` — a normal release.
- `X.Y.ZrcN` — a release candidate. Published to PyPI but ignored by `pip` unless
  you pass `--pre` or pin the exact version.

## Supported Python

Each release states its floor in `requires-python` (currently **>= 3.13**).
Dropping a Python version is a minor-version change while the project is `0.x`.

## Public surface

While the project is `0.x`, treat every release as potentially breaking. The
supported surface is:

- the `bootstrap` CLI ({doc}`reference/cli`);
- the `py_bootstrap_templates` entry-point contract for
  {doc}`plugins <guides/distribute-bootstraps-as-a-plugin>`;
- names exported via `__all__` in `py_bootstrap` modules.

Anything else is internal and may change without notice.

## Changes

Every user-visible change is recorded in the {doc}`changelog`, assembled from news
fragments at release time.
