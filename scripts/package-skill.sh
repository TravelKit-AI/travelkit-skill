#!/bin/sh
set -eu

repo_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
source_dir="$repo_root/skills/travelkit"
output_file="${PACKAGE_OUTPUT:-$repo_root/skills/travelkit.zip}"
tmp_dir=$(mktemp -d "${TMPDIR:-/tmp}/travelkit-package.XXXXXX")

cleanup() {
  rm -rf "$tmp_dir"
}
trap cleanup EXIT INT TERM

if [ ! -f "$source_dir/SKILL.md" ]; then
  echo "Missing skill entrypoint: $source_dir/SKILL.md" >&2
  exit 1
fi

if [ ! -d "$source_dir/references" ]; then
  echo "Missing skill references directory: $source_dir/references" >&2
  exit 1
fi

mkdir -p "$(dirname -- "$output_file")"
rm -f "$output_file"
cp -R "$source_dir" "$tmp_dir/travelkit"

find "$tmp_dir/travelkit" \( \
  -name '.DS_Store' -o \
  -name '__MACOSX' -o \
  -name '._*' \
\) -exec rm -rf {} +

rm -rf "$tmp_dir/travelkit/scripts"

find "$tmp_dir/travelkit" -exec touch -t 202601010000 {} +

(
  cd "$tmp_dir"
  find travelkit -print | LC_ALL=C sort | zip -X -q "$output_file" -@
)

echo "Wrote $output_file"
