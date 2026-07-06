"""
Streaming Chat Test
"""

import requests

BASE_URL = "http://127.0.0.1:8000"

payload = {
  "session_id": "session_001",
  "document_id": "7264efa3-ffa8-4eba-9c66-563cf77c10bf",
  "user_question": "What is the main objective of this document?"
}

response = requests.post(

    f"{BASE_URL}/chat/stream",

    json=payload,

    stream=True

)

print("=" * 60)
print("KnowledgeOS AI")
print("Streaming Chat Test")
print("=" * 60)

for chunk in response.iter_content(
    chunk_size=None,
    decode_unicode=True
):
    if chunk:
        print(chunk, end="", flush=True)

print("\n" + "=" * 60)