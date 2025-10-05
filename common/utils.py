"""Common utility functions"""

def print_message(role, content):
    """Pretty print a message"""
    print(f"\n{'='*50}")
    print(f"{role.upper()}")
    print(f"{'='*50}")
    print(content)
    print()

def format_messages(conversation_history):
    """Format conversation history for Claude API"""
    return [
        {"role": msg["role"], "content": msg["content"]}
        for msg in conversation_history
    ]
