
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton 
from pyrogram.types import CallbackQuery
import random
import os
from info import SP
from Script import script
import os
from pyrogram import Client, filters
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant, MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty
from info import IMDB_TEMPLATE
from utils import extract_user, get_file_id, get_poster, last_online
import time
from datetime import datetime
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)




ALL_PIC = [
 "https://telegra.ph/file/d6693066f82ed4079c528.jpg",
 "https://telegra.ph/file/65a9972e351b02640d0f4.jpg"
 ]



START_MESSAGE ="""
H𝙻𝙾 {} 𝙱𝚁𝙾𝙷
ᗰ𝚈 𝙽𝙰𝙼𝙴 𝙸𝚂 <a href='https://t.me/pyogram_bot'>ᴅᴀᴠᴏᴏᴅ ɪʙʀᴀʜɪᴍ⚡️</a>
𝚃𝙷𝙸𝚂 𝙱𝙾𝚃 𝙸𝚂 𝙵𝙸𝚁𝚂𝚃 𝙾𝚆𝙽 𝙿𝚈𝚁𝙾𝙶𝚁𝙰𝙼 𝙱𝙾𝚃 𝙾𝙵 𝙼𝚈 𝙾𝚆𝙽𝙴𝚁 𝚂𝙾 𝚃𝙷𝙴 𝙱𝙾𝚃 𝙸𝚂 𝙾𝙽 𝚃𝙷𝙴 𝚆𝙾𝚁𝙺𝚂𝙷𝙾𝙿 𝙾𝙽 𝙿𝚈𝚁𝙾𝙶𝚁𝙰𝙼 𝙵𝙾𝚁 𝚄𝙿𝙳𝙰𝚃𝙸𝙽𝙶 𝙵𝙴𝙰𝚃𝚄𝚁𝙴𝚂 𝚂𝙾 𝙿𝙻𝙴𝙰𝚉𝙴 𝚆𝙰𝙸𝚃 𝙺𝙸𝙽𝙳𝙵𝚄𝙻𝙻𝚈...
"""
Muhammed = Client(
    "Pyrogram Bot",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"],
)


@Client.on_message(filters.command("rule")) 
async def start_message(bot, message):
    await message.reply_photo(
        photo=random.choice(ALL_PIC),
        caption=START_MESSAGE.format(message.from_user.mention),
        reply_markup=InlineKeyboardMarkup( [[
            InlineKeyboardButton("STARTES", callback_data="start")
            ]]
            )
        )




@Client.on_callback_query()
async def callback(bot: Doctor, query: CallbackQuery):
    if query.data== "start":
        await query.message.edit(
            text=START_MESSAGE.format(query.from_user.mention)
        )







@Client.on_message(filters.command(["rules", 'head']))
async def imdb_search(client, message):
    if ' ' in message.text:
        k = await message.reply('Searching ImDB')
        r, title = message.text.split(None, 1)
        movies = await get_poster(title, bulk=True)
        if not movies:
            return await message.reply("No results Found")
        btn = [
            [
                InlineKeyboardButton(
                    text=f"{movie.get('title')} - {movie.get('year')}",
                    callback_data=f"imdb#{movie.movieID}",
                )
            ]
            for movie in movies
        ]
        await k.edit('Here is what i found on IMDb', reply_markup=InlineKeyboardMarkup(btn))
    else:
        await message.reply('Give me a movie / series Name')



@Client.on_callback_query(filters.regex('^rules'))
async def imdb_callback(bot: Client, quer_y: CallbackQuery):
    i, movie = quer_y.data.split('#')
    imdb = await get_poster(query=movie, id=True)
    btn = [
            [
                InlineKeyboardButton(
                    text=f"{imdb.get('title')}",
                    url=imdb['url'],
                )
            ]
        ]
    message = quer_y.message.reply_to_message or quer_y.message
    if imdb:
        caption = IMDB_TEMPLATE.format(
            query = imdb['title'],
            title = imdb['title'],
            votes = imdb['votes'],
            aka = imdb["aka"],
            seasons = imdb["seasons"],
            box_office = imdb['box_office'],
            localized_title = imdb['localized_title'],
            kind = imdb['kind'],
            imdb_id = imdb["imdb_id"],
            cast = imdb["cast"],
            runtime = imdb["runtime"],
            countries = imdb["countries"],
            certificates = imdb["certificates"],
            languages = imdb["languages"],
            director = imdb["director"],
            writer = imdb["writer"],
            producer = imdb["producer"],
            composer = imdb["composer"],
            cinematographer = imdb["cinematographer"],
            music_team = imdb["music_team"],
            distributors = imdb["distributors"],
            release_date = imdb['release_date'],
            year = imdb['year'],
            genres = imdb['genres'],
            poster = imdb['poster'],
            plot = imdb['plot'],
            rating = imdb['rating'],
            url = imdb['url'],
            **locals()
        )
    else:
        caption = "No Results"
    if imdb.get('poster'):
        try:
            await quer_y.message.reply_photo(photo=imdb['poster'], caption=f"ok", reply_markup=InlineKeyboardMarkup(btn))
        except (MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty):
            pic = imdb.get('poster')
            poster = pic.replace('.jpg', "._V1_UX360.jpg")
            await quer_y.message.reply_photo(photo=poster, caption=f"ok", reply_markup=InlineKeyboardMarkup(btn))
        except Exception as e:
            logger.exception(e)
            await quer_y.message.reply(caption, reply_markup=InlineKeyboardMarkup(btn), disable_web_page_preview=False)
        await quer_y.message.delete()
    else:
        await quer_y.message.edit(caption, reply_markup=InlineKeyboardMarkup(btn), disable_web_page_preview=False)
    await quer_y.answer()
 

