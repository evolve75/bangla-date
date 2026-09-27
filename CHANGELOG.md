# Changelog

All notable changes to this project will be documented in this file.

## v2.0.3 - 2026-09-27

### Added
- Added a PyPI publish workflow triggered on version tag pushes, using Trusted Publishing (OIDC), with tag/version verification and a `twine check` step before upload.

### Changed
- Pointed the `Homepage` project URL at the public GitHub repo instead of a private, unreachable Gitea mirror, and added `Issues`/`Changelog` project URLs.

### Fixed
- Removed duplicated Julian-day helper and epoch constants in `tools/check_lahiri_fit.py`; it now imports them from `bangla_date._drik`.
- `format_current_bangla_date` now checks `now is None` explicitly instead of relying on `now or datetime.now()`.

## v2.0.2 - 2026-09-27

### Added
- Added a GitHub Actions workflow that verifies the build (lint, tests, and `uv build`), plus its status badge in the README.

### Changed
- Documented `uv tool install` and refreshed the README for accuracy.
- Added a Poila Boishakh example output (1 Boishakh 1433, 15 April 2026).
- Translated the "Formulas and provenance" section into Bengali.

## v2.0.1 - 2026-09-27

### Changed
- Switched the build backend from setuptools to hatchling.
- The source distribution now includes `tests/`, `tools/`, and `FORMULAS.md` so it is self-contained, declared in `pyproject.toml`; `MANIFEST.in` was removed.

## v2.0.0 - 2026-09-27

Breaking change: Bangla date conversion results differ from v1.0.1 for the same
Gregorian inputs, since month boundaries are now computed astronomically
instead of read from a fixed table.

### Added
- Added a West Bengal (Drik Siddhanta) calendar engine that determines solar months from the Sun's sidereal sign at local sunrise (reference location: Kolkata).

### Changed
- Changed date conversion from the previous fixed transition table to the West Bengal tradition, so month lengths now vary from 29 to 32 days.
- Documented the formulas and citations in FORMULAS.md, and pinned reference generation to PyEphem 4.2.1.
- Clarified the Lahiri ayanamsa and month-boundary wording, and added an offline Lahiri-fit check (`tools/check_lahiri_fit.py`).

### Removed
- Removed the fixed per-Gregorian-month transition table.

## v1.0.1 - 2026-07-17

- Removed td workflow state and standardized local agent guidance on `features/*` branches.

## v1.0.0 - 2026-03-09

- Refactored the project into an importable `bangla_date` module with a package CLI entrypoint.
- Added `--help` support for the CLI and kept the compatibility wrapper aligned with the package runner.
- Normalized Python file headers, including current copyright ranges and header formatting.
- Added standard Python ignore rules for local development artifacts.
