import os
import random
from PIL import Image
from pyrogram.types import Message
from pyrogram import Client, filters, enums


CAPTION = 'converted by nasrani_update' # caption of the files

api_id = 123456789 #int of api id get from my.telegram.org
api_hash = " Your Api Hash Here " #str of api hash get from my.telegram.org
token = ' Your Bot Token here ' #str of token get from BotFather

bot = Client('Session_Name', api_id, api_hash, bot_token=token, workers = 4 )


@Client.on_message(filters.command(['converts']))
async def sticker_image(_, msg: Message):
    user_id = msg.from_user.id
    
    name_format = f"StarkBots_{user_id}"
    if msg.photo:
        message = await msg.reply("Converting...")
        image = await msg.download(file_name=f"{name_format}.jpg")
        await message.edit("Sending...")
        im = Image.open(image).convert("RGB")
        im.save(f"{name_format}.webp", "webp")
        sticker = f"{name_format}.webp"
        await msg.reply_sticker(sticker)
        await message.delete()
        os.remove(sticker)
        os.remove(image)
    elif msg.sticker.is_animated:
        await msg.reply("Animated stickers are not supported !", quote=True)
    else:
        message = await msg.reply("Converting...")
        sticker = await msg.download(file_name=f"{name_format}.webp")
        await message.edit("Sending...")
        im = Image.open(sticker).convert("RGB")
        im.save(f"{name_format}.jpg", "jpeg")
        image = f"{name_format}.jpg"
        await msg.reply_photo(image)
        await message.delete()
        os.remove(image)
        os.remove(sticker)


@Client.on_message(filters.command(['convertp']))
async def sticker_image(_, msg: Message):
    user_id = msg.from_user.id
    
    name_format = f"StarkBots_{user_id}"
    if msg.photo:
        message = await msg.reply("Converting...")
        sticker = await msg.download(file_name=f"{name_format}.webp")
        await message.edit("Sending...")
        im = Image.open(sticker).convert("RGB")
        im.save(f"{name_format}.jpg", "jpeg")
        image = f"{name_format}.jpg"
        await msg.reply_photo(image)
        await message.delete()
        os.remove(image)
        os.remove(sticker)
#    elif msg.sticker.is_animated:
#        await msg.reply("Animated stickers are not supported !", quote=True)
    else:
        message = await msg.reply("Converting...")
        image = await msg.download(file_name=f"{name_format}.jpg")
        await message.edit("Sending...")
        im = Image.open(image).convert("RGB")
        im.save(f"{name_format}.webp", "webp")
        sticker = f"{name_format}.webp"
        await msg.reply_sticker(sticker)
        await message.delete()
        os.remove(sticker)
        os.remove(image)


@Client.on_message(filters.command(['png']) | filters.private & filters.sticker)
def photo_convert(c, m):
    rand_id = random.randint(100,900) # generate random number between 100 to 900
    m.download(f"{m.chat.id}-{rand_id}.jpg")
    img = Image.open(f'downloads/{m.chat.id}-{rand_id}.jpg')
    img.save(f"{m.chat.id}-{rand_id}.png","PNG")
    m.reply_document(f"{m.chat.id}-{rand_id}.png",caption= CAPTION )
    os.remove(f"{m.chat.id}-{rand_id}.png")
    os.remove(f'downloads/{m.chat.id}-{rand_id}.jpg')

@Client.on_message(filters.command(['png1']) | filters.private & filters.sticker)
def conver_webp(c, m):
    rand_id = random.randint(100,900) # generate random number between 100 to 900
    if (m.sticker.is_animated) == False:
        m.download(f"{m.chat.id}-{rand_id}.webp")
        img = Image.open(f'downloads/{m.chat.id}-{rand_id}.webp').convert("RGBA")
        img.save(f"{m.chat.id}-{rand_id}.png","PNG")
        m.reply_photo(f"{m.chat.id}-{rand_id}.png",caption=CAPTION)
        m.reply_document(f"{m.chat.id}-{rand_id}.png",caption=CAPTION)
        os.remove(f"{m.chat.id}-{rand_id}.png")
        os.remove(f'downloads/{m.chat.id}-{rand_id}.webp')
    if m.sticker.is_animated == True:
        ms1 = m.reply_text("Converting...")
        ms2 = m.reply_text("🤞")
        m.download(f"{m.chat.id}-{rand_id}.tgs")
        os.system(f"lottie_convert.py downloads/{m.chat.id}-{rand_id}.tgs {m.chat.id}-{rand_id}.gif")
        m.reply_animation(f"{m.chat.id}-{rand_id}.gif",caption=CAPTION)
        ms1.delete()
        ms2.delete()
        os.remove(f"{m.chat.id}-{rand_id}.gif")
        os.remove(f'downloads/{m.chat.id}-{rand_id}.tgs')










@Client.on_message(filters.command(['kangs']) & filters.incoming & (filters.sticker | filters.photo))
async def sticker_image(_, msg: Message):
    user_id = msg.from_user.id
    message_id = msg.message_id
    name_format = f"StarkBots_{user_id}_{message_id}"
    if msg.photo:
        message = await msg.reply("Converting...")
        image = await msg.download(file_name=f"{name_format}.jpg")
        await message.edit("Sending...")
        im = Image.open(image).convert("RGB")
        im.save(f"{name_format}.webp", "webp")
        sticker = f"{name_format}.webp"
        await msg.reply_sticker(sticker)
        await message.delete()
        os.remove(sticker)
        os.remove(image)
    elif msg.sticker.is_animated:
        await msg.reply("Animated stickers are not supported !", quote=True)
    else:
        message = await msg.reply("Converting...")
        sticker = await msg.download(file_name=f"{name_format}.webp")
        await message.edit("Sending...")
        im = Image.open(sticker).convert("RGB")
        im.save(f"{name_format}.jpg", "jpeg")
        image = f"{name_format}.jpg"
        await msg.reply_photo(image)
        await message.delete()
        os.remove(image)
        os.remove(sticker)
