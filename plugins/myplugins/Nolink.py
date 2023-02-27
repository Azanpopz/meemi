import os 
import pyrogram
from pyrogram import Client, filters
from info import BOT_TOKEN, API_ID, API_HASH


Bot = Client(
    "NoLink-BOT",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"]
)

@Client.on_message((filters.group) | filters.regex("http") | filters.regex("www") | filters.regex("/") | filters.regex("@") | filters.regex("t.me"))
async def nolink(bot,message):
	try:
		await message.delete()
	except:
		return
