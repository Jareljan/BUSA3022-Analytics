
from pathlib import Path
import pandas as pd

# Locate the project directory
project_dir = Path(__file__).resolve().parent.parent

# Load curated market datasets from Part 1
asx = pd.read_csv(project_dir / "data" / "curated" / "asx200_curated.csv")
vix = pd.read_csv(project_dir / "data" / "curated" / "vix_curated.csv")

# Convert date columns
asx["date"] = pd.to_datetime(asx["date"])
vix["date"] = pd.to_datetime(vix["date"])

# Display dataset information
print("ASX 200 dataset:")
print(asx[["date", "close"]].head())
print("\nASX rows:", len(asx))

print("\nVIX dataset:")
print(vix[["date", "vix"]].head())
print("\nVIX rows:", len(vix))

# Compare the latest available dates
print("\nLatest ASX date:", asx["date"].max())
print("Latest VIX date:", vix["date"].max())



# PART 2: Align ASX 200 and VIX observations

# Sort both datasets by their observation dates
asx = asx.sort_values("date").reset_index(drop=True)
vix = vix.sort_values("date").reset_index(drop=True)

# Rename the VIX date to keep track of its original observation date
vix = vix.rename(columns={"date": "vix_observation_date"})

# Match each ASX row with the latest earlier VIX observation
aligned = pd.merge_asof(
    asx,
    vix,
    left_on="date",
    right_on="vix_observation_date",
    direction="backward",
    allow_exact_matches=False
)

# Display aligned observations
print("\nAligned ASX 200 and VIX Data:")
print(aligned[["date", "close", "vix_observation_date", "vix"]].tail(10))

# Check whether any ASX dates have no matching VIX observation
print("\nUnmatched ASX observations:", aligned["vix"].isna().sum())



# PART 2: Investigate unmatched observations

unmatched = aligned[aligned["vix"].isna()]

print("\nASX Records Without a Matching VIX Observation:")
print(unmatched[["date", "close", "vix_observation_date", "vix"]])

print("\nUnmatched record count:", len(unmatched))



# PART 2: Save the aligned market dataset

# Create a dedicated folder for Part 2 outputs
output_dir = project_dir / "data" / "curated"
output_dir.mkdir(parents=True, exist_ok=True)

# Save all ASX observations, including unmatched records
output_path = output_dir / "market_aligned.csv"



print("\nAligned dataset saved successfully!")
print("File:", output_path)
print("Total observations:", len(aligned))
print("Matched VIX observations:", aligned["vix"].notna().sum())
print("Missing VIX observations:", aligned["vix"].isna().sum())



# PART 2: Integrate calculated market metrics

# Calculate the 20-day moving average
aligned["ma_20"] = (
    aligned["close"]
    .rolling(window=20, min_periods=20)
    .mean()
)

# Calculate daily percentage returns
aligned["daily_return_pct"] = (
    aligned["close"].pct_change(fill_method=None) * 100
)

# Calculate 14-day rolling volatility
aligned["volatility_14d_pct"] = (
    aligned["daily_return_pct"]
    .rolling(window=14, min_periods=14)
    .std()
)

# Save the updated dataset with all three metrics
aligned.to_csv(output_path, index=False)

print("\nFinal Analytics-Ready Dataset:")
print(
    aligned[
        [
            "date",
            "close",
            "ma_20",
            "daily_return_pct",
            "volatility_14d_pct",
            "vix"
        ]
    ].tail()
)

print("\nFinal dataset saved:", output_path)



# PART 2: Validate the final curated dataset

print("\nData Quality Validation Results:")

# Check that no ASX observations disappeared
assert len(aligned) == len(asx), "ASX row count mismatch"
print("PASS: All ASX observations preserved")

# Check for invalid ASX closing prices
assert (aligned["close"].notna() & (aligned["close"] > 0)).all(), \
    "Missing or invalid ASX closing prices"
print("PASS: All ASX closing prices are valid")

# Check for duplicate ASX dates
assert not aligned["date"].duplicated().any(), \
    "Duplicate ASX trading dates detected"
print("PASS: No duplicate ASX dates")

# Check that every matched VIX observation precedes its ASX date
matched = aligned.dropna(subset=["vix_observation_date"])

assert (
    matched["vix_observation_date"] < matched["date"]
).all(), "Invalid VIX date alignment"
print("PASS: VIX observations precede ASX trading dates")

# Check that all aligned rows contain a VIX value if a date matched
assert matched["vix"].notna().all(), \
    "Matched VIX observation contains a missing value"
print("PASS: All matched VIX values are present")

# Report unmatched observations without deleting them
print("Unmatched VIX observations:", aligned["vix"].isna().sum())

print("\nAll data-quality validation checks passed!")


# Publish the final dataset only after validation succeeds
aligned.to_csv(output_path, index=False)

print("\nValidated analytics-ready dataset published!")
print("Output:", output_path)
print("Records:", len(aligned))
