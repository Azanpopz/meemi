
from pyrogram import Client, filters

import requests
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

force_channel = "+r_y-yTPhXkQwMzdl"




@Client.on_message(filters.command("star")) 
async def start_message(bot, message)
         if  force_channel:
               try:
                    user = await bot.get_chat_member(force_channel, msg.from_user.id)
                    if user.status == "kicked out":
                          await msg.reply_text("Join channel")
                          return
               expect UserNotParticipant:
              
       button = [[
          InlineKeyboardButton("Mo Tech YT", url="https://t.me/+r_y-yTPhXkQwMzdl")
          ]]             
        await msg.reply_text(
        
        text="Hello {msg.from_user.mention}   Bro സുഖമാണോ ചാനൽ ലോഗിൻ ചെയ്യ്",
        reply_markup=InlineKeyboardMarkup(buttons)
    ) 
   
         await msg.reply_text("done")

      
