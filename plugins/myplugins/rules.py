
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
𝐇𝐞𝐥𝐥𝐨 <a href='tg://settings'>𝐓𝐡𝐚𝐧𝐤 𝐘𝐨𝐮⚡️</a> 

⭕️ Disclaimer: All The Content in this Channel is Taken From the Internet, We Don't Own Any Content.

NB:  𝙰𝚕𝚕 𝙵𝚒𝚕𝚎𝚜 𝚒𝚗 𝚝𝚑𝚒𝚜 𝙲𝚑𝚊𝚗𝚗𝚎𝚕 𝚠𝚒𝚕𝚕 𝚋𝚎 𝚍𝚎𝚕𝚎𝚝𝚎𝚍 𝚒𝚗 3 𝚖𝚒𝚗𝚞𝚝𝚎𝚜

❗️𝐃𝐨𝐧𝐭 𝐅𝐨𝐫𝐠𝐞𝐭 𝐭𝐨 𝐅𝐨𝐫𝐰𝐚𝐫𝐝 𝐭𝐡𝐞 𝐅𝐢𝐥𝐞 𝐭𝐨 𝐒𝐚𝐯𝐞𝐝 𝐌𝐞𝐬𝐬𝐚𝐠𝐞 𝐛𝐞𝐟𝐨𝐫𝐞 𝐃𝐞𝐥𝐞𝐭𝐞..!❗️

╭──── • ❰ <a href='tg://settings'>𝐆𝐫𝐨𝐮𝐩⚡️</a> ❱ • ───➤
┣ ▫️ <a href='tg://settings'𝐌𝐚𝐢𝐧 𝐂𝐡𝐚𝐧𝐧𝐞𝐥⚡️</a> | <a href='tg://settings'>𝐔𝐩𝐝𝐚𝐭𝐞 𝐂𝐡𝐚𝐧𝐧𝐞𝐥⚡️</a> 
╰──────── • ◆ • ──────➤

⚠️ Must join this Channel to get files ⚠️
             🔸 Update Channel || Join Channel 🔸



📌ഏതു മൂവി ആണോ വേണ്ടത് അത് സ്പെല്ലിങ് തെറ്റാതെ ഗ്രൂപ്പിൽ ചോദിച്ചാൽ മാത്രമേ കിട്ടുകയുള്ളു...!!

സിനിമകൾ/സീരിസുകൾ ലഭിക്കാൻ പേര് മാത്രം അയച്ചാൽ മതി, അങ്ങനെ കിട്ടിയില്ലെങ്കിൽ വർഷം/സീസൺ(s)+എപ്പിസോഡ്(E)
കൂടി ചേർത്ത് അയക്കുക, അതിന്റെ കൂടെ ഉണ്ടോ? കിട്ടുമോ? തരോ ഇങ്ങനെയുള്ളതോ അല്ലെങ്കിൽ വേറെ ഭാഷയോ ചേർക്കേണ്ടതില്ല.

Example :-

Romanjam ✅
Romanjam 2023✅
Romanjam Malayalam ✅
Romanjam Malayalam Movie ❌️
Romanjam New Movie ❌️
Romanjam Movie ❌️
Romanjam Undo ❌️

Avengers Endgame ✅
Avengers:Endgame ❌️

Rules And Bot Commands <a href='http://telegra.ph/Minnal-murali-03-06-12'>𝐓𝐡𝐚𝐧𝐤 𝐘𝐨𝐮⚡️</a>

📌നിങ്ങൾ റിക്വസ്റ്റ് ചെയ്ത മൂവി കിട്ടിയില്ലെങ്കിൽ വൈകാതെ തന്നെ ആഡ് ചെയ്യുന്നതായിരിക്കും..

🍿Don't Aks Theatre 🎭 Released Movies


Please do not stay in this group by asking for an unreleased film.  You will receive a warning if you ask.

=========================

வெளியிடப்படாத படம் கேட்டு தயவுசெய்து இந்த குழுவில் தங்க வேண்டாம்.  நீங்கள் கேட்டால் எச்சரிக்கையைப் பெறுவீர்கள்.

=========================

ദയവായ്‌ ‌ ഇറങ്ങാത്ത ഫിലിം ചോദിച്ച്‌ ഈ ഗ്രൂപ്പിൽ നിൽക്കരുത്‌.  ചോദിച്ചാൽ നിങ്ങൾക്ക്‌ മുന്നറിയിപ്പ്‌ കിട്ടുന്നതായിരിക്കും.

You Will Get Fire 🔥,If You Asking Non Released Movie.





PowerGroup {}
Group Name {}
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





@Client.on_message(filters.reply) 
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
            hmm = await message.reply_photo(photo=poster,  caption=START_MESSAGE.format(message.from_user.mention, message.chat.title),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
            )
        except Exception as e:
            logger.exception(e)
