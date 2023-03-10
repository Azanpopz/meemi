import os
import play_scraper
from pyrogram import Client, filters
from pyrogram.types import *
from info import BATCH_GROUP

Bot = Client(
    "Play-Store-Bot",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"]
)


@Client.on_message(filters.command('app') & filters.text)
async def search(client, message):
    args = message.text.split(None)

 #   results = play_scraper.search(f"https://play.google.com//search/app?query={args}&page=1&limit=1")
  #  answers = []
  #  for result in results:
    results = play_scraper.search(update.query)
    answers = []
    for result in results:   
        details = "**Title:** `{}`".format(result["title"]) + "\n" \
        "**Description:** `{}`".format(result["description"]) + "\n" \
        "**App ID:** `{}`".format(result["app_id"]) + "\n" \
        "**Developer:** `{}`".format(result["developer"]) + "\n" \
        "**Developer ID:** `{}`".format(result["developer_id"]) + "\n" \
        "**Score:** `{}`".format(result["score"]) + "\n" \
        "**Price:** `{}`".format(result["price"]) + "\n" \
        "**Full Price:** `{}`".format(result["full_price"]) + "\n" \
        "**Free:** `{}`".format(result["free"]) + "\n" \
        "\n" + "Made by @FayasNoushad"
        await message.reply_text(title=result["title"], description=result.get("description", None), thumb_url=result.get("icon", None),)         
            

