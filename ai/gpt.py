import openai
from utilities.enums.model_types_enum import Model_Types

def send_query(query, model=Model_Types.gpt35turbo.value):
    """
    sends the requested query to OpenAI's GPT Client. This uses the ChatCompletion model
    """
    completion = openai.ChatCompletion.create(model = model,
                                              messages = [{"role": "user", "content": query}])
    unwrapped = unwrap_response(completion)
    return unwrapped

def unwrap_response(res, index=0):
    """
    Attempts to return the `message.content` of a GPT ChatCompletion response at the given index.
    """
    try:
        return res.choices[index].message.content
    except Exception as e:
        print(f"""Could not unwrap the response from GPT, see full error:
              {e}""")