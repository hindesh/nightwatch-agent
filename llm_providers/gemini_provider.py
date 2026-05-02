import os
import json
from .base import BaseLLM
from tools import TOOL_REGISTRY

class GeminiProvider(BaseLLM):
    """
    Native Google Gemini support.
    """

    def __init__(self, model: str = None, api_key: str = None):
        try:
            import google.generativeai as genai
        except ImportError:
            raise ImportError("Run 'pip install google-generativeai' to use Gemini.")

        self.api_key = api_key or os.environ.get("GEMINI_API_KEY") or os.environ.get("LLM_API_KEY")
        if not self.api_key:
            raise ValueError("I need a GEMINI_API_KEY to work.")
            
        genai.configure(api_key=self.api_key)
        self.model_name = model or os.environ.get("LLM_MODEL", "gemini-1.5-flash")
        self.model = genai.GenerativeModel(self.model_name)

    def get_response(self, messages: list) -> dict:
        tools_str = "\n".join([f"- {k}: {v['description']}" for k, v in TOOL_REGISTRY.items()])
        
        # System instructions
        instructions = f"""You are an autonomous system node investigator. 
Use tools to find the root cause of the alert.
Respond ONLY with JSON.

Available Tools:
{tools_str}
"""
        # Convert our history to Gemini's format
        history = []
        for msg in messages[:-1]:
            # Simple role mapping
            role = "user" if msg["role"] in ["user", "tool"] else "model"
            txt = msg["content"]
            if msg["role"] == "tool": txt = f"Tool Result: {txt}"
            history.append({"role": role, "parts": [txt]})

        # Start the chat
        chat = self.model.start_chat(history=history)
        
        # First turn needs the instructions
        last_msg = messages[-1]["content"]
        if not history:
            prompt = f"{instructions}\n\nTask: {last_msg}"
        else:
            prompt = last_msg

        response = chat.send_message(prompt)
        return self.parse_json(response.text)

    def parse_json(self, text: str):
        # Clean markdown code blocks if the LLM adds them
        clean = text.replace("```json", "").replace("```", "").strip()
        try:
            return json.loads(clean)
        except:
            # Last ditch attempt to find the first '{' and last '}'
            start = clean.find("{")
            end = clean.rfind("}")
            return json.loads(clean[start:end+1])
        
