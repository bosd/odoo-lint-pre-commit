# /// script
# requires-python = ">=3.11"
# dependencies = ["packaging>=24"]
# ///
"""Mirror new odoo-linter releases from PyPI: one commit and tag per version.

Pins the new version in pyproject.toml and the README examples, commits
"Mirror: <version>" and tags it `v<version>`. Pushing is left to the caller.
"""

import json
import re
import subprocess
import tomllib
import urllib.request
from pathlib import Path

from packaging.requirements import Requirement
from packaging.version import Version

ROOT = Path(__file__).parent
PACKAGE = "odoo-linter"


def released_versions() -> list[Version]:
    with urllib.request.urlopen(f"https://pypi.org/pypi/{PACKAGE}/json") as response:
        releases = json.load(response)["releases"]
    # Skip versions whose files were all yanked.
    return sorted(
        Version(v)
        for v, files in releases.items()
        if files and not all(f.get("yanked") for f in files)
    )


def pinned_version() -> Version:
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text())
    for dependency in pyproject["project"]["dependencies"]:
        requirement = Requirement(dependency)
        if requirement.name == PACKAGE:
            (specifier,) = requirement.specifier
            assert specifier.operator == "==", f"{requirement} must pin a version"
            return Version(specifier.version)
    raise SystemExit(f"pyproject.toml does not depend on {PACKAGE}")


def update(path: str, pattern: str, replacement: str) -> None:
    file = ROOT / path
    text, count = re.subn(pattern, replacement, file.read_text())
    assert count, f"{pattern!r} not found in {path}"
    file.write_text(text)


def main() -> None:
    current = pinned_version()
    for version in [v for v in released_versions() if v > current]:
        update("pyproject.toml", rf'"{PACKAGE}==[^"]+"', f'"{PACKAGE}=={version}"')
        update("README.md", r"rev: v[^\s]+", f"rev: v{version}")
        subprocess.run(["git", "add", "pyproject.toml", "README.md"], check=True)
        subprocess.run(["git", "commit", "-m", f"Mirror: {version}"], check=True)
        subprocess.run(["git", "tag", "-a", f"v{version}", "-m", f"odoo-linter {version}"], check=True)


if __name__ == "__main__":
    main()
