import json
def gpt_function(description=""):
    """
    Used to simplify creating function definitions for GPT resopnses. This sets the name property for GPT to the name of your function

    Description is optional, but useful to include for code and usage alike.
    """
    def decorator(func: dict):
        def wrapper(*args, **kwargs):
            func_result = func(*args, **kwargs)
            name = func.__name__
            result = {"name": name, "description": description, **func_result}
            print(result)
            return result
        return wrapper
    return decorator

@gpt_function(description="Used to suggest which compatable API to connect to for the Users Query")
def suggest_api():
    return {
        "parameters": {
            "api": {
                "type": "string", "enum": ["octopi", "espn"] # could be dynamically built based on connectors, read dir and build this list
            }
        }
    }

@gpt_function(description="Used to suggest the route, payload, and other details of a specific API endpoint to query based on the Users Query")
def suggest_route(): 
    return {
        "parameters": {
            "route": {"type": "string", },
            "payload": {},

        }
    }



def get_functions():
    return [suggest_api(), suggest_route()]

func_list = get_functions()
print(json.dumps(func_list))