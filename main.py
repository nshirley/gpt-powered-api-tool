from dotenv import load_dotenv
from query_builder import build_client_query, parse_and_validate_response
from ai.gpt.queries import send_query

load_dotenv()

# text = "I need to start a print of cat.gcode" #input("Hello, how can I help you today?")
text = 'The printer responded with the following json, can you explain what happened with a human readable description?'
print(f"Starting app with prompt \"{text}\"")

query = build_client_query(text)

res = send_query(query)

print(res)
# parsed = parse_and_validate_response(res)