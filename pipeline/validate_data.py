
from pathlib import Path
import pandas as pd
import logging

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_FILE = BASE_DIR / "data/raw/asx200_raw.csv"
CURATED_DIR = BASE_DIR / "data/curated"
QUARANTINE_DIR = BASE_DIR / "data/quarantine"
LOG_DIR = BASE_DIR / "logs"

for folder in [CURATED_DIR, QUARANTINE_DIR, LOG_DIR]:
    folder.mkdir(parents=True, exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "pipeline.log"),
        logging.StreamHandler()
    ]
)

def validate_data():
    logging.info("Starting ASX 200 data validation")

    # Read original downloaded CSV without modifying it
    df = pd.read_csv(RAW_FILE)

    required_columns = [
        "Date", "Open", "High", "Low", "Close", "Volume"
    ]

    missing_columns = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:
        logging.error(
            f"Missing required columns: {missing_columns}"
        )
        return

    # Create a separate working copy
    clean = df.copy()

    # Convert numeric fields for validation
    for col in ["Open", "High", "Low", "Close", "Volume"]:
        clean[col] = pd.to_numeric(
            clean[col], errors="coerce"
        )

    # Apply quality checks
    bad_close = clean["Close"].isna() | (clean["Close"] <= 0)
    bad_volume = clean["Volume"].isna() | (clean["Volume"] <= 0)

    # Record every flagged row with a reason
    flagged = clean[bad_close | bad_volume].copy()

    flagged["reason"] = [
        "; ".join(
            reason for condition, reason in [
                (bc, "Missing or invalid closing price"),
                (bv, "Missing or zero volume")
            ]
            if condition
        )
        for bc, bv in zip(
            bad_close[bad_close | bad_volume],
            bad_volume[bad_close | bad_volume]
        )
    ]

    quarantine_file = (
        QUARANTINE_DIR / "asx200_quarantine.csv"
    )
    flagged.to_csv(quarantine_file, index=False)

    # Missing closing prices cannot support price analysis
    clean = clean.loc[~bad_close].copy()

    # Zero volume is flagged and treated as unavailable
    clean.loc[clean["Volume"] <= 0, "Volume"] = float("nan")

    # Standardise dates to Sydney local trading dates
    clean["date"] = (
        pd.to_datetime(clean["Date"], utc=True)
        .dt.tz_convert("Australia/Sydney")
        .dt.strftime("%Y-%m-%d")
    )

    # Match agreed group CSV structure
    clean = clean.rename(columns={
        "Open": "open",
        "High": "high",
        "Low": "low",
        "Close": "close",
        "Volume": "volume"
    })

    clean = clean[
        ["date", "open", "high", "low", "close", "volume"]
    ]

    output_file = CURATED_DIR / "asx200_curated.csv"
    clean.to_csv(output_file, index=False)

    logging.info(f"Total raw records: {len(df)}")
    logging.info(f"Flagged records: {len(flagged)}")
    logging.info(f"Invalid close records: {bad_close.sum()}")
    logging.info(f"Unavailable volume records: {bad_volume.sum()}")
    logging.info(f"Curated price records: {len(clean)}")
    logging.info(f"Quarantine saved: {quarantine_file}")
    logging.info(f"Curated data saved: {output_file}")

    print("\nValidation completed!")
    print(f"Raw records: {len(df)}")
    print(f"Flagged records: {len(flagged)}")
    print(f"Curated records: {len(clean)}")


if __name__ == "__main__":
    validate_data()
