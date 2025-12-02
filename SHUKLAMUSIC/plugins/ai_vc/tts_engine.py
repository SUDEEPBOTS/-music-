import os
import asyncio
from google import genai
from config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

VOICE_DIR = "downloads/ai_vc"
os.makedirs(VOICE_DIR, exist_ok=True)

VOICE_MAP = {
    "romantic": "female-soft",
    "cute": "female-soft",
    "shy": "female-soft",
    "sad": "female-soft",
    "happy": "female-natural",
    "angry": "female-strong",
    "neutral": "female-soft"
}

async def tts_gf_voice(text: str, chat_id: int, emotion="romantic"):
    path = f"{VOICE_DIR}/gf_{chat_id}.mp3"
    voice = VOICE_MAP.get(emotion, "female-soft")

    def _make():
        res = client.models.generate(
            model="models/gemini-2.0-flash-001",
            input=[{
                "role": "user",
                "parts": [{"text": text}]
            }],
            speech_config={
                "voice_config": {"preset_voice": voice}
            }
        )
        with open(path, "wb") as f:
            f.write(res.output_audio)

    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, _make)
    return path
