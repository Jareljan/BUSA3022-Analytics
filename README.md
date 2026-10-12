
# BUSA3022 — Analytics Implementation Plan & Portfolio

## Project Overview

This repository contains the Analytics Implementation Plan and Portfolio for BUSA3022 at Macquarie University.

The project is based on a fictional post-trade analytics team at Really Big Bank. Its purpose is to design and demonstrate a lightweight analytics solution for monitoring market activity and supporting future performance benchmarking.

The project covers three main areas:

1. Data Pipeline Implementation
2. Data Curation and Metric Development
3. Dashboard and Reporting

The solution uses two financial data sources:
- S&P/ASX 200 Index from Yahoo Finance
- CBOE Volatility Index (VIX) from FRED

The scope is limited to a proof of concept rather than a fully deployed production system.

---

## 1. Data Sources

### Yahoo Finance — S&P/ASX 200

- Ticker: `^AXJO`
- Source: https://finance.yahoo.com/
- Access method: Python `yfinance` library
- Frequency: Daily historical observations
- Data: Open, High, Low, Close, Adjusted Close, Volume
- Source timezone: Australia/Sydney

The pipeline retrieves approximately six months of historical market data.

### FRED — VIX

- Series ID: `VIXCLS`
- Source: https://fred.stlouisfed.org/series/VIXCLS
- Access method: FRED CSV download
- Frequency: Daily observations
- Data: Observation date and VIX value

VIX measures expected US equity-market volatility and is used as a financial-market risk indicator.

VIX observation dates refer to US market dates. These should not automatically be treated as equivalent to Sydney trading dates.

---

## 2. Repository Structure

    BUSA3022-Analytics/
    |
    |-- pipeline/
    |   |-- ingest_asx200.py
    |   |-- ingest_vix.py
    |   |-- validate_data.py
    |   |-- validate_vix.py
    |   |-- test_yahoo.py
    |   |-- test_retries.py
    |
    |-- curation/
    |-- dashboard/
    |
    |-- data/
    |   |-- raw/
    |   |-- curated/
    |   |-- quarantine/
    |
    |-- logs/
    |
    |-- requirements.txt
    |-- .gitignore
    |-- README.md

### Folder Descriptions

- `pipeline/`: Python scripts for data ingestion, validation, and testing.
- `curation/`: Data transformation and metric development.
- `dashboard/`: Dashboard code, charts, and visualisations.
- `data/raw/`: Downloaded source data before validation or cleaning.
- `data/curated/`: Validated and standardised CSV files.
- `data/quarantine/`: Flagged records and quality issue explanations.
- `logs/`: Local execution and error logs.

---

## 3. Environment Setup

### Requirements

- Python 3.13 or compatible version
- VS Code or another Python development environment
- Internet connection

### Installation

Clone the repository:

    git clone https://github.com/Jareljan/BUSA3022-Analytics.git

Navigate to the project:

    cd BUSA3022-Analytics

Create a virtual environment:

    python3 -m venv .venv

Activate the environment on macOS:

    source .venv/bin/activate

Install dependencies:

    python -m pip install -r requirements.txt

---

## 4. Running the Data Pipeline

Run the commands below from the main project directory.

### Step 1 — Download ASX 200 Data

    python pipeline/ingest_asx200.py

Output:

    data/raw/asx200_raw.csv

The ingestion script downloads six months of daily S&P/ASX 200 observations using Yahoo Finance.

### Step 2 — Validate ASX 200 Data

    python pipeline/validate_data.py

Outputs:

    data/curated/asx200_curated.csv
    data/quarantine/asx200_quarantine.csv

Validation checks include:
- Missing or invalid closing prices
- Missing or zero-volume observations
- Required column availability

Records with invalid closing prices are excluded from the curated dataset and logged.

Zero-volume observations are flagged and recorded in quarantine. If the closing price is valid, the price observation is retained, while volume is marked as unavailable.

### Step 3 — Download VIX Data

    python pipeline/ingest_vix.py

Output:

    data/raw/vix_raw.csv

The script downloads approximately six months of VIX observations from FRED.

### Step 4 — Validate VIX Data

    python pipeline/validate_vix.py

Outputs:

    data/curated/vix_curated.csv
    data/quarantine/vix_quarantine.csv

Validation checks include:
- Missing or invalid VIX values
- Invalid observation dates
- Duplicate observation dates

Flagged records are retained in quarantine for investigation.

---

## 5. Data Quality and Error Handling

### API Failure Handling

The ASX 200 ingestion script includes:
- A configurable request timeout
- One initial download attempt
- Up to three additional retries
- A two-second delay between retries
- Logging for failed attempts
- Protection against overwriting raw data when the download fails

### Testing Timeout Handling

Run:

    python pipeline/test_retries.py

The test simulates four consecutive API timeouts.

It verifies:
- Four total download attempts
- Three retry delays
- Failure logging
- A final unsuccessful result

The simulation does not make actual failed requests to Yahoo Finance.

### Data Quality Logging

Data quality summaries and ingestion messages are written to:

    logs/pipeline.log

Quarantine CSVs store flagged observations and their issue descriptions.

Records are not silently discarded. Original downloaded files remain separate from the validation outputs.

---

## 6. Proof-of-Concept Results

Initial testing was performed on 10 October 2026.

### ASX 200

- Raw records: 131
- Flagged records: 2
- Invalid closing prices: 0
- Unavailable/zero-volume observations: 2
- Curated price records: 131

### VIX

- Raw records: 130
- Flagged records: 0
- Invalid dates: 0
- Invalid values: 0
- Duplicate dates: 0
- Curated records: 130

### API Timeout Simulation

- Total simulated attempts: 4
- Additional retries: 3
- Test result: Passed

These results describe the initial proof-of-concept run and may change when source data is refreshed.

---

## 7. Shared Data Format

### ASX 200 Curated Data

    date,open,high,low,close,volume

The `date` column represents the Sydney trading date in YYYY-MM-DD format.

### VIX Curated Data

    date,vix

The `date` column represents the FRED VIX observation date in YYYY-MM-DD format.

Both datasets use standardised column names.

Date alignment between Australian and US financial-market observations will be addressed in the Data Curation stage.

---

## 8. Planned Production Architecture

The proposed pipeline consists of:

1. Data Sources — Yahoo Finance and FRED
2. Ingestion Layer — Python data retrieval
3. Raw Storage Layer — Original downloaded datasets
4. Validation Layer — Quality checks and exception logging
5. Curated Storage Layer — Standardised validated datasets
6. Analytics Layer — Calculated market metrics
7. Dashboard Layer — Market trend reporting

The proposed production design includes scheduled ingestion, monitoring, versioned raw snapshots, and documented recovery procedures.

The current proof of concept runs manually and overwrites its latest raw CSV snapshot on successful re-execution. Automatic scheduling and historical snapshot retention have not yet been implemented.

---

## 9. Team Responsibilities

### Part 1 — Data Pipeline

Responsible for:
- Data ingestion
- Raw data storage
- Validation and quarantine
- Failure-handling tests
- Pipeline architecture
- GitHub repository setup

### Part 2 — Data Curation

Responsible for:
- Metric definitions
- Time zone alignment
- Data transformation
- Metric calculation and validation

### Part 3 — Dashboard and Reporting

Responsible for:
- Dashboard wireframe
- Market visualisations
- VIX overlay
- Red/Amber/Green market signals

---

## 10. Current Project Status

Completed:
- Initial Python environment setup
- ASX 200 data ingestion
- VIX data ingestion
- ASX 200 validation
- VIX validation
- Quarantine CSV generation
- Error logging for ASX ingestion
- Simulated timeout retry test

Planned:
- Final architecture diagram
- Scheduled execution design
- Metric development
- Dashboard implementation
- Final report and presentation

---

## 11. Notes

- This repository supports an academic proof of concept.
- Data may be delayed, revised, or incomplete.
- No investment or trading recommendations are provided.
- Validate AI-generated code before accepting it.
- Maintain documentation for reproducibility and team handoff.
- Do not commit passwords, API keys, or local virtual environments.

## References

Federal Reserve Bank of St. Louis. FRED Economic Data.
https://fred.stlouisfed.org/

Yahoo Finance.
https://finance.yahoo.com/

yfinance Python Library.
https://github.com/ranaroussi/yfinance
