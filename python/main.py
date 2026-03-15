import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import re
from datetime import datetime, date, timedelta
from collections import Counter

def get_byte_sizes():
    num = (date.today() - date(2024, 1, 1)).days + 1
    dates = (np.datetime64("2024-01-01") + np.arange(num, dtype="timedelta64[D]")).astype(str)

    byte_sizes = np.empty(num, dtype=int)
    for i, d in enumerate(dates):
        path = f"/Users/olympus/Documents/journalEntries/{d.replace('-', '.')}.txt"
        if not os.path.exists(path):
            raise ValueError(f"path: {path} does not exist")
        with open(path, "rb") as f:
            byte_sizes[i] = len(f.read())

    return pd.DataFrame({
        "date": dates,
        "byte_size": byte_sizes,
    })

def plot_avg_sizes(df, use_log_scale: bool=True):
    df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")

    df["sma20"] = df["byte_size"].rolling(window=20, min_periods=1).mean()
    df["sma50"] = df["byte_size"].rolling(window=50, min_periods=1).mean()
    df["sma100"] = df["byte_size"].rolling(window=100, min_periods=1).mean()

    ax = df.plot(
        x="date",
        y=["byte_size", "sma20", "sma50", "sma100"],
        style=[".", "-", "-"],
        markersize=6
    )

    ax.lines[0].set_alpha(0.4)

    if use_log_scale:
        ax.set_yscale("log", base=2)

    ax.grid(True, linewidth=0.5, alpha=0.3)
    ax.set_ylabel("bytes")
    ax.set_title("byte_size vs. time")
    plt.show()

def tokenize(text):
    return re.findall(r"[a-z']+", text.lower())

def find_most_common_words(df, num_of_words: int):
    paths = [
        f"/Users/olympus/Documents/journalEntries/{d.strftime('%Y.%m.%d')}.txt"
        for d in df["date"]
    ]

    counter = Counter()

    for path in paths:
        with open(path, "r", encoding="utf-8") as f:
            counter.update(tokenize(f.read()))

    print("Most common words:")
    for word, count in counter.most_common(num_of_words):
        print(f"{word:<15} {count}")

def plot_string_occurrences_over_time(df: pd.DataFrame, search_terms: list[str]):
    """
    For each journal entry date in df, count how many times each search term appears
    in the corresponding text file, then plot:
      - top subplot: daily occurrence counts as light scatter points
      - bottom subplot: 10-day moving average as solid lines
    """
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")

    results = []

    for entry_date in df["date"]:
        path = f"/Users/olympus/Documents/journalEntries/{entry_date.strftime('%Y.%m.%d')}.txt"

        if not os.path.exists(path):
            raise ValueError(f"path: {path} does not exist")

        with open(path, "r", encoding="utf-8") as f:
            text = f.read()

        row = {"date": entry_date}

        for term in search_terms:
            row[term] = len(re.findall(re.escape(term), text, flags=re.IGNORECASE))

        results.append(row)

    occurrences_df = pd.DataFrame(results).sort_values("date")

    for term in search_terms:
        occurrences_df[f"{term}_10dma"] = (
            occurrences_df[term].rolling(window=10, min_periods=1).mean()
        )

    fig, (ax1, ax2) = plt.subplots(
        2, 1,
        figsize=(13, 8),
        sharex=True,
        gridspec_kw={"height_ratios": [2, 1]}
    )

    cmap = plt.get_cmap("tab10")
    colors = [cmap(i % 10) for i in range(len(search_terms))]

    for term, color in zip(search_terms, colors):
        mask = occurrences_df[term] > 0
        ax1.scatter(
            occurrences_df.loc[mask, "date"],
            occurrences_df.loc[mask, term],
            color=color,
            alpha=0.22,
            s=24,
            label=term
        )

        ax2.plot(
            occurrences_df["date"],
            occurrences_df[f"{term}_10dma"],
            color=color,
            linewidth=2,
            label=term
        )

    raw_max = occurrences_df[search_terms].to_numpy().max()
    dma_max = occurrences_df[[f"{term}_10dma" for term in search_terms]].to_numpy().max()

    ax1.set_ylim(0, raw_max * 1.05 if raw_max > 0 else 1)
    ax2.set_ylim(0, dma_max * 1.10 if dma_max > 0 else 1)

    ax1.set_ylabel("daily occurrences")
    ax1.set_title("string occurrences over time")
    ax1.grid(True, linewidth=0.5, alpha=0.3)
    ax1.legend(loc="upper left")

    ax2.set_xlabel("date")
    ax2.set_ylabel("10DMA")
    ax2.grid(True, linewidth=0.5, alpha=0.3)

    plt.tight_layout()
    plt.show()

    return occurrences_df

def main():
    df = get_byte_sizes()
    plot_avg_sizes(df)
    find_most_common_words(df, 1000)
    plot_string_occurrences_over_time(df, ["minecraft", "london", "pickleball"])

if __name__ == "__main__":
    main()
