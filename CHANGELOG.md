# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-10-07
### Added
- Full CLI unification under a single `testforge` command with subcommands (`validate`, `generate`, `schema`, `batch`).
- Automated release workflow via GitHub Actions (`.github/workflows/release.yml`) for building, testing, linting, GitHub Releases, and PyPI publishing.
- `bumpversion` configuration for semantic versioning automation.
- Comprehensive documentation of the release process in `README.md`.
- Updated `README.md` with Quick Start guide and Command Overview table for the unified CLI.

### Changed
- Refactored all individual CLI modules (`testforge.cli.main`, `testforge.devtools.generators.csv_generator`, `testforge.core.schema`, `testforge.devtools.batch_tests.batch_runner`) to expose their core logic as functions callable by the unified CLI.
- Modified `pyproject.toml` to reflect the new unified CLI entry point and updated development dependencies.
- Updated all CLI-related tests to use the new `testforge` command structure.

### Fixed
- Resolved `TOMLDecodeError` in `pyproject.toml` due to duplicate sections.
- Corrected test assertions and CLI invocation methods in test files to ensure all tests pass with the unified CLI.

## [0.1.0] - 2025-09-XX
### Added
- Initial project structure and basic module setup.
- Core CSV validation logic (`testforge.core.validator`).
- Basic CLI for CSV validation (`testforge.cli.main`).
- CSV generation utility (`testforge.devtools.generators.csv_generator`).
- Schema inference utility (`testforge.core.schema`).
- Batch validation utility (`testforge.devtools.batch_tests.batch_runner`).
- Initial test suite using `pytest`.
- Basic `ruff` and `black` configurations for code quality.
- `.gitignore` and `pyproject.toml` for project management.
- `README.md` with project description, features, and getting started guide.
