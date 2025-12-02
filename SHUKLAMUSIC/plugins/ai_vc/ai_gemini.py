import asyncio
import google.generativeai as genai
from config import GEMINI_API_KEY

# Gemini client config
genai.configure(api_key=GEMINI_API_KEY)

# Correct working model from your API list
MODEL_NAME = "models/gemini-2.5-flash"

_MODEL = genai.GenerativeModel(MODEL_NAME)

async def ask_gemini(prompt: str) -> str:
    """
    Prompt ko Gemini ko bhejta hai aur text reply return karta hai.
    Blocking call ko background thread me chala rahe hain.
    """

    loop = asyncio.get_event_loop()

    def _call():
        try:
            response = _MODEL.generate_content(prompt)
            return getattr(response, "text", str(response))
        except Exception as e:
            return f"Gemini Error: {e}"

    return await loop.run_in_executor(None, _call)
