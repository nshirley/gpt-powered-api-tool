from connectors.api_octopi_connector import Octopi_API_Connector
import json

def build_client_query(user_query):
    query_object = {
        "user_input": user_query,
        "api_reference": None
    }
    connector = Octopi_API_Connector()
    query_object["api_reference"] = get_connector_data(connector)   

    logical_query = """
Conforming to the Rules and sub-set of rules above, and the API's I currently support, please respond with as much data as you can in the outlined response JSON object.

If it appears I have missed something, or the instructions are unclear simply state so in the error
The following is the Users Query: """

    rules = """I have a set of rules that I would like you to follow for this interaction:
    1. All responses you give back must contain ONLY a JSON object in the following format: 
        {route: 'string or null', payload: 'string or null', suggested_api: 'string or null', message: 'list of strings' errors: ['list of strings']}
    2. The route property of your response can be null, but should contain an appropriate API route closest to meeting the uesrs query
    3. The payload property of your response can be null, but should contain a minimum of an example payload for the provided route
        a. If possible, please populate appropriate values in the payload based on the Users Query
        b. If there is not enough information in the Users Query to populate the payload fully, please note as such in the errors list
    4. The message property of your response can contain any additional human firendly context, messaging, or items that I explicitly request to be in there. This should ALWAYS be a list and should NEVER contain any potential error messaging
    5. The suggested_api property of your response can be null, it is for indicating which API integration that I support and that you think meets the Users Query.
    6. The error propery of your response can contain anything that I've requested be noted as errors, or that does not fit into any of the above, this should also ALWAYS be a list
    """

## TODO: Make it so that we make two GPT calls. First is ONLY to get a suggestion API integration
##       second is to then provide the users query, the API documentation (in this case just a message that it's Octopi)
##       and ask back the specific payload and route. which is then piped into the connector to make the query. 
##       If successful, then we spit out the response payload to the user. OR we send the payload to GPT and ask
##       it to make a friendly message of what happened. 

    support_rules = """
I also have a sub-set of rules related to this specific query:
    1. I currently support calls to the following APIs [Octopi, ESPN]
    2. If the users request does not appear to be supported by my API integrations, respond with 'not supported' in messages
    3. If the users request does appear to be suported by my API integrations, respond only with the name of the api as noted in rule 1 for the suggested_api property
"""

    api_reference = """
Additionally, here are the API references I currently have"""

    gpt_query = rules + support_rules + logical_query + user_query
                # get_response_type_query("message-only") + \

    return gpt_query

def parse_and_validate_response(res):
    try:
        if res["route"] is not None and res["payload"] is not None:
            return res
    except Exception as e:
        print(f"I'm sorry, the response I got back from GPT was not JSON. Here is the full response: \n\n{res}")

def get_connector_data(api_connector):
    return api_connector.get_docs()

def get_response_type_query(response_type):
    if response_type == "message-only":
        return "Please format your response into the message property only."
    else:
        raise Exception('Invalid response type requested')