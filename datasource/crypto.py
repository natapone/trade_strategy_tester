import ccxt
import pandas as pd

def fetch(symbols, since_dt=None, timeframe='1h', candle_limit=1000):

    # Initialize the exchange
    exchange = ccxt.binance()
    data = {}
    since_ts = exchange.parse8601(since_dt)

    for symbol in symbols:
        # Fetch historical data
        # raw_ohlcv = []
        raw_ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=candle_limit, since=since_ts)

        # Convert the data to pandas dataframes
        df = pd.DataFrame(raw_ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)

        print(f"=={symbol}==")
        print(df.head(3))
        print(df.tail(3))
        data[symbol] = df

    return data
