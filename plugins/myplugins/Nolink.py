import os 
import pyrogram
from pyrogram import Client, filters
from info import BOT_TOKEN, API_ID, API_HASH
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputMediaPhoto
import asyncio




Bot = Client(
    "NoLink-BOT",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"]
)



        




	
		
        




@Client.on_message(filters.regex("http") & filters.regex("www") | filters.regex("@") | filters.regex("https") | filters.regex("t.me") & filters.group)
async def nolink(bot,message):
        
	try:
                 
                buttons = [[
                    InlineKeyboardButton('sᴜʀᴘʀɪsᴇ', url='https://t.me/nasrani_update')
                ]]
                reply_markup = InlineKeyboardMarkup(buttons)
                k = await message.reply_sticker("CAACAgUAAx0CXPjPGAACAmVkAAHLpxQlUkQIctGPhN_l36xk9psAAlcJAAKTvwlU-kg3cws4x6geBA") 
                await asyncio.sleep(3)      
                k = await message.delete()
                hmm = await message.delete()
                return
                


	except:
		return
        




