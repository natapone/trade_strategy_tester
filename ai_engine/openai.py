import openai

default_input = '''
- Select indicators for hourly intraday trading strategy to explain market status for Bear, Bull, Overbought, Oversold, Volatility
- Interpret market status from all indicators above into columns, enter trade only when Volatility is in proper level
- Generate enter long condition, set status = 1
- Generate exit long condition, set status = 1
- Generate enter short condition, set status = 1
- Generate exit short condition, set status = 1
'''

def enhance_prompt_trade_strategy(prompt_input):
    prompt_input_pre  = '''
As python code generator, Write python function
- Start function with 'def generate_trading_signal(dataframe):' for trading signal generator
- import numpy as np, import talib.abstract as ta, import pandas as pd
- Take input as 'dataframe' with colums: 'high', 'low', 'open', 'close'
- Start function with 'def generate_trading_signal(dataframe):'
'''

    prompt_input_post = '''
- ensure to use column name 'enter_long' for entering long condition
- ensure to use column name 'exit_long' for exiting long condition
- ensure to use column name 'enter_short' for enter short condition
- ensure to use column name 'exit_short' for exit short condition
- End function with 'return dataframe'
'''

    if len(prompt_input.strip()) == 0:
        prompt_input = default_input

    prompt_input = prompt_input_pre.strip() + \
                "\n\n" + "Use trade strategy as below\n" + prompt_input.strip() + \
                "\n\n" + "Close function with\n" + prompt_input_post.strip()

    return prompt_input

def enhance_prompt_interpret_test_result(prompt_input):
    prompt_input_pre  = '''
As non-technical person interpret strategy testing result of t-test with the null hypothesis being that the expected mean return is zero. as the rules below
- The result contain: 'symbol returns', 't_stat', 'p_value'
- Use default p_value level = 0.06
- 'All_Symbols' is aggregated returns from all test data and run t-test together

Interpret result following steps below
- p_value > default level, mean returns is not significant from 0, suggest the strategy return random result
- p_value < default, mean returns is significant from 0, need to check t-test as below
- p_value < default and t-test > 0, mean returns is significant above 0, this could be profitable strategy
- p_value < default and t-test < 0, mean returns is significant below 0, this could be lost strategy

List of t-test results
'''

    prompt_input = prompt_input_pre + prompt_input

    return prompt_input

def fetch_prompt(prompt_params):
    # init key
    openai.api_key = prompt_params.get('api_key','')

    response = openai.Completion.create(
        model = prompt_params.get('model','text-davinci-003'),
        prompt = prompt_params.get('prompt',''),
        temperature = prompt_params.get('temperature',0.7),
        max_tokens = prompt_params.get('max_tokens',2500),
        top_p = 1,
        frequency_penalty = 0,
        presence_penalty = 0
    )

    # print(response)
    return response



# - Generate Enter long condition, set field 'sig_enter_long' = 1
# - Generate Exit long condition, set field 'sig_exit_long' = 1
# - Generate Enter short condition, set field 'sig_enter_short' = 1
# - Generate Exit short condition, set field 'sig_exit_short' = 1
# - Return dataframe
