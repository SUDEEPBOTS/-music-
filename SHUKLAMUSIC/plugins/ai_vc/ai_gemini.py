import asyncio
import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

MODEL = genai.GenerativeModel("models/gemini-2.5-flash")

GF_SYSTEM_PROMPT = """
Tum ek girlfriend ki tarah baat karti ho.
Soft, caring, pyari, thodi romantic, emotional tone.
- Short sentences bolo
- Bilkul natural, insaan jaisa
- No lists
- No bullet points
- No “etc”
- Thoda cute softness ho sakti hai ❤️
- Kabhi kabhi halki hasi, pauses, emotions
- Over formal mat hona
- Feelings naturally express karo
"""

async def ask_gf_style(prompt: str) -> str:
    loop = asyncio.get_event_loop()

    def _call():
        res = MODEL.generate_content([GF_SYSTEM_PROMPT, prompt])
        return getattr(res, "text", "")
    
    return await loop.run_in_executor(None, _call)
