"""
LLM Configuration
"""

import litellm

from backend.core.config import settings

# LiteLLM Configuration
litellm.drop_params = True
litellm.set_verbose = False

MODEL = f"openrouter/{settings.LLM_MODEL}"

API_KEY = settings.OPENROUTER_API_KEY

TEMPERATURE = settings.LLM_TEMPERATURE

MAX_TOKENS = settings.LLM_MAX_TOKENS

API_BASE = "https://openrouter.ai/api/v1"