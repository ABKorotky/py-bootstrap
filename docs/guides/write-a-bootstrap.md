# Write a bootstrap from scratch

A bootstrap is a directory containing:

- `__entry_point__.py` — the entry point that drives generation for this bootstrap;
- any files and directories that provide its content, static or templated.

The `bootstrap` bootstrap scaffolds a new one for you:

```console
$ bootstrap build --dest=demo-bootstrap bootstrap --name=demo-bs --description="The demo bootstrap"
$ tree -L 2 demo-bootstrap
demo-bootstrap
├── demo-file.txt.tmpl
└── __entry_point__.py
```

## Add content

- **Static files** are copied verbatim.
- **Templates** — files ending in `.tmpl` — are rendered, then written without the
  `.tmpl` suffix. `demo-file.txt.tmpl` shows the placeholders the tool provides by
  default (see {doc}`../concepts/architecture`).

Edit `__entry_point__.py` to declare the bootstrap's CLI options and to compute
the values your templates consume.

## Try it

Generation from an unregistered directory is not supported directly — register it
first ({doc}`register-a-bootstrap`), then iterate: edit templates, re-register,
regenerate, inspect. Registration overwrites, so the loop is fast.

## See also

- {doc}`export-and-modify-a-bootstrap` — often easier than starting blank.
- {doc}`../concepts/architecture` — the files-processor and placeholder model.
