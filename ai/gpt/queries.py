import openai
import json
from utilities.enums.model_types_enum import Model_Types
from utilities.helpers import get_property, get_gpt_decorator_results, all_gpt_decorated_functions

def send_query(query, model=Model_Types.gpt35turbo0613.value):
    """
    sends the requested query to OpenAI's GPT Client. This uses the ChatCompletion model
    """
    functions = get_gpt_decorator_results()
    messages = [{"role": "user", "content": query}]
    completion = openai.ChatCompletion.create(model=model,
                                              messages=messages,
                                              functions=functions)
    unwrapped = unwrap_response(completion)
    function_to_call, arguments = get_function_call(completion.choices[0])
    function_result = function_to_call(arguments)
    print(function_result)
    return unwrapped

def get_function_call(choice: object):
    try:
        function_call = get_property(choice, ["message", "function_call"])
        function_name = get_property(function_call, ["name"])
        arguments = get_property(function_call, ["arguments"])
        arguments = json.loads(arguments)
        # MUST pull the wrapped function out of the wrapper. otherwise we try to call the decorator
        function_to_call = all_gpt_decorated_functions[function_name]

        return (function_to_call, arguments)
    except Exception as e:
        print(f"Failed to get a function_call on the message")

def unwrap_response(res, index=0):
    """
    Attempts to return the `message.content` of a GPT ChatCompletion response at the given index.
    """
    try:
        print(f"******* Full gpt response: {res}")
        return res.choices[index].message.content
    except Exception as e:
        print(f"""Could not unwrap the response from GPT, see full error:
              {e}""")