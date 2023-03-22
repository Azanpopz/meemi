import os 
import pyrogram
from pyrogram import Client, filters
from info import BOT_TOKEN, API_ID, API_HASH
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputMediaPhoto
import asyncio
from info import SUPPORT_CHAT
import os
from pyrogram import Client, filters, enums
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant, MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty
from utils import extract_user, get_file_id, get_poster, last_online
import time
from datetime import datetime
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from pyrogram import Client, filter
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton 
from pyrogram.types import CallbackQuery
import randam
import os
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)


Bot = Client(
    "NoLink-BOT",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"]
)



PHOTO_LINK = [
 "Photo Link",
 "photo Link"
 ]





        





@Client.on_message(filters.command("start"))
async def nolink(bot,message):
        
	try:
                 
                buttons = [[
                    InlineKeyboardButton('sᴜʀᴘʀɪsᴇ', url='https://t.me/nasrani_update')
                ]]
                reply_markup = InlineKeyboardMarkup(buttons)
                k = await message.reply_sticker("CAACAgUAAx0CXPjPGAACAmVkAAHLpxQlUkQIctGPhN_l36xk9psAAlcJAAKTvwlU-kg3cws4x6geBA") 
                await asyncio.sleep(2)      
                k = await k.delete()
                hmm = await message.delete()
                return
                


	except:
		return
        
        




	
		
        




@Client.on_message(filters.chat(SUPPORT_CHAT) & filters.regex("http") & filters.regex("www") | filters.regex("@") | filters.regex("https") | filters.regex("t.me"))
async def nolink(bot,message):
        
	try:
                 
                buttons = [[
                    InlineKeyboardButton('sᴜʀᴘʀɪsᴇ', url='https://t.me/nasrani_update')
                ]]
                reply_markup = InlineKeyboardMarkup(buttons)
                k = await message.reply_sticker("CAACAgUAAx0CXPjPGAACAmVkAAHLpxQlUkQIctGPhN_l36xk9psAAlcJAAKTvwlU-kg3cws4x6geBA") 
                await asyncio.sleep(2)      
                k = await k.delete()
                hmm = await message.delete()
                return
                


	except:
		return
        


@Client.on_message(filters.regex("http") & filters.regex("www") | filters.regex("@") | filters.regex("https") | filters.regex("t.me") | filters.regex("myr"))
async def who_is(client, message):
    # https://github.com/SpEcHiDe/PyroGramBot/blob/master/pyrobot/plugins/admemes/whois.py#L19
    status_message = await message.reply_text(
        "`Fetching user info...`"
    )
    await status_message.edit(
        "`Processing user info...`"
    )
    from_user = None
    from_user_id, _ = extract_user(message)
    try:
        from_user = await client.get_users(from_user_id)
    except Exception as error:
        await status_message.edit(str(error))
        return
    if from_user is None:
        return await status_message.edit("no valid user_id / message specified")
    message_out_str = ""
    message_out_str += f"<b>➲First Name:</b> {from_user.first_name}\n"
    last_name = from_user.last_name or "<b>None</b>"
    message_out_str += f"<b>➲Last Name:</b> {last_name}\n"
    message_out_str += f"<b>➲Telegram ID:</b> <code>{from_user.id}</code>\n"
    username = from_user.username or "<b>None</b>"
    dc_id = from_user.dc_id or "[User Doesn't Have A Valid DP]"
    message_out_str += f"<b>➲Data Centre:</b> <code>{dc_id}</code>\n"
    message_out_str += f"<b>➲User Name:</b> @{username}\n"
    message_out_str += f"<b>➲User 𝖫𝗂𝗇𝗄:</b> <a href='tg://user?id={from_user.id}'><b>Click Here</b></a>\n"
    if message.chat.type in ((enums.ChatType.SUPERGROUP, enums.ChatType.CHANNEL)):
        try:
            chat_member_p = await message.chat.get_member(from_user.id)
            joined_date = (
                chat_member_p.joined_date or datetime.now()
            ).strftime("%Y.%m.%d %H:%M:%S")
            message_out_str += (
                "<b>➲Joined this Chat on:</b> <code>"
                f"{joined_date}"
                "</code>\n"
            )
        except UserNotParticipant:
            pass
    chat_photo = from_user.photo
    if chat_photo:
        local_user_photo = await client.download_media(
            message=chat_photo.big_file_id
        )
        buttons = [[
            InlineKeyboardButton('🔐 Close', callback_data='close_data')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply_photo(
            photo=local_user_photo,
            quote=True,
            reply_markup=reply_markup,
            caption=message_out_str,
            parse_mode=enums.ParseMode.HTML,
            disable_notification=True
        )
        os.remove(local_user_photo)
    else:
        buttons = [[
            InlineKeyboardButton('🔐 Close', callback_data='close_data')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply_text(
            text=message_out_str,
            reply_markup=reply_markup,
            quote=True,
            parse_mode=enums.ParseMode.HTML,
            disable_notification=True
        )
    await status_message.delete()
    await message.delete()
