#!/usr/bin/env bash
set -euo pipefail

OUTPUT_DIR="results/mutation/survivor_details"
SURVIVORS_FILE="results/mutation/manual/surviving_results.txt"

mkdir -p "$OUTPUT_DIR"
rm -f "$OUTPUT_DIR"/*.txt

grep ': survived$' "$SURVIVORS_FILE" |
while IFS=: read -r mutant status; do
    mutant="$(printf '%s' "$mutant" | xargs)"
    safe_name="$(printf '%s' "$mutant" | tr '/ǁ:' '___')"

    echo "Exporting $mutant"
    mutmut show "$mutant" > "$OUTPUT_DIR/${safe_name}.txt"
done

echo "Export complete."
