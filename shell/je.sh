#!/usr/bin/env bash
set -euo pipefail
shopt -s nullglob

DIR="$HOME/Documents/journalEntries"

first=$(ls -l "$DIR"/2024.*.txt | wc -l)
second=$(ls -l "$DIR"/2025.*.txt | wc -l)
third=$(ls -l "$DIR"/2026.*.txt | wc -l)
sum=$((first + second + third))

in_previous_years=$((366 + 365 + 0))
in_latest_year=$((10#$(date +%j)))
total_days=$((in_previous_years + in_latest_year))

files=( "$DIR"/20{24,25,26}*.txt )
sum=${#files[@]}

# Optimized non-ASCII file count (single grep; stop after first match per file)
# this is some wizardry from AI. bash is such an undecipherable language
# runtime is now SPEEDY though, which is what matters
count=0
if ((${#files[@]})); then
  count=$(LC_ALL=C grep -I -m1 -l '[^ -~]' "${files[@]}" | wc -l | xargs || true)
fi

echo -n "$sum/$total_days | "
echo -n "$count non-ASCII files | shortest: "
ls -lS "$DIR" | tail -n 1 | awk ' {print $5 "B on", $9}'
