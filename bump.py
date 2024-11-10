#!/usr/bin/python3
"""
Usage:
  bump.py <directory> --major <release_notes>
  bump.py <directory> --minor <release_notes>
  bump.py <directory> --patch <release_notes>

Options:
  <directory>      The directory where the app's config files are located.
  <release_notes>  Release notes describing the changes for this version.
  --major          Increment the major version (e.g., 1.0.0 -> 2.0.0).
  --minor          Increment the minor version (e.g., 1.0.0 -> 1.1.0).
  --patch          Increment the patch version (e.g., 1.0.0 -> 1.0.1).
"""

import os
import re
import sys
import subprocess
import logging
from docopt import docopt

# Setup logger
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# File names
CONFIG_FILE = "config.json"
DOCKER_FILE = "Dockerfile"
CHANGELOG_FILE = "CHANGELOG.md"


def get_current_version(directory):
    config_path = os.path.join(directory, CONFIG_FILE)
    logger.info(f"Reading current version from {config_path}...")
    with open(config_path, "r") as f:
        for line in f:
            match = re.search(r'"version":\s*"(\d+\.\d+\.\d+)"', line)
            if match:
                current_version = match.group(1)
                logger.info(f"Current version found: {current_version}")
                return current_version
    raise ValueError("Version not found in config.json")


def increment_version(version, part):
    major, minor, patch = map(int, version.split("."))
    if part == "major":
        new_version = f"{major + 1}.0.0"
    elif part == "minor":
        new_version = f"{major}.{minor + 1}.0"
    elif part == "patch":
        new_version = f"{major}.{minor}.{patch + 1}"
    else:
        raise ValueError("Invalid version part")
    logger.info(f"Version incremented to: {new_version}")
    return new_version


def update_version_in_files(directory, new_version):
    config_path = os.path.join(directory, CONFIG_FILE)
    logger.info(f"Updating version in {config_path}...")
    with open(config_path, "r") as f:
        content = f.read()
    content = re.sub(
        r'"version":\s*"\d+\.\d+\.\d+"', f'"version": "{new_version}"', content
    )

    content = re.sub(
        r'local/duty-cycle-controller:\d+\.\d+\.\d+', f'"version": "{new_version}"', content
    )

    with open(config_path, "w") as f:
        f.write(content)

    docker_path = os.path.join(directory, DOCKER_FILE)
    logger.info(f"Updating version in {docker_path} if applicable...")
    if os.path.exists(docker_path):
        with open(docker_path, "r") as f:
            content = f.read()
        if "version" in content:
            content = re.sub(
                r'("version":\s*"\d+\.\d+\.\d+")',
                f'"version": "{new_version}"',
                content,
            )
        with open(docker_path, "w") as f:
            f.write(content)


def update_changelog(directory, new_version, release_notes):
    changelog_path = os.path.join(directory, CHANGELOG_FILE)
    logger.info(f"Updating {changelog_path}...")
    if not os.path.exists(changelog_path):
        logger.info(f"{CHANGELOG_FILE} not found. Creating a new one.")
        with open(changelog_path, "w") as f:
            f.write("")

    with open(changelog_path, "r") as f:
        changelog_content = f.read()

    new_entry = (
        f"## [{new_version}] - {sys.argv[-1]}\n### Changes\n- {release_notes}\n\n"
    )
    with open(changelog_path, "w") as f:
        f.write(new_entry + changelog_content)


def commit_and_tag_repo(directory, new_version):
    logger.info("Committing changes and tagging the new version...")
    try:
        subprocess.run(
            [
                "git",
                "add",
                os.path.join(directory, CONFIG_FILE),
                os.path.join(directory, DOCKER_FILE),
                os.path.join(directory, CHANGELOG_FILE),
            ],
            check=True,
        )
        subprocess.run(
            ["git", "commit", "-m", f"Bump version to {new_version}"], check=True
        )
        subprocess.run(["git", "tag", f"v{new_version}"], check=True)
        logger.info(f"Version {new_version} tagged successfully.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Git command failed: {e}")
        sys.exit(1)


def main():
    args = docopt(__doc__)
    directory = args["<directory>"]
    release_notes = args["<release_notes>"]

    if not os.path.isdir(directory):
        logger.error(f"Directory '{directory}' does not exist.")
        sys.exit(1)

    current_version = get_current_version(directory)
    if args["--major"]:
        new_version = increment_version(current_version, "major")
    elif args["--minor"]:
        new_version = increment_version(current_version, "minor")
    elif args["--patch"]:
        new_version = increment_version(current_version, "patch")
    else:
        logger.error("Invalid option. Use --major, --minor, or --patch.")
        sys.exit(1)

    # Update version numbers in files
    update_version_in_files(directory, new_version)

    # Update CHANGELOG.md
    update_changelog(directory, new_version, release_notes)

    # Commit and tag the new version in Git
    commit_and_tag_repo(directory, new_version)

    logger.info(f"Version bumped to {new_version} with changelog updated.")


if __name__ == "__main__":
    main()
