import datetime
from translation import *
from config import ADMINS, SOURCE_CODE, HEROKU_API_KEY, HEROKU_APP_NAME, HEROKU
from database import db
from helpers import temp
from config import WELCOME_IMAGE
from pyrogram import Client, filters
from pyrogram.types import Message

import logging

from utils import broadcast_admins, get_size, getHerokuDetails
logger = logging.getLogger(__name__)


@Client.on_message(filters.command('start') & filters.incoming)
async def start(c:Client, m:Message):

    user_method = await db.get_bot_method(temp.BOT_USERNAME)
    if not user_method:
        mode = "None"
    else:
        mode = user_method
    if WELCOME_IMAGE:
        t = START_MESSAGE.format(m.from_user.mention, mode)
        return await m.reply_photo(photo=WELCOME_IMAGE, caption=t, reply_markup=START_MESSAGE_REPLY_MARKUP)

    t = START_MESSAGE.format(m.from_user.mention, mode)
    await m.reply_text(t, reply_markup=START_MESSAGE_REPLY_MARKUP, disable_web_page_preview=True)


@Client.on_message(filters.command('help') & filters.incoming)
async def help_command(c, m):
    s = HELP_MESSAGE.format(
            firstname=temp.FIRST_NAME,
            username=temp.BOT_USERNAME,
            repo=SOURCE_CODE,
            owner="@potter_00" )
    if WELCOME_IMAGE:
        return await m.reply_photo(photo=WELCOME_IMAGE, caption=s, reply_markup=HELP_REPLY_MARKUP)
    await m.reply_text(s, reply_markup=HELP_REPLY_MARKUP, disable_web_page_preview=True)
    

@Client.on_message(filters.command('about') & filters.user(ADMINS))
async def about_command(c, m):
    bot = await c.get_me()
    if WELCOME_IMAGE:
        return await m.reply_photo(photo=WELCOME_IMAGE, caption=ABOUT_TEXT.format(bot.mention(style='md')), reply_markup=ABOUT_REPLY_MARKUP, disable_web_page_preview=True)
    await m.reply_text(ABOUT_TEXT.format(bot.mention(style='md')), reply_markup=ABOUT_REPLY_MARKUP, disable_web_page_preview=True)

@Client.on_message(filters.command('method') & filters.user(ADMINS) & filters.private)
async def method_handler(c:Client, m:Message):
    user = temp.BOT_USERNAME
    user_method = await db.get_bot_method(user)
    if len(m.command) == 1:    
        return await m.reply_text(METHOD_MESSAGE.format(method=user_method), reply_markup=METHOD_REPLY_MARKUP)
    if len(m.command) == 2:
        method_name = m.command[1]

        if method_name not in ['mdisk', 'mdlink', 'droplink']:
            return await m.reply_text(METHOD_MESSAGE.format(method=user_method), reply_markup=METHOD_REPLY_MARKUP)

        if not await db.get_bot_method(user):
            await db.add_method(user, method_name)
        else:
            await db.update_method(user, method_name)

        logger.info("Updated method to %s", method_name)
        
        b_msg = "Method changed successfully to `{method}` for @{username} by {mention}".format(method=method_name.upper(), username=user, mention=m.from_user.mention)
        await broadcast_admins(c, b_msg, m.from_user.id)

        await m.reply("Method changed successfully to {method} for @{username}".format(method=method_name, username=user))


@Client.on_message(filters.command('restart') & filters.user(ADMINS) & filters.private)
async def restart_handler(c: Client, m:Message):
    RESTARTE_MARKUP = InlineKeyboardMarkup([
    [
        InlineKeyboardButton('Sure', callback_data=f'restart'),
        InlineKeyboardButton('No', callback_data=f'delete'),

    ],

])

    await m.reply("Are you sure you want to restart / re-deploy the server?", reply_markup=RESTARTE_MARKUP)


@Client.on_message(filters.command('stats') & filters.user(ADMINS) & filters.private)
async def stats_handler(c: Client, m:Message):
    txt = await m.reply('`Fetching stats...`')
    size = await db.get_db_size()
    free = 536870912 - size
    size = await get_size(size)
    free = await get_size(free)
    link_stats = await db.get_bot_stats()
    runtime = datetime.datetime.now()

    t = runtime - temp.START_TIME
    runtime = str(datetime.timedelta(seconds=t.seconds))



    msg = f"""
**- Total Posts:** `{link_stats['posts']}`
**- Total Links:** `{link_stats['links']}`
**- Total Mdisk Links:** `{link_stats['mdisk_links']}`
**- Total Droplink Links:** `{link_stats['droplink_links']}`
**- Used Storage:** `{size}`
**- Total Free Storage:** `{free}`

**- Runtime:** `{runtime}`
"""
    if HEROKU:
        heroku = await getHerokuDetails(HEROKU_API_KEY, HEROKU_APP_NAME)
        msg += f"\n- **Heroku Stats:**\n{heroku}"

    return await txt.edit(msg)


@Client.on_message(filters.command('logs') & filters.user(ADMINS) & filters.private)
async def log_file(bot, message):
    """Send log file"""
    try:
        await message.reply_document('TelegramBot.log')
    except Exception as e:
        await message.reply(str(e))
