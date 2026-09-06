# Changelog workflow (towncrier)

`CHANGELOG.md` is **generated**. You never edit it by hand except for the
preamble. Unreleased changes live as one-file-per-change *news fragments* in
[`changelog.d/`](../../changelog.d/), and `towncrier` folds them into a dated
`## [X.Y.Z]` section at release time.

Why: parallel PRs stop colliding on a shared `## [Unreleased]` block, and CI can
mechanically enforce "every change is documented".

## During development

Each PR that changes user-visible behaviour adds one file to `changelog.d/`:

```
changelog.d/<issue>.<type>.md
```

* `<issue>` - GitHub issue/PR number, or a `+slug` when there is none.
* `<type>` - `added` | `changed` | `deprecated` | `removed` | `fixed` | `security`.

The file body is the changelog line, past tense. See
[`changelog.d/README.md`](../../changelog.d/README.md) for examples.

Preview any time:

```
make cl-preview VERSION=0.10.0
```

CI (`.github/workflows/changelog.yml`) runs `towncrier check` on every PR and
fails if no fragment was added. Trivial PRs can carry the `skip-changelog` label.

## At release time

`make cl-build VERSION=0.10.0` rewrites `CHANGELOG.md` - a new `## [0.10.0] - <today>`
section built from the fragments, inserted just after the
`<!-- towncrier release notes start -->` marker - and `git rm`s the consumed
fragments.

`make cut-tag VERSION=0.10.0` bundles this with the commit and the tag. The full release flow, including release
candidates, is in
[configure-github-actions.md](configure-github-actions.md) step 7.

`make cut-tag` runs `tools/check_version.py` first, so a version that is not
PEP 440, or whose tag already exists locally or on the remote, is rejected
before `CHANGELOG.md` is touched.

## Release candidates

Run `make cl-build VERSION=0.10.0` **once**, when cutting `v0.10.0rc1`. The
`## [0.10.0]` section is written then and reused as-is for `rc2`, `rc3` and the
final `v0.10.0` tag (`render_changelog_section.py` maps any pre-release tag back
to its `X.Y.Z` section). Only add more fragments if new changes land between rcs.

## Notes

* Always pass `--version` explicitly. `towncrier` has no `package` configured, so
  it cannot infer the version (by design - the version comes from git tags).
* `changelog.d/README.md` is excluded via `ignore = ["README.md"]` in
  `pyproject.toml`.
