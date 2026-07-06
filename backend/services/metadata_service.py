"""
Metadata Service

Uses the LLM to generate document metadata.
"""

from backend.prompts.metadata import (
    METADATA_SYSTEM_PROMPT,
    METADATA_USER_PROMPT,
)

from backend.services.llm_service import (
    LLMService
)


class MetadataService:

    @staticmethod
    def generate_metadata(
        document_text: str
    ):

        prompt = METADATA_USER_PROMPT.format(
            document=document_text[:12000]
        )

        response = LLMService.generate_json(

            prompt=prompt,

            system_prompt=METADATA_SYSTEM_PROMPT

        )

        return response