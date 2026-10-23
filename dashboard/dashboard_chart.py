import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

df = pd.read_csv("market_aligned.csv", parse_dates=["date"])
last90 = df.tail(90).copy()

avg_vol = df["volatility_14d_pct"].mean()
latest_vol = df["volatility_14d_pct"].iloc[-1]
ratio = latest_vol / avg_vol

def rag(r):
    if r > 1.5:
        return "Red"
    elif r > 1.2:
        return "Amber"
    else:
        return "Green"

status = rag(ratio)
colours = {"Green": "green", "Amber": "orange", "Red": "red"}

last90["status"] = (last90["volatility_14d_pct"] / avg_vol).apply(rag)

fig, (top, bottom) = plt.subplots(
    2, 1, figsize=(10, 7), sharex=True,
    gridspec_kw={"height_ratios": [3, 1]}
)

top.plot(last90["date"], last90["close"], label="ASX 200 closing price")
top.plot(last90["date"], last90["ma_20"], label="20-day average")
top.set_title("ASX 200: last 90 trading days")
top.legend()

dates = last90["date"].tolist()
statuses = last90["status"].tolist()

for i in range(len(dates) - 1):
    if statuses[i] != "Green":
        top.axvspan(dates[i], dates[i + 1],
                    color=colours[statuses[i]], alpha=0.2, linewidth=0)

bottom.plot(last90["date"], last90["vix"], color="grey", label="Market fear index (VIX)")
bottom.legend()

bottom.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))

fig.suptitle(f"Volatility signal: {status}  |  price swings at {ratio:.2f}x normal",
             color=colours[status], fontsize=14, fontweight="bold")

plt.tight_layout()

plt.savefig("assets/part3_dashboard_chart.png", dpi=200)

plt.show()