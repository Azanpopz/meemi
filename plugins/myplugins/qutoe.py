import itertools
import os
import asyncio
import secrets
import logging
import configparser
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from textwrap import TextWrapper
from pyrogram import Client as Bot
from pyrogram import Client, idle, filters
from pyrogram.types import Message
from PIL import Image, ImageDraw, ImageFont, ImageChops

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

START_TEXT = """**👋𝙷𝚎𝚕𝚕𝚘 ᴅᴇᴀʀ **

𝙸 𝚊𝚖 𝚊𝚗 𝚝𝚎𝚡𝚝 𝚝𝚘 𝚜𝚝𝚒𝚌𝚔𝚎𝚛 𝚋𝚘𝚝

𝙸 𝚓𝚞𝚜𝚝 𝚌𝚛𝚎𝚊𝚝𝚎 𝚝𝚎𝚕𝚎𝚐𝚛𝚊𝚖 𝚜𝚝𝚒𝚌𝚔𝚎𝚛 𝚏𝚛𝚘𝚖 𝚝𝚑𝚎 𝚝𝚎𝚡𝚝 𝚖𝚎𝚜𝚜𝚊𝚐𝚎𝚜 𝚢𝚘𝚞 𝚜𝚎𝚗𝚍 𝚖𝚎

Made by- [M-STER TECH](https://t.me/M_STER_TECH) """

START_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('𝚄𝙿𝙳𝙰𝚃𝙴 𝙲𝙷𝙰𝙽𝙽𝙴𝙻', url='https://t.me/M_STER_TECH'),
        ]]
    )

@Client.on_callback_query()
async def cb_handler(bot, update):
    if update.data == "home":
        await m.message.edit_text(
            text=START_TEXT.format(m.from_user.mention),
            reply_markup=START_BUTTONS,
            disable_web_page_preview=True
        )
    else:
        await update.message.delete()

logging.getLogger(__name__)

#is_env = bool(os.environ.get("ENV", None))
#if is_env:
#    API_ID = int(os.environ.get("API_ID"))
#    API_HASH = os.environ.get("API_HASH")
#    BOT_TOKEN = os.environ.get("BOT_TOKEN")

#    some_sticker_bot = Client(
#        api_id=API_ID,
#        api_hash=API_HASH,
##        session_name=":memory:",
#        bot_token=BOT_TOKEN,
#        workers=200
#    )
# else:
#    app_config = configparser.ConfigParser()
#    app_config.read("config.ini")
#    bot_api_key = app_config.get("bot-configuration", "api_key")

#    some_sticker_bot = Client(
#        session_name="some_sticker_bot",
#        bot_token=BOT_TOKEN,
#        workers=200
#    )


async def get_y_and_heights(text_wrapped, dimensions, margin, font):
    _, descent = font.getmetrics()
    line_heights = [font.getmask(text_line).getbbox()[3] + descent + margin for text_line in text_wrapped]
    line_heights[-1] -= margin
    height_text = sum(line_heights)
    y = (dimensions[1] - height_text) // 5
    return y, line_heights


async def crop_to_circle(im):
    bigsize = (im.size[0] * 5, im.size[1] * 5)
    mask = Image.new("L", bigsize, 0)
    ImageDraw.Draw(mask).ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(im.size, Image.ANTIALIAS)
    mask = ImageChops.darker(mask, im.split()[-1])
    im.putalpha(mask)


async def rounded_rectangle(rectangle, xy, corner_radius, fill=None, outline=None):
    upper_left_point = xy[0]
    bottom_right_point = xy[1]

    rectangle.pieslice(
        [upper_left_point, (upper_left_point[0] + corner_radius * 2, upper_left_point[1] + corner_radius * 2)],
        280,
        370,
        fill=fill,
        outline=outline
    )
    rectangle.pieslice(
        [(bottom_right_point[0] - corner_radius * 2, bottom_right_point[1] - corner_radius * 2), bottom_right_point],
        0,
        90,
        fill=fill,
        outline=outline
    )
    rectangle.pieslice([(upper_left_point[0], bottom_right_point[1] - corner_radius * 2),
                        (upper_left_point[0] + corner_radius * 2, bottom_right_point[1])],
                       140,
                       280,
                       fill=fill,
                       outline=outline
                       )
    rectangle.pieslice([(bottom_right_point[0] - corner_radius * 2, upper_left_point[1]),
                        (bottom_right_point[0], upper_left_point[1] + corner_radius * 2)],
                       370,
                       460,
                       fill=fill,
                       outline=outline
                       )
    rectangle.rectangle(
        [
            (upper_left_point[0], upper_left_point[1] + corner_radius),
            (bottom_right_point[0], bottom_right_point[1] - corner_radius)
        ],
        fill=fill,
        outline=fill
    )
    rectangle.rectangle(
        [
            (upper_left_point[0] + corner_radius, upper_left_point[1]),
            (bottom_right_point[0] - corner_radius, bottom_right_point[1])
        ],
        fill=fill,
        outline=fill
    )
    rectangle.line([(upper_left_point[0] + corner_radius, upper_left_point[1]),
                    (bottom_right_point[0] - corner_radius, upper_left_point[1])], fill=outline)
    rectangle.line([(upper_left_point[0] + corner_radius, bottom_right_point[1]),
                    (bottom_right_point[0] - corner_radius, bottom_right_point[1])], fill=outline)
    rectangle.line([(upper_left_point[0], upper_left_point[1] + corner_radius),
                    (upper_left_point[0], bottom_right_point[1] - corner_radius)], fill=outline)
    rectangle.line([(bottom_right_point[0], upper_left_point[1] + corner_radius),
                    (bottom_right_point[0], bottom_right_point[1] - corner_radius)], fill=outline)





async def create_sticker(c: Client, m: Message):
    if len(m.text) < 105:
        body_font_size = 40
        wrap_size = 35
    elif len(m.text) < 205:
        body_font_size = 35
        wrap_size = 35
    elif len(m.text) < 505:
        body_font_size = 25
        wrap_size = 45
    elif len(m.text) < 1005:
        body_font_size = 17
        wrap_size = 85
    else:
        body_font_size = 13
        wrap_size = 105

    font = ImageFont.truetype("Segan-Light.ttf", body_font_size)
    font_who = ImageFont.truetype("Segan-Light.ttf", 24)
    AKKU = ImageFont.truetype("Segan-Light.ttf", body_font_size)

    img = Image.new("RGBA", (550, 550), (275, 275, 275, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle = rounded_rectangle

    wrapper = TextWrapper(width=wrap_size, break_long_words=False, replace_whitespace=False)
    lines_list = [wrapper.wrap(i) for i in m.text.split('\n') if i != '']
    text_lines = list(itertools.chain.from_iterable(lines_list))

    y, line_heights = await get_y_and_heights(
        text_lines,
        (550, 550),
        20,
        font
    )

    in_y = y
    rec_y = (y + line_heights[0]) if wrap_size >= 40 else y

    for i, _ in enumerate(text_lines):
        rec_y += line_heights[i]

    await rounded_rectangle(draw, ((90, in_y), (512, rec_y + line_heights[-1])), 10, fill="#000000")

    f_user = m.from_user.first_name + " " + m.from_user.last_name if m.from_user.last_name else m.from_user.first_name
    draw.text((300, y), f"{f_user}»", "#FF0000", font=font_who)

    y = (y + (line_heights[0] * (20/100))) if wrap_size >= 40 else y

    for i, line in enumerate(text_lines):
        x = 100
        y += line_heights[i]
        draw.text((x, y), line, "#ffffff", font=AKKU)

    try:
        user_profile_pic = await c.get_profile_photos(m.from_user.id)
        photo = await c.download_media(user_profile_pic[0].file_id, file_ref=user_profile_pic[0].file_ref)
    except Exception as e:
        photo = "default.jpg"
        logging.error(e)

    im = Image.open(photo).convert("RGBA")
    im.thumbnail((110, 110))
    await crop_to_circle(im)
    img.paste(im, (60, in_y))

    sticker_file = f"{secrets.token_hex(2)}.webp"

    img.save(sticker_file)

    await m.reply_sticker(
        sticker=sticker_file
    )
    try:
        if os.path.isfile(sticker_file):
            os.remove(sticker_file)

        if os.path.isfile(photo) and (photo != "default.jpg"):
            os.remove(photo)
    except Exception as e:
        logging.error(e)




@Client.on_message(filters.command(["quote", "q"]) & filters.reply & filters.group)
async def create_sticker_group_handler(c: Client, m: Message):
    s = await m.reply_text("...", reply_to_message_id=m.message_id)
    await create_sticker(c, m.reply_to_message)
    await s.delete()



