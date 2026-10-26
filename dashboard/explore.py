import pandas as pd

df = pd.read_csv("market_aligned.csv", parse_dates=["date"])

print(df.columns.tolist())
print(df.tail())

vol = df["volatility_14d_pct"]

print(vol.describe())

avg_vol = vol.mean()
latest_vol = vol.iloc[-1]

print("6-month average:", round(avg_vol, 2))
print("Latest:", round(latest_vol, 2))
print("Latest vs average:", round(latest_vol / avg_vol, 2), "x")

ratio = vol / avg_vol

def rag(r):
    if r > 1.5:
        return "Red"
    elif r > 1.2:
        return "Amber"
    else:
        return "Green"

colours = ratio.dropna().apply(rag)
print(colours.value_counts())

last90 = df.tail(90)
change = (last90["close"].iloc[-1] / last90["close"].iloc[0] - 1) * 100
print("90-day change:", round(change, 1), "%")