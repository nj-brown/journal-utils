#!/usr/bin/env bash
set -euo pipefail
shopt -s nullglob

DIR="$HOME/Documents/journalEntries"

# this is because I started journaling on Jan 1, 2024 (2024-01-01)
first=$(ls -l "$DIR"/2024.*.txt | wc -l)
second=$(ls -l "$DIR"/2025.*.txt | wc -l)
third=$(ls -l "$DIR"/2026.*.txt | wc -l)
sum=$((first + second + third))

in_previous_years=$((366 + 365 + 0))
in_latest_year=$((10#$(date +%j))) # force base10 interpretation (NOT octal)
total_days=$((in_previous_years + in_latest_year))

files=( "$DIR"/20{24,25,26}*.txt )
sum=${#files[@]}

# wizardry from AI that speeds up runtime a lot (bash is so indecipherable)
count=0
if ((${#files[@]})); then
  count=$(LC_ALL=C grep -I -m1 -l '[^ -~]' "${files[@]}" | wc -l | xargs || true)
fi

echo -n "$sum/$total_days | "
echo -n "$count non-ASCII files | shortest: "
ls -lS "$DIR" | tail -n 1 | awk ' {print $5 "B on", $9}'
