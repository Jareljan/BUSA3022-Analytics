
from pathlib import Path
import pandas as pd

# Locate the project folder
project_dir = Path(__file__).resolve().parent.parent

# Load the cleaned ASX 200 dataset from Part 1
asx_path = project_dir / "data" / "curated" / "asx200_curated.csv"

asx = pd.read_csv(asx_path)

# Display the first five rows
print("ASX 200 Curated Data:")
print(asx.head())

# Check the number of rows and columns
print("\nDataset shape:", asx.shape)


# PART 2: Calculate the 20-day moving average

# Convert dates into datetime format
asx["date"] = pd.to_datetime(asx["date"])

# Sort observations from oldest to newest
asx = asx.sort_values("date").reset_index(drop=True)

# Calculate the average closing price over 20 trading days
asx["ma_20"] = asx["close"].rolling(window=20, min_periods=20).mean()

# Display the latest five results
print("\n20-Day Moving Average Results:")
print(asx[["date", "close", "ma_20"]].tail())



# PART 2: Calculate daily percentage returns

# Calculate the percentage change between trading sessions
asx["daily_return_pct"] = asx["close"].pct_change(fill_method=None) * 100

# Display the latest five daily returns
print("\nDaily Return Results:")
print(asx[["date", "close", "daily_return_pct"]].tail())



# PART 2: Calculate 14-day rolling volatility

# Calculate standard deviation of daily returns over 14 trading days
asx["volatility_14d_pct"] = (
    asx["daily_return_pct"]
    .rolling(window=14, min_periods=14)
    .std()
)

# Display the latest five volatility results
print("\n14-Day Rolling Volatility Results:")
print(asx[["date", "daily_return_pct", "volatility_14d_pct"]].tail())
