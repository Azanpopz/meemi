
from pyrogram import Client, filters

import requests
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import Client, filter
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton 
from pyrogram.types import CallbackQuery
import randam
import os


force_channel = "+r_y-yTPhXkQwMzdl"




@Client.on_message(filters.command("star")) 
async def start_message(bot, message)
   if  force_channel:
        try:
            user = await bot.get_chat_member(force_channel, message.from_user.id)
            if user.status == "kicked out":
                await message.reply_text("Join channel")
                return
        except UserNotParticipant:
              
           button = [[
              InlineKeyboardButton("Mo Tech YT", url="https://t.me/+r_y-yTPhXkQwMzdl")
              ]]             
            await message.reply_text(
        
            text="Hello {message.from_user.mention}   Bro സുഖമാണോ ചാനൽ ലോഗിൻ ചെയ്യ്",
            reply_markup=InlineKeyboardMarkup(buttons)
        ) 
   
            await message.reply_text("done")

      
