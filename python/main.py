import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import re
from datetime import datetime, date, timedelta
from collections import Counter

def main():
    choice = input(
        "Choose an option.\n"
        "1: occurrences of a string over time\n"
        "2: data of journal sizes\n"
        "--> "
    )

    if choice == "1":
        string_occurrences_over_time()
    elif choice == "2":
        basic_stats()

def basic_stats():
    days = (date.today() - date(2024, 1, 1)).days + 1
    byte_sizes = np.zeros(days)

    for i in range(days):

        dt = datetime(2024, 1, 1) + timedelta(days=i)
        formatted_date = dt.strftime("%Y.%m.%d")
        path = f"/Users/olympus/Documents/journalEntries/{formatted_date}.txt"

        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
            byte_sizes[i] = len(text.encode("utf-8"))

        else:
            print("uh oh... missing a journal entry somewhere")

    # ChatGPT boilerplate, cleaned by me

    valid_sizes = byte_sizes[byte_sizes > 0]
    mean_size = np.mean(valid_sizes)
    median_size = np.median(valid_sizes)
    min_size = np.min(valid_sizes)
    std_size = np.std(valid_sizes)

    # Basic stats
    print("Journal Entry Statistics")
    print(f"Mean size: {mean_size:.2f} bytes")
    print(f"Median size: {median_size:.2f} bytes")
    print(f"Standard deviation: {std_size:.2f} bytes")
    print(f"Total entries: {len(valid_sizes)} / {days} days recorded")

    # Histogram
    plt.figure(figsize=(10, 6))
    plt.hist(byte_sizes[byte_sizes > 0], 
             bins=50, edgecolor='black', alpha=0.7)
    plt.title("Distribution of Journal Entry Sizes (in bytes)", fontsize=16)
    plt.xlabel("Byte Size", fontsize=14)
    plt.ylabel("Frequency", fontsize=14)
    plt.axvline(mean_size, 
                color='red', 
                linestyle='-', 
                linewidth=2,
                label=f"Mean: {mean_size:.0f}")
    plt.axvline(median_size, 
                color='green', 
                linestyle='-', 
                linewidth=2,
                label=f"Median: {median_size:.0f}") 
    plt.axvline(min_size,
                color='orange',
                linestyle='-',
                linewidth=2,
                label=f"Min: {min_size:.0f}")
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.legend()
    plt.show()

def string_occurrences_over_time():
    search_term = input("Enter search term: ").strip()
    days = (date.today() - date(2024, 1, 1)).days + 1
    occurrences = np.zeros(shape=days)
    entry_sizes = np.zeros(shape=days)

    for i in range(days):
        dt = datetime(2024, 1, 1) + timedelta(days=i)
        formatted_date = dt.strftime("%Y.%m.%d")
        path = f"/Users/olympus/Documents/journalEntries/{formatted_date}.txt"

        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
            count = text.lower().count(search_term.lower())
            occurrences[i] = count
            entry_sizes[i] = len(text.encode("utf-8"))

        else:
            occurrences[i] = 0
            entry_sizes[i] = 0

    dates = pd.date_range(start=date(2024, 1, 1), periods=len(occurrences),
                          freq="D")
    s_occ = pd.Series(occurrences, index=dates)
    s_size = pd.Series(entry_sizes, index=dates)
    occ_per_kb = s_occ / (s_size / 1024)
    window1 = 10
    
    rolling_occ = s_occ.rolling(window=window1, center=True).mean()
    rolling_occ_per_kb = occ_per_kb.rolling(window=window1, center=True).mean()
    rolling_size = s_size.rolling(window=100, center=True).mean()

    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Left axis: occurrences
    ax1.plot(s_occ.index, rolling_occ, color="blue", linewidth=2,
             label=f"{window1}-day avg '{search_term}' count")
    ax1.scatter(s_occ.index, s_occ.values, color="lightgray", s=10, alpha=0.5)
    ax1.plot(s_occ.index, rolling_occ_per_kb, color="green", linewidth=2,
             linestyle="-", label=f"{window1}-day avg '{search_term}' per KB")

    ax1.set_xlabel("Date")
    ax1.set_ylabel("Normalized Occurrences", color="blue")
    ax1.tick_params(axis="y", labelcolor="blue")

    # Right axis: journal size (100-day smoothing)
    ax2 = ax1.twinx()
    ax2.plot(s_size.index, rolling_size, color="red", linewidth=2,
             linestyle="--", label="100-day avg size")
    ax2.set_ylabel("Journal size (bytes)", color="red")
    ax2.tick_params(axis="y", labelcolor="red")

    # Force right axis from 0 to max
    if not rolling_size.isna().all():
        ax2.set_ylim(0, rolling_size.max())

    plt.title(
        f"Occurrences of '{search_term}' & Avg Journal Size "
        f"(occ: {window1}-day, size: 100-day rolling average)"
    )
    fig.tight_layout()

    # Combine legends from both axes
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")

    plt.show()

if __name__ == "__main__":
    main()
