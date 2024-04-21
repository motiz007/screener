import talib
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

end_date = datetime.now().date()
start_date = end_date - timedelta(days=5)
intervals = ["15m", "1h", "90m", "1d"]
pair_stats = {}

for timeframe in intervals:
    data = yf.download("EURUSD=X", start=start_date, end=end_date, interval=timeframe)

    engulfing = talib.CDLENGULFING(data['Open'], data['High'], data['Low'], data['Close'])

    data['Engulfing'] = engulfing

    engulfing_days = data[data['Engulfing'] != 0]
    pair_stats[timeframe] = engulfing_days

    #print(f"Timeframe: {timeframe}")
    #print(engulfing_days[['Engulfing']])

for key, value in pair_stats.items():
    print(f"{key}:")
    print(value[['Engulfing']])