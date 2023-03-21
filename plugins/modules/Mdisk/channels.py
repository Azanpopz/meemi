from config import CHANNEL_ID, CHANNELS
from pyrogram import Client, filters
from utils import main_convertor_handler


# Channel
@Client.on_message(~filters.forwarded & filters.chat(CHANNEL_ID) & (
                filters.channel | filters.group) & filters.incoming & ~filters.private &
        ~filters.forwarded)
async def channel_link_handler(c:Client, message):
    if CHANNELS is True or CHANNELS == "True":
        try:
            await main_convertor_handler(message, 'mdisk', True)
            # Updating DB stats
        except Exception as e:
            print(e)
