import os
import json
from .base import BaseLLM
from tools import TOOL_REGISTRY

class OpenAICompatibleProvider(BaseLLM):
    """
    Handles anything that talks like OpenAI (OpenAI, Groq, Ollama).
    """

    def __init__(self, model: str = None, api_key: str = None, base_url: str = None):
        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError("Run 'pip install openai' to use this provider.")

        self.client = OpenAI(
            api_key=api_key or os.environ.get("LLM_API_KEY"), 
            base_url=base_url or os.environ.get("LLM_BASE_URL")
        )
        self.model = model or os.environ.get("LLM_MODEL", "gpt-4o")

    def get_response(self, messages: list) -> dict:
        # Build a list of tools so the LLM knows what it can do
        tools_list = "\n".join([f"- {k}: {v['description']}" for k, v in TOOL_REGISTRY.items()])
        
        system_prompt = f"""You are a senior system investigator. Use the tools below to find the root cause of the user's alert.

RULES:
1. Call exactly ONE tool at a time.
2. Explain your thinking in the 'thought' field.
3. When you're 100% sure, give a final_answer.
4. Respond ONLY with JSON.

AVAILABLE TOOLS:
{tools_list}

JSON FORMATS:
- To call a tool: {{"type": "tool_call", "thought": "why", "tool": "name", "parameters": {{...}}}}
- For final answer: {{"type": "final_answer", "thought": "summary", "answer": "diagnosis"}}
"""
        # OpenAI chat call
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "system", "content": system_prompt}] + messages,
            temperature=0,
            response_format={"type": "json_object"}
        )

        return json.loads(completion.choices[0].message.content)
