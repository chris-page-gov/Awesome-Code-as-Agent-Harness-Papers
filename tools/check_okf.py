#!/usr/bin/env python3
"""Validate the local OKF v0.1 + OKFR profile."""

from __future__ import annotations

import sys

from okf_lib import okf_errors


def main() -> int:
    errors = okf_errors()
    if errors:
        print("OKF validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("OKF validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
