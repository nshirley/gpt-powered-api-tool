from dotenv import load_dotenv
from query_builder import build_client_query, parse_and_validate_response
from ai.gpt import send_query

load_dotenv()

text = input("Hello, how can I help you today?")

query = build_client_query(text)
print(query)

res = send_query(query)
parsed = parse_and_validate_response(res)
print(parsed)