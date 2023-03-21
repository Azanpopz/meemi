from pyrogram import Client, filters
from config import ADMINS, SOURCE_CODE
from pyrogram.types import Message

from util import main_convertor_handler


import json
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import Client, filters
from util import replace_mdisk_link, caption
from config import ADMINS, SOURCE_CODE
from pyrogram.types import Message
import re
from info import BATCH_GROUP

# Private Chat

@Client.on_message(filters.text & filters.chat(BATCH_GROUP))
async def private_link_handler(c, message):
    if message.from_user.id not in ADMINS:
        return await message.reply_text(f"This bot works only for ADMINS of this bot. Make your own Bot.\n\n[Source Code]({SOURCE_CODE})")
        
    try:
        txt = await message.reply('`Cooking... It will take some time if you have enabled Link Bypass`', quote=True)
        await main_convertor_handler(message, 'mdisk')

        # Updating DB stats
    except Exception as e:
        await message.reply("Error while trying to convert links %s:" % e, quote=True)
    finally:
        await txt.delete()

