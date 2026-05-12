#!/usr/bin/env bash
set -euo pipefail

if [[ -z "${TRAVELKIT_API_KEY:-}" ]]; then
  echo "Missing TRAVELKIT_API_KEY environment variable." >&2
  exit 1
fi

CODE="${TRAVELKIT_API_KEY:0:6}"
API_KEY="${TRAVELKIT_API_KEY:6}"

TS="${TS:-$(date -u +%s)}"
SIG="$(printf "%s" "${CODE}${TS}${API_KEY}" | shasum -a 1 | awk '{print $1}')"

printf 'TS=%s\nSIG=%s\n' "${TS}" "${SIG}"
