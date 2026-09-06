# Export and modify a bootstrap

Instead of starting blank, export an existing bootstrap and adapt it.

```console
$ bootstrap export --dest=bs-application-copy application
```

`bs-application-copy/` then contains:

- the original `__entry_point__.py`;
- every static file and template that makes up the `application` bootstrap.

Reading these files is the fastest way to understand how bootstrapping works in
detail — the placeholders, the directory layout, and how `__entry_point__.py`
wires CLI options to template values.

Modify the copy to fit your needs, then {doc}`register it <register-a-bootstrap>`.

## See also

- {doc}`register-a-bootstrap`
- {doc}`../concepts/architecture`
