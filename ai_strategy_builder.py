import importlib
import os
from custom_module.trade_strategy_tester import tester

module_host_path = "."
module_tester_path = 'custom_module.trade_strategy_tester.tester'

def generate_strategy(prompt_input,
    prompt_params={}, ai_name='openai', host_path=module_host_path):

    #1 init openai engine
    ai_path = f"custom_module.trade_strategy_tester.ai_engine.{ai_name}"
    ai_engine = importlib.import_module(ai_path)

    #2 enhance prompt with pre-defined structure
    prompt_params['prompt'] = ai_engine.enhance_prompt_trade_strategy(prompt_input)
    # print(prompt_params['prompt'])

    #3 call openai API
    strategy_function_id = ""
    strategy_function_text = ""
    try:
        strategy_function = ai_engine.fetch_prompt(prompt_params)
        # print("id: " + strategy_function.id)
        # print(strategy_function.choices[0].text)

        strategy_function_id = strategy_function.id
        strategy_function_text = strategy_function.choices[0].message.content
    except Exception as e:
        return {
            'id': '',
            'success_status': False,
            'error_message': 'Call OpenAI API failed! Please try again',
            'strategy_function_text': str(e)
        }

    #4 save strategy to file with prompt, response key as file name
    strategy_function_text_full = strategy_function_text + \
        "\n\n\'\'\'\n" + prompt_params['prompt'] + "\n\'\'\'"

    if len(strategy_function_id.strip()) > 0 and len(strategy_function_text.strip()) > 0:
        strategy_path = f"{host_path}/custom_module/trade_strategy_tester/signal_generator/strategy_{strategy_function_id}.py"

        with open(strategy_path, 'w') as f:
            f.write(strategy_function_text_full)

    #5 Run quick test with dummy data, delete if function can't execute
    tester = importlib.import_module(module_tester_path)
    quicktest_result = tester.run_quick_test(strategy_name=strategy_function_id, delete_if_fail=True, host_path=host_path)
    # print(quicktest_result)

    #6 return strategy name (key)
    if bool(quicktest_result):
        # True = not empty => pass quick test
        return {
            'id': strategy_function_id.strip(),
            'success_status': True,
            'error_message': '',
            'strategy_function_text': strategy_function_text.strip()
        }
    else:
        return {
            'id': strategy_function_id.strip(),
            'success_status': False,
            'error_message': 'Quick test fail! Please update prompt and create again',
            'strategy_function_text': strategy_function_text.strip()
        }
