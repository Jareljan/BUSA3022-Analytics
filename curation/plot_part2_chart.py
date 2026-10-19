
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# ==============================================
# BUSA3022 - PART 2: DATA CURATION PORTFOLIO
# Figure 3: Market Trends and VIX Context
# ==============================================

# 1. Load validated, aligned data
project_dir = Path(__file__).resolve().parent.parent

data_path = project_dir / "data" / "curated" / "market_aligned.csv"
df = pd.read_csv(data_path, parse_dates=["date"])

df = df.sort_values("date")

# Select the last 90 trading observations
df = df.tail(90)

# 2. Define professional chart colours
navy = "#20344D"
blue = "#4479B9"
teal = "#159E91"
purple = "#8868BE"
grey = "#60738B"

# 3. Create figure
fig, ax1 = plt.subplots(figsize=(13, 6.5))

fig.patch.set_facecolor("white")
ax1.set_facecolor("white")

# 4. Plot ASX closing price
line1, = ax1.plot(
    df["date"],
    df["close"],
    color=blue,
    linewidth=2,
    label="ASX 200 Closing Price"
)

# 5. Plot 20-day moving average
line2, = ax1.plot(
    df["date"],
    df["ma_20"],
    color=teal,
    linewidth=2.5,
    label="20-Day Moving Average"
)

# 6. Plot VIX on secondary axis
ax2 = ax1.twinx()

line3, = ax2.plot(
    df["date"],
    df["vix"],
    color=purple,
    linewidth=1.8,
    linestyle="--",
    alpha=0.85,
    label="Lagged VIX"
)

# 7. Add chart labels
ax1.set_title(
    "MARKET INTELLIGENCE | DATA CURATION RESULTS",
    fontsize=16,
    fontweight="bold",
    color=navy,
    loc="left",
    pad=25
)

ax1.text(
    0,
    1.015,
    "ASX 200 closing prices, 20-day moving average and lagged US volatility context",
    transform=ax1.transAxes,
    fontsize=10,
    color=grey
)

ax1.set_xlabel(
    "ASX Trading Date",
    fontsize=10,
    color=navy,
    labelpad=12
)

ax1.set_ylabel(
    "ASX 200 Index Level",
    fontsize=10,
    color=navy
)

ax2.set_ylabel(
    "VIX Index Level",
    fontsize=10,
    color=purple
)

# 8. Format date axis
ax1.xaxis.set_major_locator(mdates.MonthLocator())
ax1.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))

plt.setp(ax1.get_xticklabels(), rotation=0)

# 9. Add subtle horizontal gridlines
ax1.grid(
    axis="y",
    linestyle="--",
    alpha=0.18
)

ax1.set_axisbelow(True)

# 10. Remove unnecessary chart borders
ax1.spines["top"].set_visible(False)
ax1.spines["right"].set_visible(False)

ax2.spines["top"].set_visible(False)
ax2.spines["left"].set_visible(False)

# 11. Create combined legend
ax1.legend(
    handles=[line1, line2, line3],
    loc="upper right",
    frameon=False,
    fontsize=9,
    ncol=3
)

# 12. Add source and methodological note
fig.text(
    0.11,
    0.035,
    "Source: Yahoo Finance (ASX 200) and FRED (VIX). "
    "VIX matched to earlier US observation dates.",
    fontsize=8,
    color=grey
)

# 13. Save high-resolution figure
output_dir = project_dir / "assets"
output_dir.mkdir(parents=True, exist_ok=True)

output_path = output_dir / "part2_market_chart.png"

fig.subplots_adjust(
    left=0.11,
    right=0.89,
    top=0.82,
    bottom=0.17
)

fig.savefig(
    output_path,
    dpi=300,
    bbox_inches="tight",
    facecolor="white"
)

plt.close(fig)

print("Figure 3 generated successfully!")
print("Saved to:", output_path)
print("Chart observations:", len(df))
print("Start date:", df["date"].min().date())
print("End date:", df["date"].max().date())
