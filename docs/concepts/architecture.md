# Architecture

## Bootstraps

A **bootstrap** is a directory with:

- `__entry_point__.py` — a module exposing a `BuildOperation` (and, for built-ins,
  a descriptor) that declares the bootstrap's CLI options and computes template
  values;
- content files — copied as-is, or, if named `*.tmpl`, rendered and written
  without the `.tmpl` suffix.

The built-in `application`, `package` and `bootstrap` bootstraps live in
`py_bootstrap/templates/`.

## Operations

`bootstrap` is a dispatcher over four operations:

`list`
: Discovers bootstraps and prints each name with its description.

`build`
: Generates a skeleton from a chosen bootstrap into `--dest` (current directory by
  default). Each discovered bootstrap contributes its own sub-parser, so
  `bootstrap build <name> --help` shows that bootstrap's options.

`export`
: Copies a bootstrap's directory (entry point + all content) to `--dest` verbatim,
  for inspection or as a starting point for a new one.

`register`
: Installs a local bootstrap directory into the tool under a given name.
  Overwrites an existing name.

Operations are composed as a recursive tree of CLI parsers; the
{doc}`../reference/cli` is generated from that same tree.

## Files processors

Generation is done by a files processor that walks the bootstrap directory and
writes into the destination:

`CopyFilesProcessor`
: Writes every file unchanged. Used by `export`.

`GenerateFilesProcessor`
: Same walk, but `*.tmpl` files are rendered against a **context** and written
  without the suffix; the `__entry_point__.py` file is skipped. Used by `build`.

### Template context

The context is a flat `str -> str` mapping. The base placeholders every `build`
provides:

| Placeholder | Value |
| --- | --- |
| `empty` | `""` |
| `date_today` | today's date, `YYYY-MM-DD` |
| `date_year` | current year |
| `python_major` | default target Python major (e.g. `3`) |
| `python_minor` | default target Python minor (e.g. `13`) |

Individual bootstraps add their own — for example `application` and `package` add
`name`, `python_name` (the normalized, import-safe form) and `description` from
their CLI options.

## Discovery and plugins

Bootstraps are found through the `py_bootstrap_templates` setuptools entry-point
group. Each contributing package points the entry point at its
`...py_bootstrap.templates` module, which exposes an `ENABLED_TEMPLATES` list of
directory names; each of those directories must contain `__entry_point__.py`.

`py-bootstrap` registers its own built-ins the same way, so from the tool's
perspective built-in, registered, and plugin-provided bootstraps are equivalent.
See {doc}`../guides/distribute-bootstraps-as-a-plugin`.
