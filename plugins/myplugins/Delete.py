import asyncio
from os import environ
from pyrogram import Client, filters, idle
from pyrogram import enums
import re
from os import environ

from info import API_HASH, API_ID, BOT_TOKEN, SESSION, SUPPORT_CHAT_ID, ADMINS

API_ID = int(environ.get("API_ID"))
API_HASH = environ.get("API_HASH")
BOT_TOKEN = environ.get("BOT_TOKEN")
SESSION = environ.get('SESSION', 'UFSBotz')


ADMINS = []
for usr in environ.get("ADMINS").split():
    ADMINS.append(int(usr))

START_MSG = "<b>Hai {},\nI'm a private bot of @mh_world to delete group messages after a specific time</b>"


Bot = Client(name="auto-delete",
              session_string=SESSION,
              api_id=API_ID,
              api_hash=API_HASH,
              workers=300
              )


Bot = Client(name="auto-delete",
             api_id=API_ID,
             api_hash=API_HASH,
             bot_token=BOT_TOKEN,
             workers=300
             )


@Client.on_message(filters.command('start') & filters.private)
async def start(bot, message):
    await message.reply(START_MSG.format(message.from_user.mention))

@Client.on_message(filters.chat(SUPPORT_CHAT_ID))
async def delete(bot, message):
    try:
       if message.from_user.id in ADMINS:
          return
       else:
          await asyncio.sleep(6)
          await Bot.delete_messages(message.chat.id, message.id)
    except Exception as e:
       print(e)
       
