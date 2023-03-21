import logging
from pyrogram import Client,filters
from info import BATCH_GROUP
import asyncio
import math
import os
import time
from Script import script
from pyrogram.types import Message
from database.users_chats_db import add_user



@Client.on_message(filters.command('footer') & filters.private)
async def footer_handler(client, message):
    user_id = message.from_user.id
    cmd = message.command
    user = add_user(user_id)
    if not message.reply_to_message:
        if "remove" not in cmd:
            return await message.reply(PICS + "\n\nCurrent Footer Text: " + user["footer_text"].replace("\n", "\n"))

        await add_user(user_id, {"footer_text": ""})
        return await message.reply("Footer Text Successfully Removed")
    elif message.reply_to_message.text:
        footer_text = message.reply_to_message.text.html
        await add_user(user_id, {"footer_text": footer_text})
        await message.reply("Footer Text Updated Successfully")
