
from pathlib import Path
import pandas as pd
import logging

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent

RAW_FILE = BASE_DIR / "data/raw/vix_raw.csv"
CURATED_DIR = BASE_DIR / "data/curated"
QUARANTINE_DIR = BASE_DIR / "data/quarantine"
LOG_DIR = BASE_DIR / "logs"

for folder in [CURATED_DIR, QUARANTINE_DIR, LOG_DIR]:
    folder.mkdir(parents=True, exist_ok=True)

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "pipeline.log"),
        logging.StreamHandler()
    ]
)

def validate_vix():
    logging.info("Starting VIX data validation")

    # Read raw data without changing the source file
    df = pd.read_csv(
        RAW_FILE,
        dtype=str,
        keep_default_na=False
    )

    required = ["observation_date", "VIXCLS"]
    missing = [c for c in required if c not in df.columns]

    if missing:
        logging.error(f"Missing VIX columns: {missing}")
        raise ValueError(f"Invalid FRED schema: {missing}")

    # Validate dates and numeric values
    dates = pd.to_datetime(
        df["observation_date"],
        format="%Y-%m-%d",
        errors="coerce"
    )

    values = pd.to_numeric(
        df["VIXCLS"],
        errors="coerce"
    )

    bad_date = dates.isna()
    bad_vix = values.isna() | (values <= 0)
    duplicate = df.duplicated(
        subset=["observation_date"],
        keep="first"
    )

    flagged_mask = bad_date | bad_vix | duplicate

    # Record all flagged rows with specific reasons
    flagged = df.loc[flagged_mask].copy()

    reasons = []
    for index in flagged.index:
        issues = []

        if bad_date.loc[index]:
            issues.append("Invalid observation date")

        if bad_vix.loc[index]:
            issues.append("Missing or invalid VIX value")

        if duplicate.loc[index]:
            issues.append("Duplicate observation date")

        reasons.append("; ".join(issues))

    flagged["reason"] = reasons

    quarantine_file = (
        QUARANTINE_DIR / "vix_quarantine.csv"
    )
    flagged.to_csv(quarantine_file, index=False)

    # Keep valid records only
    clean = pd.DataFrame({
        "date": dates.loc[~flagged_mask].dt.strftime(
            "%Y-%m-%d"
        ),
        "vix": values.loc[~flagged_mask]
    })

    clean = clean.sort_values("date")

    output_file = CURATED_DIR / "vix_curated.csv"
    clean.to_csv(output_file, index=False)

    # Quality logging
    logging.info(f"Total VIX records: {len(df)}")
    logging.info(f"Flagged VIX records: {len(flagged)}")
    logging.info(f"Valid VIX records: {len(clean)}")
    logging.info(f"Invalid dates: {bad_date.sum()}")
    logging.info(f"Invalid values: {bad_vix.sum()}")
    logging.info(f"Duplicate dates: {duplicate.sum()}")
    logging.info(f"Quarantine saved: {quarantine_file}")
    logging.info(f"Curated data saved: {output_file}")

    print("\nVIX validation completed!")
    print(f"Raw records: {len(df)}")
    print(f"Flagged records: {len(flagged)}")
    print(f"Curated records: {len(clean)}")


if __name__ == "__main__":
    validate_vix()
