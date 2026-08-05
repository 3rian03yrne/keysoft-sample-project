# Dependency Report

**Repo:** keysoft-sample-project (0.1.0)
**Generated:** 2026-08-05
**Environment:** `.venv` — Python 3.11.15 (project requires `>=3.10`)

## Declared dependencies

| Source | Dependency | Constraint |
|---|---|---|
| `pyproject.toml` `[project].dependencies` | *(none)* | — |
| `pyproject.toml` `[project.optional-dependencies].dev` | `pytest` | unpinned |
| `pyproject.toml` `[build-system].requires` | `setuptools` | `>=61` |
| `requirements.txt` | `-e .[dev]` (this project + dev extra) | — |

The package has **zero runtime third-party dependencies**. Imports found in `src/` and `tests/`
are limited to the stdlib (`logging`, `dataclasses`), first-party `orders.*`, and `pytest` in tests.

## Installed packages

| Package | Installed | Latest | Status |
|---|---|---|---|
| keysoft-sample-project | 0.1.0 (editable) | — | local |
| pytest | 9.1.1 | 9.1.1 | current |
| iniconfig | 2.3.0 | 2.3.0 | current (pytest transitive) |
| packaging | 26.3 | 26.3 | current (pytest transitive) |
| pluggy | 1.6.0 | 1.6.0 | current (pytest transitive) |
| Pygments | 2.20.0 | 2.20.0 | current (pytest transitive) |
| pip | 24.0 | 26.2.1 | **outdated** |
| setuptools | 79.0.1 | 83.0.0 | **outdated** |

## Outdated / flagged

1. **pip 24.0 → 26.2.1** (tooling only, not shipped). Upgrade:
   `.venv/bin/python -m pip install --upgrade pip`
2. **setuptools 79.0.1 → 83.0.0** — the build backend. `[build-system].requires` only asks for
   `>=61`, so builds will pick up the newest release anyway; the stale pin is just in this venv.
   `.venv/bin/python -m pip install --upgrade setuptools`
3. **GitHub Actions** in `.github/workflows/` pin `actions/checkout@v4` and
   `actions/setup-node@v4`; **v5** is available for both. Not verified against the registry in this
   run — confirm before bumping.
4. **`pytest` is unpinned** in the `dev` extra. Fine for a sample project, but a floor
   (e.g. `pytest>=8`) makes CI reproducible if pytest lands a breaking major.

## Observations

- No known-vulnerable packages surfaced; there is no lockfile and no `pip-audit`/`safety` in the
  toolchain, so this is not a security audit — only an outdated-version check.
- `actions/setup-node` in a Python-only repo looks accidental; worth checking whether the workflow
  needs Node at all.
- Everything shipped to users is stdlib-only, so the dependency risk surface here is effectively
  the build backend plus CI actions.
