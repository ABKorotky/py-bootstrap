# Configure PyPI and TestPyPI

The `release` workflow uploads with **Trusted Publishing** (OIDC). GitHub Actions
proves its identity to PyPI and receives a short-lived, project-scoped upload
token at publish time. Nothing is stored in the repo, there is no secret to
rotate, and nothing to leak.

You configure this **once per index** (PyPI and TestPyPI are separate services
with separate accounts, and each needs its own trusted-publisher entry).

---

## 0. Prerequisites

* A PyPI account and a TestPyPI account, both with 2FA enabled.
* The project already exists on PyPI as **`ak-py-bootstrap`** (it does). If it did
  not, use the *pending publisher* form instead - see the note at the end.
* Decide the two GitHub *environment* names the workflow uses. They must match
  `release.yml` exactly:

  | Index    | GitHub environment | Uploaded by job     |
  | -------- | ------------------ | ------------------- |
  | PyPI     | `pypi`            | `publish-pypi`      |
  | TestPyPI | `testpypi`        | `publish-testpypi`  |

---

## 1. Add the trusted publisher on PyPI

1. Sign in to <https://pypi.org>.
2. Go to the project: **Your projects -> `ak-py-bootstrap` -> Manage -> Publishing**
   (direct URL: `https://pypi.org/manage/project/ak-py-bootstrap/settings/publishing/`).
3. Under **Add a new publisher -> GitHub**, fill in exactly:

   | Field               | Value              |
   | ------------------- | ------------------ |
   | Owner               | `ABKorotky`        |
   | Repository name     | `py-bootstrap`     |
   | Workflow name       | `release.yml`      |
   | Environment name    | `pypi`             |

4. **Add**. It appears immediately in the publisher list; no confirmation step.

---

## 2. Add the trusted publisher on TestPyPI

Same steps on <https://test.pypi.org>, project settings ->
`https://test.pypi.org/manage/project/ak-py-bootstrap/settings/publishing/`:

| Field            | Value           |
| ---------------- | --------------- |
| Owner            | `ABKorotky`     |
| Repository name  | `py-bootstrap`  |
| Workflow name    | `release.yml`   |
| Environment name | `testpypi`      |

If `ak-py-bootstrap` does not exist on TestPyPI yet, use **Publishing -> Add a
pending publisher** with the same four values plus the project name
`ak-py-bootstrap`. The first successful upload creates the project and converts
the pending entry into a normal trusted publisher.

---

## 3. Verify

* PyPI/TestPyPI -> project -> **Manage -> Publishing** lists a GitHub publisher
  with owner `ABKorotky`, repo `py-bootstrap`, workflow `release.yml`, and the
  right environment.
* Run the workflow manually against `main` (see
  [configure-github-actions.md](configure-github-actions.md) step 6). A green
  `publish-testpypi` job and a new dev version on
  <https://test.pypi.org/project/ak-py-bootstrap/> confirm the whole path works.

---

## What NOT to do

* **Do not create a PyPI API token for CI.** Trusted Publishing replaces it.
* **Revoke the account-wide token on your laptop.** It can modify every project
  you own. If you want a local manual-release fallback, mint a token *scoped to
  `ak-py-bootstrap`* and keep it in a password manager, not in `~/.pypirc` in
  plain text.
* If some future non-GitHub CI genuinely cannot use OIDC: create a
  **project-scoped** token, store it as a **GitHub Environment secret** on the
  `pypi` environment (never a repo-wide secret), and pass it to
  `pypa/gh-action-pypi-publish` via the `password:` input. It is then readable
  only by jobs that declare `environment: pypi`, behind the reviewer gate.

---

## Version / index rules worth remembering

* **Filenames are immutable and forever.** You cannot re-upload `0.10.0` to an
  index even after deleting it. Never publish a `.dev` build to real PyPI - the
  `check-version` job blocks it.
* **Pre-releases are safe on real PyPI.** `pip install ak-py-bootstrap` ignores
  `0.10.0rc1`; only `pip install --pre` or an exact pin picks it up. That is the
  staging mechanism - not TestPyPI.
* **TestPyPI is a sandbox for the pipeline**, not a staging mirror. It is pruned
  periodically and its dependency resolution differs from PyPI. Use it to prove
  the publish path (via manual `workflow_dispatch` runs), not to validate the
  package contents - the `test-wheel` job does that.
