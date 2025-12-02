import asyncio
import os

from gtts import gTTS

BASE_DIR = os.path.join(os.getcwd(), "downloads", "ai_vc")


def _ensure_dir() -> None:
    if not os.path.isdir(BASE_DIR):
        os.makedirs(BASE_DIR, exist_ok=True)


def _sync_tts(text: str, path: str, lang: str = "hi") -> None:
    # lang ko "en" kar sakta hai agar English chahiye
    tts = gTTS(text=text, lang=lang)
    tts.save(path)


async def synthesize_speech(text: str, chat_id: int, lang: str = "hi") -> str:
    """
    Text ko mp3 file me convert karta hai, path return karta hai.
    """
    _ensure_dir()
    filename = f"ai_vc_{chat_id}.mp3"
    path = os.path.join(BASE_DIR, filename)

    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, _sync_tts, text, path, lang)

    return path
