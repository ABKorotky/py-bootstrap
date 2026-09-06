# Distribute bootstraps as a plugin

Ship bootstraps inside your own package and `py-bootstrap` will discover them
automatically — no manual {doc}`register <register-a-bootstrap>` step for users.

## 1. Declare the entry point

In your package's `pyproject.toml` (replace the placeholders):

```text
[project.entry-points.py_bootstrap_templates]
<your-package-name> = "<package_root>.py_bootstrap.templates"
```

## 2. Lay out the templates package

```text
<package_root>
└── py_bootstrap
    └── templates
        ├── __init__.py
        ├── <your-bootstrap>
        │   ├── __entry_point__.py
        │   └── ...
        └── <your-other-bootstrap>
            ├── __entry_point__.py
            └── ...
```

## 3. List the enabled bootstraps

`<package_root>/py_bootstrap/templates/__init__.py`:

```python
__all__ = ("ENABLED_TEMPLATES",)

ENABLED_TEMPLATES = [
    "<your-bootstrap>",
    "<your-other-bootstrap>",
]
```

## 4. Ship it

Build and publish your package. In any environment where it is installed
alongside `ak-py-bootstrap`:

```console
$ bootstrap list
...
your-bootstrap: Your bootstrap description.
your-other-bootstrap: Your other bootstrap description.
```

## See also

- {doc}`../concepts/architecture` — how discovery via the
  `py_bootstrap_templates` entry-point group works.
