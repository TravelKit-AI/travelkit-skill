#!/bin/sh
set -eu

repo_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
package_file="$repo_root/skills/travelkit.zip"
tmp_dir=$(mktemp -d "${TMPDIR:-/tmp}/travelkit-package-check.XXXXXX")
expected_package="$tmp_dir/travelkit.zip"

cleanup() {
  rm -rf "$tmp_dir"
}
trap cleanup EXIT INT TERM

if [ ! -f "$package_file" ]; then
  echo "Missing package file: $package_file" >&2
  echo "Run scripts/package-skill.sh to generate it." >&2
  exit 1
fi

PACKAGE_OUTPUT="$expected_package" "$repo_root/scripts/package-skill.sh" >/dev/null

if ! cmp -s "$expected_package" "$package_file"; then
  echo "skills/travelkit.zip is out of date." >&2
  echo "Run scripts/package-skill.sh and commit the updated package." >&2
  exit 1
fi

if ! unzip -Z1 "$package_file" | grep -qx 'travelkit/SKILL.md'; then
  echo "Package is missing travelkit/SKILL.md." >&2
  exit 1
fi

if ! unzip -Z1 "$package_file" | grep -Eq '^travelkit/references/[^/]+\.md$'; then
  echo "Package is missing travelkit/references/*.md files." >&2
  exit 1
fi

echo "skills/travelkit.zip is up to date."
