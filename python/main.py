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

def plot_string_occurrences_over_time(
    df: pd.DataFrame,
    search_term: str,
    entries_dir: str = "/Users/olympus/Documents/journalEntries",
    window_occ: int = 10,
    window_size: int = 100,
    use_log_scale_size: bool = False,
):
    """
    Plot raw occurrences and occurrences per KB of `search_term` over time,
    alongside smoothed entry byte sizes.

    Expects df to contain:
      - "date": str or datetime-like
      - optionally "byte_size": int (bytes). If missing, it will be computed by reading files as bytes.

    Returns a DataFrame with per-day metrics.
    """
    if df is None or "date" not in df.columns:
        raise ValueError("df must be a DataFrame with a 'date' column")

    if not isinstance(search_term, str) or not search_term.strip():
        raise ValueError("search_term must be a non-empty string")
    search_term = search_term.strip()

    data = df.copy()
    data["date"] = pd.to_datetime(data["date"])
    data = data.sort_values("date").reset_index(drop=True)

    # Build paths for each date using the same formatting as your other functions
    data["path"] = data["date"].dt.strftime("%Y.%m.%d").map(lambda s: f"{entries_dir}/{s}.txt")

    # Ensure byte_size exists; compute if needed
    if "byte_size" not in data.columns:
        byte_sizes = np.empty(len(data), dtype=int)
        for i, path in enumerate(data["path"]):
            if not os.path.exists(path):
                raise ValueError(f"path: {path} does not exist")
            with open(path, "rb") as f:
                byte_sizes[i] = len(f.read())
        data["byte_size"] = byte_sizes

    occurrences = np.zeros(len(data), dtype=float)
    for i, path in enumerate(data["path"]):
        if not os.path.exists(path):
            raise ValueError(f"path: {path} does not exist")
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        occurrences[i] = text.lower().count(search_term.lower())

    data["occurrences"] = occurrences

    # Avoid divide-by-zero; per-KB will be NaN where byte_size is 0
    data["occ_per_kb"] = data["occurrences"] / (data["byte_size"] / 1024.0).replace(0, np.nan)

    data["occ_sma"] = data["occurrences"].rolling(window=window_occ, center=True, min_periods=1).mean()
    data["occ_per_kb_sma"] = data["occ_per_kb"].rolling(window=window_occ, center=True, min_periods=1).mean()
    data["size_sma"] = data["byte_size"].rolling(window=window_size, center=True, min_periods=1).mean()

    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Left axis: occurrences + occurrences per KB
    ax1.plot(
        data["date"],
        data["occ_sma"],
        linewidth=2,
        label=f"{window_occ}-day avg '{search_term}' count",
    )
    ax1.scatter(data["date"], data["occurrences"], s=10, alpha=0.5)
    ax1.plot(
        data["date"],
        data["occ_per_kb_sma"],
        linewidth=2,
        linestyle="-",
        label=f"{window_occ}-day avg '{search_term}' per KB",
    )
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Occurrences (raw & per KB)")
    ax1.grid(True, linewidth=0.5, alpha=0.3)

    # Right axis: size
    ax2 = ax1.twinx()
    ax2.plot(
        data["date"],
        data["size_sma"],
        linewidth=2,
        linestyle="--",
        label=f"{window_size}-day avg size (bytes)",
    )
    ax2.set_ylabel("Journal size (bytes)")

    if use_log_scale_size:
        ax2.set_yscale("log", base=2)
    else:
        if not data["size_sma"].isna().all():
            ax2.set_ylim(0, float(data["size_sma"].max()))

    plt.title(
        f"Occurrences of '{search_term}' & Avg Journal Size "
        f"(occ: {window_occ}-day, size: {window_size}-day rolling average)"
    )
    fig.tight_layout()

    # Combine legends
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")

    plt.show()

def main():
    df = get_byte_sizes()
    plot_avg_sizes(df)
    find_most_common_words(df, 1000)
    plot_string_occurrences_over_time(df, "pickleball")

if __name__ == "__main__":
    main()
