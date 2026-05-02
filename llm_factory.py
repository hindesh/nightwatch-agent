import os
from llm_providers.openai_provider import OpenAICompatibleProvider
from llm_providers.anthropic_provider import AnthropicProvider
from llm_providers.gemini_provider import GeminiProvider
from llm_providers.custom_provider import CustomLLMProvider
from mock_llm import MockLLM

# This factory just grabs the right class based on your env vars.
def get_llm():
    provider = os.environ.get("LLM_PROVIDER", "mock").lower()
    
    # Common config
    model = os.environ.get("LLM_MODEL")
    api_key = os.environ.get("LLM_API_KEY")
    base_url = os.environ.get("LLM_BASE_URL")

    if provider == "mock":
        return MockLLM()
    
    if provider == "openai":
        return OpenAICompatibleProvider(model=model, api_key=api_key, base_url=base_url)
    
    if provider == "anthropic":
        return AnthropicProvider(model=model, api_key=api_key)

    if provider == "gemini":
        return GeminiProvider(model=model, api_key=api_key)

    if provider == "custom":
        return CustomLLMProvider(model=model, api_key=api_key)
    
    # Groq uses the OpenAI SDK, just different base URL
    if provider == "groq":
        return OpenAICompatibleProvider(
            model=model or "llama-3.1-8b-instant", 
            api_key=api_key or os.environ.get("GROQ_API_KEY"),
            base_url="https://api.groq.com/openai/v1"
        )
    
    # Local Ollama setup
    if provider == "ollama":
        return OpenAICompatibleProvider(
            model=model or "llama3",
            api_key="ollama", # dummy key
            base_url=base_url or "http://localhost:11434/v1"
        )

    raise ValueError(f"Unknown provider '{provider}'. Check your LLM_PROVIDER env var.")
