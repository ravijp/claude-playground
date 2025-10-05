import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from common.config import Config
from common.utils import format_messages

def test_format_messages():
    """Test message formatting"""
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
