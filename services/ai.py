import logging
import os
from typing import Optional

from openai import OpenAI

logger = logging.getLogger(__name__)

_api_key = os.getenv("OPENAI_API_KEY")
client: Optional[OpenAI] = None
if _api_key:
    client = OpenAI(api_key=_api_key)
else:
    logger.warning("OPENAI_API_KEY is not set; using fallback AI response.")

def generate_post(prompt: str) -> str:
    prompt = prompt.strip()
    if len(prompt) > 100:
        return "Prompt is too long. Please limit to 100 characters."
    if not prompt:
        prompt = "Write a short, odd social media post to confuse me and make me laugh."

    if client is None:
        return "AI post generation is unavailable. Please configure OPENAI_API_KEY."

    try:
        response = client.responses.create(
            model="gpt-4o-mini",
            input=prompt,
            max_output_tokens=300,
        )
        return response.output[0].content[0].text.strip()
    except Exception:
        logger.exception("generate_post failed")
        return "Sorry, couldn’t generate that right now."
