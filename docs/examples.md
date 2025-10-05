# Examples

## Basic Chat

```python
from common.claude_client import ClaudeClient

client = ClaudeClient()
messages = [{"role": "user", "content": "Hello!"}]
response = client.send_message(messages)
print(response.content[0].text)
```

## With System Prompt

```python
system = "You are a helpful Python coding assistant."
response = client.send_message(messages, system=system)
```

## With Tools

```python
tools = [
    {
        "name": "get_time",
        "description": "Get current time",
        "input_schema": {
            "type": "object",
            "properties": {}
        }
    }
]

response = client.send_message(messages, tools=tools)
```

## Streaming

```python
with client.send_message(messages, stream=True) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```
