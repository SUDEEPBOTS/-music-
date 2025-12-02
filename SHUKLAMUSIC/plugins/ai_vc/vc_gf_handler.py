from pyrogram import filters
from SHUKLAMUSIC import app
from SHUKLAMUSIC.core.call import SHUKLA

# Correct imports
from SHUKLAMUSIC.plugins.ai_vc.ai_gemini import ask_gemini
from SHUKLAMUSIC.plugins.ai_vc.tts_engine import tts_gf_voice
from SHUKLAMUSIC.plugins.ai_vc.ai_emotion import detect_emotion


@app.on_message(filters.command("vcask"))
async def gf_voice_in_vc(client, message):
    if len(message.text.split()) < 2:
        return await message.reply_text("Kya puchna hai baby? 😌❤️")

    chat_id = message.chat.id
    user_msg = message.text.split(None, 1)[1]

    # 1️⃣ Detect mood / emotion
    mood = await detect_emotion(user_msg)

    # 2️⃣ GF-style Gemini reply
    reply = await ask_gemini(user_msg)

    # 3️⃣ Convert Gemini reply → whisper romantic GF voice
    audio = await tts_gf_voice(reply, chat_id, mood)

    # 4️⃣ Play in VC
    assistant = await SHUKLA.get_assistant(chat_id)
    await assistant.play(
        chat_id, audio
    )

    # Optionally send text reply too
    # await message.reply_text(f"**GF:** {reply}")
