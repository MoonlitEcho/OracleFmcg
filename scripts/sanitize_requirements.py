#!/usr/bin/env python3
"""Generate installable requirements from a platform-specific requirements file."""

from __future__ import annotations

import argparse
from pathlib import Path
import re

BASE_ALLOWED = {
    "fastapi",
    "google-generativeai",
    "joblib",
    "prometheus-fastapi-instrumentator",
    "lightgbm",
    "numpy",
    "pandas",
    "plotly",
    "pydantic",
    "reportlab",
    "requests",
    "scikit-learn",
    "shap",
    "streamlit",
    "uvicorn",
}

DEV_ALLOWED = {
    "bandit",
    "flake8",
    "httpx",
    "mypy",
    "pip-audit",
    "pytest",
    "pytest-cov",
    "types-requests",
}

PACKAGE_RE = re.compile(r"^([A-Za-z0-9_.-]+)")


def decode_requirements(raw: bytes) -> str:
    for encoding in ("utf-8", "utf-16", "utf-16-le", "utf-16-be"):
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            continue
    raise ValueError("Unable to decode requirements file.")


def parse_requirements(lines: list[str], allowed: set[str]) -> list[str]:
    seen: dict[str, str] = {}
    for line in lines:
        cleaned = line.replace("\x00", "").strip()
        if not cleaned or cleaned.startswith("#"):
            continue
        if " @ file:///" in cleaned:
            continue

        match = PACKAGE_RE.match(cleaned)
        if not match:
            continue
        package = match.group(1).lower()
        if package in allowed and package not in seen:
            seen[package] = cleaned

    for package in sorted(allowed):
        seen.setdefault(package, package)

    return [seen[pkg] for pkg in sorted(seen)]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--with-dev", action="store_true", help="Include development dependencies")
    args = parser.parse_args()

    allowed = set(BASE_ALLOWED)
    if args.with_dev:
        allowed |= DEV_ALLOWED

    text = decode_requirements(args.input.read_bytes())
    parsed = parse_requirements(text.splitlines(), allowed)
    args.output.write_text("\n".join(parsed) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
