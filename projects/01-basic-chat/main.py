import sys
import os

# Add parent directory to path to import common modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from common.claude_client import ClaudeClient
from common.utils import print_message

def main():
    """Basic chat example with Claude"""
    
    print("\n🤖 Claude Basic Chat Example\n")
    
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
    print("\n--- Multi-turn Conversation ---\n")
    
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
