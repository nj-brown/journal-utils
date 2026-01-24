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

count=0
for file in "$DIR"/20{24,25,26}*.txt; do
  if LC_ALL=C grep -q "[^ -~]" "$file"; then
    # echo "$file"
    ((count++))
  fi
done

echo -n "$sum/$total_days | "
echo -n "$count non-ASCII files | shortest: "
ls -lS "$DIR" | tail -n 1 | awk ' {print $5 "B on", $9}'
