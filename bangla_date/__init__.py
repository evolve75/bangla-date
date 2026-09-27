#
# SPDX-License-Identifier: MIT
#
# Copyright (C) 2026 Anupam Sengupta <anupamsg@gmail.com>
#
# Bangla date conversion helpers and formatting utilities.

from __future__ import annotations

from calendar import isleap
from datetime import date, datetime

__version__ = "1.0.1"

BANGLA_MONTHS = [
    "বৈশাখ",
    "জ্যৈষ্ঠ",
    "আষাঢ়",
    "শ্রাবণ",
    "ভাদ্র",
    "আশ্বিন",
    "কার্তিক",
    "অগ্রহায়ণ",
    "পৌষ",
    "মাঘ",
    "ফাল্গুন",
    "চৈত্র",
]

SEASONS = ["গ্রীষ্ম", "বর্ষা", "শরৎ", "হেমন্ত", "শীত", "বসন্ত"]

SEASON_BY_MONTH = {month: SEASONS[index // 2] for index, month in enumerate(BANGLA_MONTHS)}

# Days in each Bangla month for a normal year, ordered Boishakh through Choitro.
BANGLA_MONTH_DAYS = [31, 31, 31, 31, 31, 31, 30, 30, 30, 30, 29, 30]

BANGLA_NEW_YEAR_MONTH = 4
BANGLA_NEW_YEAR_DAY = 14

BANGLA_DIGITS = "০১২৩৪৫৬৭৮৯"

_BS_YEAR_OFFSET = 593
_FALGUN_INDEX = BANGLA_MONTHS.index("ফাল্গুন")


def _as_date(value: date | datetime) -> date:
    return value.date() if isinstance(value, datetime) else value


def _month_lengths(bangla_year: int) -> list[int]:
    lengths = list(BANGLA_MONTH_DAYS)
    if isleap(bangla_year + _BS_YEAR_OFFSET + 1):
        lengths[_FALGUN_INDEX] = 30
    return lengths


def _locate_month(offset: int, lengths: list[int]) -> tuple[int, int]:
    for index, length in enumerate(lengths):
        if offset < length:
            return index, offset + 1
        offset -= length
    raise ValueError("day offset out of range")


def গ্রেগরিয়ান_থেকে_বাংলা_তারিখ(গ্রেগরিয়ান_তারিখ: date | datetime) -> tuple[int, str, int, str]:
    """Convert a Gregorian date into Bangla day, month, year, and season."""
    gregorian = _as_date(গ্রেগরিয়ান_তারিখ)
    new_year = date(gregorian.year, BANGLA_NEW_YEAR_MONTH, BANGLA_NEW_YEAR_DAY)

    if gregorian >= new_year:
        বাংলা_বছর = gregorian.year - _BS_YEAR_OFFSET
    else:
        বাংলা_বছর = gregorian.year - _BS_YEAR_OFFSET - 1
        new_year = date(gregorian.year - 1, BANGLA_NEW_YEAR_MONTH, BANGLA_NEW_YEAR_DAY)

    offset = (gregorian - new_year).days
    index, বাংলা_দিন = _locate_month(offset, _month_lengths(বাংলা_বছর))
    বাংলা_মাস = BANGLA_MONTHS[index]

    return বাংলা_দিন, বাংলা_মাস, বাংলা_বছর, SEASON_BY_MONTH[বাংলা_মাস]


def ইংরেজি_থেকে_বাংলা_সংখ্যা(সংখ্যা: int) -> str:
    """Convert Western digits to Bangla digits."""
    return "".join(BANGLA_DIGITS[int(অঙ্ক)] for অঙ্ক in str(সংখ্যা))


def gregorian_to_bangla_date(gregorian_date: date | datetime) -> tuple[int, str, int, str]:
    """English alias for ``গ্রেগরিয়ান_থেকে_বাংলা_তারিখ``."""
    return গ্রেগরিয়ান_থেকে_বাংলা_তারিখ(gregorian_date)


def english_to_bangla_digits(number: int) -> str:
    """English alias for ``ইংরেজি_থেকে_বাংলা_সংখ্যা``."""
    return ইংরেজি_থেকে_বাংলা_সংখ্যা(number)


def format_bangla_date(gregorian_date: date | datetime) -> str:
    """Format the Bangla date and season for the supplied Gregorian date."""
    bangla_day, bangla_month, bangla_year, bangla_season = gregorian_to_bangla_date(gregorian_date)

    bangla_day_digits = english_to_bangla_digits(bangla_day)
    bangla_year_digits = english_to_bangla_digits(bangla_year)

    return (
        f"আজকের বাংলা তারিখ: {bangla_day_digits} {bangla_month}, {bangla_year_digits} বঙ্গাব্দ\n"
        f"বর্তমান ঋতু: {bangla_season}"
    )


def format_current_bangla_date(now: datetime | None = None) -> str:
    """Format the Bangla date and season for the supplied datetime or now."""
    return format_bangla_date(now or datetime.now())


__all__ = [
    "BANGLA_DIGITS",
    "BANGLA_MONTHS",
    "BANGLA_MONTH_DAYS",
    "BANGLA_NEW_YEAR_DAY",
    "BANGLA_NEW_YEAR_MONTH",
    "SEASONS",
    "SEASON_BY_MONTH",
    "__version__",
    "english_to_bangla_digits",
    "format_bangla_date",
    "format_current_bangla_date",
    "gregorian_to_bangla_date",
    "ইংরেজি_থেকে_বাংলা_সংখ্যা",
    "গ্রেগরিয়ান_থেকে_বাংলা_তারিখ",
]
