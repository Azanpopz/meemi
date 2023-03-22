
from io import BytesIO
from traceback import format_exc
from aiohttp import ClientSession
from pyrogram import Client, filters
from pyrogram.types import Message
from functools import wraps
from info import ADMINS, API_ID, API_HASH, LOG_CHANNEL

# from wbb import SUDOERS, USERBOT_PREFIX, app, app2, arq
# from wbb.core.decorators.errors import capture_err

import sys
import traceback
from functools import wraps

from pyrogram.errors.exceptions.forbidden_403 import ChatWriteForbidden


def split_limits(text):
    if len(text) < 2048:
        return [text]

    lines = text.splitlines(True)
    small_msg = ""
    result = []
    for line in lines:
        if len(small_msg) + len(line) < 2048:
            small_msg += line
        else:
            result.append(small_msg)
            small_msg = line
    else:
        result.append(small_msg)

    return result







def capture_err(func):
    @wraps(func)
    async def capture(client, message, *args, **kwargs):
        try:
            return await func(client, message, *args, **kwargs)
        except ChatWriteForbidden:
            await app.leave_chat(message.chat.id)
            return
        except Exception as err:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            errors = traceback.format_exception(
                etype=exc_type,
                value=exc_obj,
                tb=exc_tb,
            )
            error_feedback = split_limits(
                "**ERROR** | `{}` | `{}`\n\n```{}```\n\n```{}```\n".format(
                    0 if not message.from_user else message.from_user.id,
                    0 if not message.chat else message.chat.id,
                    message.text or message.caption,
                    "".join(errors),
                ),
            )
            for x in error_feedback:
                await client.send_message(LOG_CHANNEL, x)
            raise err

    return capture


async def quotify(messages: list):
    response = await arq.quotly(messages)
    if not response.ok:
        return [False, response.result]
    sticker = response.result
    sticker = BytesIO(sticker)
    sticker.name = "sticker.webp"
    return [True, sticker]


def getArg(message: Message) -> str:
    arg = message.text.strip().split(None, 1)[1].strip()
    return arg


def isArgInt(message: Message) -> list:
    count = getArg(message)
    try:
        count = int(count)
        return [True, count]
    except ValueError:
        return [False, 0]



@Client.on_message(filters.command("qu"))
@capture_err
async def quotly_func(client, message: Message):   
    
    try:
        
        sticker = await quotify(messages)
        if not sticker[0]:
            await message.reply_text(sticker[1])
            
        sticker = sticker[1]
        await message.reply_sticker(sticker)
        
        sticker.close()
    except Exception as e:
        await message.edit(
            "Something went wrong while quoting messages,"
            + " This error usually happens when there's a "
            + " message containing something other than text,"
            + " or one of the messages in-between are deleted."
        )
        e = format_exc()
        print(e)
