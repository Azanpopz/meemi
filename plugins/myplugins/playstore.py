import asyncio
from pyrogram import Client, filters
from pyrogram.errors import QueryIdInvalid, FloodWait
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, InlineQuery, InlineQueryResultArticle, \
    InputTextMessageContent

import os
import play_scraper
from pyrogram import Client, filters
from pyrogram.types import *


Bot = Client(
    "Play-Store-Bot",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"]
)


@Client.on_inline_query()
async def inline_handlers(_, inline: InlineQuery):
    results = play_scraper.search(inline.query)
    answers = []
    if result in results:
        
        answers.append(
                InlineQueryResultArticle(
                    title=result["title"],
                    description=result.get("description", None),
                    thumb_url=result.get("icon", None),
                    input_message_content=InputTextMessageContent(
                        message_text=details, disable_web_page_preview=True
                    ),
                    reply_markup=reply_markup
                )
            )

    elif search_ts.startswith("!yts"):
        query = search_ts.split(" ", 1)[-1]
        if (query == "") or (query == " "):
            answers.append(
                InlineQueryResultArticle(
                    title="!yts [text]",
                    description="Search For Torrent in YTS ...",
                    input_message_content=InputTextMessageContent(
                        message_text="`!yts [text]`\n\nSearch YTS Torrents from Inline!",
                        message_text=details, disable_web_page_preview=True
                    ),
                    reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton("Search Again", switch_inline_query_current_chat="!yts ")]])
                )
            )
            try:
                for i in range(len(results)):
                    answers.append(
                        InlineQueryResultArticle(
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
                            
                                
                            
                    except Exception as error:
                        print(error)
                await inline.answer(answers)
