
import yfinance as yf

# Market index: S&P/ASX 200
ticker = "^AXJO"

print("Connecting to Yahoo Finance...")

# Download five trading days of historical data
data = yf.Ticker(ticker).history(
    period="5d",
    interval="1d",
    auto_adjust=False
)

if data.empty:
    print("No data returned. Check the connection.")
else:
    print("Connection successful!")
    print(f"Rows downloaded: {len(data)}")
    print(data[["Open", "High", "Low", "Close", "Volume"]])
