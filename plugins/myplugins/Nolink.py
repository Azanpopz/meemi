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

@Client.on_message((filters.group) & filters.regex("http") | filters.regex("www") | filters.regex("@") | filters.regex("https") | filters.regex("t.me"))
async def nolink(bot,message):
	try:
                hmm = await message.sleep(6)
                await hmm.delete()
                
		k = await message.reply_text(            
                text=f"SORRY DUDE",
                parse_mode=enums.ParseMode.HTML,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(
                            [
                                [
                                    InlineKeyboardButton(
                                        '🎭 ⭕️ ᴄᴏɴᴛᴀᴄᴛ ᴍᴇ ⭕️', url=f'https://t.me/nasrani_update'
                                    )
                                ]
                            ]
                        )
                    )

                await asyncio.sleep(6)
                await k.delete()


	except:
		return
        




