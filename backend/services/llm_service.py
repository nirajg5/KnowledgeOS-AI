"""
LLM Service

Centralized LiteLLM Gateway
"""

import json

from litellm import completion

from backend.core.llm import (
    MODEL,
    API_KEY,
    TEMPERATURE,
    MAX_TOKENS
)
from backend.core.llm import (
    MODEL,
    API_KEY,
    API_BASE,
    TEMPERATURE,
    MAX_TOKENS
)

class LLMService:

    @staticmethod
    def generate(
        prompt: str,
        system_prompt: str = "You are a helpful AI assistant."
    ):

       response = completion(
        model=MODEL,
         api_key=API_KEY,
         api_base=API_BASE,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
        messages=[
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": prompt
        }
    ]
)

       return response.choices[0].message.content


    @staticmethod
    def generate_json(
        prompt: str,
        system_prompt: str
    ):

        response = LLMService.generate(
            prompt,
            system_prompt
        )

        try:

            return json.loads(response)

        except Exception:

            return {
                "raw_response": response
            }