import talib
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

try:
    end_date = datetime.now()
    start_date = end_date - timedelta(hours=4)
    intervals = ["15m"]
    currency_pairs = ["EURUSD=X", "GBPUSD=X", "EURGBP=X", "EURJPY=X", "AUDCAD=X", "AUDNZD=X", "GBPAUD=X", "CHFJPY=X"]
    candlestick_patterns = ["CDLENGULFING", "CDLHAMMER", "CDLDOJI", "CDLHANGINGMAN"]
    pair_stats = {}

    for pair in currency_pairs:
        pair_data = {}
        
        for timeframe in intervals:
            data = yf.download(pair, start=start_date, end=end_date, interval=timeframe)

            if len(data) < 2:
                print(f"Not enough data for {pair} - {timeframe} interval.")
                continue

            for pattern in candlestick_patterns:
                cdl_func = getattr(talib, pattern)
                data[pattern] = cdl_func(data['Open'], data['High'], data['Low'], data['Close'])
        
            # Create a DataFrame with only the candlestick pattern columns
            patterns_df = data[candlestick_patterns]

            # Filter out rows where all pattern values are 0
            patterns_df = patterns_df[(patterns_df.T != 0).any()]

            if not patterns_df.empty:  # Check if the DataFrame is not empty
                pair_data[timeframe] = patterns_df
        
        if pair_data:  # Check if pair_data dictionary is not empty
            pair_stats[pair] = pair_data

    for pair, data in pair_stats.items():
        print(f"Pair: {pair}")
        for key, value in data.items():
            print(f"{key}:")
            print(value)
            print("-------")

except Exception as e:
    print(f"An error occurred: {e}")