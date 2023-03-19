import importlib
import pandas as pd
import os

module_quick_test_data_path = 'custom_module/trade_strategy_tester/quick_test_data'
module_strategy_path = "custom_module.trade_strategy_tester.signal_generator.strategy"

def run_quick_test(strategy_name='example', delete_if_fail=True):
    # load quick test data
    # print(f"Run quick test >> {strategy_name}")
    try:
        data = _load_quick_test_data(module_quick_test_data_path)
        test_result = run_test(strategy_name=strategy_name, quick_test_data=data)
    except:
        # Delete strategy file if try = error
        # print("Strategy error!")
        if delete_if_fail and strategy_name != 'example':
            strategy_path = f"{module_strategy_path}_{strategy_name}"
            strategy_path = strategy_path.replace(".", "/") + ".py"
            # print(f"Delete >> {strategy_path}")

            if os.path.isfile(strategy_path):
                os.remove(strategy_path)

        return {}

    return test_result

def run_test(symbols=None,
    since_dt=None,
    timeframe='1h',
    datasource_name='crypto',
    strategy_name='example',
    test_name='ttest',
    quick_test_data=None):

    datasource_path = f"custom_module.trade_strategy_tester.datasource.{datasource_name}"
    strategy_path = f"{module_strategy_path}_{strategy_name}"
    test_path = f"custom_module.trade_strategy_tester.test_engine.{test_name}"

    signal_generator = importlib.import_module(strategy_path)
    tester = importlib.import_module(test_path)
    datasource = importlib.import_module(datasource_path)

    # Steps

    #1 select set of test data, fetch from source
    data = {}
    if quick_test_data == None:
        data = datasource.fetch(symbols,since_dt=since_dt,timeframe=timeframe)
    else:
        data = quick_test_data
        symbols = quick_test_data.keys()

    #2 generate_trading_signals
    signal_returns = {}
    for symbol in symbols:
        df = data[symbol]
        # print(f"=== Signal {symbol} ===")

        signals = signal_generator.generate_trading_signal(data[symbol])

        #3 Simulate trades, Calculate return
        signal_returns[symbol] = calculate_returns(signals)

    #4 Test for Significance
    all_return = pd.DataFrame()
    strategy_test_results = {}
    for symbol in symbols:

        # signal_returns[symbol].plot.hist(bins=100, alpha=0.5)
        # plot_daily_return(signal_returns[symbol])

        t_stat, p_value = tester.test_result( signal_returns[symbol] )

        if len(all_return.index) == 0:
            all_return = signal_returns[symbol]
        else:
            all_return = pd.concat([all_return, signal_returns[symbol]], ignore_index=True)


        strategy_test_results[symbol] = {
            't_stat': t_stat,
            'p_value': p_value
        }

    t_stat, p_value = tester.test_result(all_return)

    strategy_test_results['All_Symbols'] = {
            't_stat': t_stat,
            'p_value': p_value
        }

    #5 return score
    return strategy_test_results

def calculate_returns(signals):
    signals['ret'] = (signals['close'] - signals['close'].shift(1)) / signals['close'].shift(1) * 100

    # Position
    signals['position'] = 0
    previous_position = 0
    for index, row in signals.iterrows():
#         print(index, ' ===== ', row)

        # Keep position as default
        if previous_position != 0:
            signals.loc[index, 'position'] = previous_position

        # enter long
        if row['enter_long'] == 1:
            signals.loc[index, 'position'] = 1

        # enter short
        if row['enter_short'] == 1:
            signals.loc[index, 'position'] = -1

        # exit long
        if ((row['exit_long'] == 1)
            & (previous_position > 0)):
            signals.loc[index, 'position'] = 0

        # exit short
        if ((row['exit_short'] == 1)
            & (previous_position < 0)):
            signals.loc[index, 'position'] = 0

        # ---
        previous_position = signals.loc[index, 'position']

    # Shift to exacute next candle
    signals['position'] = signals['position'].shift(1)

    # Calculate return
    signals['position_ret'] = signals['position'] * signals['ret']

    # Select only when signel
    idx_signal = signals['position'] != 0
    signal_return = signals.loc[idx_signal, 'position_ret']
    signal_return = signal_return.dropna()

#     print(signal_return.tail(50))

    return signal_return

def plot_daily_return(signal_return):
    daily_returns = signal_return.dropna() / 100
    cumulative_returns = (1 + daily_returns).cumprod() - 1
    cumulative_returns *= 100
    cumulative_returns.sort_index().plot()

def print_test_result(strategy_test_results):

    for symbol in strategy_test_results.keys():
        t_stat = strategy_test_results[symbol]['t_stat']
        p_value = strategy_test_results[symbol]['p_value']

        print(
"""
{} Significant T-Test result comparing to mean return = 0:
t-stat:        {:.3f}
p-value:        {:.6f}
""".format(symbol, t_stat, p_value))

    # Save image
    # ax = s.plot.hist()
    # ax.figure.savefig('demo-file.pdf')
    return None

def _symbol_to_filename(symbol):
    filename = symbol.replace("/", "_")
    return filename

def _filename_to_symbol(filename):
    symbol = filename.replace("_", "/")
    return symbol

def _save_quick_test_data(data):

    if not os.path.exists(module_quick_test_data_path):
       os.makedirs(module_quick_test_data_path)

    for symbol in data.keys():
        filename = _symbol_to_filename(symbol) + ".csv"
        data[symbol].to_csv(f"{test_data_path}/{filename}")

    return test_data_path

def _load_quick_test_data(module_quick_test_data_path):

    # loop read files in folders
    files = {}

    # Iterate directory
    for file in os.listdir(module_quick_test_data_path):

        file_path = os.path.join(module_quick_test_data_path, file)
        symbol = file.split(".")
        symbol = _filename_to_symbol(symbol[0])

        if os.path.isfile(file_path):
            files[symbol] = file_path

#     print(files)
    quick_test_data = {}

#     # Loop read dataframe
    for symbol in files.keys():
        df = pd.read_csv(file_path)
        quick_test_data[symbol] = df

    return quick_test_data
