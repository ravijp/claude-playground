import sys
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
    """Run the agent with a given task"""
    
    client = ClaudeClient()
    messages = [{"role": "user", "content": task}]
    
    print(f"\n🤖 Agent Task: {task}\n")
    print("="*60)
    
    for iteration in range(max_iterations):
        print(f"\n--- Iteration {iteration + 1} ---\n")
        
        response = client.send_message(messages, tools=TOOLS)
        
        if response.stop_reason == "end_turn":
            # Agent is done
            final_text = next(
                (block.text for block in response.content if hasattr(block, "text")),
                ""
            )
            print(f"\n✅ Agent Complete!\n")
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
                    print(f"   Result: {result}\n")
                    
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": str(result)
                    })
            
            messages.append({"role": "user", "content": tool_results})

def main():
    """Run example agent tasks"""
    
    tasks = [
        "Search for the latest Python version and calculate 2024 - 1991 to find how old Python is.",
        "Find information about Claude AI and calculate how many days are in 3 years."
    ]
    
    for task in tasks:
        run_agent(task)
        print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    main()
