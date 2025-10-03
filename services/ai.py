import logging
import os
from openai import OpenAI

logger = logging.getLogger(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
if not client.api_key:
    raise RuntimeError("OPENAI_API_KEY is not set.")

def generate_post(prompt: str) -> str:
    prompt = prompt.strip()
    if len(prompt) > 100:
        return "Prompt is too long. Please limit to 100 characters."
    if not prompt:
        prompt = "Write a short, odd social media post to confuse me and make me laugh."

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
