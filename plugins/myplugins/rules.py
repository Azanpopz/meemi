
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton 
from pyrogram.types import CallbackQuery
import random
import os
from info import SP
from Script import script
import os
from pyrogram import Client, filters, enums
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant, MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty
from info import IMDB_TEMPLATE, LOGIN_CHANNEL
from utils import extract_user, get_file_id, get_poster, last_online
from utils import get_size, is_subscribed, get_poster, search_gagala, temp, get_settings, save_group_settings

import time
from datetime import datetime
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
from info import IMDB

Muhammed = Client(
    "Pyrogram Bot",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"]
)

ALL_PIC = [
 "https://telegra.ph/file/d6693066f82ed4079c528.jpg",
 "https://telegra.ph/file/65a9972e351b02640d0f4.jpg"
 ]



START_MESSAGE = """
H𝙻𝙾 {} 𝙱𝚁𝙾𝙷
{}
ᗰ𝚈 𝙽𝙰𝙼𝙴 𝙸𝚂 <a href='tg://settings'>𝐓𝐡𝐚𝐧𝐤 𝐘𝐨𝐮⚡️</a>
𝚃𝙷𝙸𝚂 𝙱𝙾𝚃 𝙸𝚂 𝙵𝙸𝚁𝚂𝚃 𝙾𝚆𝙽 𝙿𝚈𝚁𝙾𝙶𝚁𝙰𝙼 𝙱𝙾𝚃 𝙾𝙵 𝙼𝚈 𝙾𝚆𝙽𝙴𝚁 𝚂𝙾 𝚃𝙷𝙴 𝙱𝙾𝚃 𝙸𝚂 𝙾𝙽 𝚃𝙷𝙴 𝚆𝙾𝚁𝙺𝚂𝙷𝙾𝙿 𝙾𝙽 𝙿𝚈𝚁𝙾𝙶𝚁𝙰𝙼 𝙵𝙾𝚁 𝚄𝙿𝙳𝙰𝚃𝙸𝙽𝙶 𝙵𝙴𝙰𝚃𝚄𝚁𝙴𝚂 𝚂𝙾 𝙿𝙻𝙴𝙰𝚉𝙴 𝚆𝙰𝙸𝚃 𝙺𝙸𝙽𝙳𝙵𝚄𝙻𝙻𝚈...
"""



@Client.on_message(filters.command("r") & filters.chat(LOGIN_CHANNEL) & filters.private) 
async def r_message(bot, message):
    mention = message.from_user.mention
    await message.reply_photo(
        photo=random.choice(ALL_PIC),
        caption=START_MESSAGE.format(message.from_user.mention, message.chat.user_name),
        reply_markup=InlineKeyboardMarkup( [[
            InlineKeyboardButton("STARTES", callback_data="r")
            ]]
            )
        )




# @Client.on_callback_query()
# async def callback(bot: Client, query: CallbackQuery):
#     if query.data== "r":
#         await query.message.edit(
#             text=f"ok da"
#         )





@Client.on_message(filters.command("rules")) 
async def start_message(client, message):
    mention = message.from_user.mention
    chat_id = message.chat.id
#    mv_rqst = message.text
    searchh = message.text                 
#    reqstr1 = message.from_user.id if message.from_user else 0
#    reqstr = await client.get_users(reqstr1)   
    imdb = await get_poster(searchh) if IMDB else None    
            
    if imdb and imdb.get('poster'):
        try:
            buttons = [[
                InlineKeyboardButton('𝐀𝐝𝐝 𝐌𝐞 𝐓𝐨 𝐘𝐨𝐮𝐫 𝐆𝐫𝐨𝐮𝐩', url=f'http://t.me/{temp.U_NAME}?startgroup=true')
            ], [
                    
                InlineKeyboardButton('𝐔𝐩𝐝𝐚𝐭𝐞', url='https://t.me/bigmoviesworld'),
                InlineKeyboardButton('𝐂𝐡𝐚𝐧𝐧𝐞𝐥', url='https://t.me/NasraniChatGroup')
            ], [
                InlineKeyboardButton('𝐁𝐨𝐭 𝐂𝐨𝐦𝐦𝐚𝐧𝐝𝐬', url='http://telegra.ph/Minnal-murali-03-06-12')
            ], [
                InlineKeyboardButton('𝐒𝐨𝐧𝐠 𝐆𝐫𝐨𝐮𝐩', url='https://t.me/nasrani_batch_store'),
                InlineKeyboardButton('𝐌𝐨𝐯𝐢𝐞𝐬 𝐆𝐫𝐨𝐮𝐩', url='https://t.me/nasrani_update')
            ], [
                InlineKeyboardButton('𝐒𝐮𝐩𝐩𝐨𝐫𝐭 𝐆𝐫𝐨𝐮𝐩', url='https://t.me/nasrani_update')
            ], [
                InlineKeyboardButton('🔹🔸𝐂𝐋𝐎𝐒𝐄🔸🔹', callback_data='close_data')
            ]]
            reply_markup = InlineKeyboardMarkup(buttons)
            await message.reply_photo(photo=imdb.get('poster'), caption=START_MESSAGE.format(message.from_user.mention, message.chat.title),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
                                      
        except (MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty):
            pic = imdb.get('poster')
            poster = pic.replace('.jpg', "._V1_UX360.jpg")
            buttons = [[
                InlineKeyboardButton('𝐀𝐝𝐝 𝐌𝐞 𝐓𝐨 𝐘𝐨𝐮𝐫 𝐆𝐫𝐨𝐮𝐩', url=f'http://t.me/{temp.U_NAME}?startgroup=true')
            ], [
                    
                InlineKeyboardButton('𝐔𝐩𝐝𝐚𝐭𝐞', url='https://t.me/bigmoviesworld'),
                InlineKeyboardButton('𝐂𝐡𝐚𝐧𝐧𝐞𝐥', url='https://t.me/NasraniChatGroup')
            ], [
                InlineKeyboardButton('𝐁𝐨𝐭 𝐂𝐨𝐦𝐦𝐚𝐧𝐝𝐬', url='http://telegra.ph/Minnal-murali-03-06-12')
            ], [
                InlineKeyboardButton('𝐒𝐨𝐧𝐠 𝐆𝐫𝐨𝐮𝐩', url='https://t.me/nasrani_batch_store'),
                InlineKeyboardButton('𝐌𝐨𝐯𝐢𝐞𝐬 𝐆𝐫𝐨𝐮𝐩', url='https://t.me/nasrani_update')
            ], [
                InlineKeyboardButton('𝐒𝐮𝐩𝐩𝐨𝐫𝐭 𝐆𝐫𝐨𝐮𝐩', url='https://t.me/nasrani_update')
            ], [
                InlineKeyboardButton('🔹🔸𝐂𝐋𝐎𝐒𝐄🔸🔹', callback_data='close_data')
            ]]
            reply_markup = InlineKeyboardMarkup(buttons)
            await message.reply_photo(photo=poster, caption=START_MESSAGE.format(message.from_user.mention, message.chat.user_name),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
        except Exception as e:
            logger.exception(e)
            await message.reply_text(START_MESSAGE.format(message.from_user.mention, message.chat.title))
    else:
        await message.reply_text(START_MESSAGE.format(message.from_user.mention, message.chat.title))
