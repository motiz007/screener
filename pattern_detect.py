import talib
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

try:
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=2)
    intervals = ["15m", "1h"]
    currency_pairs = ["EURUSD=X", "GBPUSD=X", "USDJPY=X"]
    candlestick_patterns = ["CDLENGULFING", "CDLHAMMER", "CDLDOJI", "CDLHARAMI"]
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

            pair_data[timeframe] = patterns_df
        
        pair_stats[pair] = pair_data

    for pair, data in pair_stats.items():
        print(f"Pair: {pair}")
        for key, value in data.items():
            print(f"{key}:")
            print(value)
            print("-------")

except Exception as e:
    print(f"An error occurred: {e}")