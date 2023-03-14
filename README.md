# Trade strategy tester
Quick test trading strategy

## T-test
Use t-test to determine strategy profit by comparing with zero return

Ref: https://www.investopedia.com/terms/t/t-test.asp

A t-test is an inferential statistic used to determine if there is a significant difference between the means of two groups and how they are related. In this case, returns from strategy should be significantly difference from random returns (assume mean = 0).

- T-score or t-value: is distance from mean
- P-value: indicate confident level to reject null hypothesis (lower than limit => significantly different)

### Run T-test
from custom_module.trade_strategy_tester import tester
symbols = ['BTC/USDT', 'ETH/USDT']

strategy_test_results = tester.run_test(symbols)

# symbols = ['BTC/USDT', 'ETH/USDT', 'BNB/USDT', 'XRP/USDT', 'ADA/USDT', 'MATIC/USDT', 'DOGE/USDT']
# since_dt = '2023-01-10 00:00:00'
# timeframe='5m'
# strategy_test_results = tester.run_test(symbols,since_dt=since_dt,timeframe=timeframe)

# strategy_name = 'simple'
# strategy_test_results = tester.run_test(symbols, strategy_name=strategy_name)

tester.print_test_result(strategy_test_results)
