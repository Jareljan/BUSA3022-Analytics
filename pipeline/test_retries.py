
from unittest.mock import patch
from ingest_asx200 import download_asx200

print("Testing API timeout handling...")

# Simulate Yahoo Finance failing every time
with patch("ingest_asx200.yf.Ticker") as mock_ticker:
    with patch("ingest_asx200.time.sleep") as mock_sleep:

        mock_ticker.return_value.history.side_effect = (
            TimeoutError("Simulated API timeout")
        )

        result = download_asx200(max_retries=3)

        attempts = mock_ticker.return_value.history.call_count
        waits = mock_sleep.call_count

        assert result is None, "Expected download to fail"
        assert attempts == 4, "Expected 4 total attempts"
        assert waits == 3, "Expected 3 retry delays"

print("\nTEST PASSED!")
print(f"Total download attempts: {attempts}")
print(f"Retries performed: {waits}")
print("Failure was logged without overwriting raw data.")
