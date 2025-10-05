"""
Setup script for Claude Playground repository
Run this script to create the complete folder structure and files
"""

import os
import sys

def create_file(path, content):
    """Create a file with given content"""
    dir_path = os.path.dirname(path)
    if dir_path:  # Only create directory if path is not empty
        os.makedirs(dir_path, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✓ Created: {path}")

def create_folder(path):
    """Create a folder"""
    os.makedirs(path, exist_ok=True)
    print(f"✓ Created folder: {path}")

def setup_playground():
    """Create the complete Claude playground structure"""
    
    base_dir = "claude-playground"
    
    print(f"\n🚀 Setting up Claude Playground in '{base_dir}'...\n")
    
    # Create base directory
    create_folder(base_dir)
    os.chdir(base_dir)
    
    # Root .gitignore
    create_file(".gitignore", """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
dist/
*.egg-info/

# Environment variables
.env
*.env

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Jupyter
.ipynb_checkpoints/

# Logs
*.log
""")

    # Root README.md
    create_file("README.md", """# Claude Playground

Experimental projects using Claude SDK for building AI agents and applications.

## Setup

1. Install Python 3.13
2. Create virtual environment:
   ```bash
   python -m venv venv
   venv\\Scripts\\activate  # Windows
   # source venv/bin/activate  # Linux/Mac
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   copy .env.example .env  # Windows
   # cp .env.example .env  # Linux/Mac
   # Edit .env and add your ANTHROPIC_API_KEY
   ```

## Projects

- **01-basic-chat**: Simple Claude chat interface
- **02-tool-use**: Claude with function calling
- **03-agentic-workflow**: Multi-step agent with tools
- **04-streaming-responses**: Real-time streaming responses

## Running a Project

```bash
cd projects/01-basic-chat
python main.py
```

## Documentation

See `docs/` folder for detailed guides and best practices.

## Quick Start

```bash
# Activate virtual environment
venv\\Scripts\\activate

# Run basic chat example
cd projects/01-basic-chat
python main.py
```
""")

    # Root requirements.txt
    create_file("requirements.txt", """anthropic>=0.40.0
python-dotenv>=1.0.0
pydantic>=2.0.0
httpx>=0.25.0
requests>=2.31.0
""")

    # .env.example
    create_file(".env.example", """ANTHROPIC_API_KEY=your_api_key_here
DEFAULT_MODEL=claude-sonnet-4-20250514
MAX_TOKENS=4096
""")

    # Common folder
    create_file("common/__init__.py", """\"\"\"
Common utilities and shared code for Claude playground projects
\"\"\"
from .config import Config
from .claude_client import ClaudeClient

__all__ = ['Config', 'ClaudeClient']
""")

    create_file("common/config.py", """import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    \"\"\"Configuration management for Claude SDK\"\"\"
    
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "claude-sonnet-4-20250514")
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "4096"))
    
    @classmethod
    def validate(cls):
        \"\"\"Validate that required configuration exists\"\"\"
        if not cls.ANTHROPIC_API_KEY:
            raise ValueError(
                "ANTHROPIC_API_KEY not found in environment. "
                "Please create .env file from .env.example"
            )
        return True
""")

    create_file("common/utils.py", """\"\"\"Common utility functions\"\"\"

def print_message(role, content):
    \"\"\"Pretty print a message\"\"\"
    print(f"\\n{'='*50}")
    print(f"{role.upper()}")
    print(f"{'='*50}")
    print(content)
    print()

def format_messages(conversation_history):
    \"\"\"Format conversation history for Claude API\"\"\"
    return [
        {"role": msg["role"], "content": msg["content"]}
        for msg in conversation_history
    ]
""")

    create_file("common/claude_client.py", """import anthropic
from .config import Config

class ClaudeClient:
    \"\"\"Wrapper for Claude API client with common functionality\"\"\"
    
    def __init__(self, model=None, max_tokens=None):
        Config.validate()
        self.client = anthropic.Anthropic(api_key=Config.ANTHROPIC_API_KEY)
        self.model = model or Config.DEFAULT_MODEL
        self.max_tokens = max_tokens or Config.MAX_TOKENS
    
    def send_message(self, messages, system=None, tools=None, stream=False):
        \"\"\"Send a message to Claude\"\"\"
        params = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "messages": messages
        }
        
        if system:
            params["system"] = system
        if tools:
            params["tools"] = tools
        
        if stream:
            return self.client.messages.stream(**params)
        else:
            return self.client.messages.create(**params)
    
    def chat(self, user_message, conversation_history=None, system=None):
        \"\"\"Simple chat interface\"\"\"
        if conversation_history is None:
            conversation_history = []
        
        conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        response = self.send_message(conversation_history, system=system)
        assistant_message = response.content[0].text
        
        conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })
        
        return assistant_message, conversation_history
""")

    # Project 01: Basic Chat
    create_file("projects/01-basic-chat/README.md", """# Project 01: Basic Chat

A simple example of chatting with Claude using the SDK.

## What This Does

- Sends a single message to Claude
- Receives and displays the response
- Shows basic API usage

## Run

```bash
python main.py
```

## Key Concepts

- Creating a Claude client
- Sending messages
- Handling responses
""")

    create_file("projects/01-basic-chat/main.py", """import sys
import os

# Add parent directory to path to import common modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from common.claude_client import ClaudeClient
from common.utils import print_message

def main():
    \"\"\"Basic chat example with Claude\"\"\"
    
    print("\\n🤖 Claude Basic Chat Example\\n")
    
    # Initialize Claude client
    client = ClaudeClient()
    
    # Single message example
    print("Sending message to Claude...")
    
    messages = [
        {"role": "user", "content": "Hello! Explain what agentic AI is in 3 sentences."}
    ]
    
    response = client.send_message(messages)
    
    # Display response
    print_message("Assistant", response.content[0].text)
    
    # Multi-turn conversation example
    print("\\n--- Multi-turn Conversation ---\\n")
    
    conversation_history = []
    
    # First message
    response1, conversation_history = client.chat(
        "What are the key components of an AI agent?",
        conversation_history
    )
    print_message("Assistant", response1)
    
    # Follow-up message
    response2, conversation_history = client.chat(
        "Can you give me an example of each component?",
        conversation_history
    )
    print_message("Assistant", response2)

if __name__ == "__main__":
    main()
""")

    create_file("projects/01-basic-chat/requirements.txt", """# Inherits from root requirements.txt
# Add project-specific dependencies here if needed
""")

    # Project 02: Tool Use
    create_file("projects/02-tool-use/README.md", """# Project 02: Tool Use

Example of Claude using tools (function calling) to perform actions.

## What This Does

- Defines tools that Claude can use
- Claude decides when to use tools
- Handles tool execution and returns results to Claude

## Run

```bash
python main.py
```

## Key Concepts

- Tool definitions
- Tool use detection
- Multi-step reasoning with tools
""")

    create_file("projects/02-tool-use/tools.py", """\"\"\"Tool definitions for Claude\"\"\"

def get_weather(location):
    \"\"\"Simulated weather API\"\"\"
    # In real scenario, call actual weather API
    weather_data = {
        "San Francisco": "Sunny, 72°F",
        "New York": "Cloudy, 65°F",
        "London": "Rainy, 58°F",
        "Tokyo": "Clear, 75°F"
    }
    return weather_data.get(location, f"Weather data not available for {location}")

def calculate(expression):
    \"\"\"Safe calculator\"\"\"
    try:
        # Simple eval for demo - in production use safer alternatives
        result = eval(expression, {"__builtins__": {}}, {})
        return str(result)
    except Exception as e:
        return f"Error calculating: {str(e)}"

# Tool definitions for Claude
TOOLS = [
    {
        "name": "get_weather",
        "description": "Get the current weather for a location",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city name, e.g., San Francisco"
                }
            },
            "required": ["location"]
        }
    },
    {
        "name": "calculate",
        "description": "Perform a mathematical calculation",
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "The mathematical expression to evaluate, e.g., '2 + 2' or '10 * 5'"
                }
            },
            "required": ["expression"]
        }
    }
]

# Map tool names to functions
TOOL_FUNCTIONS = {
    "get_weather": get_weather,
    "calculate": calculate
}
""")

    create_file("projects/02-tool-use/main.py", """import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from common.claude_client import ClaudeClient
from common.utils import print_message
from tools import TOOLS, TOOL_FUNCTIONS

def main():
    \"\"\"Tool use example with Claude\"\"\"
    
    print("\\n🛠️  Claude Tool Use Example\\n")
    
    client = ClaudeClient()
    
    messages = [
        {
            "role": "user",
            "content": "What's the weather in San Francisco? Also, what's 15 * 24?"
        }
    ]
    
    print("User: What's the weather in San Francisco? Also, what's 15 * 24?\\n")
    
    # Initial request with tools
    response = client.send_message(messages, tools=TOOLS)
    
    # Process tool use
    while response.stop_reason == "tool_use":
        # Extract tool use blocks
        tool_uses = [block for block in response.content if block.type == "tool_use"]
        
        print(f"Claude wants to use {len(tool_uses)} tool(s):\\n")
        
        # Add assistant's response to messages
        messages.append({
            "role": "assistant",
            "content": response.content
        })
        
        # Execute tools and collect results
        tool_results = []
        for tool_use in tool_uses:
            tool_name = tool_use.name
            tool_input = tool_use.input
            
            print(f"  📌 Using tool: {tool_name}")
            print(f"     Input: {tool_input}")
            
            # Execute the tool
            result = TOOL_FUNCTIONS[tool_name](**tool_input)
            print(f"     Result: {result}\\n")
            
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": tool_use.id,
                "content": result
            })
        
        # Send tool results back to Claude
        messages.append({
            "role": "user",
            "content": tool_results
        })
        
        # Get Claude's next response
        response = client.send_message(messages, tools=TOOLS)
    
    # Final response
    final_text = next(
        (block.text for block in response.content if hasattr(block, "text")),
        None
    )
    
    if final_text:
        print_message("Final Response", final_text)

if __name__ == "__main__":
    main()
""")

    create_file("projects/02-tool-use/requirements.txt", """# Inherits from root requirements.txt
""")

    # Project 03: Agentic Workflow
    create_file("projects/03-agentic-workflow/README.md", """# Project 03: Agentic Workflow

A more complex agent that can use multiple tools and plan its actions.

## What This Does

- Agent with multiple specialized tools
- Multi-step reasoning and planning
- Error handling and retry logic

## Run

```bash
python agent.py
```

## Key Concepts

- Agent orchestration
- Tool chaining
- State management
""")

    create_file("projects/03-agentic-workflow/agent.py", """import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from common.claude_client import ClaudeClient
from tools.web_search import search_web
from tools.calculator import calculate

TOOLS = [
    {
        "name": "search_web",
        "description": "Search the web for information (simulated)",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "calculate",
        "description": "Perform mathematical calculations",
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "Mathematical expression to evaluate"
                }
            },
            "required": ["expression"]
        }
    }
]

TOOL_MAP = {
    "search_web": search_web,
    "calculate": calculate
}

def run_agent(task, max_iterations=5):
    \"\"\"Run the agent with a given task\"\"\"
    
    client = ClaudeClient()
    messages = [{"role": "user", "content": task}]
    
    print(f"\\n🤖 Agent Task: {task}\\n")
    print("="*60)
    
    for iteration in range(max_iterations):
        print(f"\\n--- Iteration {iteration + 1} ---\\n")
        
        response = client.send_message(messages, tools=TOOLS)
        
        if response.stop_reason == "end_turn":
            # Agent is done
            final_text = next(
                (block.text for block in response.content if hasattr(block, "text")),
                ""
            )
            print(f"\\n✅ Agent Complete!\\n")
            print(f"Result: {final_text}")
            break
        
        if response.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": response.content})
            
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    print(f"🔧 Tool: {block.name}")
                    print(f"   Input: {block.input}")
                    
                    result = TOOL_MAP[block.name](**block.input)
                    print(f"   Result: {result}\\n")
                    
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": str(result)
                    })
            
            messages.append({"role": "user", "content": tool_results})

def main():
    \"\"\"Run example agent tasks\"\"\"
    
    tasks = [
        "Search for the latest Python version and calculate 2024 - 1991 to find how old Python is.",
        "Find information about Claude AI and calculate how many days are in 3 years."
    ]
    
    for task in tasks:
        run_agent(task)
        print("\\n" + "="*60 + "\\n")

if __name__ == "__main__":
    main()
""")

    create_file("projects/03-agentic-workflow/tools/__init__.py", "")

    create_file("projects/03-agentic-workflow/tools/web_search.py", """def search_web(query):
    \"\"\"Simulated web search\"\"\"
    # In production, integrate with real search API
    results = {
        "python version": "Python 3.13 is the latest stable version released in 2024",
        "claude ai": "Claude is an AI assistant created by Anthropic, launched in 2023",
        "latest": "Current year is 2025"
    }
    
    query_lower = query.lower()
    for key, value in results.items():
        if key in query_lower:
            return value
    
    return f"Search results for '{query}': [Simulated results - integrate real API in production]"
""")

    create_file("projects/03-agentic-workflow/tools/calculator.py", """def calculate(expression):
    \"\"\"Safe calculator\"\"\"
    try:
        # Simple eval - use safer alternatives in production
        allowed_names = {
            'abs': abs, 'round': round, 'min': min, 'max': max,
            'sum': sum, 'pow': pow
        }
        result = eval(expression, {"__builtins__": {}}, allowed_names)
        return f"{expression} = {result}"
    except Exception as e:
        return f"Error: {str(e)}"
""")

    create_file("projects/03-agentic-workflow/requirements.txt", """# Inherits from root requirements.txt
""")

    # Project 04: Streaming
    create_file("projects/04-streaming-responses/README.md", """# Project 04: Streaming Responses

Real-time streaming of Claude's responses for better UX.

## What This Does

- Streams responses token by token
- Shows real-time output
- Better user experience for long responses

## Run

```bash
python main.py
```

## Key Concepts

- Streaming API
- Real-time output handling
- Token-by-token processing
""")

    create_file("projects/04-streaming-responses/main.py", """import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from common.claude_client import ClaudeClient

def main():
    \"\"\"Streaming response example\"\"\"
    
    print("\\n📡 Claude Streaming Response Example\\n")
    print("="*60)
    
    client = ClaudeClient()
    
    messages = [
        {
            "role": "user",
            "content": "Write a short story about an AI learning to understand human emotions."
        }
    ]
    
    print("\\nUser: Write a short story about an AI learning to understand human emotions.\\n")
    print("Assistant (streaming):\\n")
    
    # Stream the response
    with client.send_message(messages, stream=True) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
    
    print("\\n\\n" + "="*60)
    print("\\n✅ Streaming complete!\\n")

if __name__ == "__main__":
    main()
""")

    create_file("projects/04-streaming-responses/requirements.txt", """# Inherits from root requirements.txt
""")

    # Tests
    create_file("tests/__init__.py", "")

    create_file("tests/test_common.py", """import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from common.config import Config
from common.utils import format_messages

def test_format_messages():
    \"\"\"Test message formatting\"\"\"
    history = [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there!"}
    ]
    
    formatted = format_messages(history)
    assert len(formatted) == 2
    assert formatted[0]["role"] == "user"
    print("✓ test_format_messages passed")

if __name__ == "__main__":
    test_format_messages()
""")

    # Docs
    create_file("docs/setup.md", """# Setup Guide

## Prerequisites

- Python 3.13
- Anthropic API key ([get one here](https://console.anthropic.com/))

## Installation Steps

1. **Clone the repository**
   ```bash
   cd claude-playground
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   venv\\Scripts\\activate  # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   copy .env.example .env
   ```
   
   Edit `.env` and add your API key:
   ```
   ANTHROPIC_API_KEY=sk-ant-...
   ```

5. **Test installation**
   ```bash
   cd projects/01-basic-chat
   python main.py
   ```

## Troubleshooting

- **ImportError**: Make sure virtual environment is activated
- **API Key Error**: Check that `.env` file exists and has valid key
- **Module not found**: Run `pip install -r requirements.txt`
""")

    create_file("docs/best-practices.md", """# Best Practices

## API Usage

1. **Always use environment variables** for API keys
2. **Implement error handling** for API calls
3. **Use streaming** for long responses
4. **Cache responses** when appropriate

## Code Organization

1. **Separate concerns**: Keep tools, agents, and utilities separate
2. **Reuse common code**: Use the `common/` module
3. **Document your code**: Add docstrings and comments
4. **Test your code**: Write tests for critical functionality

## Security

1. **Never commit `.env`** files
2. **Validate user inputs** before sending to API
3. **Sanitize tool outputs** before displaying
4. **Use rate limiting** in production

## Performance

1. **Use async/await** for concurrent requests
2. **Batch requests** when possible
3. **Stream responses** for better UX
4. **Monitor token usage** to control costs
""")

    create_file("docs/examples.md", """# Examples

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
""")

    # Scripts
    create_file("scripts/setup_env.py", """import os
import shutil

def setup():
    \"\"\"Setup environment file\"\"\"
    if not os.path.exists('.env'):
        shutil.copy('.env.example', '.env')
        print("✓ Created .env file")
        print("⚠️  Please edit .env and add your ANTHROPIC_API_KEY")
    else:
        print("✓ .env already exists")

if __name__ == "__main__":
    setup()
""")

    create_file("scripts/run_project.py", """import sys
import subprocess

def run_project(project_name):
    \"\"\"Run a specific project\"\"\"
    project_path = f"projects/{project_name}"
    
    if not os.path.exists(project_path):
        print(f"❌ Project '{project_name}' not found")
        return
    
    print(f"\\n🚀 Running {project_name}...\\n")
    
    main_file = os.path.join(project_path, "main.py")
    if not os.path.exists(main_file):
        main_file = os.path.join(project_path, "agent.py")
    
    subprocess.run([sys.executable, main_file])

if __name__ == "__main__":
    import os
    
    if len(sys.argv) < 2:
        print("Usage: python run_project.py <project-name>")
        print("\\nAvailable projects:")
        for item in os.listdir("projects"):
            if os.path.isdir(os.path.join("projects", item)):
                print(f"  - {item}")
    else:
        run_project(sys.argv[1])
""")

    # Notebooks folder
    create_folder("notebooks")
    create_file("notebooks/README.md", """# Notebooks

Place your Jupyter notebooks here for experiments and explorations.

## Setup Jupyter

```bash
pip install jupyter
jupyter notebook
```
""")

    print("\n" + "="*60)
    print("✅ Claude Playground setup complete!")
    print("="*60)
    print(f"\nNext steps:")
    print(f"1. cd {base_dir}")
    print(f"2. python -m venv venv")
    print(f"3. venv\\Scripts\\activate")
    print(f"4. pip install -r requirements.txt")
    print(f"5. copy .env.example .env")
    print(f"6. Edit .env and add your ANTHROPIC_API_KEY")
    print(f"7. cd projects/01-basic-chat && python main.py")
    print()

if __name__ == "__main__":
    try:
        setup_playground()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)