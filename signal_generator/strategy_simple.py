# def generate_trading_signal(name):
#   return "==> generate_trading_signal, " + name

#import necessary modules
# import pandas as pd
import numpy as np
import talib.abstract as ta
# import pandas_ta as pta

def generate_trading_signal(dataframe, *args):


    #set default values for args
    if args:
        time_frame, MACD_period, MACD_fast, MACD_slow, MACD_signal, RSI_time_period, RSI_low, RSI_high, bband_time_period, bband_std = args
    else:
        time_frame = 14
        MACD_period = 12
        MACD_fast = 26
        MACD_slow = 9
        MACD_signal = 9
        RSI_time_period = 14
        RSI_low = 30
        RSI_high = 70
        bband_time_period = 20
        bband_std = 2.0

    #calculate indicators
    dataframe['SMA'] = ta.SMA(dataframe['close'], time_frame)
    dataframe['MACD'], dataframe['MACD_Signal'], dataframe['MACD_Hist'] = ta.MACD(dataframe['close'], MACD_period, MACD_fast, MACD_slow, MACD_signal)
    dataframe['RSI'] = ta.RSI(dataframe['close'], RSI_time_period)
    dataframe['BB_Upper'], dataframe['BB_Middle'], dataframe['BB_Lower'] = ta.BBANDS(dataframe['close'], bband_time_period, bband_std)

    #combile conditions from all indicators to create Bullish, Bearish, Overbought, Oversold signals
    dataframe['Enter_Long'] = np.where((dataframe['SMA'] > dataframe['close']) & (dataframe['MACD'] < dataframe['MACD_Signal']) & (dataframe['RSI'] < RSI_low) & (dataframe['close'] < dataframe['BB_Lower']), 1, 0)
    dataframe['Exit_Long'] = np.where((dataframe['SMA'] < dataframe['close']) & (dataframe['MACD'] > dataframe['MACD_Signal']) & (dataframe['RSI'] > RSI_high) & (dataframe['close'] > dataframe['BB_Upper']), 1, 0)
    dataframe['Enter_Short'] = np.where((dataframe['SMA'] < dataframe['close']) & (dataframe['MACD'] > dataframe['MACD_Signal']) & (dataframe['RSI'] > RSI_high) & (dataframe['close'] > dataframe['BB_Upper']), 1, 0)
    dataframe['Exit_Short'] = np.where((dataframe['SMA'] > dataframe['close']) & (dataframe['MACD'] < dataframe['MACD_Signal']) & (dataframe['RSI'] < RSI_low) & (dataframe['close'] < dataframe['BB_Lower']), 1, 0)

    #return close price and signal columns
#     return dataframe[['close', 'Enter_Long', 'Exit_Long', 'Enter_Short', 'Exit_Short']]
    return dataframe

#Example how to run 'generate_trading_signals' function and default value of 'args'
# dataframe = pd.read_csv('data.csv')
# dataframe = btc_df
# signals = generate_trading_signals(dataframe)
#
# print(signals.head(50))
