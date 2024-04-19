import talib
import yfinance as yf
from datetime import datetime, timedelta

end_date = datetime.now().date()
start_date = end_date - timedelta(days=5)

data = yf.download("EURUSD=X", start=start_date, end=end_date, interval="15m")

morning_star = talib.CDLMORNINGSTAR(data['Open'], data['High'], data['Low'], data['Close'])

engulfing = talib.CDLENGULFING(data['Open'], data['High'], data['Low'], data['Close'])

data['Morning Star'] = morning_star
data['Engulfing'] = engulfing

engulfing_days = data[data['Engulfing'] != 0]

print(engulfing_days)