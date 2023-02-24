import os
import asyncio
from pyrogram import Client, filters, enums
from pyrogram.types import Message, User, ChatJoinRequest
from info import APPROVE_ID, APPROVED 
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


@Client.on_chat_join_request((filters.group | filters.channel) & filters.chat(APPROVE_ID) if APPROVE_ID else (filters.group | filters.channel))
async def autoapprove(client, message: ChatJoinRequest):
    chat=message.chat 
    user=message.from_user 
    print(f"{user.first_name} Joined") 
    await client.approve_chat_join_request(chat_id=chat.id, user_id=user.id)
    if APPROVED == "on":
        buttons = [[
            InlineKeyboardButton('sᴜᴘᴘᴏʀᴛ​', url=f'https://t.me/MLZ_BOTZ_SUPPORT')
            
        ]]
        markup = InlineKeyboardMarkup(buttons)
        caption = f"<b>Dᴇᴀʀ {message.from_user.mention()},\n\nYour Request To Jᴏɪɴ {message.chat.title} Was Approved</b>"
        await client.send_photo(
            chat_id=message.from_user.id, 
            photo='https://telegra.ph/file/f7738f04ea74e16c9db02.jpg', 
            caption=caption, 
            parse_mode=enums.ParseMode.HTML
        )
