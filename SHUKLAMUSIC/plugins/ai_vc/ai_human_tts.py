import os
import asyncio
from gtts import gTTS
from random import choice

BASE_DIR = os.path.join(os.getcwd(), "downloads", "ai_vc")

breaths = ["hmm…", "umm…", "haa…", "mmh…"]
romantic_add = ["jaan…", "baby…", "Sudeep…", "meri jaan…"]
sad_add = ["😭", "🥺", "thoda rukna…", "uff…"]
angry_add = ["😤", "kya yaar…", "huh…"]
flirty_add = ["😏", "hehe…", "closer aa na…"]

def ensure():
    if not os.path.isdir(BASE_DIR):
        os.makedirs(BASE_DIR, exist_ok=True)

def style_text(text: str, mood: str) -> str:
    """Different mood ke hisab se human-like voice reply generate karta hai"""

    if mood == "romantic":
        return f"{choice(breaths)} {choice(romantic_add)} {text}… hmm…"

    if mood == "sad":
        return f"{choice(breaths)} {choice(sad_add)} {text}… 🥺"

    if mood == "angry":
        return f"{choice(angry_add)} {text}… huh…"

    if mood == "flirty":
        return f"{choice(flirty_add)} {text}… 😉"

    if mood == "shy":
        return f"uhh… {choice(breaths)} {text}…"

    if mood == "jealous":
        return f"hmm… Sudeep… {text}… par tum kiske sath the? 😒"

    return f"{choice(breaths)} {text}"

def sync_tts(t, p):
    tts = gTTS(text=t, lang="hi")
    tts.save(p)

async def human_tts(text: str, chat_id: int, mood: str):
    ensure()
    path = os.path.join(BASE_DIR, f"gf_voice_{chat_id}.mp3")

    clean = style_text(text, mood)

    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, sync_tts, clean, path)

    return path
