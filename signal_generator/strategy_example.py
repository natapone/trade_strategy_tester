import numpy as np
import talib.abstract as ta

def generate_trading_signal(dataframe):
    #Select indicators
    close = dataframe['close']
    high = dataframe['high']
    low = dataframe['low']
    #Interpret market status from indicators
    dataframe['rsi'] = ta.RSI(close, timeperiod=14)
    dataframe['trix'] = ta.TRIX(close, timeperiod=14)
    dataframe['vol'] = ta.ATR(high, low, close, timeperiod=14) / dataframe['close'] * 100
    dataframe['bullish'] = np.where(dataframe['trix'] > 0, 1, 0)
    dataframe['bearish'] = np.where(dataframe['trix'] < 0, 1, 0)
    dataframe['overbought'] = np.where(dataframe['rsi'] > 70, 1, 0)
    dataframe['oversold'] = np.where(dataframe['rsi'] < 30, 1, 0)
    dataframe['volatility'] = np.where(dataframe['vol'] > 0.015, 1, 0)
    #Generate trading signals
    dataframe['Enter_Long'] = np.where(((dataframe['oversold'] == 1) | (dataframe['bullish'] == 1)) & (dataframe['volatility'] == 1), 1, 0)
    dataframe['Exit_Long'] = np.where((dataframe['overbought'] == 1) | (dataframe['bearish'] == 1), 1, 0)
    dataframe['Enter_Short'] = np.where((dataframe['overbought'] == 1) & (dataframe['bearish'] == 1) & (dataframe['volatility']==1), 1, 0)
    dataframe['Exit_Short'] = np.where((dataframe['oversold'] == 1) | (dataframe['bullish'] == 1), 1, 0)
    #Return dataframe
    return dataframe


# Prompt
# Write python function for trading signal generator name 'generate_trading_signals'
# - Import necessary modules before start the function
# - import numpy as np, import talib.abstract as ta
# - Take input as 'dataframe' of high, low, open, close
# - Start function with 'def generate_trading_signal(dataframe):'
# - Select indicators for hourly intraday trading strategy to explain market status for Bear, Bull, Overbought, Oversold, Volatility
# - Interpret market status from all indicators above into columns, enter trade only when Volatility is in proper level
# - Generate Enter long condition, set field 'sig_enter_long' = 1
# - Generate Exit long condition, set field 'sig_exit_long' = 1
# - Generate Enter short condition, set field 'sig_enter_short' = 1
# - Generate Exit short condition, set field 'sig_exit_short' = 1
# - Return dataframe
