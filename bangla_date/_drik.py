#
# SPDX-License-Identifier: MIT
#
# Copyright (C) 2026 Anupam Sengupta <anupamsg@gmail.com>
#
# Solar model used by this project's West Bengal calendar approximation.
#
# Formulas, constants, and citations: see FORMULAS.md.
# - Solar longitude: Meeus, Astronomical Algorithms (2nd ed.), ch. 25.
# - Sunrise geometry: NOAA, General Solar Position Calculations, p. 2.
# - Ayanamsa: linear approximation of the Lahiri (SE_SIDM_LAHIRI) definition.
# A solar month is the project's rule: the Sun's sidereal sign at Kolkata sunrise.

from __future__ import annotations

import math
from datetime import date, timedelta

_DEG_TO_RAD = math.pi / 180.0
_ONE_DAY = timedelta(days=1)

# Reference location for sunrise: Kolkata, West Bengal.
_REFERENCE_LATITUDE = 22.5726
_REFERENCE_LONGITUDE = 88.3639
# NOAA sunrise equation: zenith of 90.833 deg accounts for refraction and the
# Sun's semidiameter.
_SUNRISE_ZENITH = 90.833

# Linear approximation of the Lahiri (SE_SIDM_LAHIRI) ayanamsa; compared in
# tools/check_lahiri_fit.py. No Swiss Ephemeris code is used.
_AYANAMSA_J2000 = 23.85322
_PRECESSION_PER_YEAR = 50.2888 / 3600.0

# Mean obliquity of the ecliptic at J2000.0 and its rate per Julian century
# (Meeus, "Astronomical Algorithms", 2nd ed., ch. 22).
_OBLIQUITY_J2000 = 23.439291
_OBLIQUITY_RATE = 0.0130042

_SIDEREAL_MONTH_SPAN = 30.0
_J2000_JULIAN_DAY = 2451545.0
_BS_YEAR_OFFSET = 593
_SUNRISE_ITERATIONS = 3

# Julian Day Number at 00:00 of the proleptic Gregorian ordinal epoch (0001-01-01).
_ORDINAL_EPOCH_JULIAN_DAY = 1721424.5


def _normalize_degrees(value: float) -> float:
    return value % 360.0


def _julian_day(day: date) -> float:
    """Julian Day Number at 00:00 for a proleptic Gregorian date."""
    return day.toordinal() + _ORDINAL_EPOCH_JULIAN_DAY


def _apparent_solar_longitude(julian_day: float) -> float:
    """Apparent geocentric ecliptic longitude of the Sun, in degrees.

    Meeus, "Astronomical Algorithms" (2nd ed.), ch. 25; the same coefficients are
    published as eqs. 47-51 in Colonna & Tramutoli, Earth 2021, 2(2), 191-207.
    """
    centuries = (julian_day - _J2000_JULIAN_DAY) / 36525.0
    mean_longitude = 280.46646 + 36000.76983 * centuries + 0.0003032 * centuries * centuries
    mean_anomaly = 357.52911 + 35999.05029 * centuries - 0.0001537 * centuries * centuries
    anomaly_radians = mean_anomaly * _DEG_TO_RAD
    equation_of_center = (
        (1.914602 - 0.004817 * centuries - 0.000014 * centuries * centuries)
        * math.sin(anomaly_radians)
        + (0.019993 - 0.000101 * centuries) * math.sin(2 * anomaly_radians)
        + 0.000289 * math.sin(3 * anomaly_radians)
    )
    true_longitude = mean_longitude + equation_of_center
    ascending_node = 125.04 - 1934.136 * centuries
    return _normalize_degrees(
        true_longitude - 0.00569 - 0.00478 * math.sin(ascending_node * _DEG_TO_RAD)
    )


def _lahiri_ayanamsa(julian_day: float) -> float:
    """Lahiri (Chitrapaksha) ayanamsa in degrees (linear approximation)."""
    years = (julian_day - _J2000_JULIAN_DAY) / 365.25
    return _AYANAMSA_J2000 + years * _PRECESSION_PER_YEAR


def _sunrise_julian_day(day: date) -> float:
    """Julian Day of local sunrise at the reference location.

    Uses the NOAA sunrise equation: hour angle from the solar declination, then
    solar noon from the equation of time.
    """
    base = _julian_day(day)
    julian_day = base + 0.25
    latitude_radians = _REFERENCE_LATITUDE * _DEG_TO_RAD
    for _ in range(_SUNRISE_ITERATIONS):
        centuries = (julian_day - _J2000_JULIAN_DAY) / 36525.0
        ecliptic_longitude = _apparent_solar_longitude(julian_day) * _DEG_TO_RAD
        obliquity = (_OBLIQUITY_J2000 - _OBLIQUITY_RATE * centuries) * _DEG_TO_RAD
        declination = math.asin(math.sin(obliquity) * math.sin(ecliptic_longitude))

        mean_longitude = 280.46646 + 36000.76983 * centuries + 0.0003032 * centuries * centuries
        right_ascension = math.atan2(
            math.cos(obliquity) * math.sin(ecliptic_longitude), math.cos(ecliptic_longitude)
        )
        equation_of_time = (
            ((mean_longitude - math.degrees(right_ascension) + 180.0) % 360.0) - 180.0
        ) / 15.0

        cos_hour_angle = (
            math.cos(_SUNRISE_ZENITH * _DEG_TO_RAD)
            - math.sin(latitude_radians) * math.sin(declination)
        ) / (math.cos(latitude_radians) * math.cos(declination))
        hour_angle = math.degrees(math.acos(max(-1.0, min(1.0, cos_hour_angle))))

        julian_day = (
            base
            + (12.0 - _REFERENCE_LONGITUDE / 15.0 - equation_of_time - hour_angle / 15.0) / 24.0
        )
    return julian_day


def _month_index_at_sunrise(day: date) -> int:
    julian_day = _sunrise_julian_day(day)
    sidereal = _normalize_degrees(
        _apparent_solar_longitude(julian_day) - _lahiri_ayanamsa(julian_day)
    )
    return int(sidereal // _SIDEREAL_MONTH_SPAN)


def _month_start(day: date) -> tuple[date, int]:
    index = _month_index_at_sunrise(day)
    start = day
    probe = day - _ONE_DAY
    while _month_index_at_sunrise(probe) == index:
        start = probe
        probe -= _ONE_DAY
    return start, index


def _boishakh_start(year: int) -> date:
    probe = date(year, 3, 1)
    while _month_index_at_sunrise(probe) != 0:
        probe += _ONE_DAY
    return probe


def bangla_date_from_gregorian(year: int, month: int, day: int) -> tuple[int, int, int]:
    """Return the West Bengal Bangla ``(day, month_index, year)`` for a Gregorian date.

    ``month_index`` is zero-based, with ``0`` for Boishakh.
    """
    current = date(year, month, day)
    start, month_index = _month_start(current)
    bangla_day = (current - start).days + 1

    if current < _boishakh_start(year):
        year -= 1

    return bangla_day, month_index, year - _BS_YEAR_OFFSET
