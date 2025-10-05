import anthropic
from .config import Config

class ClaudeClient:
    """Wrapper for Claude API client with common functionality"""
    
    def __init__(self, model=None, max_tokens=None):
        Config.validate()
        self.client = anthropic.Anthropic(api_key=Config.ANTHROPIC_API_KEY)
        self.model = model or Config.DEFAULT_MODEL
        self.max_tokens = max_tokens or Config.MAX_TOKENS
    
    def send_message(self, messages, system=None, tools=None, stream=False):
        """Send a message to Claude"""
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
        """Simple chat interface"""
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
