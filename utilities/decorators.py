import functools

def gpt_function(description="", parameters={}):
    """
    Used to simplify creating function definitions for GPT resopnses. This sets the name property for GPT to the name of your function

    Description is optional, but useful to include for code and usage alike.
    """
    def decorator(func: dict):
        # This is needed to set some things that don't usually get set on wrapping - it
        # sets the `__wrapped__` att (and others) which allows access to both this func
        # and the wrapped func independently. 
        @functools.wraps(func) 
        def gpt_function_wrapper():
            name = func.__name__
            return {"name": name, "description": description, "parameters": parameters}
        return gpt_function_wrapper
    return decorator