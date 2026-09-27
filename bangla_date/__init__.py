#
# SPDX-License-Identifier: MIT
#
# Copyright (C) 2026 Anupam Sengupta <anupamsg@gmail.com>
#
# Bangla date conversion helpers and formatting utilities.

from __future__ import annotations

from datetime import date, datetime

from bangla_date._drik import bangla_date_from_gregorian

__version__ = "2.0.3"

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

BANGLA_DIGITS = "০১২৩৪৫৬৭৮৯"


def _as_date(value: date | datetime) -> date:
    return value.date() if isinstance(value, datetime) else value


def গ্রেগরিয়ান_থেকে_বাংলা_তারিখ(গ্রেগরিয়ান_তারিখ: date | datetime) -> tuple[int, str, int, str]:
    """Convert a Gregorian date into Bangla day, month, year, and season."""
    gregorian = _as_date(গ্রেগরিয়ান_তারিখ)
    bangla_day, month_index, bangla_year = bangla_date_from_gregorian(
        gregorian.year, gregorian.month, gregorian.day
    )
    bangla_month = BANGLA_MONTHS[month_index]

    return bangla_day, bangla_month, bangla_year, SEASON_BY_MONTH[bangla_month]


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
    return format_bangla_date(now if now is not None else datetime.now())


__all__ = [
    "BANGLA_DIGITS",
    "BANGLA_MONTHS",
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
