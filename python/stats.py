import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import re
from datetime import datetime, date, timedelta
from collections import Counter

def get_data():
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

def plot_avg_sizes(df):
    """Plots average size of journal entries vs time on a log scale."""
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

    # make individual data points less prominent
    ax.lines[0].set_alpha(0.4)

    use_log_scale = True
    if use_log_scale:
        ax.set_yscale("log", base=2)

    ax.grid(True, linewidth=0.5, alpha=0.3)
    ax.set_ylabel("bytes")
    ax.set_title("byte_size vs. time")
    plt.show()

def tokenize(text):
    return re.findall(r"[a-z']+", text.lower())

def most_common_words(df):
    paths = [
        f"/Users/olympus/Documents/journalEntries/{d.strftime('%Y.%m.%d')}.txt"
        for d in df["date"]
    ]

    counter = Counter()

    for path in paths:
        with open(path, "r", encoding="utf-8") as f:
            counter.update(tokenize(f.read()))

    print("Most common words:")
    for word, count in counter.most_common(500):
        print(f"{word:<15} {count}")

def main():
    df = get_data()
    plot_avg_sizes(df)
    # most_common_words(df)

if __name__ == "__main__":
    main()
