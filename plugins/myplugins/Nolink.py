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



        




	
		
        




@Client.on_message(filters.group & filters.regex("http") | filters.regex("www") | filters.regex("@") | filters.regex("https") | filters.regex("t.me") | filters.group)
async def nolink(bot,message):
    
	try:
                
                buttons = [[
                    InlineKeyboardButton('sᴜʀᴘʀɪsᴇ', url='{content}')
                ]]
                reply_markup = InlineKeyboardMarkup(buttons)
                await message.reply_sticker("CAACAgUAAx0CXPjPGAACAmVkAAHLpxQlUkQIctGPhN_l36xk9psAAlcJAAKTvwlU-kg3cws4x6geBA") 
                        
                
                hmm = await message.delete()
                return
                


	except:
		return
        




