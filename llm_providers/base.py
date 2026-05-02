class BaseLLM:
    """Simple interface. Any new provider just needs to implement get_response."""
    def get_response(self, messages: list) -> dict:
        raise NotImplementedError("You forgot to implement get_response!")
