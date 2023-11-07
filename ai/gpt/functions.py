from utilities.decorators import gpt_function
from utilities.helpers import get_property

# Actual functions to do things
@gpt_function(
        description="Used to send any command or payload to Octopi enabled 3D Printer",
        parameters={
            "type": "object",
            "properties": {
                "route": {

                },
                "payload": {

                },
                "method": {

                }
            }
        })
def send_printer_command(args):
    ## this uses the wrapper to build the 'function' for GPT but then this also does the actual work
    print('Successfully called!')
    pass

@gpt_function(
        description="General handler for an Octopi 3D Printer API Responses",
        parameters={
            "type": "object",
            "properties": {
                "description": {
                    #TODO: fill in
                },
                "errors": {

                }
            }
        })
def handle_printer_response(args):
    description = get_property(args, ['description'])
    print(description)