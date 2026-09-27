#!/usr/bin/env python3
#
# SPDX-License-Identifier: MIT
#
# Copyright (C) 2026 Anupam Sengupta <anupamsg@gmail.com>
#
# Command-line entrypoint for printing today's Bangla date.

from __future__ import annotations

import argparse

from bangla_date import __version__, format_current_bangla_date


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line argument parser."""
    parser = argparse.ArgumentParser(
        prog="bangla-date",
        description="Print today's Bangla date and current season.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the Bangla date command-line interface."""
    parser = build_parser()
    parser.parse_args(argv)

    print(format_current_bangla_date())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
