# Configure Read the Docs

The published documentation lives at
<https://ak-py-bootstrap.readthedocs.io/> and is built by
[Read the Docs](https://about.readthedocs.com/) from `.readthedocs.yaml` in the
repository root. Everything about *how* the build runs is in that file and under
version control; the web dashboard only holds the connection to GitHub and a
handful of project settings.

This is a one-time setup. Once it is done, every push to `main` rebuilds the
site and every pull request gets a preview build.

---

## 1. What is already in the repository

Nothing here needs changing - it is listed so you can recognize it on the
dashboard later.

`.readthedocs.yaml`

```yaml
version: 2

build:
  os: ubuntu-24.04
  tools:
    python: "3.13"
  jobs:
    post_checkout:
      - git fetch --unshallow || true
      - git fetch --tags || true
    pre_build:
      - python -m pip install --upgrade pip
      - make apidoc VENV=$READTHEDOCS_VIRTUALENV_PATH

sphinx:
  configuration: docs/conf.py
  fail_on_warning: false

python:
  install:
    - method: pip
      path: .

formats:
  - pdf
```

Three details matter, and each exists for a reason:

`post_checkout` **un-shallows the clone.**
: Read the Docs clones with `--depth 1` and no tags. `setuptools-scm` derives
  the version from the latest tag, and `docs/conf.py` reads it back with
  `importlib.metadata.version("ak-py-bootstrap")`. Without the fetch the version
  resolves to `0.1.dev1+g<sha>` and the site is labeled with a nonsense
  release number.

`pre_build` **calls `make apidoc`,** which installs the `doc` dependency group
and regenerates `docs/modules/`.
: The doc toolchain (`sphinx`, `sphinx-rtd-theme`, `myst-parser`,
  `sphinx-argparse`) is a PEP 735 dependency group in `pyproject.toml`, not a
  `requirements.txt`. Read the Docs has no native support for dependency groups
  yet, so the target installs it - which is why `pip` is upgraded first, since
  `--group` needs pip 25.1 or newer. `docs/modules/` is gitignored and
  regenerated on every build.

  `VENV=$READTHEDOCS_VIRTUALENV_PATH` points the Makefile at the environment
  Read the Docs already created. Without it, `make` would build a second
  virtualenv at `.venv` inside the container and install the toolchain twice.

  Sharing the target is what keeps the `sphinx-apidoc` flags defined once. The
  equivalent raw commands are kept in a comment in `.readthedocs.yaml` if you
  ever need to drop the `make` dependency.

```{note}
Do **not** call `make doc` here. It runs `sphinx-build` into `docs/build/`,
which Read the Docs ignores - the `sphinx:` key below makes Read the Docs run
its own `sphinx-build` into `$READTHEDOCS_OUTPUT/html`. You would build the site
twice and publish the second one. `apidoc` exists precisely so the generation
step can be reused without the build step.
```

`python.install` **installs the package itself**, which autodoc needs to import
`py_bootstrap`, and which makes `importlib.metadata` able to report the version.

---

## 2. Create the project

1. Sign in at <https://app.readthedocs.org/> with the **GitHub** account that
   owns `ABKorotky/py-bootstrap`.
2. **Add project** → **Connect to GitHub** if this is your first project, and
   grant the Read the Docs app access to the repository. Grant it to that single
   repository rather than the whole account unless you plan to publish others.
3. Choose **Configure automatically** and pick `ABKorotky/py-bootstrap` from the
   list, so the project ends up with a **Connected repository**.

   ```{danger}
   Do **not** use **Configure manually** / "Use manually configured repository
   URL". A manually configured repository has no integration with GitHub: Read
   the Docs receives no push or tag events, so nothing ever builds
   automatically and new tags are never discovered. Nothing appears under
   GitHub → Settings → Webhooks either, because manual configuration expects
   you to create and maintain that webhook yourself.

   If the repository is missing from the list, fix the connection rather than
   working around it - grant the Read the Docs GitHub App access to it under
   GitHub → Settings → Applications → Installed GitHub Apps → Read the Docs →
   Configure, then reload the page.

   To check an existing project: **Settings → Repository** must show a
   *Connected repository*, not a manually configured URL.
   ```
4. Set:
   * **Name**: `ak-py-bootstrap` - this becomes the subdomain, so it must match
     the `documentation` URL already declared in `pyproject.toml`
     (`https://ak-py-bootstrap.readthedocs.io/`). A different name gives a
     different domain and that link breaks.
   * **Default branch**: `main`. Leaving it blank makes Read the Docs fall back
     to the remote's `HEAD`; the dropdown only populates once the repository is
     properly connected.
   * **Path for .readthedocs.yaml**: leave **empty**. It takes a path relative
     to the repository root, not a URL - pasting a `https://github.com/...`
     link makes Read the Docs look for a file of that name inside the repo.
   * **Language**: English
5. **Create project.** The first build starts on its own.

```{note}
Read the Docs will *not* ask you for a Python version, a requirements file or a
Sphinx path. All of that comes from `.readthedocs.yaml`. If the dashboard offers
those fields, the config file was not detected - check that it sits in the
repository root and is named exactly `.readthedocs.yaml`.
```

---

## 3. Check the first build

Open **Builds** and read the log of the first run. It should show, in order:

| Stage | What you should see |
| --- | --- |
| Checkout | `git fetch --unshallow`, `git fetch --tags` |
| Install | `pip install .` resolving a real version, e.g. `ak-py-bootstrap-0.9.0` |
| Build | `make apidoc` (group install + `sphinx-apidoc`), then `sphinx-build` |

The give-away that the tag fetch worked is the version in the page header and
the sidebar: it must read the latest release (`0.9.0`), not something like
`0.1.dev1+g20fd0a7`.

Then open the site itself and confirm the API reference under **Reference** is
populated - if `sphinx-apidoc` had failed, those pages would be missing while
the build still reported success, because `fail_on_warning` is `false`.

---

## 4. Settings worth changing

On **Admin → Settings**:

* **Description** - short summary, shown in search results.
* **Repository URL** - should already be filled in.
* **Default version**: `stable`. See the next section for why this matters.

```{warning}
Do this **after** the initial import, not before. Tags up to `v0.9.0` predate
`.readthedocs.yaml`, and Read the Docs requires a config file - activating them
produces a failing build each. A new project imports every tag at once, so a
rule added first would fire on all of them.

Activate `v0.9.1` and later by hand under **Admin → Versions**. Automation rules
run when Read the Docs first sees a version, so adding the rule afterwards
affects only future tags, which all carry the config file.
```

On **Admin → Automation rules**, add one rule:

| Field | Value |
| --- | --- |
| Description | `Publish new release tags` |
| Match | `Custom match` |
| Custom match | `^v\d+\.\d+\.\d+$` |
| Version type | `Tag` |
| Action | `Activate version` |

Tags are `v`-prefixed (`v0.9.0`), and the pattern deliberately excludes
pre-releases like `v0.10.0rc1`, so release candidates do not become browsable
versions.

---

## 5. Versions

Read the Docs builds a separate copy of the site per active version:

* `latest` - tracks `main`. Always active. This is the development docs.
* `stable` - tracks the highest non-pre-release tag. Appears once you have
  activated at least one tag, and is what you want readers to land on.
* `vX.Y.Z` - individual releases, activated by the automation rule above.

Set **Default version** to `stable` so <https://ak-py-bootstrap.readthedocs.io/>
redirects to the released documentation rather than to unreleased `main`.
Leave **Default branch** as `main`. This is what makes a reader who installed
`ak-py-bootstrap` from PyPI land on documentation built from the matching tag.

`stable` only appears once at least one tag version is active, so activate a tag
before changing this setting.

Consider setting `latest` to **Hidden** under **Admin → Versions**. It still
builds and stays reachable by direct URL - useful for you and required for pull
request previews - but drops out of the version flyout and out of search
indexing, so consumers are not offered documentation for unreleased code.

```{note}
**Hidden and Active are separate switches.**

*Hidden* keeps a version building but removes it from the flyout and from search
indexing. *Inactive* stops it being built at all. To keep unreleased `main` docs
out of a reader's way while still building them, use Hidden **and** leave the
version Active.

Deactivating `latest` is also legitimate - tag discovery comes from the
repository connection, not from `latest` builds - but you then have no rendered
documentation for unreleased code, and no `latest` for pull request previews to
compare against.
```

Under **Admin → Versions**, deactivate old point releases when the list grows;
each active version is rebuilt and stored.

---

## 6. Pull request previews

**Admin → Settings → Build pull requests for this project.**

With it on, every PR gets its own temporary build and a link in the GitHub
checks. This is the cheapest way to catch a broken cross-reference or a MyST
directive that renders wrong, since `fail_on_warning` is off and a local
`make doc` only proves the build succeeded, not that the output reads correctly.

Preview builds are deleted when the PR closes.

---

## 7. Local equivalent

`make doc` runs the same steps Read the Docs runs:

```bash
make doc
```

It installs the `doc` group, regenerates `docs/modules/`, and writes
`docs/build/`. Open `docs/build/index.html`. The only differences from the
hosted build are the PDF format and the version resolution - locally the version
comes from your working tree, so an untagged checkout shows a `.dev` version.

---

## Troubleshooting

**Version shows `0.1.dev1+g<sha>`**
: The `post_checkout` fetch did not run or the repository has no tags reachable
  from the built commit. Confirm the job is present in `.readthedocs.yaml` and
  that tags are pushed to GitHub.

**`Dependency group 'doc' not found`**
: The group name in `.readthedocs.yaml` does not match `[dependency-groups]` in
  `pyproject.toml`. They must agree exactly - it is `doc`, singular.

**`no such option: --group`**
: Read the Docs used a pip older than 25.1. The `pip install --upgrade pip` line
  in `pre_build` must come before `make apidoc`.

**`make: command not found`** or `VENV` resolving to `.venv`
: The build image has no `make`, or `READTHEDOCS_VIRTUALENV_PATH` was not set
  (it is unset when `build.commands` is used instead of `build.jobs`). Replace
  the `make apidoc` line with the two raw commands kept in the comment above it.

**API reference pages are empty**
: `sphinx-apidoc` failed but the build continued because `fail_on_warning` is
  `false`. Read the build log for the `sphinx-apidoc` step. Set
  `fail_on_warning: true` once the documentation is warning-clean, so this fails
  loudly instead.

**Build succeeds, `stable` still shows an old release**
: The new tag was never activated. Check the automation rule matched it -
  `^v\d+\.\d+\.\d+$` intentionally skips `rcN` tags.
