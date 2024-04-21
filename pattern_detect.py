import talib
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

try:
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=5)
    intervals = ["15m", "1h", "1d"]
    currency_pairs = ["EURUSD=X", "GBPUSD=X", "USDJPY=X"]  # Add more currency pairs as needed
    pair_stats = {}

    for pair in currency_pairs:
        pair_data = {}
        
        for timeframe in intervals:
            data = yf.download(pair, start=start_date, end=end_date, interval=timeframe)

            if len(data) < 2:  # Ensure there's enough data to compute engulfing patterns
                print(f"Not enough data for {pair} - {timeframe} interval.")
                continue

            engulfing = talib.CDLENGULFING(data['Open'], data['High'], data['Low'], data['Close'])

            data['Engulfing'] = engulfing

            engulfing_days = data[data['Engulfing'] != 0]
            pair_data[timeframe] = engulfing_days
        
        pair_stats[pair] = pair_data

    for pair, data in pair_stats.items():
        print(f"Pair: {pair}")
        for key, value in data.items():
            print(f"{key}:")
            print(value[['Engulfing']])
            print("-------")

except Exception as e:
    print(f"An error occurred: {e}")