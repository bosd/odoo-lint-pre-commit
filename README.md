# odoo-lint-pre-commit

A [pre-commit](https://pre-commit.com/) hook for
[odoo-lint](https://github.com/bosd/odoo-lint) (`odl`), a fast linter for
Odoo addons with the checks of pylint-odoo and `oca-checks-po`.

It installs the prebuilt `odoo-linter` wheel from PyPI, so nothing is
compiled. Every odoo-lint release gets a matching tag here.

## Usage

In `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/bosd/odoo-lint-pre-commit
    rev: v0.1.0a8
    hooks:
      - id: odoo-lint
```

The hook lints the staged `.py`, `.xml`, `.po` and `.pot` files, and skips the ones
your configuration excludes. odoo-lint reads its
configuration from `[tool.odoo-lint]` in `pyproject.toml`, or from
`odoo-lint.toml`; see the
[configuration docs](https://odoo-lint.readthedocs.io/en/latest/configuration.html).

To try odoo-lint next to the linters that gate your commits, use the
advisory hook instead (odoo-lint 0.1.0a8 and later). It shows the findings on
every commit but never fails it:

```yaml
      - id: odoo-lint-advisory
```

To apply the safe fixes as well (odoo-lint 0.1.0a2 and later):

```yaml
      - id: odoo-lint
        args: [--fix]
```

Checks that look across a module's files (a `.po` against its `.pot`, a
manifest against the module) read the other files from disk, so they also
work when only one file is staged.

## License

MIT
