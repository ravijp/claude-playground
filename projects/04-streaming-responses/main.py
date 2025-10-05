import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from common.claude_client import ClaudeClient

def main():
    """Streaming response example"""
    
    print("\n📡 Claude Streaming Response Example\n")
    print("="*60)
    
    client = ClaudeClient()
    
    messages = [
        {
            "role": "user",
            "content": "Write a short story about an AI learning to understand human emotions."
        }
    ]
    
    print("\nUser: Write a short story about an AI learning to understand human emotions.\n")
    print("Assistant (streaming):\n")
    
    # Stream the response
    with client.send_message(messages, stream=True) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
    
    print("\n\n" + "="*60)
    print("\n✅ Streaming complete!\n")

if __name__ == "__main__":
    main()
