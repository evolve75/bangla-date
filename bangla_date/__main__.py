#!/usr/bin/env python3
#
# SPDX-License-Identifier: MIT
#
# Copyright (C) 2026 Anupam Sengupta <anupamsg@gmail.com>
#
# Command-line entrypoint for printing today's Bangla date.

from __future__ import annotations

import sys

from bangla_date import format_current_bangla_date

HELP_TEXT = """Print today's Bangla date and current season.

Usage:
  python3 -m bangla_date
  python3 -m bangla_date --help
  bangla-date
"""


def main(argv: list[str] | None = None) -> int:
    """Run the Bangla date command-line interface."""
    args = sys.argv[1:] if argv is None else argv

    if args in (["-h"], ["--help"]):
        print(HELP_TEXT)
        return 0

    if args:
        print(f"error: unrecognized arguments: {' '.join(args)}", file=sys.stderr)
        print("Use --help to see supported options.", file=sys.stderr)
        return 2

    print(format_current_bangla_date())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
