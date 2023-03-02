import os 
import pyrogram
from pyrogram import Client, filters
from info import BOT_TOKEN, API_ID, API_HASH
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputMediaPhoto
from pyrogram.errors import UserNotparticipant


Bot = Client(
    "NoLink-BOT",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"]
)

@Client.on_message((filters.group) & filters.regex("http") | filters.regex("www") | filters.regex("@") | filters.regex("https") | filters.regex("t.me"))
async def nolink(bot,message):
	try:
		await message.delete(5)
	except:
		return
        




@Client.on_message((filters.group) & filters.regex("http") | filters.regex("www") | filters.regex("@") | filters.regex("https") | filters.regex("t.me")) 
async def start_message(bot, message):
   
        try:
            
                await message.delete(5)
	except:
                return
        except UserNotParticipant:
              
           button = [[
             InlineKeyboardButton("Mo Tech YT", url="https://t.me/+r_y-yTPhXkQwMzdl")
             ]]             
           await message.reply_text(
        
           text="Hello {message.from_user.mention} {content}  Bro സുഖമാണോ ചാനൽ ലോഗിൻ ചെയ്യ്",
           reply_markup=InlineKeyboardMarkup(buttons)
       ) 
   
           
