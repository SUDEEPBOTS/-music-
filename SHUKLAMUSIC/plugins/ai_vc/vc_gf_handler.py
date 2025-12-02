from pyrogram import filters
from SHUKLAMUSIC import app, call

from SHUKLAMUSIC.plugins.ai_vc.ai_gemini import ask_gf
from SHUKLAMUSIC.plugins.ai_vc.tts_engine import tts_gf_voice
from SHUKLAMUSIC.plugins.ai_vc.ai_emotion import detect_emotion

@app.on_message(filters.command("vcask"))
async def gf_voice_in_vc(client, message):
    if len(message.text.split()) < 2:
        return

    chat_id = message.chat.id
    user_msg = message.text.split(None, 1)[1]

    # detect mood
    mood = await detect_emotion(user_msg)

    # gf-style reply
    reply = await ask_gf(user_msg)

    # convert to whisper romantic voice
    audio = await tts_gf_voice(reply, chat_id, mood)

    await call.one.play(chat_id, audio)
