import os
import requests
from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    InlineQueryResultPhoto
)
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


Bot = Client(
    "Image-Search-Bot",
    bot_token=os.environ.get("BOT_TOKEN"),
    api_id=int(os.environ.get("API_ID")),
    api_hash=os.environ.get("API_HASH")
)

API = "https://apibu.herokuapp.com/api/y-images?query="







@Client.on_message(filters.text & filters.command(["img"]))
async def song(client, message):
    
    
    results = requests.get(
        API + requests.utils.requote_uri(message.query)
    ).json()["result"][:50]
    
    answers = []
    buttons = [[
        InlineKeyboardButton("JOIN MOVIES", url="https://t.me/NASRANI_UPDATE")
    ]]                           
    await message.reply_audio(
    title=update.query.capitalize(),
    description=result,
    caption="Made by @FayasNoushad",
    photo_url=result,
    reply_markup=InlineKeyboardMarkup(buttons)
) 
    
    await message.answer(answers)



