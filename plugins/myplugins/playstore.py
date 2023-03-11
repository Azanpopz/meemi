import requests
from dotenv import load_dotenv
from requests.utils import requote_uri
from pyrogram import Client, filters
from pyrogram.types import *


load_dotenv()
API = "https://api.abirhasan.wtf/google?query="


Bot = Client(
    "Google-Search-Bot",
    bot_token=os.environ.get("BOT_TOKEN"),
    api_id=int(os.environ.get("API_ID")),
    api_hash=os.environ.get("API_HASH")
)


@Client.on_message(filters.private & filters.command(["google"]))
async def start(bot, update):    
    r = requests.get(API + requote_uri(query))
    informations = r.json()["results"][:50]
    text = f"**Title:** `{info['title']}`"
    text += f"\n**Description:** `{info['description']}`"
    text += f"\n\nMade by @FayasNoushad"
    buttons = [[
        InlineKeyboardButton("JOIN MOVIES", url="https://t.me/NASRANI_UPDATE")
    ]]                           
    await message.reply_audio(
    text = f"**Title:** `{info['title']}`",
    reply_markup=InlineKeyboardMarkup(buttons)
) 
    return results
