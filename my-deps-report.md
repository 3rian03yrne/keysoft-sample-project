# Dependency Report — keysoft-sample-project

**FAIL** — 7 findings (0 high, 5 medium, 2 low): every dependency in the repo is unpinned or floating, and two installed tools are behind.

**Repo:** keysoft-sample-project 0.1.0 · **Generated:** 2026-08-05
**Environment:** `.venv` — Python 3.11.15 (project requires `>=3.10`)

## Findings

| # | Severity | Finding |
|---|---|---|
| 1 | Medium | `pytest` unpinned in `[project.optional-dependencies].dev` |
| 2 | Medium | `setuptools>=61` has no upper bound in `[build-system].requires` |
| 3 | Medium | No lockfile anywhere; `requirements.txt` is only `-e .[dev]` |
| 4 | Medium | GitHub Actions pinned to mutable major tags (`@v4`), not commit SHAs |
| 5 | Medium | `actions/checkout@v4` and `actions/setup-node@v4` are a major version behind (v5) |
| 6 | Low | `setuptools` installed 79.0.1, latest 83.0.0 |
| 7 | Low | `pip` installed 24.0, latest 26.2.1 |

### 1. `pytest` unpinned — Medium
`pyproject.toml` declares `dev = ["pytest"]` with no version constraint. Any pytest major
(currently 9.x) satisfies it, so a breaking release changes CI behaviour with no repo change.
**Fix:** `dev = ["pytest>=9,<10"]`.

### 2. `setuptools>=61` unbounded — Medium
`[build-system].requires = ["setuptools>=61"]` floats to whatever setuptools is newest at build
time. setuptools has shipped breaking changes across majors (79 → 83 in this window).
**Fix:** `["setuptools>=61,<84"]`.

### 3. No lockfile — Medium
`requirements.txt` contains only `-e .[dev]`. Nothing records the transitive set
(iniconfig, packaging, pluggy, Pygments), so two installs on different days can differ.
**Fix:** commit a `requirements.lock` from `pip freeze`, or adopt `uv lock` / `pip-tools`.

### 4. Actions pinned to mutable tags — Medium
`@v4` is a moving tag the upstream owner can repoint. For supply-chain integrity, actions should be
pinned to a full commit SHA with the version in a trailing comment.
**Fix:** `uses: actions/checkout@<sha>  # v5.0.0`.

### 5. Actions a major behind — Medium
Both `actions/checkout` and `actions/setup-node` are on v4; v5 is available for each.
Not verified against the GitHub registry in this run — confirm the current major before bumping.
Also: `setup-node` in a Python-only repo looks accidental — check whether the workflow needs Node.

### 6. `setuptools` outdated — Low
79.0.1 → 83.0.0. Build backend only, never shipped to users.
`.venv/bin/python -m pip install --upgrade setuptools`

### 7. `pip` outdated — Low
24.0 → 26.2.1. Local tooling only, no effect on the published package.
`.venv/bin/python -m pip install --upgrade pip`

## Declared dependencies

| Source | Dependency | Constraint |
|---|---|---|
| `pyproject.toml` `[project].dependencies` | *(none)* | — |
| `pyproject.toml` `dev` extra | `pytest` | unpinned → finding 1 |
| `pyproject.toml` `[build-system].requires` | `setuptools` | `>=61` → finding 2 |
| `requirements.txt` | `-e .[dev]` | → finding 3 |

Zero runtime third-party dependencies. Imports across `src/` and `tests/` are stdlib only
(`logging`, `dataclasses`), first-party `orders.*`, and `pytest` in tests.

## Installed packages

| Package | Installed | Latest | Status |
|---|---|---|---|
| keysoft-sample-project | 0.1.0 (editable) | — | local |
| pytest | 9.1.1 | 9.1.1 | current |
| iniconfig | 2.3.0 | 2.3.0 | current (transitive) |
| packaging | 26.3 | 26.3 | current (transitive) |
| pluggy | 1.6.0 | 1.6.0 | current (transitive) |
| Pygments | 2.20.0 | 2.20.0 | current (transitive) |
| setuptools | 79.0.1 | 83.0.0 | outdated → finding 6 |
| pip | 24.0 | 26.2.1 | outdated → finding 7 |

## Scope

`pip list --outdated` against PyPI plus a source-import sweep. No `pip-audit`/`safety` in the
toolchain and no CVE lookup was performed — this is **not** a vulnerability audit, so "0 high"
means no high-severity *version/pinning* findings, not "no known vulnerabilities."

The FAIL verdict is driven entirely by pinning hygiene and CI action currency; everything shipped to
users is stdlib-only, so the practical blast radius is the build backend and CI.
