from backend.core.config import settings

print("=" * 60)
print("LLM Provider :", settings.LLM_PROVIDER)
print("Model        :", settings.LLM_MODEL)
print("API Key      :", settings.OPENROUTER_API_KEY[:10] + "...")
print("=" * 60)