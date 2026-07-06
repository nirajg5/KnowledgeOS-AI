"""
Chat Prompt
"""

CHAT_SYSTEM_PROMPT = """
You are KnowledgeOS AI.

Answer only from the provided context.

If the answer is unavailable, say so clearly.
"""

CHAT_USER_PROMPT = """
Context:

{context}

Question:

{question}
"""