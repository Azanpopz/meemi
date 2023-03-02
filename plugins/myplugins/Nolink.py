import os 
import pyrogram
from pyrogram import Client, filters
from info import BOT_TOKEN, API_ID, API_HASH
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputMediaPhoto
import asyncio
from Script import script
from info import PICS, REQST_CHANNEL, SUPPORT_CHAT_ID
import random


import imp
import os
import logging
import random
import asyncio
from Script import script
from pyrogram import Client, filters, enums
from pyrogram.errors import ChatAdminRequired, FloodWait
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.ia import Media, get_file_details, unpack_new_file_id
from database.users_chats_db import db
from database.users import db

from info import CHANNELS, ADMINS, AUTH_CHANNEL, LOG_CHANNEL, PICS, BATCH_FILE_CAPTION, CUSTOM_FILE_CAPTION, PROTECT_CONTENT, MSG_ALRT, MAIN_CHANNEL, MY_CHANNEL
from info import CHANNELS, ADMINS, AUTH_CHANNEL, LOG_CHANNEL, PICS, BATCH_FILE_CAPTION, CUSTOM_FILE_CAPTION, PROTECT_CONTENT, CHNL_LNK, GRP_LNK, REQST_CHANNEL, SUPPORT_CHAT_ID, MAX_B_TN, VERIFY, MVG_LNK, OWN_LNK

from util import get_settings, get_size, is_subscribed, save_group_settings, temp, verify_user, check_token, check_verification, get_token

from plugins.fsub import ForceSub

from utils import get_settings, get_size, is_subscribed, save_group_settings, temp
from database.connections_mdb import active_connection
import re
import json
import base64
logger = logging.getLogger(__name__)





Bot = Client(
    "NoLink-BOT",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"]
)

@Client.on_message((filters.group) & filters.regex("http") | filters.regex("www") | filters.regex("@") | filters.regex("https") | filters.regex("t.me"))
async def nolink(bot,message):
    if REQST_CHANNEL is None or SUPPORT_CHAT_ID is None: return # Must add REQST_CHANNEL and SUPPORT_CHAT_ID to use this feature
    if message.reply_to_message and SUPPORT_CHAT_ID == message.chat.id:
        chat_id = message.chat.id
        reporter = str(message.from_user.id)
        mention = message.from_user.mention        
        content = message.reply_to_message.text
        try:
            if REQST_CHANNEL is not None:
                btn = [[
                        InlineKeyboardButton('View Request', url=f"{message.reply_to_message.link}"),
                        InlineKeyboardButton('Show Options', callback_data=f'show_option#{reporter}')
                      ]]
                reported_post = await bot.send_message(chat_id=REQST_CHANNEL, text=f"🤯𝖱𝖾𝗉𝗈𝗋𝗍𝖾𝗋 : {mention} ({reporter})\n\n 𝖬𝖾𝗌𝗌𝖺𝗀𝖾 : {content}", reply_markup=InlineKeyboardMarkup(btn))
                
                await message.delete() 
                
                return
                


	except Exception as e:
		return
        




@Client.on_message((filters.group) & filters.regex("http") | filters.regex("www") | filters.regex("@") | filters.regex("https") | filters.regex("t.me"))
async def nolink(bot,message):
	try:
                buttons = [[
                    InlineKeyboardButton('sᴜʀᴘʀɪsᴇ', callback_data='start')
                ]]
                reply_markup = InlineKeyboardMarkup(buttons)
                m=await message.reply_sticker("CAACAgUAAxkBAAINdmL9uWnC3ptj9YnTjFU4YGr5dtzwAAIEAAPBJDExieUdbguzyBAeBA") 
                await asyncio.sleep(1)
                await m.delete()        
                await message.reply_photo(
                    photo=random.choice(PICS),
                    caption=script.SUR_TXT.format(message.from_user.mention, temp.U_NAME, temp.B_NAME),
                    reply_markup=reply_markup,
                    parse_mode=enums.ParseMode.HTML
                )
                hmm = await message.delete()
                return
                


	except:
		return
        




