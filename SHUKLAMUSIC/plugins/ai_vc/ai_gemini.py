import asyncio

import google.generativeai as genai
from config import GEMINI_API_KEY

# Gemini client configure karo
genai.configure(api_key=GEMINI_API_KEY)

# Fast + cheap model
_MODEL = genai.GenerativeModel("gemini-1.5-flash")


async def ask_gemini(prompt: str) -> str:
    """
    Prompt ko Gemini ko bhejta hai aur reply return karta hai.
    Blocking call ko thread me chala rahe hain taki bot lag na kare.
    """
    loop = asyncio.get_event_loop()

    def _call():
        response = _MODEL.generate_content(prompt)
        # .text normally main answer hota hai
        return getattr(response, "text", str(response))

    return await loop.run_in_executor(None, _call)
