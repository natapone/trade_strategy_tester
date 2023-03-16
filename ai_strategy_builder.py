<<<<<<< HEAD
def generate_strategy(prompt_input):
    pass
=======
import importlib

def generate_strategy(prompt_input,
    prompt_params={}, ai_name='openai'):

    #1 init openai engine
    ai_path = f"custom_module.trade_strategy_tester.ai_engine.{ai_name}"
    ai_engine = importlib.import_module(ai_path)

    #2 enhance prompt with pre-defined structure
    prompt_params['prompt'] = ai_engine.enhance_prompt_trade_strategy(prompt_input)

    #3 call openai API
    ai_engine.fetch_prompt(prompt_params)

    #4 save strategy to file with response key as file name

    #5 return strategy name (key)

    return 1
>>>>>>> ab088ec (create strategy from prompt)
