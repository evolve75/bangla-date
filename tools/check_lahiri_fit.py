#!/usr/bin/env python3
#
# SPDX-License-Identifier: MIT
#
# Copyright (C) 2026 Anupam Sengupta <anupamsg@gmail.com>
#
# Approximate comparison of the runtime Lahiri ayanamsa with a local evaluation
# of the Swiss Ephemeris SE_SIDM_LAHIRI precession model, sampled at January 1,
# 2000-2050. Offline utility only: it reads the published numerical parameters
# (sweph.h) and the IAU 1976 general precession in longitude, and does not use or
# copy any Swiss Ephemeris code. This is not a verified Swiss Ephemeris
# computation. See FORMULAS.md.

from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from bangla_date._drik import _J2000_JULIAN_DAY, _julian_day, _lahiri_ayanamsa  # noqa: E402

# Swiss Ephemeris SE_SIDM_LAHIRI parameters (sweph.h):
#   {2435553.5, 23.250182778 - 0.004658035, FALSE, SEMOD_PREC_IAU_1976}
# from the Indian Astronomical Ephemeris 1989, p. 556.
_SE_T0_JULIAN_DAY = 2435553.5
_SE_AYAN_T0 = 23.250182778 - 0.004658035


def _general_precession_arcseconds(centuries_from_j2000: float) -> float:
    # IAU 1976 general precession in longitude (Lieske et al., 1977; also Meeus,
    # "Astronomical Algorithms", ch. 21), in arcseconds.
    return (
        5029.0966 * centuries_from_j2000
        + 1.11113 * centuries_from_j2000**2
        - 0.000006 * centuries_from_j2000**3
    )


def _reference_lahiri_ayanamsa(julian_day: float) -> float:
    centuries = (julian_day - _J2000_JULIAN_DAY) / 36525.0
    t0_centuries = (_SE_T0_JULIAN_DAY - _J2000_JULIAN_DAY) / 36525.0
    precession = _general_precession_arcseconds(centuries) - _general_precession_arcseconds(
        t0_centuries
    )
    return _SE_AYAN_T0 + precession / 3600.0


def main() -> None:
    print("Approximate comparison: January 1 samples, 2000-2050 inclusive.")
    print("year  runtime_deg  reference_deg  diff_arcsec")
    worst = 0.0
    worst_year = 2000
    for year in range(2000, 2051):
        julian_day = _julian_day(date(year, 1, 1))
        runtime = _lahiri_ayanamsa(julian_day)
        reference = _reference_lahiri_ayanamsa(julian_day)
        difference = abs(runtime - reference) * 3600.0
        if difference > worst:
            worst = difference
            worst_year = year
        if year % 10 == 0:
            print(f"{year}  {runtime:.5f}     {reference:.5f}      {difference:.2f}")
    print(f"max |diff| = {worst:.2f} arcsec = {worst / 3600.0:.5f} deg (January 1, {worst_year})")


if __name__ == "__main__":
    main()
