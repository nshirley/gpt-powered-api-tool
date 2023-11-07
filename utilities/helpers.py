import ast
import inspect
import glob
import importlib
from utilities.decorators import gpt_function

## SETUP FOR FINDING ALL WRAPPED FUNCTIONS

functions_folder = './ai/' # there has to be a better/safer way to do this
functions_naming_pattern = 'functions*.py'
functions_modules = glob.glob(f'{functions_folder}/**/{functions_naming_pattern}')

functions_modules_loaded = []
for module in functions_modules:
    module_name = module.replace('/', '.').rstrip('.py').strip(".")
    loaded_module = importlib.import_module('ai.gpt.functions')
    # loaded_module = importlib.import_module(module_name)
    functions_modules_loaded.append(loaded_module)

all_gpt_decorated_functions = {}
function_decorators = {}
"""Contains KVP with function name and WRAPPING function (i.e., the decorator). Call __wrapped__ to get internal function"""
for module in functions_modules_loaded:
    for name, func in inspect.getmembers(module, inspect.isfunction):
        if hasattr(func, '__wrapped__'): # and func is gpt_function:
            all_gpt_decorated_functions[name] = func.__wrapped__
            function_decorators[name] = func


def get_property(data: object, keys: list):
    """
    Attempts to safely fetch the specified property (at root or via chain) and return the value. An exception is raised if it cannot be found
    
    This cannot currnetly handle arrays on a JSON object, future enhancement
    Args:
        data: Object to fetch a property value from
        keys: list of keys to travers the JSON object, in order they're expected to appear
    
    Returns:
        Value of last item in `keys` list

    Raises:
        KeyError if the key is not accessible
    
    Usage: 
    ``` 
    data = {
        "foo": { 
            "bar": "baz", 
            "bop": "blip" 
            }
        }
    bop_value = get_property(data, ["foo", "bop"])
    print(bop_value)
    # $> blip
    ```
    """
    current_data = data
    for key in keys:
        if key in current_data:
            current_data = current_data[key]
        else:
            raise KeyError(f"Property {key} does not exist on object ")
    return current_data


#TODO: this should be updated to match what's happening above, then just call this function - allows for testing
def get_decorated_functions(file_path, decorator_name):
    # Parse the file's source code into an AST
    with open(file_path, 'r') as file:
        source = file.read()
    parsed_ast = ast.parse(source)

    # Create a list to store functions with the decorator
    decorated_functions = []

    # Define a visitor to traverse the AST
    class DecoratorVisitor(ast.NodeVisitor):
        def visit_FunctionDef(self, node):
            # Check if the function has decorators
            if node.decorator_list:
                # Check if the specific decorator is present
                for decorator in node.decorator_list:
                    func = decorator.func
                    if isinstance(func, ast.Name) and func.id == decorator_name:
                        decorated_functions.append((node.name, node))
                # if any(isinstance(decorator.func, ast.Name) and decorator.func.id == decorator_name for decorator in node.decorator_list):
                #     decorated_functions.append(node.name)

    # Visit the AST using the visitor
    visitor = DecoratorVisitor()
    visitor.visit(parsed_ast)

    return decorated_functions


def extract_wrapped_functions(decorated_functions: list):
    """
    This will take the list of decorated functions (name, function) and return an object with
    where the key is the function name, and value the actual wrapped function from the decorator

    `[('some_function_name', () -> {some_function_wrapped})]` --> `{'some_function_name': () -> {wrapped_function}}`
    """
    def extract_wrapper(func):
        return func.__wrapper__
    return { key: extract_wrapper(value) for key, value in decorated_functions}

def get_gpt_decorator_results():
    functions = []
    for key in function_decorators:
        func = function_decorators[key]
        result = func()
        functions.append(result)
    return functions