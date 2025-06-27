from abc import ABC, abstractmethod
import openai
import anthropic
import os
import requests

# Strategy Interface
class LLMStrategy(ABC):
    @abstractmethod
    def get_response(self, query: str) -> str:
        pass

# OpenAI Strategy
class OpenAIStrategy(LLMStrategy):
    def get_response(self, query: str) -> str:
        response = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY")).chat.completions.create(
            model="gpt-3.5-turbo",  # or "gpt-4"
            messages=[
                {"role": "user", "content": query}
            ]
        )
        return response.choices[0].message.content.strip()
    
class AnthropicStrategy(LLMStrategy):
    def __init__(self):
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        self.api_url = "https://api.anthropic.com/v1/messages"
        self.api_version = "2023-06-01"

    def get_response(self, query: str) -> str:
        try:
            headers = {
                "x-api-key": self.api_key,
                "anthropic-version": self.api_version,
                "content-type": "application/json",
            }
            payload = {
                "model": "claude-3-5-sonnet-20241022",  # Replace with the correct model name
                "max_tokens": 1024,
                "messages": [
                    {"role": "user", "content": query}
                ]
            }
            response = requests.post(self.api_url, headers=headers, json=payload)
            response.raise_for_status()  # Raise an exception for HTTP errors
            response_data = response.json()
            print(f"Anthropic API Response: {response_data}")  # Debugging output
            
            # Extract the text response from the content field
            content_list = response_data.get("content", [])
            if content_list and isinstance(content_list[0], dict):
                return content_list[0].get("text", "").strip()
            else:
                raise RuntimeError("Invalid response structure: 'content' field is missing or malformed.")
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Error in AnthropicStrategy: {str(e)}")

# Strategy Factory
class LLMStrategyFactory:
    strategies = {
        "openai": OpenAIStrategy(),
        "anthropic": AnthropicStrategy(),
    }

    @staticmethod
    def get_strategy(provider: str) -> LLMStrategy:
        if provider not in LLMStrategyFactory.strategies:
            raise ValueError(f"Unsupported LLM provider: {provider}")
        return LLMStrategyFactory.strategies[provider]
