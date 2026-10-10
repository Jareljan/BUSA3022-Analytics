
from pathlib import Path
from datetime import date, timedelta
import requests
import pandas as pd

# Project folders
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

# FRED VIX series
URL = "https://fred.stlouisfed.org/graph/fredgraph.csv"

end_date = date.today()
start_date = end_date - timedelta(days=183)

params = {
    "id": "VIXCLS",
    "cosd": start_date.isoformat(),
    "coed": end_date.isoformat()
}

print("Downloading VIX data from FRED...")

try:
    response = requests.get(
        URL,
        params=params,
        timeout=20
    )
    response.raise_for_status()

    if not response.content.strip():
        raise ValueError("FRED returned an empty file")

    # Save the downloaded CSV without modifying it
    output_file = RAW_DIR / "vix_raw.csv"
    output_file.write_bytes(response.content)

    # Inspect the saved data
    data = pd.read_csv(output_file)

    print("VIX download successful!")
    print(f"Total rows: {len(data)}")
    print(f"Saved to: {output_file}")
    print("\nFirst five rows:")
    print(data.head())

except (requests.RequestException, ValueError) as error:
    print(f"VIX download failed: {error}")
