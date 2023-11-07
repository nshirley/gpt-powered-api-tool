# Overview
Sample project to demonstrate feeding OpenAI a set of API Documentation, LLM queries and then getting back (or even executing) the API Payload best suited to the request.

## Setup
This project uses `pipenv` to manage the virtual environment and dependencies. Make sure to have install [pipenv](https://pipenv.pypa.io/en/latest/) first!

- Install: `pipenv install`
- Activate Shell: `pipenv shell`
- Run a Command: `pipenv run <SCIPRT>`
---

## Examples
This will take the user input, call to GPT to parse it and propose a function call, _make_ the function call, and then handle the response. Future improvements could be to keep a running message history so there is context aware message chains

```
> I need to start a print of cat.gcode
// will suggest that the `send_printer_command` function be called (and result in a call to the api)

> What is the status of my print?
// will suggest that the `printer_status` function be called (maybe?)

> The API responded with the folloing payload, can you describe what this means in human readable description? {some_payload_here}
// will suggest that the `handle_printer_response` function be called (which then parses and presents the human readable description!)
```