
import yfinance as yf
import logging
import time
from pathlib import Path

# Project configuration
TICKER = "^AXJO"
BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "data" / "raw"
LOG_DIR = BASE_DIR / "logs"

RAW_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "pipeline.log"),
        logging.StreamHandler()
    ]
)

def download_asx200(max_retries=3):
    total_attempts = max_retries + 1

    for attempt in range(1, total_attempts + 1):
        try:
            logging.info(
                f"Downloading ASX 200: attempt "
                f"{attempt}/{total_attempts}"
            )

            data = yf.Ticker(TICKER).history(
                period="6mo",
                interval="1d",
                auto_adjust=False,
                actions=False,
                timeout=10
            )

            if data.empty:
                raise ValueError("No data returned")

            logging.info(
                f"Download successful: {len(data)} rows"
            )

            return data

        except Exception as error:
            logging.warning(
                f"Attempt {attempt} failed: {error}"
            )

            if attempt < total_attempts:
                logging.info("Retrying in 2 seconds...")
                time.sleep(2)

    logging.error(
        "All download attempts failed. "
        "Existing raw data will not be overwritten."
    )

    return None


def main():
    data = download_asx200()

    if data is not None:
        output_file = RAW_DIR / "asx200_raw.csv"

        # Preserve downloaded data without cleaning
        data.to_csv(output_file)

        logging.info(f"Raw data saved to {output_file}")
        print(f"\nTotal rows downloaded: {len(data)}")
        print(data.head())
    else:
        logging.error(
            "Pipeline ingestion skipped because "
            "no new data was available."
        )


if __name__ == "__main__":
    main()

