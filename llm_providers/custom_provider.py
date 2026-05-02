import json
from .base import BaseLLM

# USE THIS to plug in any LLM you want.
# Just implement the get_response method below.
class CustomLLMProvider(BaseLLM):

    def __init__(self, model: str = None, api_key: str = None):
        # 1. Setup your library or client here
        self.model = model
        self.api_key = api_key

    def get_response(self, messages: list) -> dict:
        """
        Add your code to call your private API or custom model.
        
        Args:
            messages: List of [{"role": "user", "content": "..."}, ...]
            
        Returns:
            Must be a dict: 
            {"type": "tool_call", "thought": "...", "tool": "...", "parameters": {...}}
            OR
            {"type": "final_answer", "thought": "...", "answer": "..."}
        """

        # 2. Put your logic here!
        # (Example: call your proprietary API or a local model binary)

        # Placeholder so it doesn't crash if you run it before editing
        print("\n[!] You selected the CUSTOM provider but haven't written the code in 'custom_provider.py' yet.")
        return {
            "type": "final_answer",
            "thought": "Provider not implemented.",
            "answer": "Check custom_provider.py to add your own LLM logic."
        }
