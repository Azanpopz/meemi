import os 
import pyrogram
from pyrogram import Client, filters
from info import BOT_TOKEN, API_ID, API_HASH, SUPPORT_CHAT_ID
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputMediaPhoto
import asyncio
from Script import script
from info import PICS
import random

Bot = Client(
    "NoLink-BOT",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"]
)

@Client.on_message((filters.group) & filters.regex("http") | filters.regex("www") | filters.regex("@") | filters.regex("https") | filters.regex("t.me"))
async def nolink(bot,message):
    if message.reply_to_message and SUPPORT_CHAT_ID == message.chat.id:
        chat_id = message.chat.id
        reporter = str(message.from_user.id)
        mention = message.from_user.mention    
        content = message.reply_to_message.text
    	try:
                buttons = [[
                    InlineKeyboardButton('sᴜʀᴘʀɪsᴇ', callback_data='start')
                ]]
                reply_markup = InlineKeyboardMarkup(buttons)
                        
                await message.reply_photo(
                    chat_id=message.chat.id
                    photo=random.choice(PICS),
                    caption=f"{message.from_user.mention}, ({reporter})  {content}"),
                    reply_markup=reply_markup,
                    parse_mode='html'
        
                )
                hmm = await message.delete()
                return
                


	except:
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
        




