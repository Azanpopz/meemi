import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import asyncio
from pyrogram import Client, filters
from bot import Bot
from config import Config


# =
usercaption_position = Config.CAPTION_POSITION
caption_position = usercaption_position.lower()
caption_text = Config.CAPTION_TEXT

@Client.on_message(filters.channel & (filters.document | filters.video | filters.audio) & ~filters.edited, group=-1)
async def editing(bot, message):
      try:
         media = message.document or message.video or message.audio or message.image
         caption_text = Config.CAPTION_TEXT
      except:
         caption_text = ""
         pass 
      if (message.document or message.video or message.audio or message.image): 
          if message.caption:
             fname = media.file_name
             filename = fname.replace("_", ".")
             file_caption = f"`{filename}`"                
          else:
             fname = media.file_name
             filename = fname.replace("_", ".")
             file_caption = f"`{filename}`"  
              
      try:
          if caption_position == "top":
             await bot.edit_message_caption(
                 chat_id = message.chat.id, 
                 message_id = message.message_id,
                 caption = caption_text + "\n" + file_caption,
                 parse_mode = "markdown"
             )
          elif caption_position == "bottom":
             await bot.edit_message_caption(
                 chat_id = message.chat.id, 
                 message_id = message.message_id,
                 caption = file_caption + "\n" + caption_text,
                 parse_mode = "markdown"
             )
          elif caption_position == "nil":
             await bot.edit_message_caption(
                 chat_id = message.chat.id,
                 message_id = message.message_id,
                 caption = caption_text, 
                 parse_mode = "markdown"
             ) 
      except:
          pass

@Client.on_message(filters.command("hello"))
async def hello(bot, message):
  await bot.reply("hello")
      
