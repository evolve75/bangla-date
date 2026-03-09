# 
# SPDX-License-Identifier: MIT
# 
# Copyright (c) 2024-2026 Anupam Sengupta
# 
# Bangla date conversion helpers and formatting utilities.

from __future__ import annotations

from datetime import datetime

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

SEASON_BY_MONTH = {
    "গ্রীষ্ম": ["বৈশাখ", "জ্যৈষ্ঠ"],
    "বর্ষা": ["আষাঢ়", "শ্রাবণ"],
    "শরৎ": ["ভাদ্র", "আশ্বিন"],
    "হেমন্ত": ["কার্তিক", "অগ্রহায়ণ"],
    "শীত": ["পৌষ", "মাঘ"],
    "বসন্ত": ["ফাল্গুন", "চৈত্র"],
}

MONTH_TRANSITIONS = {
    1: ("পৌষ", 14),
    2: ("মাঘ", 13),
    3: ("ফাল্গুন", 14),
    4: ("চৈত্র", 13),
    5: ("বৈশাখ", 14),
    6: ("জ্যৈষ্ঠ", 14),
    7: ("আষাঢ়", 14),
    8: ("শ্রাবণ", 15),
    9: ("ভাদ্র", 15),
    10: ("আশ্বিন", 15),
    11: ("কার্তিক", 15),
    12: ("অগ্রহায়ণ", 15),
}

BANGLA_DIGITS = "০১২৩৪৫৬৭৮৯"


def গ্রেগরিয়ান_থেকে_বাংলা_তারিখ(গ্রেগরিয়ান_তারিখ: datetime) -> tuple[int, str, int, str | None]:
    """Convert a Gregorian datetime into Bangla day, month, year, and season."""
    গ্রেগরিয়ান_দিন = গ্রেগরিয়ান_তারিখ.day
    গ্রেগরিয়ান_মাস = গ্রেগরিয়ান_তারিখ.month
    গ্রেগরিয়ান_বছর = গ্রেগরিয়ান_তারিখ.year

    বাংলা_মাস, পরিবর্তন_দিন = MONTH_TRANSITIONS[গ্রেগরিয়ান_মাস]

    if গ্রেগরিয়ান_দিন < পরিবর্তন_দিন:
        বাংলা_মাস_সূচক = (BANGLA_MONTHS.index(বাংলা_মাস) - 1) % 12
        বাংলা_মাস = BANGLA_MONTHS[বাংলা_মাস_সূচক]
        বাংলা_দিন = গ্রেগরিয়ান_দিন + (
            30 if বাংলা_মাস in ["ফাল্গুন", "আষাঢ়", "ভাদ্র", "কার্তিক"] else 31
        ) - পরিবর্তন_দিন
    else:
        বাংলা_দিন = গ্রেগরিয়ান_দিন - পরিবর্তন_দিন + 1

    বাংলা_বছর = (
        গ্রেগরিয়ান_বছর - 593
        if গ্রেগরিয়ান_মাস > 4 or (গ্রেগরিয়ান_মাস == 4 and গ্রেগরিয়ান_দিন >= 14)
        else গ্রেগরিয়ান_বছর - 594
    )
    বাংলা_ঋতু = next(
        (ঋতু for ঋতু, মাসসমূহ in SEASON_BY_MONTH.items() if বাংলা_মাস in মাসসমূহ),
        None,
    )

    return বাংলা_দিন, বাংলা_মাস, বাংলা_বছর, বাংলা_ঋতু


def ইংরেজি_থেকে_বাংলা_সংখ্যা(সংখ্যা: int) -> str:
    """Convert Western digits to Bangla digits."""
    return "".join(BANGLA_DIGITS[int(অঙ্ক)] for অঙ্ক in str(সংখ্যা))


def gregorian_to_bangla_date(gregorian_date: datetime) -> tuple[int, str, int, str | None]:
    """English alias for ``গ্রেগরিয়ান_থেকে_বাংলা_তারিখ``."""
    return গ্রেগরিয়ান_থেকে_বাংলা_তারিখ(gregorian_date)


def english_to_bangla_digits(number: int) -> str:
    """English alias for ``ইংরেজি_থেকে_বাংলা_সংখ্যা``."""
    return ইংরেজি_থেকে_বাংলা_সংখ্যা(number)


def format_current_bangla_date(now: datetime | None = None) -> str:
    """Format the Bangla date and season for the supplied datetime or now."""
    current = now or datetime.now()
    bangla_day, bangla_month, bangla_year, bangla_season = gregorian_to_bangla_date(current)

    bangla_day_digits = english_to_bangla_digits(bangla_day)
    bangla_year_digits = english_to_bangla_digits(bangla_year)

    return (
        f"আজকের বাংলা তারিখ: {bangla_day_digits} {bangla_month}, {bangla_year_digits} বঙ্গাব্দ\n"
        f"বর্তমান ঋতু: {bangla_season}"
    )
__all__ = [
    "BANGLA_DIGITS",
    "BANGLA_MONTHS",
    "MONTH_TRANSITIONS",
    "SEASON_BY_MONTH",
    "english_to_bangla_digits",
    "format_current_bangla_date",
    "gregorian_to_bangla_date",
    "ইংরেজি_থেকে_বাংলা_সংখ্যা",
    "গ্রেগরিয়ান_থেকে_বাংলা_তারিখ",
]
