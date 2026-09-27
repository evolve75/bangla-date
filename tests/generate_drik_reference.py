#!/usr/bin/env python3
#
# SPDX-License-Identifier: MIT
#
# Copyright (C) 2026 Anupam Sengupta <anupamsg@gmail.com>
#
# Regenerate tests/drik_reference.tsv from an independent ephemeris.
#
# This script computes the project's month boundaries with PyEphem
# (VSOP87-based) rather than with bangla_date itself, so the reference data used
# by the test suite is not circular. Run it with:
#
#     uv run --no-project --python 3.13.7 --with ephem==4.2.1 \
#         python tests/generate_drik_reference.py --check
#
# See FORMULAS.md for release-license verification and dataset provenance.
#
# Method: local sunrise at the reference location (Kolkata, West Bengal) is found
# with PyEphem, and the Sun's apparent geocentric ecliptic longitude of date is
# converted to sidereal longitude using a True Chitrapaksha ayanamsa (Spica held
# at sidereal 180 degrees). A solar month is the sign the Sun occupies at that
# sunrise.
#
# This True Chitrapaksha construction is distinct from the runtime's Lahiri
# approximation; agreement does not validate the runtime's exact Lahiri
# definition or month-boundary rule. See FORMULAS.md. PyEphem is a
# reference-generation-only dependency.

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import math
import platform
from datetime import date, datetime, timedelta
from pathlib import Path

import ephem

REFERENCE_LATITUDE = 22.5726
REFERENCE_LONGITUDE = 88.3639
IST_DAYS = (5 * 60 + 30) / (24 * 60)
REFERENCE_PATH = Path(__file__).with_name("drik_reference.tsv")

FIRST_START = date(2024, 4, 1)
LAST_START = date(2034, 4, 14)


def _sidereal_longitude_at_sunrise(day: date) -> float:
    observer = ephem.Observer()
    observer.lat = str(REFERENCE_LATITUDE)
    observer.lon = str(REFERENCE_LONGITUDE)
    observer.horizon = "0"
    observer.date = ephem.Date(datetime(day.year, day.month, day.day)) - IST_DAYS
    sunrise = observer.next_rising(ephem.Sun())

    sun = ephem.Sun(sunrise)
    tropical = math.degrees(ephem.Ecliptic(sun, epoch=sunrise).lon) % 360.0

    spica = ephem.star("Spica")
    spica.compute(sunrise)
    ayanamsa = (math.degrees(ephem.Ecliptic(spica, epoch=sunrise).lon) % 360.0) - 180.0

    return (tropical - ayanamsa) % 360.0


def _month_index(day: date) -> int:
    return int(_sidereal_longitude_at_sunrise(day) // 30.0)


def _bangla_year(month_index: int, start: date) -> int:
    if month_index == 0 or start.month >= 4:
        civil_year = start.year
    else:
        civil_year = start.year - 1
    return civil_year - 593


def _segments(scan_start: date, scan_end: date) -> list[tuple[date, int]]:
    segments: list[tuple[date, int]] = []
    previous_index = _month_index(scan_start)
    segment_start = scan_start
    current = scan_start + timedelta(days=1)
    while current <= scan_end:
        index = _month_index(current)
        if index != previous_index:
            segments.append((segment_start, previous_index))
            segment_start = current
            previous_index = index
        current += timedelta(days=1)
    segments.append((segment_start, previous_index))
    return segments


def _boundary_rows() -> list[tuple[str, int, int, int]]:
    segments = _segments(date(2024, 1, 1), date(2034, 4, 20))
    rows: list[tuple[str, int, int, int]] = []
    for position, (start, month_index) in enumerate(segments):
        if not FIRST_START <= start < LAST_START:
            continue
        next_start = segments[position + 1][0]
        length = (next_start - start).days
        bangla_year = _bangla_year(month_index, start)
        last_day = start + timedelta(days=length - 1)
        rows.append((start.isoformat(), 1, month_index, bangla_year))
        rows.append((last_day.isoformat(), length, month_index, bangla_year))
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate or verify the PyEphem reference.")
    parser.add_argument("--output", type=Path, default=REFERENCE_PATH)
    parser.add_argument("--check", action="store_true", help="Compare without writing the output.")
    args = parser.parse_args()
    if ephem.__version__ != "4.2.1":
        parser.error("reference generation requires ephem==4.2.1")
    rows = _boundary_rows()
    handle = io.StringIO(newline="")
    writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
    writer.writerow(["# date", "day", "month_index", "year"])
    writer.writerows(rows)
    data = handle.getvalue().encode("utf-8")
    if args.check:
        if args.output.read_bytes() != data:
            parser.exit(1, f"reference differs: {args.output}\n")
        action = "verified"
    else:
        args.output.write_bytes(data)
        action = "wrote"
    print(f"{action} {len(rows)} rows: {args.output}")
    print(f"Python {platform.python_version()}; PyEphem {ephem.__version__}")
    print(f"SHA-256 {hashlib.sha256(data).hexdigest()}")


if __name__ == "__main__":
    main()
