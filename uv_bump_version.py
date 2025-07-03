#!/usr/bin/env python3
import subprocess
import sys
import tomllib  # Python 3.11+. Use tomli if on older versions
from pathlib import Path


def get_version_from_toml(toml_text):
    data = tomllib.loads(toml_text)
    return data.get("project", {}).get("version")


def main():
    pyproject_path = Path("pyproject.toml")
    if not pyproject_path.exists():
        print("No pyproject.toml found")
        return 1

    current_content = pyproject_path.read_text()
    current_version = get_version_from_toml(current_content)

    try:
        git_show = subprocess.run(
            ["git", "show", "HEAD:pyproject.toml"],
            capture_output=True,
            text=True,
            check=True
        )
        head_content = git_show.stdout
        head_version = get_version_from_toml(head_content)
    except subprocess.CalledProcessError:
        # Likely first commit or pyproject.toml doesn't exist yet in HEAD
        head_version = None

    if current_version == head_version:
        print("No version bump detected. Bumping patch version via `uv version`.")
        subprocess.run(["uv", "version", "--bump", "patch"], check=True)
    else:
        print(f"Version bumped already: {head_version} → {current_version}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
