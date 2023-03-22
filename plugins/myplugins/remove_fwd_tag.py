import pyrogram
import os
from pyrogram import Client, filters
from pyrogram.types import Message, User


bot = Client(
    "Remove FwdTag",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"]
)

@Client.on_message(filters.media | filters.forwarded & filters.channel & filters.group & filters.incoming)
async def channel_tag(bot, message):
    try:
        chat_id = message.chat.id
        forward_msg = await message.copy(chat_id)
        await message.delete()
    except:
        await message.reply_text("Oops , Recheck My Admin Permissions & Try Again")




# @Client.on_message(filters.group | filters.media )
# async def tag(client, message):
# await message.copy(message.chat.id)



@Client.on_message(filters.group & filters.channel & filters.forwarded)
async def fwdrmv(c, m):
    try:
        if m.media and not (m.video_note or m.sticker):
            await m.copy(m.chat.id, caption = m.caption if m.caption else None)
            await m.delete()
        else:
            await m.copy(m.chat.id)
            
    except FloodWait as e:
        await asyncio.sleep(e.x)


