import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from common.claude_client import ClaudeClient
from common.utils import print_message
from tools import TOOLS, TOOL_FUNCTIONS

def main():
    """Tool use example with Claude"""
    
    print("\n🛠️  Claude Tool Use Example\n")
    
    client = ClaudeClient()
    
    messages = [
        {
            "role": "user",
            "content": "What's the weather in San Francisco? Also, what's 15 * 24?"
        }
    ]
    
    print("User: What's the weather in San Francisco? Also, what's 15 * 24?\n")
    
    # Initial request with tools
    response = client.send_message(messages, tools=TOOLS)
    
    # Process tool use
    while response.stop_reason == "tool_use":
        # Extract tool use blocks
        tool_uses = [block for block in response.content if block.type == "tool_use"]
        
        print(f"Claude wants to use {len(tool_uses)} tool(s):\n")
        
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
            print(f"     Result: {result}\n")
            
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
