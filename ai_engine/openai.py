<<<<<<< HEAD
def generate_prompt_string(animal):
    pass

def fetch_prompt(prompt_string):
    pass
=======
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
Write python function for trading signal generator name 'generate_trading_signals'
- Import necessary modules before start the function
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
                "\n" + prompt_input.strip() + \
                "\n" + prompt_input_post.strip()

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
>>>>>>> ab088ec (create strategy from prompt)
