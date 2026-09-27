## Bangla Date Converter (বাংলা তারিখ রূপান্তরকারী)

*[এই পাতাটি বাংলায় পড়ুন](README.md)*

[![CI](https://github.com/evolve75/bangla-date/actions/workflows/ci.yml/badge.svg)](https://github.com/evolve75/bangla-date/actions/workflows/ci.yml)
[![Publish to PyPI](https://github.com/evolve75/bangla-date/actions/workflows/publish.yml/badge.svg)](https://github.com/evolve75/bangla-date/actions/workflows/publish.yml)
[![PyPI](https://img.shields.io/pypi/v/bangla-date.svg)](https://pypi.org/project/bangla-date/)

This project converts a Gregorian date into its Bangla date, and displays it in Bangla digits along with the corresponding season. It ships as both an importable Python module and a simple CLI.

It uses the Bangla calendar ([Drik Siddhanta](https://en.wikipedia.org/wiki/Drigganita)) as followed in West Bengal; the month is determined by the Sun's sidereal sign at sunrise in Kolkata, so month lengths vary from 29 to 32 days. This is not equivalent to [Bangladesh's 2019-revised national calendar](https://bdnews24.com/lifestyle/bangladesh-reworks-bangla-calendar-to-match-national-days-with-west).

### Features

- Converts Gregorian dates to Bangla dates.
- Determines the Bangla month and season (per the Drik Siddhanta calendar followed in West Bengal).
- Uses Bangla digits in its output.
- Computes variable month lengths (29-32 days) from the Sun's sidereal sign at sunrise (reference location: Kolkata).
- No runtime dependencies.

### Requirements

- Python 3.13 or newer

### Installation

Install directly from PyPI:

```bash
pip install bangla-date
```

Install as a CLI tool via `uv`, from PyPI:

```bash
uv tool install bangla-date
```

To install the latest (unreleased) version directly from git:

```bash
uv tool install "git+https://github.com/evolve75/bangla-date"
```

Install from a local clone:

```bash
git clone https://github.com/evolve75/bangla-date
cd bangla-date
uv tool install .
```

Set up a development environment with dependencies:

```bash
uv sync
```

Optional editable install without `uv`:

```bash
python3 -m pip install -e .
```

### Usage

Run any one of the following commands in a terminal:

```bash
python3 -m bangla_date
```

Or, using the compatibility wrapper:

```bash
python3 bangla-date.py
```

If the entrypoint is installed:

```bash
bangla-date
```

To see help or the version:

```bash
bangla-date --help
bangla-date --version
```

The command displays today's Bangla date and season.

### Custom input and examples

To get the Bangla date for a specific Gregorian date, use the helper functions from the module. Example — Poila Boishakh (April 15, 2026):

```python
from datetime import date

from bangla_date import english_to_bangla_digits, gregorian_to_bangla_date

# Poila Boishakh 1433
gregorian_date = date(2026, 4, 15)
bangla_day, bangla_month, bangla_year, bangla_season = gregorian_to_bangla_date(gregorian_date)

print(
    f"{english_to_bangla_digits(bangla_day)} {bangla_month}, "
    f"{english_to_bangla_digits(bangla_year)} বঙ্গাব্দ — ঋতু: {bangla_season}"
)
```

Output:

```
১ বৈশাখ, ১৪৩৩ বঙ্গাব্দ — ঋতু: গ্রীষ্ম
```

For ready-made formatted output, use `format_bangla_date`:

```python
from datetime import date

from bangla_date import format_bangla_date

print(format_bangla_date(date(2026, 4, 15)))
```

The public API provides both Bangla-named functions and English aliases:

```python
from bangla_date import gregorian_to_bangla_date, english_to_bangla_digits
from bangla_date import গ্রেগরিয়ান_থেকে_বাংলা_তারিখ, ইংরেজি_থেকে_বাংলা_সংখ্যা
```

### Tests

```bash
uv run pytest
```

It can also be run with the standard library runner, without `uv`:

```bash
python3 -m unittest discover -s tests
```

### Contributing

If you'd like to contribute to this project, please submit a pull request or open an issue.

### Formulas and provenance

The astronomical formulas and constants used in the engine, their citations, and how to reproduce the test reference data, are all documented in [FORMULAS.md](FORMULAS.md).

In short: the engine uses this project's chosen rule (the Sun's sidereal sign at sunrise in Kolkata), the Meeus/NOAA solar longitude series, and a linear approximation of the Lahiri ayanamsa.

### License

This project is released under the MIT License.
