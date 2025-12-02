from pyrogram import filters
from pyrogram.types import Message
from pytgcalls import StreamType
from pytgcalls.types.input_stream import AudioPiped
from pytgcalls.types.input_stream.quality import HighQualityAudio

from SHUKLAMUSIC import app
from SHUKLAMUSIC.core.call import SHUKLA
from SHUKLAMUSIC.utils.database import group_assistant
from config import BANNED_USERS

from SHUKLAMUSIC.plugins.ai_vc.ai_gemini import ask_gemini
from SHUKLAMUSIC.plugins.ai_vc.tts_engine import synthesize_speech

# Yaad rakhe ki kis chat me AI VC ON hai
AI_VC_CHATS = set()


@app.on_message(filters.command("vcai") & filters.group & ~BANNED_USERS)
async def vcai_toggle(client, message: Message):
    """
    /vcai on  → bot VC join karke AI VC mode ON
    /vcai off → AI VC band + stream stop
    """
    if len(message.command) < 2:
        return await message.reply_text(
            "Usage:\n`/vcai on` – AI VC chalu\n`/vcai off` – AI VC band",
            quote=True,
        )

    mode = message.command[1].lower()
    chat_id = message.chat.id

    assistant = await group_assistant(SHUKLA, chat_id)

    if mode == "on":
        try:
            # assets me call.mp3 already hai, usko base stream bana dete hain
            source = "SHUKLAMUSIC/assets/call.mp3"
            await assistant.join_group_call(
                chat_id,
                AudioPiped(source, audio_parameters=HighQualityAudio()),
                stream_type=StreamType().pulse_stream,
            )
        except Exception:
            # agar already joined hai to ignore
            pass

        AI_VC_CHATS.add(chat_id)
        return await message.reply_text(
            "✅ **AI VC ON.**\nAb `/vcask <text>` likho, jawab VC pe voice me aayega.",
            quote=True,
        )

    if mode == "off":
        AI_VC_CHATS.discard(chat_id)
        try:
            await SHUKLA.stop_stream(chat_id)
        except Exception:
            pass
        return await message.reply_text("🛑 **AI VC OFF.**", quote=True)

    return await message.reply_text(
        "Usage:\n`/vcai on` – AI VC chalu\n`/vcai off` – AI VC band",
        quote=True,
    )


@app.on_message(filters.command(["vcask", "vcsay"]) & filters.group & ~BANNED_USERS)
async def vcai_ask(client, message: Message):
    """
    /vcask <text> – Gemini se sawaal, jawab VC + chat dono me.
    """
    chat_id = message.chat.id

    if chat_id not in AI_VC_CHATS:
        return await message.reply_text(
            "⚠️ Pehle is group me `/vcai on` karo.",
            quote=True,
        )

    # Prompt text nikaalo
    if len(message.command) > 1:
        prompt = message.text.split(maxsplit=1)[1]
    elif message.reply_to_message and (
        message.reply_to_message.text or message.reply_to_message.caption
    ):
        prompt = message.reply_to_message.text or message.reply_to_message.caption
    else:
        return await message.reply_text(
            "Kya puchna hai?\nExample: `/vcask aaj kya scene hai?`",
            quote=True,
        )

    status = await message.reply_text("🤖 Gemini soch raha hai...", quote=True)

    # Gemini se reply
    try:
        answer = await ask_gemini(prompt)
    except Exception as e:
        await status.edit_text(f"❌ Gemini error: `{type(e).__name__}`")
        return

    if not answer:
        await status.edit_text("❌ Gemini ne jawab nahi diya.")
        return

    # Text → audio
    try:
        audio_path = await synthesize_speech(answer, chat_id)
    except Exception as e:
        await status.edit_text(f"❌ TTS error: `{type(e).__name__}`")
        return

    assistant = await group_assistant(SHUKLA, chat_id)

    # VC me play karo
    try:
        await assistant.change_stream(
            chat_id,
            AudioPiped(audio_path, audio_parameters=HighQualityAudio()),
        )
    except Exception:
        # agar VC disconnect ho gaya ho to dobara join karo
        try:
            await assistant.join_group_call(
                chat_id,
                AudioPiped(audio_path, audio_parameters=HighQualityAudio()),
                stream_type=StreamType().pulse_stream,
            )
        except Exception as e:
            await status.edit_text(f"❌ VC stream error: `{type(e).__name__}`")
            return

    await status.edit_text("✅ Gemini ka jawab VC pe play ho raha hai.")
    await message.reply_text(
        f"**Q:** {prompt}\n\n**Gemini:** {answer}",
        quote=True,
    )
