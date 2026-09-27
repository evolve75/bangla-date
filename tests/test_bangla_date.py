#
# SPDX-License-Identifier: MIT
#
# Copyright (C) 2026 Anupam Sengupta <anupamsg@gmail.com>
#
# Tests for Bangla date conversion helpers and CLI entrypoints.

from __future__ import annotations

import subprocess
import sys
import unittest
from datetime import date, datetime

from bangla_date import (
    __version__,
    english_to_bangla_digits,
    format_bangla_date,
    format_current_bangla_date,
    gregorian_to_bangla_date,
    ইংরেজি_থেকে_বাংলা_সংখ্যা,
    গ্রেগরিয়ান_থেকে_বাংলা_তারিখ,
)


class BanglaDateTests(unittest.TestCase):
    def test_gregorian_to_bangla_date_matches_known_examples(self) -> None:
        cases = [
            (datetime(2024, 4, 14), (1, "বৈশাখ", 1431, "গ্রীষ্ম")),
            (datetime(2024, 5, 14), (31, "বৈশাখ", 1431, "গ্রীষ্ম")),
            (datetime(2024, 8, 15), (31, "শ্রাবণ", 1431, "বর্ষা")),
            (datetime(2024, 10, 17), (1, "কার্তিক", 1431, "হেমন্ত")),
            (datetime(2025, 1, 14), (30, "পৌষ", 1431, "শীত")),
        ]

        for gregorian_date, expected in cases:
            with self.subTest(gregorian_date=gregorian_date.date().isoformat()):
                self.assertEqual(gregorian_to_bangla_date(gregorian_date), expected)
                self.assertEqual(গ্রেগরিয়ান_থেকে_বাংলা_তারিখ(gregorian_date), expected)

    def test_leap_year_extends_falgun(self) -> None:
        self.assertEqual(
            gregorian_to_bangla_date(datetime(2024, 2, 29)), (16, "ফাল্গুন", 1430, "বসন্ত")
        )
        self.assertEqual(gregorian_to_bangla_date(datetime(2024, 3, 15)), (1, "চৈত্র", 1430, "বসন্ত"))
        self.assertEqual(gregorian_to_bangla_date(datetime(2025, 3, 15)), (1, "চৈত্র", 1431, "বসন্ত"))

    def test_accepts_plain_date(self) -> None:
        self.assertEqual(gregorian_to_bangla_date(date(2024, 4, 14)), (1, "বৈশাখ", 1431, "গ্রীষ্ম"))

    def test_digit_conversion_supports_english_and_bangla_aliases(self) -> None:
        self.assertEqual(english_to_bangla_digits(0), "০")
        self.assertEqual(english_to_bangla_digits(42), "৪২")
        self.assertEqual(ইংরেজি_থেকে_বাংলা_সংখ্যা(1432), "১৪৩২")

    def test_formatter_includes_date_and_season(self) -> None:
        output = format_bangla_date(datetime(2024, 8, 15))

        self.assertIn("আজকের বাংলা তারিখ: ৩১ শ্রাবণ, ১৪৩১ বঙ্গাব্দ", output)
        self.assertIn("বর্তমান ঋতু: বর্ষা", output)

    def test_current_formatter_delegates_to_date_formatter(self) -> None:
        self.assertEqual(
            format_current_bangla_date(datetime(2024, 8, 15)),
            format_bangla_date(datetime(2024, 8, 15)),
        )

    def test_module_cli_prints_expected_sections(self) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "bangla_date"],
            check=True,
            capture_output=True,
            text=True,
        )

        self.assertIn("আজকের বাংলা তারিখ:", result.stdout)
        self.assertIn("বর্তমান ঋতু:", result.stdout)

    def test_module_cli_help_describes_command(self) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "bangla_date", "--help"],
            check=True,
            capture_output=True,
            text=True,
        )

        self.assertIn("Print today's Bangla date and current season.", result.stdout)
        self.assertIn("usage: bangla-date", result.stdout)

    def test_module_cli_reports_version(self) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "bangla_date", "--version"],
            check=True,
            capture_output=True,
            text=True,
        )

        self.assertIn(__version__, result.stdout)

    def test_module_cli_rejects_unknown_arguments(self) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "bangla_date", "--nope"],
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 2)
        self.assertIn("unrecognized arguments", result.stderr)

    def test_wrapper_cli_help_matches_module_help(self) -> None:
        result = subprocess.run(
            [sys.executable, "bangla-date.py", "--help"],
            check=True,
            capture_output=True,
            text=True,
        )

        self.assertIn("Print today's Bangla date and current season.", result.stdout)
        self.assertIn("usage: bangla-date", result.stdout)


if __name__ == "__main__":
    unittest.main()
