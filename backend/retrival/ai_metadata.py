"""
AI Metadata Generator
"""

import json

from litellm import completion

from backend.core.llm import MODEL


class AIMetadataGenerator:

    @staticmethod
    def generate(text: str):

        prompt = f"""
You are an enterprise document analyzer.

Analyze the following document.

Return ONLY valid JSON.

Required format:

{{
"title":"",
"summary":"",
"keywords":[],
"category":"",
"language":""
}}

Document:

{text[:12000]}
"""

        response = completion(

            model=MODEL,

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]

        )

        output = response.choices[0].message.content

        return json.loads(output)