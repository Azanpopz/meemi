import logging
import logging.config

# Get logging configurations
logging.config.fileConfig('logging.conf')
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("imdbpy").setLevel(logging.ERROR)


from pyrogram import Client, __version__, filters
from pyrogram.raw.all import layer
from database.ia_filterdb import Media
from database.users_chats_db import db
from info import SESSION, API_ID, API_HASH, BOT_TOKEN, LOG_STR, LOG_CHANNEL, PORT
from utils import temp
from typing import Union, Optional, AsyncGenerator
from pyrogram import types
from Script import script 
from datetime import date, datetime 
import pytz


from config import Config

from pyrogram import Client
from os import environ,sys,mkdir,path
import logging
from sys import executable
#from Python_ARQ import ARQ
from aiohttp import ClientSession
from dotenv import load_dotenv
import shutil
load_dotenv("config.env")
import os 
# Log
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(message)s",
    handlers = [logging.FileHandler('bot.log'), logging.StreamHandler()]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
LOGGER = logging.getLogger(__name__)

# Mandatory Variable
try:
    API_ID = int(environ['API_ID'])
    API_HASH = environ['API_HASH']
    BOT_TOKEN = environ['BOT_TOKEN']
    OWNER_ID = int(environ['OWNER_ID'])
except KeyError:
    LOGGER.debug("One or More ENV variable not found.")
    sys.exit(1)
# Optional Variable
SUDO_USERS = environ.get("SUDO_USERS",str(OWNER_ID)).split()
SUDO_USERS = [int(_x) for _x in SUDO_USERS]
if OWNER_ID not in SUDO_USERS:
    SUDO_USERS.append(OWNER_ID)
AUTH_CHATS = environ.get('AUTH_CHATS',None ).split()
AUTH_CHATS = [int(_x) for _x in AUTH_CHATS]
LOG_GROUP = environ.get("LOG_GROUP", None)
if LOG_GROUP:
    LOG_GROUP = int(LOG_GROUP)
BUG = environ.get("BUG", None)
if BUG:
    BUG = int(BUG)
genius_api = environ.get("genius_api",None)
if genius_api:
    genius_api = genius_api




class Bot(Client):

    def __init__(self):
        super().__init__(
            name=SESSION,
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            workers=150,
            plugins={"root": "plugins"},
            sleep_threshold=5,
        )

    async def start(self):
        b_users, b_chats = await db.get_banned()
        temp.BANNED_USERS = b_users
        temp.BANNED_CHATS = b_chats
        await super().start()
        await Media.ensure_indexes()
        me = await self.get_me()
        temp.ME = me.id
        temp.U_NAME = me.username
        temp.B_NAME = me.first_name
        self.username = '@' + me.username
        logging.info(f"{me.first_name} with for Pyrogram v{__version__} (Layer {layer}) started on {me.username}.")
        logging.info(LOG_STR)
        logging.info(script.LOGO)
        tz = pytz.timezone('Asia/Kolkata')
        today = date.today()
        now = datetime.now(tz)
        time = now.strftime("%H:%M:%S %p")
        await self.send_message(chat_id=LOG_CHANNEL, text=script.RESTART_TXT.format(today, time))

    async def stop(self, *args):
        await super().stop()
        logging.info("Bot stopped. Bye.")
    
    async def iter_messages(
        self,
        chat_id: Union[int, str],
        limit: int,
        offset: int = 0,
    ) -> Optional[AsyncGenerator["types.Message", None]]:
        """Iterate through a chat sequentially.
        This convenience method does the same as repeatedly calling :meth:`~pyrogram.Client.get_messages` in a loop, thus saving
        you from the hassle of setting up boilerplate code. It is useful for getting the whole chat messages with a
        single call.
        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).
                
            limit (``int``):
                Identifier of the last message to be returned.
                
            offset (``int``, *optional*):
                Identifier of the first message to be returned.
                Defaults to 0.
        Returns:
            ``Generator``: A generator yielding :obj:`~pyrogram.types.Message` objects.
        Example:
            .. code-block:: python
                for message in app.iter_messages("pyrogram", 1, 15000):
                    print(message.text)
        """
        current = offset
        while True:
            new_diff = min(200, limit - current)
            if new_diff <= 0:
                return
            messages = await self.get_messages(chat_id, list(range(current, current+new_diff+1)))
            for message in messages:
                yield message
                current += 1




app = Bot()
app.run()
