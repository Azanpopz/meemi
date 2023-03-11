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

       else: 
            results = play_scraper.search(inline.query)
            if not torrentList:
                answers.append(
                    InlineQueryResultArticle(
                        title="No Torrents Found in ThePirateBay!",
                        description=f"Can't find torrents for {query} in ThePirateBay !!",
                        input_message_content=InputTextMessageContent(
                            message_text=f"No Torrents Found For `{query}` in ThePirateBay !!",
                            parse_mode="Markdown"
                        ),
                        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Try Again", switch_inline_query_current_chat="!pb ")]])
                    )
                )
            else:
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
                            parse_mode="Markdown",
                                disable_web_page_preview=True
                            ),
                            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Search Again", switch_inline_query_current_chat="!yts ")]]),
                            thumb_url=torrentList[i]["Poster"]
                        )
                    )
                    
                except Exception as error:
                    print(error)
            await inline.answer(answers)
