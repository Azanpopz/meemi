# short and repost forwarded message

from pyrogram import Client, filters
from config import CHANNEL_ID, FORWARD_MESSAGE, CHANNELS
from util import main_convertor_handler


@Client.on_message(filters.chat(CHANNEL_ID) & (
        filters.channel | filters.group) & filters.incoming & ~filters.private & filters.forwarded)
async def channel_forward_link_handler(c:Client, message):
    if FORWARD_MESSAGE == "True" or FORWARD_MESSAGE is True and CHANNELS is True or CHANNELS == 'True':
        try:
            await main_convertor_handler(message, 'mdisk')
            await message.delete()
            # Updating DB stats
        except Exception as e:
            print(e)
