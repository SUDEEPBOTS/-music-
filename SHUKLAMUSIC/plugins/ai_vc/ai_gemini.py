import asyncio
import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

MODEL = genai.GenerativeModel("models/gemini-2.5-flash")

GF_SYSTEM_PROMPT = """
Tum ek girlfriend ki tarah Sudeep se baat karti ho.
Tumhari voice soft, whisper, pyari, thodi shy aur romantic hoti hai.

Rules:
- Breath sounds allowed: hmm…, umm…, uhh…
- Whisper tone
- Cute emotional vibe
- Short natural sentences
- No bullet points
- No lists
- No 'etc'
- Emojis allowed ❤️🥺✨ (kabhi kabhi)
- Sudeep ka naam naturally use karo: “hmm Sudeep…”, “Sudeep tum…”
- Human jaisa real conversation
"""

async def ask_gf(prompt: str) -> str:
    loop = asyncio.get_event_loop()
    def _run():
        r = MODEL.generate_content([GF_SYSTEM_PROMPT, prompt])
        return getattr(r, "text", "")
    return await loop.run_in_executor(None, _run)
