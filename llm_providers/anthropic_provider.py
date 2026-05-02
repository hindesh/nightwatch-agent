import os
import json
from .base import BaseLLM
from tools import TOOL_REGISTRY

class AnthropicProvider(BaseLLM):
    """
    Claude support.
    """

    def __init__(self, model: str = None, api_key: str = None):
        try:
            from anthropic import Anthropic
        except ImportError:
            raise ImportError("Run 'pip install anthropic' to use Claude.")

        self.api_key = api_key or os.environ.get("LLM_API_KEY")
        self.model = model or os.environ.get("LLM_MODEL", "claude-3-5-sonnet-20240620")
        self.client = Anthropic(api_key=self.api_key)

    def get_response(self, messages: list) -> dict:
        tools_str = "\n".join([f"- {k}: {v['description']}" for k, v in TOOL_REGISTRY.items()])
        
        system_prompt = f"""You are a senior system troubleshooter.
You have tools to investigate nodes and logs.
Call ONE tool at a time and respond with valid JSON.

AVAILABLE TOOLS:
{tools_str}
"""
        # Convert our history for Claude
        # (Claude expects 'tool' results as user messages if not using native tools)
        formatted_msgs = []
        for m in messages:
            if m["role"] == "tool":
                formatted_msgs.append({"role": "user", "content": f"Result from last tool: {m['content']}"})
            else:
                formatted_msgs.append(m)

        # Call the API
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            system=system_prompt,
            messages=formatted_msgs,
            temperature=0
        )

        txt = response.content[0].text
        return self.quick_json_parse(txt)

    def quick_json_parse(self, text):
        # Humans deal with Claude's occasional markdown chatter
        clean = text.strip()
        if "```json" in clean:
            clean = clean.split("```json")[1].split("```")[0].strip()
        elif "```" in clean:
            clean = clean.split("```")[1].split("```")[0].strip()
        return json.loads(clean)
