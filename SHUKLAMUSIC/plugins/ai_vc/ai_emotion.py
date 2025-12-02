import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)
MODEL = genai.GenerativeModel("models/gemini-2.5-flash")

async def detect_emotion(text: str) -> str:
    prompt = f"""
    Detect mood in ONE word:
    happy, sad, romantic, cute, angry, impressed, shy, neutral
    Text: "{text}"
    """
    try:
        r = MODEL.generate_content(prompt).text.lower().strip()
        allowed = ["happy","sad","romantic","cute","angry","impressed","shy","neutral"]
        return r if r in allowed else "romantic"
    except:
        return "romantic"
