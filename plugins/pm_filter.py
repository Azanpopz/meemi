# Kanged From @TroJanZheX
# REDIRECT added https://github.com/Joelkb
import asyncio
import re
import ast
import math
import random
from pyrogram.errors.exceptions.bad_request_400 import MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty
from Script import script
import pyrogram
from database.connections_mdb import active_connection, all_connections, delete_connection, if_active, make_active, \
    make_inactive
from info import ADMINS, AUTH_CHANNEL, MY_CHANNEL, FILE_CHANNEL, AUTH_USERS, CUSTOM_FILE_CAPTION, NOR_IMG, AUTH_GROUPS, P_TTI_SHOW_OFF, IMDB, \
    SINGLE_BUTTON, SPELL_CHECK_REPLY, IMDB_TEMPLATE, SPELL_IMG, MSG_ALRT, FILE_FORWARD, MAIN_CHANNEL, LOG_CHANNEL, PICS, SUPPORT_CHAT_ID
from info import LANGUAGES, MAX_BTN, ADMINS, AUTH_CHANNEL, AUTH_USERS, SUPPORT_CHAT_ID, CUSTOM_FILE_CAPTION, MSG_ALRT, PICS, AUTH_GROUPS, P_TTI_SHOW_OFF, GRP_LNK, CHNL_LNK, NOR_IMG, LOG_CHANNEL, SPELL_IMG, MAX_B_TN, IMDB, \
    SINGLE_BUTTON, SPELL_CHECK_REPLY, IMDB_TEMPLATE, NO_RESULTS_MSG, REQ_CHANNEL, MVG_LNK, OWN_LNK

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputMediaPhoto
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait, UserIsBlocked, MessageNotModified, PeerIdInvalid
from utils import get_size, is_subscribed, get_poster, search_gagala, temp, get_settings, save_group_settings, get_shortlink

from database.users_chats_db import db
from database.users import db

from database.ia_filterdb import Media, get_file_details, get_search_results, get_bad_files
from database.ia import Media, get_file_details, get_search_results, get_bad_files

from database.filters_mdb import (
    del_all,
    find_filter,
    get_filters,
)
from database.gfilters_mdb import (
    find_gfilter,
    get_gfilters,
)
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

BUTTONS = {}
SPELL_CHECK = {}
FILTER_MODE = {}

BUTTONS = {}
BATCH_FILES = {}
SPELL_CHECK = {}

FILE_PROTECT = {}
IMPORTED = {}
HELPABLE = {}
SELECT = {}
FILES = {}

@Client.on_message(filters.command('autofilter') & filters.user(ADMINS))
async def fil_mod(client, message): 
      mode_on = ["yes", "on", "true"]
      mode_of = ["no", "off", "false"]

      try: 
         args = message.text.split(None, 1)[1].lower() 
      except: 
         return await message.reply("**𝙸𝙽𝙲𝙾𝙼𝙿𝙴𝚃𝙴𝙽𝚃 𝙲𝙾𝙼𝙼𝙰𝙳...**")
      
      m = await message.reply("**𝚂𝙴𝚃𝚃𝙸𝙽𝙶.../**")

      if args in mode_on:
          FILTER_MODE[str(message.chat.id)] = "True" 
          await m.edit("**𝙰𝚄𝚃𝙾𝙵𝙸𝙻𝚃𝙴𝚁 𝙴𝙽𝙰𝙱𝙻𝙴𝙳**")
      
      elif args in mode_of:
          FILTER_MODE[str(message.chat.id)] = "False"
          await m.edit("**𝙰𝚄𝚃𝙾𝙵𝙸𝙻𝚃𝙴𝚁 𝙳𝙸𝚂𝙰𝙱𝙻𝙴𝙳**")
      else:
          await m.edit("𝚄𝚂𝙴 :- /autofilter on 𝙾𝚁 /autofilter off")

@Client.on_message((filters.group) & filters.text & filters.incoming)
async def give_filter(client,message):
    await global_filters(client, message)
    group_id = message.chat.id
    name = message.text

    keywords = await get_filters(group_id)
    for keyword in reversed(sorted(keywords, key=len)):
        pattern = r"( |^|[^\w])" + re.escape(keyword) + r"( |$|[^\w])"
        if re.search(pattern, name, flags=re.IGNORECASE):
            reply_text, btn, alert, fileid = await find_filter(group_id, keyword)

            if reply_text:
                reply_text = reply_text.replace("\\n", "\n").replace("\\t", "\t")

            if btn is not None:
                try:
                    if fileid == "None":
                        if btn == "[]":
                            await message.reply_text(reply_text, disable_web_page_preview=True)
                        else:
                            button = eval(btn)
                            await message.reply_text(
                                reply_text,
                                disable_web_page_preview=True,
                                reply_markup=InlineKeyboardMarkup(button)
                            )
                    elif btn == "[]":
                        await message.reply_cached_media(
                            fileid,
                            caption=reply_text or ""
                        )
                    else:
                        button = eval(btn) 
                        await message.reply_cached_media(
                            fileid,
                            caption=reply_text or "",
                            reply_markup=InlineKeyboardMarkup(button)
                        )
                except Exception as e:
                    print(e)
                break 

    else:
        if FILTER_MODE.get(str(message.chat.id)) == "False":
            return
        else:
            await auto_filter(client, message)





@Client.on_callback_query(filters.regex(r"^select"))
async def select_files(bot, query):
    ident, req, key, offset = query.data.split("_")
    ad_user = query.from_user.id
    if int(ad_user) in ADMINS:
        pass
    elif int(req) not in [query.from_user.id, 0]:
        return await query.answer(
            "കാര്യമൊക്കെ കൊള്ളാം, പക്ഷേ, ഇത്‌ നിങ്ങളുടേതല്ല.;\n"
            "Nice Try! But, This Was Not Your Request, Request Yourself;",
            show_alert=True)

    if SELECT.get(int(req)):
        del SELECT[int(req)]

    if FILES.get(int(req)):
        del FILES[int(req)]

    SELECT[int(req)] = "ACTIVE"
    try:
        offset = int(offset)
    except:
        offset = 0
    search = BUTTONS.get(key)
    if not search:
        await query.answer("You Are Using One Of My Old Messages, Please Send The Request Again.", show_alert=True)
        return

    i = 3
    lines = []
    sublines = []
    btn = []
    btn1 = []
    try:
        while True:
            j = 0
            lines = query.message.reply_markup.inline_keyboard[i]
            if len(lines) == 1:
                fs = json.loads(str(lines[0]))
                if fs['text'] not in ["De-Select", "Select", "Send"]:
                    btn.append([InlineKeyboardButton(text=fs['text'], callback_data=fs['callback_data'])])
            else:
                while True:
                    sublines = lines[j]
                    fs1 = json.loads(str(sublines))
                    if fs1['text'] not in ["De-Select", "Select", "Send"]:
                        btn1.append([fs1['text'], fs1['callback_data'], True])

                    j = j + 1
                    sublines = []
                    if j > len(lines) - 1:
                        keyboard = build_keyboard(btn1)
                        btn.insert(i, keyboard[0])
                        btn1 = []
                        break
            i = i + 1
            lines = []
            if i > len(query.message.reply_markup.inline_keyboard) - 1:
                break

    except Exception as e:
        print(str(e))

    if SELECT.get(int(req)) == "ACTIVE":
        btn.append(
            [InlineKeyboardButton(text=f"De-Select", callback_data=f"deselect_{req}_{key}_{offset}"),
             InlineKeyboardButton(text="Send", callback_data=f"send_{req}_{key}_{offset}")]
        )
    else:
        btn.append(
            [InlineKeyboardButton(text="Select", callback_data=f"select_{req}_{key}_{offset}")]
        )

    btn.insert(0, [
        InlineKeyboardButton("🧲 Tᴏʀʀᴇɴᴛ Gʀᴏᴜᴘ", url="https://t.me/UFSLeechPublic")
    ])
    btn.insert(0, [
        InlineKeyboardButton("ᴘᴍ ᴍᴇ", url="https://t.me/UFSChatBot"),
        InlineKeyboardButton("⚜ Nᴇᴡ Oᴛᴛ Mᴏᴠɪᴇs ⚜", url="https://t.me/+uuLR9YwyRjg0ODQ0")
    ])

    btn.insert(0, [
        InlineKeyboardButton("🔄 Nᴇᴡ Uᴘᴅᴀᴛᴇs", url="https://t.me/UFSFilmUpdate")
    ])

    await query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(btn))

@Client.on_callback_query(filters.regex(r"^deselect"))
async def deselect_all(bot, query):
    ident, req, key, offset = query.data.split("_")
    ad_user = query.from_user.id
    if int(ad_user) in ADMINS:
        pass
    elif int(req) not in [query.from_user.id, 0]:
        return await query.answer(
            "കാര്യമൊക്കെ കൊള്ളാം, പക്ഷേ, ഇത്‌ നിങ്ങളുടേതല്ല.;\n"
            "Nice Try! But, This Was Not Your Request, Request Yourself;",
            show_alert=True)

    if SELECT.get(int(req)):
        del SELECT[int(req)]

    if FILES.get(int(req)):
        del FILES[int(req)]

    SELECT[int(req)] = "DE-ACTIVE"
    await auto_filter(bot, query.message.reply_to_message, cb=query)


@Client.on_callback_query(filters.regex(r"^send"))
async def send_files(bot, query):
    ident, req, key, offset = query.data.split("_")
    ad_user = query.from_user.id

    settings = await sett_db.get_settings(str(query.message.chat.id))

    if settings is not None:
        SINGLE_BUTTON = settings["button"]
        SPELL_CHECK_REPLY = settings["spell_check"]
        P_TTI_SHOW_OFF = settings["botpm"]
        IMDB = settings["imdb"]

    if FILE_PROTECT.get(query.from_user.id):
        del FILE_PROTECT[query.from_user.id]
    FILE_PROTECT[query.from_user.id] = str(query.message.chat.id)
    if int(ad_user) in ADMINS:
        pass
    elif int(ad_user) in ADMINS:
        pass
    elif int(req) not in [query.from_user.id, 0]:
        return await query.answer(
            "കാര്യമൊക്കെ കൊള്ളാം, പക്ഷേ, ഇത്‌ നിങ്ങളുടേതല്ല.;\n"
            "Nice Try! But, This Was Not Your Request, Request Yourself;",
            show_alert=True)

    for file_id in FILES[int(req)]:
        files_ = await get_file_details(file_id)

        if not files_:
            return await query.answer('No such file exist.')
        files = files_[0]
        title = files.file_name
        size = get_size(files.file_size)
        f_caption = files.caption
        if CUSTOM_FILE_CAPTION:
            try:
                f_caption = CUSTOM_FILE_CAPTION.format(file_name=title, file_size=size, file_caption=f_caption)
            except Exception as e:
                logger.exception(e)
            f_caption = f_caption
        if f_caption is None:
            f_caption = f"{files.file_name}"

        f_sub_caption = f"<code>💾 Size: {size}</code>\n\n🌟༺ ──•◈•─ ─•◈•──༻🌟\n<b>➧ പുതിയ സിനിമകൾ / വെബ്‌ സീരീസ് " \
                        f"വേണോ? എന്നാൽ പെട്ടെന്ന് ഗ്രൂപ്പിൽ ജോയിൻ ആയിക്കോ\n\n🔊 Gʀᴏᴜᴘ: " \
                        f"@UniversalFilmStudio \n🔊 Gʀᴏᴜᴘ: @UniversalFilmStudioo \n🔊 " \
                        f"Cʜᴀɴɴᴇʟ: <a href='https://t.me/+uuLR9YwyRjg0ODQ0'>Nᴇᴡ Oᴛᴛ Mᴏᴠɪᴇs</a> \n\n" \
                        f"🎗️ʝσιи 🎗️ ѕнαяє🎗️ ѕυρρσят🎗️ </b>"

        f_caption = f_caption + f"\n\n{f_sub_caption}"

        await bot.send_cached_media(
            chat_id=query.from_user.id,
            file_id=file_id,
            caption=f_caption,
            protect_content=settings["file_secure"] if settings["file_secure"] else False,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            '🎭 Nᴇᴡ Uᴘᴅᴀᴛᴇs', url="https://t.me/UFSFilmUpdate"
                        ),
                        InlineKeyboardButton(
                            '🎭 ᴍᴏᴠɪᴇs', url="https://t.me/UniversalFilmStudio"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "⚜ Nᴇᴡ Oᴛᴛ Mᴏᴠɪᴇs ⚜", url="https://t.me/+uuLR9YwyRjg0ODQ0"
                        )
                    ]
                ]
            )
        )

    await query.answer('Check My PM, I Have Sent Selected Files In Your PM', show_alert=True)
    if SELECT[int(req)]:
        del SELECT[int(req)]

    if FILES[int(req)]:
        del FILES[int(req)]

    SELECT[int(req)] = "DE-ACTIVE"
    await auto_filter(bot, query.message.reply_to_message, cb=query)


@Client.on_message(filters.group & filters.text & filters.incoming)  # & ~filters.edited
async def give_filter(client, message):
    group_id = message.chat.id
    chat_type = message.sender_chat.type if message.sender_chat else message.chat.type
    name = message.text

    if chat_type.name in ["CHANNEL"]:
        text = f"""
#DETECT_SENDER_AS_CHANNEL

**CHANNEL: {message.sender_chat.title} ({message.sender_chat.id})** 
`CHAT: {message.chat.title} ({message.chat.id})`
**MESSAGE: You Cannot Request Via Channel**"""
        chat_channel = await message.reply_text(text, quote=True)
        await asyncio.sleep(5)
        await chat_channel.delete()
        await message.delete()
        return

    if len(message.text) < 1:
        try:
            msg = await message.reply_text(
                f"**Nice Try! But, I Need Minimum --__3__-- Character To Find Your Requesting Details,\n"
                f"Please Edit Your Request** `{message.text}`", quote=True)
            req = message.from_user.id if message.from_user else 0
            if temp.TEMP_USER.get(req):
                del temp.TEMP_USER[req]
            temp.TEMP_USER[req] = "edit"
            await asyncio.sleep(10)
            await msg.delete()
            return
        except Exception as e:
            logging.info(f"Error: \n{str(e)}")
            return

    keywords = await get_filters(group_id)
    for keyword in reversed(sorted(keywords, key=len)):
        pattern = r"( |^|[^\w])" + re.escape(keyword) + r"( |$|[^\w])"
        if re.search(pattern, name, flags=re.IGNORECASE):
           await check_manual_filter(client, group_id, keyword, message, 0)
           return
           reply_text, btn, alert, fileid = await find_filter(group_id, keyword)
             
           if reply_text:
               reply_text = reply_text.replace("\\n", "\n").replace("\\t", "\t")
             
           if btn is not None:
               try:
                   if fileid == "None":
                       if btn == "[]":
                           await message.reply_text(reply_text, disable_web_page_preview=True)
                       else:
                           button = eval(btn)
                           await message.reply_text(
                               reply_text,
                               disable_web_page_preview=True,
                               reply_markup=InlineKeyboardMarkup(button)
                           )
                   elif btn == "[]":
                       await message.reply_cached_media(
                           fileid,
                           caption=reply_text or ""
                       )
                   else:
                       button = eval(btn)
                       await message.reply_cached_media(
                           fileid,
                           caption=reply_text or "",
                           reply_markup=InlineKeyboardMarkup(button)
                       )
               except Exception as e:
                   logger.exception(e)
               break
    else:
        await auto_filter(client, message)


@Client.on_edited_message(filters.group & filters.text & filters.incoming)  # & filters.edited
async def give_filter_edited(client, message):
    group_id = message.chat.id
    chat_type = message.sender_chat.type if message.sender_chat else message.chat.type
    name = message.text

    if chat_type.name in ["CHANNEL"]:
        text = f"""
#DETECT_SENDER_AS_CHANNEL

**CHANNEL: {message.sender_chat.title} ({message.sender_chat.id})** 
`CHAT: {message.chat.title} ({message.chat.id})`
**MESSAGE: You Cannot Request Via Channel**"""
        chat_channel = await message.reply_text(text, quote=True)
        await asyncio.sleep(5)
        await chat_channel.delete()
        await message.delete()
        return

    if temp.TEMP_USER.get(message.from_user.id) == "edit":
        del temp.TEMP_USER[message.from_user.id]
    else:
        return

    keywords = await get_filters(group_id)
    for keyword in reversed(sorted(keywords, key=len)):
        pattern = r"( |^|[^\w])" + re.escape(keyword) + r"( |$|[^\w])"
        if re.search(pattern, name, flags=re.IGNORECASE):
            await check_manual_filter(client, group_id, keyword, message, 0)
            return
            reply_text, btn, alert, fileid = await find_filter(group_id, keyword)
            
            if reply_text:
                reply_text = reply_text.replace("\\n", "\n").replace("\\t", "\t")
           
            if btn is not None:
                try:
                    if fileid == "None":
                        if btn == "[]":
                            await message.reply_text(reply_text, disable_web_page_preview=True)
                        else:
                            button = eval(btn)
                            await message.reply_text(
                                reply_text,
                                disable_web_page_preview=True,
                                reply_markup=InlineKeyboardMarkup(button)
                            )
                    elif btn == "[]":
                        await message.reply_cached_media(
                            fileid,
                            caption=reply_text or ""
                        )
                    else:
                        button = eval(btn)
                        await message.reply_cached_media(
                            fileid,
                            caption=reply_text or "",
                            reply_markup=InlineKeyboardMarkup(button)
                        )
                except Exception as e:
                    logger.exception(e)
                break
    else:
        await auto_filter(client, message)

























@Client.on_message(filters.group | filters.private & filters.text & filters.incoming)
async def give_filter(client, message):
    if message.chat.id != SUPPORT_CHAT_ID:
        await global_filters(client, message)
    manual = await manual_filters(client, message)
    if manual == False:
        settings = await get_settings(message.chat.id)
        try:
            if settings['auto_ffilter']:
                await auto_filter(client, message)
        except KeyError:
            grpid = await active_connection(str(message.from_user.id))
            await save_group_settings(grpid, 'auto_ffilter', True)
            settings = await get_settings(message.chat.id)
            if settings['auto_ffilter']:
                await auto_filter(client, message) 


@Client.on_message(filters.private & filters.text & filters.incoming)
async def pm_text(bot, message):
    content = message.text
    user = message.from_user.first_name
    user_id = message.from_user.id
    if content.startswith("/") or content.startswith("#"): return  # ignore commands and hashtags
    await message.reply_text("<b>Your message has been sent to my moderators !</b>")
    await bot.send_message(
        chat_id=LOG_CHANNEL,
        text=f"<b>#PM_MSG\n\nName : {user}\n\nID : {user_id}\n\nMessage : {content}</b>"
    )



@Client.on_callback_query(filters.regex(r"^next"))
async def next_page(bot, query):
    ident, req, key, offset = query.data.split("_")
    if int(req) not in [query.from_user.id, 0]:
        return await query.answer(script.ALRT_TXT.format(query.from_user.first_name), show_alert=True)
    try:
        offset = int(offset)
    except:
        offset = 0
    search = BUTTONS.get(key)
    if not search:
        await query.answer(script.OLD_ALRT_TXT.format(query.from_user.first_name),show_alert=True)
        return

    files, n_offset, total = await get_search_results(query.message.chat.id, search, offset=offset, filter=True)
    try:
        n_offset = int(n_offset)
    except:
        n_offset = 0

    if not files:
        return
    settings = await get_settings(query.message.chat.id)
    if 'is_shortlink' in settings.keys():
        ENABLE_SHORTLINK = settings['is_shortlink']
    else:
        await save_group_settings(query.message.chat.id, 'is_shortlink', False)
        ENABLE_SHORTLINK = False
    if ENABLE_SHORTLINK == True:
        if settings['button']:
            btn = [
                [
                    InlineKeyboardButton(
                        text=f"▫️{get_size(file.file_size)} ⊳ {file.file_name}", url=await get_shortlink(message.chat.id, f"https://telegram.me/{temp.U_NAME}?start=files_{file.file_id}")
                    ),
                ]
                for file in files
            ]
        else:
            btn = [
                [
                    InlineKeyboardButton(
                        text=f"{file.file_name}",
                        url=await get_shortlink(message.chat.id, f"https://telegram.me/{temp.U_NAME}?start=files_{file.file_id}")
                    ),
                    InlineKeyboardButton(
                        text=f"{get_size(file.file_size)}",
                        url=await get_shortlink(message.chat.id, f"https://telegram.me/{temp.U_NAME}?start=files_{file.file_id}")
                    ),
                ]
                for file in files
            ]
    else:
        if settings['button']:
            btn = [
                [
                    InlineKeyboardButton(
                        text=f"▫️{get_size(file.file_size)} ⊳ {file.file_name}", url=await get_shortlink(message.chat.id, f"https://telegram.me/{temp.U_NAME}?start=files_{file.file_id}")
                    ),
                ]
                for file in files
            ]
        else:
            btn = [
                [
                    InlineKeyboardButton(
                        text=f"{file.file_name}",
                        url=await get_shortlink(message.chat.id, f"https://telegram.me/{temp.U_NAME}?start=files_{file.file_id}")
                    ),
                    InlineKeyboardButton(
                        text=f"{get_size(file.file_size)}",
                        url=await get_shortlink(message.chat.id, f"https://telegram.me/{temp.U_NAME}?start=files_{file.file_id}")
                    ),
                ]
                for file in files
            ]
            
    try:
        if settings['auto_delete']:
            btn.insert(0, 
                [
                    InlineKeyboardButton(f'♻️ ɪɴꜰᴏ', 'info'),
                    InlineKeyboardButton("Languages", callback_data=f"languages#{search.replace(' ', '_')}#{key}"),
                    InlineKeyboardButton(f'ᴛɪᴘs​ ⚜', 'tips')
                ]
            )

        else:
            btn.insert(0, 
                [
                    InlineKeyboardButton(f'♻️ ɪɴꜰᴏ', 'info'),
                    InlineKeyboardButton("Languages", callback_data=f"languages#{search.replace(' ', '_')}#{key}"),
                    InlineKeyboardButton(f'ᴛɪᴘs​ ⚜', 'tips')
                ]
            )
                
    except KeyError:
        grpid = await active_connection(str(query.message.from_user.id))
        await save_group_settings(grpid, 'auto_delete', True)
        settings = await get_settings(query.message.chat.id)
        if settings['auto_delete']:
            btn.insert(0, 
                [
                    InlineKeyboardButton(f'♻️ ɪɴꜰᴏ', 'info'),
                    InlineKeyboardButton("Languages", callback_data=f"languages#{search.replace(' ', '_')}#{key}"),
                    InlineKeyboardButton(f'ᴛɪᴘs​ ⚜', 'tips')
                ]
            )

        else:
            btn.insert(0, 
                [
                    InlineKeyboardButton(f'♻️ ɪɴꜰᴏ', 'info'),
                    InlineKeyboardButton("Languages", callback_data=f"languages#{search.replace(' ', '_')}#{key}"),
                    InlineKeyboardButton(f'ᴛɪᴘs​ ⚜', 'tips')
                ]
            )
    try:
        settings = await get_settings(query.message.chat.id)
        if settings['max_btn']:
            if 0 < offset <= MAX_BTN:
                off_set = 0
            elif offset == 0:
                off_set = None
            else:
                off_set = offset - 10
            if n_offset == 0:
                btn.append(
                    [InlineKeyboardButton("≪ ʙᴀᴄᴋ​", callback_data=f"next_{req}_{key}_{off_set}"), InlineKeyboardButton(f"{math.ceil(int(offset) / MAX_BTN)+1} / {math.ceil(total / MAX_BTN)}", callback_data="pages")]
                )
            elif off_set is None:
                btn.append([InlineKeyboardButton("ᴘᴀɢᴇ​", callback_data="pages"), InlineKeyboardButton(f"{math.ceil(int(offset) / MAX_BTN)+1} / {math.ceil(total / MAX_BTN)}", callback_data="pages"), InlineKeyboardButton("ɴᴇxᴛ​ ≫", callback_data=f"next_{req}_{key}_{n_offset}")])
            else:
                btn.append(
                    [
                        InlineKeyboardButton("≪ ʙᴀᴄᴋ​", callback_data=f"next_{req}_{key}_{off_set}"),
                        InlineKeyboardButton(f"{math.ceil(int(offset) / MAX_BTN)+1} / {math.ceil(total / MAX_BTN)}", callback_data="pages"),
                        InlineKeyboardButton("ɴᴇxᴛ​ ≫", callback_data=f"next_{req}_{key}_{n_offset}")
                    ],
                )
        else:
            if 0 < offset <= int(MAX_B_TN):
                off_set = 0
            elif offset == 0:
                off_set = None
            else:
                off_set = offset - int(MAX_B_TN)
            if n_offset == 0:
                btn.append(
                    [InlineKeyboardButton("≪ ʙᴀᴄᴋ​", callback_data=f"next_{req}_{key}_{off_set}"), InlineKeyboardButton(f"{math.ceil(int(offset)/int(MAX_B_TN))+1} / {math.ceil(total/int(MAX_B_TN))}", callback_data="pages")]
                )
            elif off_set is None:
                btn.append([InlineKeyboardButton("ᴘᴀɢᴇ​", callback_data="pages"), InlineKeyboardButton(f"{math.ceil(int(offset)/int(MAX_B_TN))+1} / {math.ceil(total/int(MAX_B_TN))}", callback_data="pages"), InlineKeyboardButton("ɴᴇxᴛ​ ≫", callback_data=f"next_{req}_{key}_{n_offset}")])
            else:
                btn.append(
                    [
                        InlineKeyboardButton("≪ ʙᴀᴄᴋ​", callback_data=f"next_{req}_{key}_{off_set}"),
                        InlineKeyboardButton(f"{math.ceil(int(offset)/int(MAX_B_TN))+1} / {math.ceil(total/int(MAX_B_TN))}", callback_data="pages"),
                        InlineKeyboardButton("ɴᴇxᴛ​ ≫", callback_data=f"next_{req}_{key}_{n_offset}")
                    ],
                )
    except KeyError:
        await save_group_settings(query.message.chat.id, 'max_btn', False)
        settings = await get_settings(query.message.chat.id)
        if settings['max_btn']:
            if 0 < offset <= 10:
                off_set = 0
            elif offset == 0:
                off_set = None
            else:
                off_set = offset - 10
            if n_offset == 0:
                btn.append(
                    [InlineKeyboardButton("ɴᴇxᴛ​ ≫", callback_data=f"next_{req}_{key}_{off_set}"), InlineKeyboardButton(f"{math.ceil(int(offset)/10)+1} / {math.ceil(total/10)}", callback_data="pages")]
                )
            elif off_set is None:
                btn.append([InlineKeyboardButton("ᴘᴀɢᴇ​", callback_data="pages"), InlineKeyboardButton(f"{math.ceil(int(offset)/10)+1} / {math.ceil(total/10)}", callback_data="pages"), InlineKeyboardButton("ɴᴇxᴛ​ ≫", callback_data=f"next_{req}_{key}_{n_offset}")])
            else:
                btn.append(
                    [
                        InlineKeyboardButton("≪ ʙᴀᴄᴋ​", callback_data=f"next_{req}_{key}_{off_set}"),
                        InlineKeyboardButton(f"{math.ceil(int(offset)/10)+1} / {math.ceil(total/10)}", callback_data="pages"),
                        InlineKeyboardButton("ɴᴇxᴛ​ ≫", callback_data=f"next_{req}_{key}_{n_offset}")
                    ],
                )
        else:
            if 0 < offset <= int(MAX_B_TN):
                off_set = 0
            elif offset == 0:
                off_set = None
            else:
                off_set = offset - int(MAX_B_TN)
            if n_offset == 0:
                btn.append(
                    [InlineKeyboardButton("≪ ʙᴀᴄᴋ​", callback_data=f"next_{req}_{key}_{off_set}"), InlineKeyboardButton(f"{math.ceil(int(offset)/int(MAX_B_TN))+1} / {math.ceil(total/int(MAX_B_TN))}", callback_data="pages")]
                )
            elif off_set is None:
                btn.append([InlineKeyboardButton("ᴘᴀɢᴇ​", callback_data="pages"), InlineKeyboardButton(f"{math.ceil(int(offset)/int(MAX_B_TN))+1} / {math.ceil(total/int(MAX_B_TN))}", callback_data="pages"), InlineKeyboardButton("ɴᴇxᴛ​ ≫", callback_data=f"next_{req}_{key}_{n_offset}")])
            else:
                btn.append(
                    [
                        InlineKeyboardButton("≪ ʙᴀᴄᴋ​", callback_data=f"next_{req}_{key}_{off_set}"),
                        InlineKeyboardButton(f"{math.ceil(int(offset)/int(MAX_B_TN))+1} / {math.ceil(total/int(MAX_B_TN))}", callback_data="pages"),
                        InlineKeyboardButton("ɴᴇxᴛ​ ≫", callback_data=f"next_{req}_{key}_{n_offset}")
                    ],
                )
    btn.insert(0, [
        InlineKeyboardButton(f'⛔️ ᴊᴏɪɴ ꜰᴏʀ ɴᴇᴡ ᴍᴏᴠɪᴇs​ ⛔️', url='https://t.me/nasrani_update')
    ])






    if SELECT[int(req)] == "ACTIVE":
        btn.append(
            [InlineKeyboardButton(text=f"De-Select", callback_data=f"deselect_{req}_{key}_{offset}"),
             InlineKeyboardButton(text="Send", callback_data=f"send_{req}_{key}_{offset}")]
        )
    else:
        btn.append(
            [InlineKeyboardButton(text="Select", callback_data=f"select_{req}_{key}_{offset}")]
        )

    btn.insert(0, [
        InlineKeyboardButton("⭕️ Nᴇᴡ Uᴘᴅᴀᴛᴇs ⭕️", url="https://t.me/UFSFilmUpdate")
    ])

    btn.insert(0, [
        InlineKeyboardButton("⭕️ ᴘᴍ ᴍᴇ ⭕️", url="https://t.me/UFSChatBot"),
        InlineKeyboardButton("⚜ ɴᴇᴡ ᴍᴏᴠɪᴇs ⚜", url="https://t.me/UFSNewRelease")
    ])
    try:
        await query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(btn)
        )    
    except MessageNotModified:
        pass
    await query.answer()






    try:
        await query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(btn)
        )
    except MessageNotModified:
        pass
    await query.answer()


@Client.on_callback_query(filters.regex(r"^spol"))
async def advantage_spoll_choker(bot, query):
    _, user, movie_ = query.data.split('#')
    movies = SPELL_CHECK.get(query.message.reply_to_message.id)
    if not movies:
        return await query.answer(script.OLD_ALRT_TXT.format(query.from_user.first_name), show_alert=True)
    if int(user) != 0 and query.from_user.id != int(user):
        return await query.answer(script.ALRT_TXT.format(query.from_user.first_name), show_alert=True)
    if movie_ == "close_spellcheck":
        return await query.message.delete()
    movie = movies[(int(movie_))]
    await query.answer(script.TOP_ALRT_MSG)
    k = await manual_filters(bot, query.message, text=movie)
    if k == False:
        files, offset, total_results = await get_search_results(query.message.chat.id, movie, offset=0, filter=True)
        if files:
            k = (movie, files, offset, total_results)
            await auto_filter(bot, query, k)
        else:
            reqstr1 = query.from_user.id if query.from_user else 0
            reqstr = await bot.get_users(reqstr1)
            if NO_RESULTS_MSG:
                await bot.send_message(chat_id=LOG_CHANNEL, text=(script.NORSLTS.format(reqstr.id, reqstr.mention, movie)))
            k = await query.message.edit(script.MVE_NT_FND)
            await asyncio.sleep(10)
            await k.delete()

#languages

@Client.on_callback_query(filters.regex(r"^languages#"))
async def languages_cb_handler(client: Client, query: CallbackQuery):

    if int(query.from_user.id) not in [query.message.reply_to_message.from_user.id, 0]:
        return await query.answer(
            f"⚠️ 𝗛𝗲𝘆, {query.from_user.first_name}.. \n\n𝗦𝗲𝗮𝗿𝗰𝗵 𝗬𝗼𝘂𝗿 𝗢𝘄𝗻𝗲𝗿 𝗙𝗶𝗹𝗲,\n\n⚠️𝗗𝗼𝗻'𝘁 𝗖𝗹𝗶𝗰𝗸 𝗢𝘁𝗵𝗲𝗿𝘀 𝗥𝗲𝘀𝘂𝗹𝘁𝘀 😬",
            show_alert=True,
        )
    
    _, search, key = query.data.split("#")

    btn = [
        [
            InlineKeyboardButton(
                text=lang.title(),
                callback_data=f"fl#{lang.lower()}#{search}#{key}"
                ),
        ]
        for lang in LANGUAGES
    ]

    btn.insert(
        0,
        [
            InlineKeyboardButton(
                text="Select your languages", callback_data="ident"
            )
        ],
    )
    req = query.from_user.id
    offset = 0
    btn.append([InlineKeyboardButton(text="Back to files", callback_data=f"next_{req}_{key}_{offset}")])

    await query.edit_message_reply_markup(InlineKeyboardMarkup(btn))


@Client.on_callback_query(filters.regex(r"^fl#"))
async def filter_languages_cb_handler(client: Client, query: CallbackQuery):
    _, lang, search, key = query.data.split("#")

    search = search.replace("_", " ")
    req = query.from_user.id
    chat_id = query.message.chat.id
    message = query.message
    if int(req) not in [query.message.reply_to_message.from_user.id, 0]:
        return await query.answer(
            f"⚠️ 𝗛𝗲𝘆, {query.from_user.first_name}.. \n\n𝗦𝗲𝗮𝗿𝗰𝗵 𝗬𝗼𝘂𝗿 𝗢𝘄𝗻𝗲𝗿 𝗙𝗶𝗹𝗲,\n\n⚠️𝗗𝗼𝗻'𝘁 𝗖𝗹𝗶𝗰𝗸 𝗢𝘁𝗵𝗲𝗿𝘀 𝗥𝗲𝘀𝘂𝗹𝘁𝘀 😬",
            show_alert=True,
        )

    search = f"{search} {lang}" 

    files, _, _ = await get_search_results(chat_id, search, max_results=10)
    files = [file for file in files if re.search(lang, file.file_name, re.IGNORECASE)]
    if not files:
        await query.answer("No files were found", show_alert=1)
        return

    settings = await get_settings(message.chat.id)
    if 'is_shortlink' in settings.keys():
        ENABLE_SHORTLINK = settings['is_shortlink']
    else:
        await save_group_settings(message.chat.id, 'is_shortlink', False)
        ENABLE_SHORTLINK = False
    pre = 'filep' if settings['file_secure'] else 'file'
    if ENABLE_SHORTLINK == True:
        btn = (
            [
                [
                    InlineKeyboardButton(
                        text=f"[{get_size(file.file_size)}] {file.file_name}",
                        url=await get_shortlink(
                            message.chat.id,
                            f"https://telegram.me/{temp.U_NAME}?start=files_{file.file_id}",
                        ),
                    ),
                ]
                for file in files
            ]
            if settings["button"]
            else [
                [
                    InlineKeyboardButton(
                        text=f"{file.file_name}",
                        url=await get_shortlink(
                            message.chat.id,
                            f"https://telegram.me/{temp.U_NAME}?start=files_{file.file_id}",
                        ),
                    ),
                    InlineKeyboardButton(
                        text=f"{get_size(file.file_size)}",
                        url=await get_shortlink(
                            message.chat.id,
                            f"https://telegram.me/{temp.U_NAME}?start=files_{file.file_id}",
                        ),
                    ),
                ]
                for file in files
            ]
        )
    elif settings["button"]:
        btn = [
            [
                InlineKeyboardButton(
                    text=f"[{get_size(file.file_size)}] {file.file_name}", callback_data=f'{pre}#{file.file_id}'
                ),
            ]
            for file in files
        ]
    else:
        btn = [
            [
                InlineKeyboardButton(
                    text=f"{file.file_name}",
                    callback_data=f'{pre}#{file.file_id}',
                ),
                InlineKeyboardButton(
                    text=f"{get_size(file.file_size)}",
                    callback_data=f'{pre}#{file.file_id}',
                ),
            ]
            for file in files
        ]
    try:
        if settings['auto_delete']:
            btn.insert(
                0,
                [
                    InlineKeyboardButton('ɪɴꜰᴏ', 'reqinfo'),
                    InlineKeyboardButton('ᴍᴏᴠɪᴇ', 'minfo'),
                    InlineKeyboardButton('ꜱᴇʀɪᴇꜱ', 'sinfo'),
                ],
            )

        else:
            btn.insert(
                0,
                [
                    InlineKeyboardButton('ᴍᴏᴠɪᴇ', 'minfo'),
                    InlineKeyboardButton('ꜱᴇʀɪᴇꜱ', 'sinfo'),
                ],
            )

    except KeyError:
        grpid = await active_connection(str(message.from_user.id))
        await save_group_settings(grpid, 'auto_delete', True)
        settings = await get_settings(message.chat.id)
        if settings['auto_delete']:
            btn.insert(
                0,
                [
                    InlineKeyboardButton('ɪɴꜰᴏ', 'reqinfo'),
                    InlineKeyboardButton('ᴍᴏᴠɪᴇ', 'minfo'),
                    InlineKeyboardButton('ꜱᴇʀɪᴇꜱ', 'sinfo'),
                ],
            )

        else:
            btn.insert(
                0,
                [
                    InlineKeyboardButton('ᴍᴏᴠɪᴇ', 'minfo'),
                    InlineKeyboardButton('ꜱᴇʀɪᴇꜱ', 'sinfo'),
                ],
            )

    btn.insert(0, [
        InlineKeyboardButton("⚡ Cʜᴇᴄᴋ Bᴏᴛ PM ⚡", url=f"https://t.me/{temp.U_NAME}")
    ])
    offset = 0

    btn.append(        [
            InlineKeyboardButton(
                text="Back to files",
                callback_data=f"next_{req}_{key}_{offset}"
                ),
        ])


    await query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(btn))




#languages




@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    if query.data == "close_data":
        await query.message.delete()
    elif query.data == "delallconfirm":
        userid = query.from_user.id
        chat_type = query.message.chat.type

        if chat_type == enums.ChatType.PRIVATE:
            grpid = await active_connection(str(userid))
            if grpid is not None:
                grp_id = grpid
                try:
                    chat = await client.get_chat(grpid)
                    title = chat.title
                except:
                    await query.message.edit_text("Make sure I'm present in your group!!", quote=True)
                    return await query.answer(MSG_ALRT)
            else:
                await query.message.edit_text(
                    "I'm not connected to any groups!\nCheck /connections or connect to any groups",
                    quote=True
                )
                return await query.answer(MSG_ALRT)

        elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
            grp_id = query.message.chat.id
            title = query.message.chat.title

        else:
            return await query.answer(MSG_ALRT)

        st = await client.get_chat_member(grp_id, userid)
        if (st.status == enums.ChatMemberStatus.OWNER) or (str(userid) in ADMINS):
            await del_all(query.message, grp_id, title)
        else:
            await query.answer("You need to be Group Owner or an Auth User to do that!", show_alert=True)
    elif query.data == "delallcancel":
        userid = query.from_user.id
        chat_type = query.message.chat.type

        if chat_type == enums.ChatType.PRIVATE:
            await query.message.reply_to_message.delete()
            await query.message.delete()

        elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
            grp_id = query.message.chat.id
            st = await client.get_chat_member(grp_id, userid)
            if (st.status == enums.ChatMemberStatus.OWNER) or (str(userid) in ADMINS):
                await query.message.delete()
                try:
                    await query.message.reply_to_message.delete()
                except:
                    pass
            else:
                await query.answer(script.ALRT_TXT.format(query.from_user.first_name),show_alert=True)
    elif "groupcb" in query.data:
        await query.answer()

        group_id = query.data.split(":")[1]

        act = query.data.split(":")[2]
        hr = await client.get_chat(int(group_id))
        title = hr.title
        user_id = query.from_user.id

        if act == "":
            stat = "CONNECT"
            cb = "connectcb"
        else:
            stat = "DISCONNECT"
            cb = "disconnect"

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"{stat}", callback_data=f"{cb}:{group_id}"),
             InlineKeyboardButton("DELETE", callback_data=f"deletecb:{group_id}")],
            [InlineKeyboardButton("BACK", callback_data="backcb")]
        ])

        await query.message.edit_text(
            f"Group Name : **{title}**\nGroup ID : `{group_id}`",
            reply_markup=keyboard,
            parse_mode=enums.ParseMode.MARKDOWN
        )
        return await query.answer(MSG_ALRT)
    elif "connectcb" in query.data:
        await query.answer()

        group_id = query.data.split(":")[1]

        hr = await client.get_chat(int(group_id))

        title = hr.title

        user_id = query.from_user.id

        mkact = await make_active(str(user_id), str(group_id))

        if mkact:
            await query.message.edit_text(
                f"Connected to **{title}**",
                parse_mode=enums.ParseMode.MARKDOWN
            )
        else:
            await query.message.edit_text('Some error occurred!!', parse_mode=enums.ParseMode.MARKDOWN)
        return await query.answer(MSG_ALRT)
    elif "disconnect" in query.data:
        await query.answer()

        group_id = query.data.split(":")[1]

        hr = await client.get_chat(int(group_id))

        title = hr.title
        user_id = query.from_user.id

        mkinact = await make_inactive(str(user_id))

        if mkinact:
            await query.message.edit_text(
                f"Disconnected from **{title}**",
                parse_mode=enums.ParseMode.MARKDOWN
            )
        else:
            await query.message.edit_text(
                f"Some error occurred!!",
                parse_mode=enums.ParseMode.MARKDOWN
            )
        return await query.answer(MSG_ALRT)
    elif "deletecb" in query.data:
        await query.answer()

        user_id = query.from_user.id
        group_id = query.data.split(":")[1]

        delcon = await delete_connection(str(user_id), str(group_id))

        if delcon:
            await query.message.edit_text(
                "Successfully deleted connection"
            )
        else:
            await query.message.edit_text(
                f"Some error occurred!!",
                parse_mode=enums.ParseMode.MARKDOWN
            )
        return await query.answer(MSG_ALRT)
    elif query.data == "backcb":
        await query.answer()

        userid = query.from_user.id

        groupids = await all_connections(str(userid))
        if groupids is None:
            await query.message.edit_text(
                "There are no active connections!! Connect to some groups first.",
            )
            return await query.answer(MSG_ALRT)
        buttons = []
        for groupid in groupids:
            try:
                ttl = await client.get_chat(int(groupid))
                title = ttl.title
                active = await if_active(str(userid), str(groupid))
                act = " - ACTIVE" if active else ""
                buttons.append(
                    [
                        InlineKeyboardButton(
                            text=f"{title}{act}", callback_data=f"groupcb:{groupid}:{act}"
                        )
                    ]
                )
            except:
                pass
        if buttons:
            await query.message.edit_text(
                "Your connected group details ;\n\n",
                reply_markup=InlineKeyboardMarkup(buttons)
            )
    elif "gfilteralert" in query.data:
        grp_id = query.message.chat.id
        i = query.data.split(":")[1]
        keyword = query.data.split(":")[2]
        reply_text, btn, alerts, fileid = await find_gfilter('gfilters', keyword)
        if alerts is not None:
            alerts = ast.literal_eval(alerts)
            alert = alerts[int(i)]
            alert = alert.replace("\\n", "\n").replace("\\t", "\t")
            await query.answer(alert, show_alert=True)
    elif "alertmessage" in query.data:
        grp_id = query.message.chat.id
        i = query.data.split(":")[1]
        keyword = query.data.split(":")[2]
        reply_text, btn, alerts, fileid = await find_filter(grp_id, keyword)
        if alerts is not None:
            alerts = ast.literal_eval(alerts)
            alert = alerts[int(i)]
            alert = alert.replace("\\n", "\n").replace("\\t", "\t")
            await query.answer(alert, show_alert=True)
    if query.data.startswith("file"):
        ident, file_id = query.data.split("#")
        clicked = query.from_user.id #fetching the ID of the user who clicked the button
        try:
            typed = query.message.reply_to_message.from_user.id #fetching user ID of the user who sent the movie request
        except:
            typed = clicked #if failed, uses the clicked user's ID as requested user ID
        files_ = await get_file_details(file_id)
        if not files_:
            return await query.answer('No such file exist.')
        files = files_[0]
        title = files.file_name
        size = get_size(files.file_size)
        f_caption = files.caption
        settings = await get_settings(query.message.chat.id)
        if CUSTOM_FILE_CAPTION:
            try:
                f_caption = CUSTOM_FILE_CAPTION.format(file_name='' if title is None else title,
                                                       file_size='' if size is None else size,
                                                       file_caption='' if f_caption is None else f_caption)
            except Exception as e:
                logger.exception(e)
            f_caption = f_caption
        if f_caption is None:
            f_caption = f"{files.file_name}"

        try:

            if AUTH_CHANNEL and not await is_subscribed(client, query):
                if clicked == typed:
                    await query.answer(url=f"https://t.me/{temp.U_NAME}?start={ident}_{file_id}")
                    return
                else:
                    await query.answer(f"Hᴇʏ {query.from_user.first_name}, Tʜɪs Is Nᴏᴛ Yᴏᴜʀ Mᴏᴠɪᴇ Rᴇǫᴜᴇsᴛ. Rᴇǫᴜᴇsᴛ Yᴏᴜʀ's !", show_alert=True)
            elif settings['botpm']:
                if clicked == typed:
                    await query.answer(url=f"https://t.me/{temp.U_NAME}?start={ident}_{file_id}")
                    return
                else:
                    await query.answer(f"Hᴇʏ {query.from_user.first_name}, Tʜɪs Is Nᴏᴛ Yᴏᴜʀ Mᴏᴠɪᴇ Rᴇǫᴜᴇsᴛ. Rᴇǫᴜᴇsᴛ Yᴏᴜʀ's !", show_alert=True)
            else:
                if clicked == typed:
                    file_send=await client.send_cached_media(
                        chat_id=FILE_CHANNEL,
                        file_id=file_id,
                        caption=script.CHANNEL_CAP.format(query.from_user.mention, title, query.message.chat.title),
                        protect_content=True if ident == "filep" else False,
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [
                                    InlineKeyboardButton("🔥 ᴄʜᴀɴɴᴇʟ 🔥", url=(MAIN_CHANNEL))
                                ]
                            ]
                        )
                    )
                    Joel_tgx = await query.message.reply_text(
                        script.FILE_MSG.format(query.from_user.mention, title, size),
                        parse_mode=enums.ParseMode.HTML,
                        reply_markup=InlineKeyboardMarkup(
                            [
                             [
                              InlineKeyboardButton('📥 𝖣𝗈𝗐𝗇𝗅𝗈𝖺𝖽 𝖫𝗂𝗇𝗄 📥 ', url = file_send.link)
                           ],[
                              InlineKeyboardButton("⚠️ 𝖢𝖺𝗇'𝗍 𝖠𝖼𝖼𝖾𝗌𝗌 ❓ 𝖢𝗅𝗂𝖼𝗄 𝖧𝖾𝗋𝖾 ⚠️", url=(FILE_FORWARD))
                             ]
                            ]
                        )
                    )
                    if settings['auto_delete']:
                        await asyncio.sleep(600)
                        await Joel_tgx.delete()
                        await file_send.delete()
                else:
                    await query.answer(f"Hᴇʏ {query.from_user.first_name}, Tʜɪs Is Nᴏᴛ Yᴏᴜʀ Mᴏᴠɪᴇ Rᴇǫᴜᴇsᴛ. Rᴇǫᴜᴇsᴛ Yᴏᴜʀ's !", show_alert=True)
                await query.answer('Cʜᴇᴄᴋ PM, I ʜᴀᴠᴇ sᴇɴᴛ ғɪʟᴇs ɪɴ PM', show_alert=True)
        except UserIsBlocked:
            await query.answer('𝐔𝐧𝐛𝐥𝐨𝐜𝐤 𝐭𝐡𝐞 𝐛𝐨𝐭 𝐦𝐚𝐡𝐧 !', show_alert=True)
        except PeerIdInvalid:
            await query.answer(url=f"https://t.me/{temp.U_NAME}?start={ident}_{file_id}")
        except Exception as e:
            await query.answer(url=f"https://t.me/{temp.U_NAME}?start={ident}_{file_id}")
    elif query.data.startswith("checksub"):
        if AUTH_CHANNEL and not await is_subscribed(client, query):
            await query.answer("𝑰 𝑳𝒊𝒌𝒆 𝒀𝒐𝒖𝒓 𝑺𝒎𝒂𝒓𝒕𝒏𝒆𝒔𝒔, 𝑩𝒖𝒕 𝑫𝒐𝒏'𝒕 𝑩𝒆 𝑶𝒗𝒆𝒓𝒔𝒎𝒂𝒓𝒕 😒\n@𝒄𝒊𝒏𝒆𝒎𝒂𝒍𝒂.𝒄𝒐𝒎", show_alert=True)
            return

        ident, file_id = query.data.split("#")
        files_ = await get_file_details(file_id)
        if not files_:
            return await query.answer('No such file exist.')
        files = files_[0]
        title = files.file_name
        size = get_size(files.file_size)
        f_caption = files.caption
        if CUSTOM_FILE_CAPTION:
            try:
                f_caption = CUSTOM_FILE_CAPTION.format(file_name='' if title is None else title,
                                                       file_size='' if size is None else size,
                                                       file_caption='' if f_caption is None else f_caption)
            except Exception as e:
                logger.exception(e)
                f_caption = f_caption
        if f_caption is None:
            f_caption = f"{title}"
        await query.answer()
        await client.send_cached_media(
            chat_id=query.from_user.id,
            file_id=file_id,
            caption=f_caption,
            protect_content=True if ident == 'checksubp' else False
        )
    elif query.data == "predvd":
        k = await client.send_message(chat_id=query.message.chat.id, text="<b>Deleting PreDVDs... Please wait...</b>")
        files, next_offset, total = await get_bad_files(
                                                  'predvd',
                                                  offset=0)
        deleted = 0
        for file in files:
            file_ids = file.file_id
            result = await Media.collection.delete_one({
                '_id': file_ids,
            })
            if result.deleted_count:
                logger.info('PreDVD File Found ! Successfully deleted from database.')
            deleted+=1
        deleted = str(deleted)
        await k.edit_text(text=f"<b>Successfully deleted {deleted} PreDVD files.</b>")

    elif query.data == "camrip":
        k = await client.send_message(chat_id=query.message.chat.id, text="<b>Deleting CamRips... Please wait...</b>")
        files, next_offset, total = await get_bad_files(
                                                  'camrip',
                                                  offset=0)
        deleted = 0
        for file in files:
            file_ids = file.file_id
            result = await Media.collection.delete_one({
                '_id': file_ids,
            })
            if result.deleted_count:
                logger.info('CamRip File Found ! Successfully deleted from database.')
            deleted+=1
        deleted = str(deleted)
        await k.edit_text(text=f"<b>Successfully deleted {deleted} CamRip files.</b>")

    elif query.data == "pages":
        await query.answer()

    elif query.data == "reqinfo":
        await query.answer("⚠ ɪɴꜰᴏʀᴍᴀᴛɪᴏɴ ⚠\n\nᴀꜰᴛᴇʀ 10 ᴍɪɴᴜᴛᴇꜱ ᴛʜɪꜱ ᴍᴇꜱꜱᴀɢᴇ ᴡɪʟʟ ʙᴇ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ᴅᴇʟᴇᴛᴇᴅ\n\nɪꜰ ʏᴏᴜ ᴅᴏ ɴᴏᴛ ꜱᴇᴇ ᴛʜᴇ ʀᴇǫᴜᴇsᴛᴇᴅ ᴍᴏᴠɪᴇ / sᴇʀɪᴇs ꜰɪʟᴇ, ʟᴏᴏᴋ ᴀᴛ ᴛʜᴇ ɴᴇxᴛ ᴘᴀɢᴇ\n\n❣ ᴘᴏᴡᴇʀᴇᴅ ʙʏ ᴄɪɴᴇᴍᴀʟᴀ.ᴄᴏᴍ", show_alert=True)

    elif query.data == "minfo":
        await query.answer("⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯\nᴍᴏᴠɪᴇ ʀᴇǫᴜᴇꜱᴛ ꜰᴏʀᴍᴀᴛ\n⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯\n\nɢᴏ ᴛᴏ ɢᴏᴏɢʟᴇ ➠ ᴛʏᴘᴇ ᴍᴏᴠɪᴇ ɴᴀᴍᴇ ➠ ᴄᴏᴘʏ ᴄᴏʀʀᴇᴄᴛ ɴᴀᴍᴇ ➠ ᴘᴀꜱᴛᴇ ᴛʜɪꜱ ɢʀᴏᴜᴘ\n\nᴇxᴀᴍᴘʟᴇ : ᴀᴠᴀᴛᴀʀ: ᴛʜᴇ ᴡᴀʏ ᴏғ ᴡᴀᴛᴇʀ\n\n🚯 ᴅᴏɴᴛ ᴜꜱᴇ ➠ ':(!,./)\n\n©️ ᴄɪɴᴇᴍᴀʟᴀ.ᴄᴏᴍ", show_alert=True)

    elif query.data == "sinfo":
        await query.answer("⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯\nꜱᴇʀɪᴇꜱ ʀᴇǫᴜᴇꜱᴛ ꜰᴏʀᴍᴀᴛ\n⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯\n\nɢᴏ ᴛᴏ ɢᴏᴏɢʟᴇ ➠ ᴛʏᴘᴇ ᴍᴏᴠɪᴇ ɴᴀᴍᴇ ➠ ᴄᴏᴘʏ ᴄᴏʀʀᴇᴄᴛ ɴᴀᴍᴇ ➠ ᴘᴀꜱᴛᴇ ᴛʜɪꜱ ɢʀᴏᴜᴘ\n\nᴇxᴀᴍᴘʟᴇ : ᴍᴏɴᴇʏ ʜᴇɪsᴛ S01E01\n\n🚯 ᴅᴏɴᴛ ᴜꜱᴇ ➠ ':(!,./)\n\n©️ ᴄɪɴᴇᴍᴀʟᴀ.ᴄᴏᴍ", show_alert=True)      

    elif query.data == "tinfo":
        await query.answer("▣ ᴛɪᴘs ▣\n\n★ ᴛʏᴘᴇ ᴄᴏʀʀᴇᴄᴛ sᴘᴇʟʟɪɴɢ (ɢᴏᴏɢʟᴇ)\n\n★ ɪғ ʏᴏᴜ ɴᴏᴛ ɢᴇᴛ ʏᴏᴜʀ ғɪʟᴇ ɪɴ ᴛʜᴇ ʙᴜᴛᴛᴏɴ ᴛʜᴇɴ ᴛʜᴇ ɴᴇxᴛ sᴛᴇᴘ ɪs ᴄʟɪᴄᴋ ɴᴇxᴛ ʙᴜᴛᴛᴏɴ.\n\n★ ᴄᴏɴᴛɪɴᴜᴇ ᴛʜɪs ᴍᴇᴛʜᴏᴅ ᴛᴏ ɢᴇᴛᴛɪɴɢ ʏᴏᴜ ғɪʟᴇ\n\n❣ ᴘᴏᴡᴇʀᴇᴅ ʙʏ ᴄɪɴᴇᴍᴀʟᴀ. ᴄᴏᴍ", show_alert=True)

    elif query.data == "surprise":
        btn = [[
            InlineKeyboardButton('sᴜʀᴘʀɪsᴇ', callback_data='start')
        ]]
        reply_markup=InlineKeyboardMarkup(btn)
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        await query.message.edit_text(
            text=script.SUR_TXT.format(query.from_user.mention, temp.U_NAME, temp.B_NAME),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )


    elif query.data.startswith("show_option"):
        ident, from_user = query.data.split("#")
        btn = [[
                InlineKeyboardButton("Uɴᴀᴠᴀɪʟᴀʙʟᴇ", callback_data=f"unavailable#{from_user}"),
                InlineKeyboardButton("Uᴘʟᴏᴀᴅᴇᴅ", callback_data=f"uploaded#{from_user}")
             ],[
                InlineKeyboardButton("Aʟʀᴇᴀᴅʏ Aᴠᴀɪʟᴀʙʟᴇ", callback_data=f"already_available#{from_user}")
              ]]
        btn2 = [[
                 InlineKeyboardButton("Vɪᴇᴡ Sᴛᴀᴛᴜs", url=f"{query.message.link}")
               ]]
        if query.from_user.id in ADMINS:
            user = await client.get_users(from_user)
            reply_markup = InlineKeyboardMarkup(btn)
            await query.message.edit_reply_markup(reply_markup)
            await query.answer("Hᴇʀᴇ ᴀʀᴇ ᴛʜᴇ ᴏᴘᴛɪᴏɴs !")
        else:
            await query.answer("Yᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ sᴜғғɪᴄɪᴀɴᴛ ʀɪɢᴛs ᴛᴏ ᴅᴏ ᴛʜɪs !", show_alert=True)
        


    elif query.data.startswith("uploaded"):
        ident, from_user = query.data.split("#")
        btn = [[
                InlineKeyboardButton("✅ Uᴘʟᴏᴀᴅᴇᴅ ✅", callback_data=f"upalert#{from_user}")
              ]]
        btn2 = [[
                 InlineKeyboardButton("Vɪᴇᴡ Sᴛᴀᴛᴜs", url=f"{query.message.link}")
               ]]
        if query.from_user.id in ADMINS:
            user = await client.get_users(from_user)
            reply_markup = InlineKeyboardMarkup(btn)
            content = query.message.text
            await query.message.edit_text(f"<b><strike>{content}</strike></b>")
            await query.message.edit_reply_markup(reply_markup)
            await query.answer("Sᴇᴛ ᴛᴏ Uᴘʟᴏᴀᴅᴇᴅ !")
            try:
                await client.send_message(chat_id=int(from_user), text=f"<b>Hᴇʏ {user.mention}, Yᴏᴜʀ ʀᴇᴏ̨ᴜᴇsᴛ ʜᴀs ʙᴇᴇɴ ᴜᴘʟᴏᴀᴅᴇᴅ ʙʏ ᴏᴜʀ ᴍᴏᴅᴇʀᴀᴛᴏʀs. Kɪɴᴅʟʏ sᴇᴀʀᴄʜ ᴀɢᴀɪɴ.</b>", reply_markup=InlineKeyboardMarkup(btn2))
            except UserIsBlocked:
                await client.send_message(chat_id=int(SUPPORT_CHAT_ID), text=f"<b>Hᴇʏ {user.mention}, Yᴏᴜʀ ʀᴇᴏ̨ᴜᴇsᴛ ʜᴀs ʙᴇᴇɴ ᴜᴘʟᴏᴀᴅᴇᴅ ʙʏ ᴏᴜʀ ᴍᴏᴅᴇʀᴀᴛᴏʀs. Kɪɴᴅʟʏ sᴇᴀʀᴄʜ ᴀɢᴀɪɴ.\n\nNᴏᴛᴇ: Tʜɪs ᴍᴇssᴀɢᴇ ɪs sᴇɴᴛ ᴛᴏ ᴛʜɪs ɢʀᴏᴜᴘ ʙᴇᴄᴀᴜsᴇ ʏᴏᴜ'ᴠᴇ ʙʟᴏᴄᴋᴇᴅ ᴛʜᴇ ʙᴏᴛ. Tᴏ sᴇɴᴅ ᴛʜɪs ᴍᴇssᴀɢᴇ ᴛᴏ ʏᴏᴜʀ PM, Mᴜsᴛ ᴜɴʙʟᴏᴄᴋ ᴛʜᴇ ʙᴏᴛ.</b>", reply_markup=InlineKeyboardMarkup(btn2))
        else:
            await query.answer("Yᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ sᴜғғɪᴄɪᴀɴᴛ ʀɪɢᴛs ᴛᴏ ᴅᴏ ᴛʜɪs !", show_alert=True)
        
    elif query.data.startswith("unavailable"):
        ident, from_user = query.data.split("#")
        btn = [[
                InlineKeyboardButton("⚠️ Uɴᴀᴠᴀɪʟᴀʙʟᴇ ⚠️", callback_data=f"unalert#{from_user}")
              ]]
        btn2 = [[
                 InlineKeyboardButton("Vɪᴇᴡ Sᴛᴀᴛᴜs", url=f"{query.message.link}")
               ]]
        if query.from_user.id in ADMINS:
            user = await client.get_users(from_user)
            reply_markup = InlineKeyboardMarkup(btn)
            content = query.message.text
            await query.message.edit_text(f"<b><strike>{content}</strike></b>")
            await query.message.edit_reply_markup(reply_markup)
            await query.answer("Sᴇᴛ ᴛᴏ Uɴᴀᴠᴀɪʟᴀʙʟᴇ !")
            try:
                await client.send_message(chat_id=int(from_user), text=f"<b>Hᴇʏ {user.mention}, Sᴏʀʀʏ Yᴏᴜʀ ʀᴇᴏ̨ᴜᴇsᴛ ɪs ᴜɴᴀᴠᴀɪʟᴀʙʟᴇ. Sᴏ ᴏᴜʀ ᴍᴏᴅᴇʀᴀᴛᴏʀs ᴄᴀɴ'ᴛ ᴜᴘʟᴏᴀᴅ ɪᴛ.</b>", reply_markup=InlineKeyboardMarkup(btn2))
            except UserIsBlocked:
                await client.send_message(chat_id=int(SUPPORT_CHAT_ID), text=f"<b>Hᴇʏ {user.mention}, Sᴏʀʀʏ Yᴏᴜʀ ʀᴇᴏ̨ᴜᴇsᴛ ɪs ᴜɴᴀᴠᴀɪʟᴀʙʟᴇ. Sᴏ ᴏᴜʀ ᴍᴏᴅᴇʀᴀᴛᴏʀs ᴄᴀɴ'ᴛ ᴜᴘʟᴏᴀᴅ ɪᴛ.\n\nNᴏᴛᴇ: Tʜɪs ᴍᴇssᴀɢᴇ ɪs sᴇɴᴛ ᴛᴏ ᴛʜɪs ɢʀᴏᴜᴘ ʙᴇᴄᴀᴜsᴇ ʏᴏᴜ'ᴠᴇ ʙʟᴏᴄᴋᴇᴅ ᴛʜᴇ ʙᴏᴛ. Tᴏ sᴇɴᴅ ᴛʜɪs ᴍᴇssᴀɢᴇ ᴛᴏ ʏᴏᴜʀ PM, Mᴜsᴛ ᴜɴʙʟᴏᴄᴋ ᴛʜᴇ ʙᴏᴛ.</b>", reply_markup=InlineKeyboardMarkup(btn2))
        else:
            await query.answer("Yᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ sᴜғғɪᴄɪᴀɴᴛ ʀɪɢᴛs ᴛᴏ ᴅᴏ ᴛʜɪs !", show_alert=True)


    elif query.data.startswith("uploaded"):
        ident, from_user = query.data.split("#")
        btn = [[
                InlineKeyboardButton("✅ Uᴘʟᴏᴀᴅᴇᴅ ✅", callback_data=f"upalert#{from_user}")
              ]]
        btn2 = [[
                 InlineKeyboardButton("Vɪᴇᴡ Sᴛᴀᴛᴜs", url=f"{query.message.link}")
               ]]
        if query.from_user.id in ADMINS:
            user = await client.get_users(from_user)
            reply_markup = InlineKeyboardMarkup(btn)
            content = query.message.text
            await query.message.edit_text(f"<b><strike>{content}</strike></b>")
            await query.message.edit_reply_markup(reply_markup)
            await query.answer("Sᴇᴛ ᴛᴏ Uᴘʟᴏᴀᴅᴇᴅ !")
            try:
                await client.send_message(chat_id=int(from_user), text=f"<b>Hᴇʏ {user.mention}, Yᴏᴜʀ ʀᴇᴏ̨ᴜᴇsᴛ ʜᴀs ʙᴇᴇɴ ᴜᴘʟᴏᴀᴅᴇᴅ ʙʏ ᴏᴜʀ ᴍᴏᴅᴇʀᴀᴛᴏʀs. Kɪɴᴅʟʏ sᴇᴀʀᴄʜ ᴀɢᴀɪɴ.</b>", reply_markup=InlineKeyboardMarkup(btn2))
            except UserIsBlocked:
                await client.send_message(chat_id=int(SUPPORT_CHAT_ID), text=f"<b>Hᴇʏ {user.mention}, Yᴏᴜʀ ʀᴇᴏ̨ᴜᴇsᴛ ʜᴀs ʙᴇᴇɴ ᴜᴘʟᴏᴀᴅᴇᴅ ʙʏ ᴏᴜʀ ᴍᴏᴅᴇʀᴀᴛᴏʀs. Kɪɴᴅʟʏ sᴇᴀʀᴄʜ ᴀɢᴀɪɴ.\n\nNᴏᴛᴇ: Tʜɪs ᴍᴇssᴀɢᴇ ɪs sᴇɴᴛ ᴛᴏ ᴛʜɪs ɢʀᴏᴜᴘ ʙᴇᴄᴀᴜsᴇ ʏᴏᴜ'ᴠᴇ ʙʟᴏᴄᴋᴇᴅ ᴛʜᴇ ʙᴏᴛ. Tᴏ sᴇɴᴅ ᴛʜɪs ᴍᴇssᴀɢᴇ ᴛᴏ ʏᴏᴜʀ PM, Mᴜsᴛ ᴜɴʙʟᴏᴄᴋ ᴛʜᴇ ʙᴏᴛ.</b>", reply_markup=InlineKeyboardMarkup(btn2))
        else:
            await query.answer("Yᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ sᴜғғɪᴄɪᴀɴᴛ ʀɪɢᴛs ᴛᴏ ᴅᴏ ᴛʜɪs !", show_alert=True)

    elif query.data.startswith("already_available"):
        ident, from_user = query.data.split("#")
        btn = [[
                InlineKeyboardButton("🟢 Aʟʀᴇᴀᴅʏ Aᴠᴀɪʟᴀʙʟᴇ 🟢", callback_data=f"alalert#{from_user}")
              ]]
        btn2 = [[
                 InlineKeyboardButton("Vɪᴇᴡ Sᴛᴀᴛᴜs", url=f"{query.message.link}")
               ]]
        if query.from_user.id in ADMINS:
            user = await client.get_users(from_user)
            reply_markup = InlineKeyboardMarkup(btn)
            content = query.message.text
            await query.message.edit_text(f"<b><strike>{content}</strike></b>")
            await query.message.edit_reply_markup(reply_markup)
            await query.answer("Sᴇᴛ ᴛᴏ Aʟʀᴇᴀᴅʏ Aᴠᴀɪʟᴀʙʟᴇ !")
            try:
                await client.send_message(chat_id=int(from_user), text=f"<b>Hᴇʏ {user.mention}, Yᴏᴜʀ ʀᴇᴏ̨ᴜᴇsᴛ ɪs ᴀʟʀᴇᴀᴅʏ ᴀᴠᴀɪʟᴀʙʟᴇ ᴏɴ ᴏᴜʀ ʙᴏᴛ's ᴅᴀᴛᴀʙᴀsᴇ. Kɪɴᴅʟʏ sᴇᴀʀᴄʜ ᴀɢᴀɪɴ.</b>", reply_markup=InlineKeyboardMarkup(btn2))
            except UserIsBlocked:
                await client.send_message(chat_id=int(SUPPORT_CHAT_ID), text=f"<b>Hᴇʏ {user.mention}, Yᴏᴜʀ ʀᴇᴏ̨ᴜᴇsᴛ ɪs ᴀʟʀᴇᴀᴅʏ ᴀᴠᴀɪʟᴀʙʟᴇ ᴏɴ ᴏᴜʀ ʙᴏᴛ's ᴅᴀᴛᴀʙᴀsᴇ. Kɪɴᴅʟʏ sᴇᴀʀᴄʜ ᴀɢᴀɪɴ.\n\nNᴏᴛᴇ: Tʜɪs ᴍᴇssᴀɢᴇ ɪs sᴇɴᴛ ᴛᴏ ᴛʜɪs ɢʀᴏᴜᴘ ʙᴇᴄᴀᴜsᴇ ʏᴏᴜ'ᴠᴇ ʙʟᴏᴄᴋᴇᴅ ᴛʜᴇ ʙᴏᴛ. Tᴏ sᴇɴᴅ ᴛʜɪs ᴍᴇssᴀɢᴇ ᴛᴏ ʏᴏᴜʀ PM, Mᴜsᴛ ᴜɴʙʟᴏᴄᴋ ᴛʜᴇ ʙᴏᴛ.</b>", reply_markup=InlineKeyboardMarkup(btn2))
        else:
            await query.answer("Yᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ sᴜғғɪᴄɪᴀɴᴛ ʀɪɢᴛs ᴛᴏ ᴅᴏ ᴛʜɪs !", show_alert=True)
    elif query.data.startswith("alalert"):
        ident, from_user = query.data.split("#")
        if int(query.from_user.id) == int(from_user):
            user = await client.get_users(from_user)
            await query.answer(f"Hᴇʏ {user.first_name}, Yᴏᴜʀ Rᴇᴏ̨ᴜᴇsᴛ ɪs Aʟʀᴇᴀᴅʏ Aᴠᴀɪʟᴀʙʟᴇ !", show_alert=True)
        else:
            await query.answer("Yᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ sᴜғғɪᴄɪᴀɴᴛ ʀɪɢᴛs ᴛᴏ ᴅᴏ ᴛʜɪs !", show_alert=True)

    elif query.data.startswith("upalert"):
        ident, from_user = query.data.split("#")
        if int(query.from_user.id) == int(from_user):
            user = await client.get_users(from_user)
            await query.answer(f"Hᴇʏ {user.first_name}, Yᴏᴜʀ Rᴇᴏ̨ᴜᴇsᴛ ɪs Uᴘʟᴏᴀᴅᴇᴅ !", show_alert=True)
        else:
            await query.answer("Yᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ sᴜғғɪᴄɪᴀɴᴛ ʀɪɢᴛs ᴛᴏ ᴅᴏ ᴛʜɪs !", show_alert=True)
        
    elif query.data.startswith("unalert"):
        ident, from_user = query.data.split("#")
        if int(query.from_user.id) == int(from_user):
            user = await client.get_users(from_user)
            await query.answer(f"Hᴇʏ {user.first_name}, Yᴏᴜʀ Rᴇᴏ̨ᴜᴇsᴛ ɪs Uɴᴀᴠᴀɪʟᴀʙʟᴇ !", show_alert=True)
        else:
            await query.answer("Yᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ sᴜғғɪᴄɪᴀɴᴛ ʀɪɢᴛs ᴛᴏ ᴅᴏ ᴛʜɪs !", show_alert=True)





    elif query.data == "start":
        buttons = [[
            InlineKeyboardButton('× ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘs ×', url=f'http://t.me/{temp.U_NAME}?startgroup=true')
        ], [
            InlineKeyboardButton('🔍 sᴇᴀʀᴄʜ', switch_inline_query_current_chat=''),
            InlineKeyboardButton('ᴏᴡɴ ɪɴғᴏ', url='https://t.me/nasrani_update')
        ], [
            InlineKeyboardButton('ʜᴇʟᴘ', callback_data='help'),
            InlineKeyboardButton('ᴀʙᴏᴜᴛ', callback_data='about')
         ],[
            InlineKeyboardButton('ʙᴀᴄᴋ ᴛᴏ sᴛᴀʀᴛ', callback_data='surprise')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        await query.message.edit_text(
            text=script.START_TXT.format(query.from_user.mention, temp.U_NAME, temp.B_NAME),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
        await query.answer(MSG_ALRT)
    elif query.data == "help":
        buttons = [[
            InlineKeyboardButton('ᴍᴀɴᴜᴀʟ', callback_data='manuelfilter'),
            InlineKeyboardButton('ᴀᴜᴛᴏ', callback_data='autofilter'),
            InlineKeyboardButton('ᴄᴏɴɴᴇᴄᴛ', callback_data='coct')
        ], [
            InlineKeyboardButton('ᴇxᴛʀᴀ', callback_data='extra'),
            InlineKeyboardButton('sᴏɴɢ', callback_data='song'),
            InlineKeyboardButton('ᴛᴛs', callback_data='tts')
        ], [
            InlineKeyboardButton('ᴠɪᴅᴇᴏ', callback_data='video'),
            InlineKeyboardButton('ᴛɢʀᴀᴘʜ', callback_data='tele'),
            InlineKeyboardButton('ɴᴇxᴛ', callback_data='aswin')    
        ], [
            InlineKeyboardButton('ʙᴀᴄᴋ', callback_data='start')      
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        await query.message.edit_text(
            text="▣ ▢ ▢"
        )
        await query.message.edit_text(
            text="▣ ▣ ▢"
        )
        await query.message.edit_text(
            text="▣ ▣ ▣"
        )       
        await query.message.edit_text(                     
            text=script.HELP_TXT.format(query.from_user.mention),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "aswin":
        buttons = [[
             InlineKeyboardButton('ᴀᴜᴅʙᴏᴏᴋ', callback_data='abook'),
             InlineKeyboardButton('ᴄᴏᴠɪᴅ', callback_data='corona'),
             InlineKeyboardButton('ɢᴀᴍᴇs', callback_data='fun')
         ], [
             InlineKeyboardButton('ᴘɪɴɢ', callback_data='pings'),
             InlineKeyboardButton('ᴊsᴏɴᴇ', callback_data='json'),
             InlineKeyboardButton('sᴛɪᴄᴋɪᴅ', callback_data='sticker')
         ], [
             InlineKeyboardButton('ᴡʜᴏɪs', callback_data='whois'),
             InlineKeyboardButton('ᴜʀʟsʜᴏʀᴛ', callback_data='urlshort'),
             InlineKeyboardButton('ɴᴇxᴛ', callback_data='aswins')  
        ], [
            InlineKeyboardButton('ʙᴀᴄᴋ', callback_data='help')         
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        await query.message.edit_text(
            text="▣ ▢ ▢"
        )
        await query.message.edit_text(
            text="▣ ▣ ▢"
        )
        await query.message.edit_text(
            text="▣ ▣ ▣"
        )       
        await query.message.edit_text(                     
            text=script.HELP_TXT.format(query.from_user.mention),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "aswins":
        buttons = [[
             InlineKeyboardButton('ғᴏɴᴛ', callback_data='font'),
             InlineKeyboardButton('ɢᴛʀᴀɴs', callback_data='gtrans'),
             InlineKeyboardButton('ᴄᴀʀʙᴏɴ', callback_data='carb'),
        ],  [
             InlineKeyboardButton('ᴄᴏᴜɴᴛʀʏ', callback_data='country'),
             InlineKeyboardButton('ᴅᴇᴘʟᴏʏ', callback_data='deploy'),
             InlineKeyboardButton('ʜᴏᴍᴇ', callback_data='start')
        ], [
             InlineKeyboardButton('ʙᴀᴄᴋ', callback_data='aswin')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        await query.message.edit_text(
            text="▣ ▢ ▢"
        )
        await query.message.edit_text(
            text="▣ ▣ ▢"
        )
        await query.message.edit_text(
            text="▣ ▣ ▣"
        )
        await query.message.edit_text(                     
            text=script.HELP_TXT.format(query.from_user.mention),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "about":
        buttons = [[
            InlineKeyboardButton('sᴛᴀᴛᴜs', callback_data='stats'),
            InlineKeyboardButton('sᴏᴜʀᴄᴇ', callback_data='source')
        ], [
            InlineKeyboardButton('ʜᴏᴍᴇ', callback_data='start'),
            InlineKeyboardButton('ᴄʟᴏsᴇ', callback_data='close_data')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        await query.message.edit_text(
            text=script.ABOUT_TXT.format(temp.B_NAME),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "source":
        buttons = [[
            InlineKeyboardButton('ʀᴇᴘᴏ', url='https://t.me/nasrani_update'),
            InlineKeyboardButton('ʙᴀᴄᴋ', callback_data='about')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.SOURCE_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "manuelfilter":
        buttons = [[
            InlineKeyboardButton('ʙᴀᴄᴋ', callback_data='help'),
            InlineKeyboardButton('ʙᴜᴛᴛᴏɴs', callback_data='button')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.MANUELFILTER_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "button":
        buttons = [[
            InlineKeyboardButton('ʙᴀᴄᴋ', callback_data='manuelfilter')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.BUTTON_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "autofilter":
        buttons = [[
            InlineKeyboardButton('ʙᴀᴄᴋ', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.AUTOFILTER_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "coct":
        buttons = [[
            InlineKeyboardButton('ʙᴀᴄᴋ', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.CONNECTION_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "extra":
        buttons = [[
            InlineKeyboardButton('ʙᴀᴄᴋ', callback_data='help'),
            InlineKeyboardButton('ᴀᴅᴍɪɴ', callback_data='admin')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.EXTRAMOD_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "admin":
        buttons = [[
            InlineKeyboardButton('ʙᴀᴄᴋ', callback_data='extra')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.ADMIN_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "song":
        buttons = [[
            InlineKeyboardButton('ʙᴀᴄᴋ', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.SONG_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "video":
        buttons = [[
            InlineKeyboardButton('ʙᴀᴄᴋ', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.VIDEO_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "tts":
        buttons = [[
            InlineKeyboardButton('ʙᴀᴄᴋ', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.TTS_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "gtrans":
        buttons = [[
            InlineKeyboardButton('ʙᴀᴄᴋ', callback_data='aswins'),
            InlineKeyboardButton('𝙻𝙰𝙽𝙶 𝙲𝙾𝙳𝙴𝚂', url='https://cloud.google.com/translate/docs/languages')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.GTRANS_TXT,
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "country":
        buttons = [[
            InlineKeyboardButton('ʙᴀᴄᴋ', callback_data='aswins'),
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.CON_TXT,
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "tele":
        buttons = [[
            InlineKeyboardButton('ʙᴀᴄᴋ', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.TELE_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "corona":
        buttons = [[
            InlineKeyboardButton('ʙᴀᴄᴋ', callback_data='aswin')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.CORONA_TXT,
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "abook":
        buttons = [[
            InlineKeyboardButton('ʙᴀᴄᴋ', callback_data='aswin')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.ABOOK_TXT,
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "deploy":
        buttons = [[
           InlineKeyboardButton('ʀᴇᴘᴏ', url='https://t.me/nasrani_update'),
           InlineKeyboardButton('ᴏᴡɴᴇʀ', url='https://t.me/nasrani_update')
        ], [
            InlineKeyboardButton('ʙᴀᴄᴋ', callback_data='aswin')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.DEPLOY_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "sticker":
        buttons = [[
            InlineKeyboardButton('ʙᴀᴄᴋ', callback_data='aswin')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.STICKER_TXT,
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "pings":
        buttons = [[
            InlineKeyboardButton('ʙᴀᴄᴋ', callback_data='aswin')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.PINGS_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "json":
        buttons = [[
            InlineKeyboardButton('ʙᴀᴄᴋ', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.JSON_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "urlshort":
        buttons = [[
            InlineKeyboardButton('ʙᴀᴄᴋ', callback_data='aswin')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.URLSHORT_TXT,
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "whois":
        buttons = [[
            InlineKeyboardButton('ʙᴀᴄᴋ', callback_data='aswin')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.WHOIS_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "font":
        buttons = [[
            InlineKeyboardButton('ʙᴀᴄᴋ', callback_data='aswins')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.FONT_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "carb":
        buttons = [[
            InlineKeyboardButton('ʙᴀᴄᴋ', callback_data='aswins')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.CARB_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "fun":
        buttons = [[
            InlineKeyboardButton('ʙᴀᴄᴋ', callback_data='aswin')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.FUN_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "stats":
        buttons = [[
            InlineKeyboardButton('ʙᴀᴄᴋ', callback_data='start'),
            InlineKeyboardButton('ʀᴇғʀᴇsʜ', callback_data='rfrsh')
        ]]
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        reply_markup = InlineKeyboardMarkup(buttons)
        total = await Media.count_documents()
        users = await db.total_users_count()
        chats = await db.total_chat_count()
        monsize = await db.get_db_size()
        free = 536870912 - monsize
        monsize = get_size(monsize)
        free = get_size(free)
        await query.message.edit_text(
            text=script.STATUS_TXT.format(total, users, chats, monsize, free),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "rfrsh":
        await query.answer("𝙁𝙚𝙩𝙘𝙝𝙞𝙣𝙜 𝙈𝙤𝙣𝙜𝙤𝘿𝙗 𝘿𝙖𝙩𝙖𝘽𝙖𝙨𝙚")
        buttons = [[
            InlineKeyboardButton('ʙᴀᴄᴋ', callback_data='stats'),
            InlineKeyboardButton('ʀᴇғʀᴇsʜ', callback_data='rfrsh')
        ]]
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        reply_markup = InlineKeyboardMarkup(buttons)
        total = await Media.count_documents()
        users = await db.total_users_count()
        chats = await db.total_chat_count()
        monsize = await db.get_db_size()
        free = 536870912 - monsize
        monsize = get_size(monsize)
        free = get_size(free)
        await query.message.edit_text(
            text=script.STATUS_TXT.format(total, users, chats, monsize, free),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data.startswith("setgs"):
        ident, set_type, status, grp_id = query.data.split("#")
        grpid = await active_connection(str(query.from_user.id))

        if str(grp_id) != str(grpid):
            await query.message.edit("Your Active Connection Has Been Changed. Go To /settings.")
            return await query.answer(MSG_ALRT)

        if status == "True":
            await save_group_settings(grpid, set_type, False)
        else:
            await save_group_settings(grpid, set_type, True)

        settings = await get_settings(grpid)
        try:
            if settings['auto_delete']:
                settings = await get_settings(grp_id)
        except KeyError:
            await save_group_settings(grp_id, 'auto_delete', True)
            settings = await get_settings(grp_id)

        if settings is not None:
            buttons = [
                [
                    InlineKeyboardButton('Fɪʟᴛᴇʀ Bᴜᴛᴛᴏɴ',
                                         callback_data=f'setgs#button#{settings["button"]}#{str(grp_id)}'),
                    InlineKeyboardButton('Single' if settings["button"] else 'Double',
                                         callback_data=f'setgs#button#{settings["button"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Redirect To', callback_data=f'setgs#botpm#{settings["botpm"]}#{str(grp_id)}'),
                    InlineKeyboardButton('Bot PM' if settings["botpm"] else 'Channel',
                                         callback_data=f'setgs#botpm#{settings["botpm"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Pʀᴏᴛᴇᴄᴛ Cᴏɴᴛᴇɴᴛ',
                                         callback_data=f'setgs#file_secure#{settings["file_secure"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✅ Yes' if settings["file_secure"] else '❌ No',
                                         callback_data=f'setgs#file_secure#{settings["file_secure"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Iᴍᴅʙ', callback_data=f'setgs#imdb#{settings["imdb"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✅ Yes' if settings["imdb"] else '❌ No',
                                         callback_data=f'setgs#imdb#{settings["imdb"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Sᴘᴇʟʟ Cʜᴇᴄᴋ',
                                         callback_data=f'setgs#spell_check#{settings["spell_check"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✅ Yes' if settings["spell_check"] else '❌ No',
                                         callback_data=f'setgs#spell_check#{settings["spell_check"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Wᴇʟᴄᴏᴍᴇ Msɢ', callback_data=f'setgs#welcome#{settings["welcome"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✅ Yes' if settings["welcome"] else '❌ No',
                                         callback_data=f'setgs#welcome#{settings["welcome"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Aᴜᴛᴏ-Dᴇʟᴇᴛᴇ',
                                         callback_data=f'setgs#auto_delete#{settings["auto_delete"]}#{str(grp_id)}'),
                    InlineKeyboardButton('10 Mins' if settings["auto_delete"] else 'OFF',
                                         callback_data=f'setgs#auto_delete#{settings["auto_delete"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Aᴜᴛᴏ-Fɪʟᴛᴇʀ',
                                         callback_data=f'setgs#auto_ffilter#{settings["auto_ffilter"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✔ Oɴ' if settings["auto_ffilter"] else '✘ Oғғ',
                                         callback_data=f'setgs#auto_ffilter#{settings["auto_ffilter"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Mᴀx Bᴜᴛᴛᴏɴs',
                                         callback_data=f'setgs#max_btn#{settings["max_btn"]}#{str(grp_id)}'),
                    InlineKeyboardButton('10' if settings["max_btn"] else f'{MAX_B_TN}',
                                         callback_data=f'setgs#max_btn#{settings["max_btn"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('ShortLink',
                                         callback_data=f'setgs#is_shortlink#{settings["is_shortlink"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✅ ON' if settings["is_shortlink"] else '❌ OFF',
                                         callback_data=f'setgs#is_shortlink#{settings["is_shortlink"]}#{str(grp_id)}')
                ]
                
            ]
            reply_markup = InlineKeyboardMarkup(buttons)
            await query.message.edit_reply_markup(reply_markup)
    await query.answer(MSG_ALRT)


async def auto_filter(client, msg, spoll=False):
    reqstr1 = msg.from_user.id if msg.from_user else 0
    reqstr = await client.get_users(reqstr1)
    if not spoll:
        message = msg
        settings = await get_settings(message.chat.id)
        if message.text.startswith("/"): return  # ignore commands
        if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
            return
        if len(message.text) < 100:
            search = message.text
            files, offset, total_results = await get_search_results(message.chat.id ,search.lower(), offset=0, filter=True)
            if not files:
                if settings["spell_check"]:
                    return await advantage_spell_chok(client, msg)
                else:
                    if NO_RESULTS_MSG:
                        await client.send_message(chat_id=LOG_CHANNEL, text=(script.NORSLTS.format(reqstr.id, reqstr.mention, search)))
                    return
        else:
            return
    else:
        message = msg.message.reply_to_message  # msg will be callback query
        search, files, offset, total_results = spoll
    settings = await get_settings(message.chat.id)
    if 'is_shortlink' in settings.keys():
        ENABLE_SHORTLINK = settings['is_shortlink']
    else:
        await save_group_settings(message.chat.id, 'is_shortlink', False)
        ENABLE_SHORTLINK = False
    pre = 'filep' if settings['file_secure'] else 'file'
    if ENABLE_SHORTLINK == True:
        if settings["button"]:
            btn = [
                [
                    InlineKeyboardButton(
                        text=f"▫️{get_size(file.file_size)} ⊳ {file.file_name}", url=await get_shortlink(message.chat.id, f"https://telegram.me/{temp.U_NAME}?start=files_{file.file_id}")
                    ),
                ]
                for file in files
            ]
        else:
            btn = [
                [
                    InlineKeyboardButton(
                        text=f"{file.file_name}",
                        url=await get_shortlink(message.chat.id, f"https://telegram.me/{temp.U_NAME}?start=files_{file.file_id}")
                    ),
                    InlineKeyboardButton(
                        text=f"{get_size(file.file_size)}",
                        url=await get_shortlink(message.chat.id, f"https://telegram.me/{temp.U_NAME}?start=files_{file.file_id}")
                    ),
                ]
                for file in files
            ]

    else:
        if settings["button"]:
            btn = [
                [
                    InlineKeyboardButton(
                        text=f"▫️{get_size(file.file_size)} ⊳ {file.file_name}", url=await get_shortlink(message.chat.id, f"https://telegram.me/{temp.U_NAME}?start=files_{file.file_id}")
                    ),
                ]
                for file in files
            ]
        else:
            btn = [
                [
                    InlineKeyboardButton(
                        text=f"{file.file_name}",
                        url=await get_shortlink(message.chat.id, f"https://telegram.me/{temp.U_NAME}?start=files_{file.file_id}")
                    ),
                    InlineKeyboardButton(
                        text=f"{get_size(file.file_size)}",
                        url=await get_shortlink(message.chat.id, f"https://telegram.me/{temp.U_NAME}?start=files_{file.file_id}")
                    ),
                ]
                for file in files
            ]

    try:
        key = f"{message.chat.id}-{message.id}"
        BUTTONS[key] = search
        if settings['auto_delete']:
            btn.insert(0, 
                [
                    InlineKeyboardButton(f'♻️ ɪɴꜰᴏ', 'info'),
                    InlineKeyboardButton("Languages", callback_data=f"languages#{search.replace(' ', '_')}#{key}"),
                    InlineKeyboardButton(f'ᴛɪᴘs​ ⚜', 'tips')
                ]
            )

        else:
            btn.insert(0, 
                [
                    InlineKeyboardButton(f'♻️ ɪɴꜰᴏ', 'info'),
                    InlineKeyboardButton("Languages", callback_data=f"languages#{search.replace(' ', '_')}#{key}"),
                    InlineKeyboardButton(f'ᴛɪᴘs​ ⚜', 'tips')
                ]
            )
                
    except KeyError:
        grpid = await active_connection(str(message.from_user.id))
        await save_group_settings(grpid, 'auto_delete', True)
        settings = await get_settings(message.chat.id)
        if settings['auto_delete']:
            btn.insert(0, 
                [
                    InlineKeyboardButton(f'♻️ ɪɴꜰᴏ', 'info'),
                    InlineKeyboardButton("Languages", callback_data=f"languages#{search.replace(' ', '_')}#{key}"),
                    InlineKeyboardButton(f'ᴛɪᴘs​ ⚜', 'tips')
                ]
            )

        else:
            btn.insert(0, 
                [
                    InlineKeyboardButton(f'♻️ ɪɴꜰᴏ', 'info'),
                    InlineKeyboardButton("Languages", callback_data=f"languages#{search.replace(' ', '_')}#{key}"),
                    InlineKeyboardButton(f'ᴛɪᴘs​ ⚜', 'tips')
                ]
            )
    

    btn.insert(0, [
        InlineKeyboardButton(f'⛔️ ᴊᴏɪɴ ꜰᴏʀ ɴᴇᴡ ᴍᴏᴠɪᴇs​ ⛔️', url='https://t.me/nasrani_update')
    ])








    if SELECT[int(req)] == "ACTIVE":
        btn.append(
            [InlineKeyboardButton(text=f"De-Select", callback_data=f"deselect_{req}_{key}_{offset}"),
             InlineKeyboardButton(text="Send", callback_data=f"send_{req}_{key}_{offset}")]
        )
    else:
        btn.append(
            [InlineKeyboardButton(text="Select", callback_data=f"select_{req}_{key}_{offset}")]
        )

    btn.insert(0, [
        InlineKeyboardButton("⭕️ Nᴇᴡ Uᴘᴅᴀᴛᴇs ⭕️", url="https://t.me/UFSFilmUpdate")
    ])

    btn.insert(0, [
        InlineKeyboardButton("⭕️ ᴘᴍ ᴍᴇ ⭕️", url="https://t.me/UFSChatBot"),
        InlineKeyboardButton("⚜ ɴᴇᴡ ᴍᴏᴠɪᴇs ⚜", url="https://t.me/UFSNewRelease")
    ])
    try:
        await query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(btn)
        )
    except MessageNotModified:
        pass
    await query.answer()



    if offset != "":
        key = f"{message.chat.id}-{message.id}"
        BUTTONS[key] = search
        req = message.from_user.id if message.from_user else 0
        try:
            settings = await get_settings(message.chat.id)
            if settings['max_btn']:
                btn.append(
                    [InlineKeyboardButton("ᴘᴀɢᴇ​", callback_data="pages"), InlineKeyboardButton(text=f"1/{math.ceil(int(total_results) / MAX_BTN)}",callback_data="pages"), InlineKeyboardButton(text="ɴᴇxᴛ​ ≫",callback_data=f"next_{req}_{key}_{offset}")]
                )
            else:
                btn.append(
                    [InlineKeyboardButton("ᴘᴀɢᴇ​", callback_data="pages"), InlineKeyboardButton(text=f"1/{math.ceil(int(total_results)/int(MAX_B_TN))}",callback_data="pages"), InlineKeyboardButton(text="ɴᴇxᴛ​ ≫",callback_data=f"next_{req}_{key}_{offset}")]
                )
        except KeyError:
            await save_group_settings(message.chat.id, 'max_btn', False)
            settings = await get_settings(message.chat.id)
            if settings['max_btn']:
                btn.append(
                    [InlineKeyboardButton("ᴘᴀɢᴇ​", callback_data="pages"), InlineKeyboardButton(text=f"1/{math.ceil(int(total_results) / MAX_BTN)}",callback_data="pages"), InlineKeyboardButton(text="ɴᴇxᴛ​ ≫",callback_data=f"next_{req}_{key}_{offset}")]
                )
            else:
                btn.append(
                    [InlineKeyboardButton("ᴘᴀɢᴇ​", callback_data="pages"), InlineKeyboardButton(text=f"1/{math.ceil(int(total_results)/int(MAX_B_TN))}",callback_data="pages"), InlineKeyboardButton(text="ɴᴇxᴛ​ ≫",callback_data=f"next_{req}_{key}_{offset}")]
                )
            
                btn.append(
                    [InlineKeyboardButton(text=f"De-Select", callback_data=f"deselect_{req}_{key}_{offset}"),
                     InlineKeyboardButton(text="Send", callback_data=f"send_{req}_{key}_{offset}")]
                )
            
                btn.append(
                    [InlineKeyboardButton(text="Select", callback_data=f"select_{req}_{key}_{offset}")]
                )




    else:
        btn.append(
            [InlineKeyboardButton(text="🔘 ɴᴏ ᴍᴏʀᴇ ᴘᴀɢᴇs​ 🔘",callback_data="pages")]
        )
    imdb = await get_poster(search, file=(files[0]).file_name) if settings["imdb"] else None
    TEMPLATE = settings['template']
    if imdb:
        cap = TEMPLATE.format(
            query=search,
            title=imdb['title'],
            votes=imdb['votes'],
            aka=imdb["aka"],
            seasons=imdb["seasons"],
            box_office=imdb['box_office'],
            localized_title=imdb['localized_title'],
            kind=imdb['kind'],
            imdb_id=imdb["imdb_id"],
            cast=imdb["cast"],
            runtime=imdb["runtime"],
            countries=imdb["countries"],
            certificates=imdb["certificates"],
            languages=imdb["languages"],
            director=imdb["director"],
            writer=imdb["writer"],
            producer=imdb["producer"],
            composer=imdb["composer"],
            cinematographer=imdb["cinematographer"],
            music_team=imdb["music_team"],
            distributors=imdb["distributors"],
            release_date=imdb['release_date'],
            year=imdb['year'],
            genres=imdb['genres'],
            poster=imdb['poster'],
            plot=imdb['plot'],
            rating=imdb['rating'],
            url=imdb['url'],
            **locals()
        )
    else:
        cap = f"<b><i>𝙃𝙚𝙧𝙚 𝙞𝙨 𝙬𝙝𝙖𝙩 𝙞𝙨 𝙛𝙤𝙪𝙣𝙙 𝙮𝙤𝙪𝙧 𝙦𝙪𝙚𝙧𝙮:\n {search}\n👤𝙍𝙚𝙦𝙪𝙚𝙨𝙩𝙚𝙙 𝘽𝙮 : {message.from_user.mention}\n👥𝙂𝙧𝙤𝙪𝙥 : {message.chat.title}</i></b>"
    if imdb and imdb.get('poster'):
        try:
            if message.chat.id == SUPPORT_CHAT_ID:
                await message.reply_text(f"<b>Hᴇʏ {message.from_user.mention}, {str(total_results)} ʀᴇsᴜʟᴛs ᴀʀᴇ ғᴏᴜɴᴅ ɪɴ ᴍʏ ᴅᴀᴛᴀʙᴀsᴇ ғᴏʀ ʏᴏᴜʀ ᴏ̨ᴜᴇʀʏ {search}. Kɪɴᴅʟʏ ᴜsᴇ ɪɴʟɪɴᴇ sᴇᴀʀᴄʜ ᴏʀ ᴍᴀᴋᴇ ᴀ ɢʀᴏᴜᴘ ᴀɴᴅ ᴀᴅᴅ ᴍᴇ ᴀs ᴀᴅᴍɪɴ ᴛᴏ ɢᴇᴛ ᴍᴏᴠɪᴇ ғɪʟᴇs. Tʜɪs ɪs ᴀ sᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ sᴏ ᴛʜᴀᴛ ʏᴏᴜ ᴄᴀɴ'ᴛ ɢᴇᴛ ғɪʟᴇs ғʀᴏᴍ ʜᴇʀᴇ...</b>")
            else:
                hehe = await message.reply_photo(photo=imdb.get('poster'), caption=cap[:1024], reply_markup=InlineKeyboardMarkup(btn))
                try:
                    if settings['auto_delete']:
                        await asyncio.sleep(600)
                        await hehe.delete()
                        await message.delete()
                except KeyError:
                    grpid = await active_connection(str(message.from_user.id))
                    await save_group_settings(grpid, 'auto_delete', True)
                    settings = await get_settings(message.chat.id)
                    if settings['auto_delete']:
                        await asyncio.sleep(600)
                        await hehe.delete()
                        await message.delete()
        except (MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty):
            if message.chat.id == SUPPORT_CHAT_ID:
                await message.reply_text(f"<b>Hᴇʏ {message.from_user.mention}, {str(total_results)} ʀᴇsᴜʟᴛs ᴀʀᴇ ғᴏᴜɴᴅ ɪɴ ᴍʏ ᴅᴀᴛᴀʙᴀsᴇ ғᴏʀ ʏᴏᴜʀ ᴏ̨ᴜᴇʀʏ {search}. Kɪɴᴅʟʏ ᴜsᴇ ɪɴʟɪɴᴇ sᴇᴀʀᴄʜ ᴏʀ ᴍᴀᴋᴇ ᴀ ɢʀᴏᴜᴘ ᴀɴᴅ ᴀᴅᴅ ᴍᴇ ᴀs ᴀᴅᴍɪɴ ᴛᴏ ɢᴇᴛ ᴍᴏᴠɪᴇ ғɪʟᴇs. Tʜɪs ɪs ᴀ sᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ sᴏ ᴛʜᴀᴛ ʏᴏᴜ ᴄᴀɴ'ᴛ ɢᴇᴛ ғɪʟᴇs ғʀᴏᴍ ʜᴇʀᴇ...</b>")
            else:
                pic = imdb.get('poster')
                poster = pic.replace('.jpg', "._V1_UX360.jpg")
                hmm = await message.reply_photo(photo=poster, caption=cap[:1024], reply_markup=InlineKeyboardMarkup(btn))
                try:
                    if settings['auto_delete']:
                        await asyncio.sleep(600)
                        await hmm.delete()
                        await message.delete()
                except KeyError:
                    grpid = await active_connection(str(message.from_user.id))
                    await save_group_settings(grpid, 'auto_delete', True)
                    settings = await get_settings(message.chat.id)
                    if settings['auto_delete']:
                        await asyncio.sleep(600)
                        await hmm.delete()
                        await message.delete()
        except Exception as e:
            if message.chat.id == SUPPORT_CHAT_ID:
                await message.reply_text(f"<b>Hᴇʏ {message.from_user.mention}, {str(total_results)} ʀᴇsᴜʟᴛs ᴀʀᴇ ғᴏᴜɴᴅ ɪɴ ᴍʏ ᴅᴀᴛᴀʙᴀsᴇ ғᴏʀ ʏᴏᴜʀ ᴏ̨ᴜᴇʀʏ {search}. Kɪɴᴅʟʏ ᴜsᴇ ɪɴʟɪɴᴇ sᴇᴀʀᴄʜ ᴏʀ ᴍᴀᴋᴇ ᴀ ɢʀᴏᴜᴘ ᴀɴᴅ ᴀᴅᴅ ᴍᴇ ᴀs ᴀᴅᴍɪɴ ᴛᴏ ɢᴇᴛ ᴍᴏᴠɪᴇ ғɪʟᴇs. Tʜɪs ɪs ᴀ sᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ sᴏ ᴛʜᴀᴛ ʏᴏᴜ ᴄᴀɴ'ᴛ ɢᴇᴛ ғɪʟᴇs ғʀᴏᴍ ʜᴇʀᴇ...</b>")
            else:
                logger.exception(e)
                fek = await message.reply_photo(photo=NOR_IMG, caption=cap, reply_markup=InlineKeyboardMarkup(btn))
                try:
                    if settings['auto_delete']:
                        await asyncio.sleep(600)
                        await fek.delete()
                        await message.delete()
                except KeyError:
                    grpid = await active_connection(str(message.from_user.id))
                    await save_group_settings(grpid, 'auto_delete', True)
                    settings = await get_settings(message.chat.id)
                    if settings['auto_delete']:
                        await asyncio.sleep(600)
                        await fek.delete()
                        await message.delete()
    else:
        if message.chat.id == SUPPORT_CHAT_ID:
            await message.reply_text(f"<b>Hᴇʏ {message.from_user.mention}, {str(total_results)} ʀᴇsᴜʟᴛs ᴀʀᴇ ғᴏᴜɴᴅ ɪɴ ᴍʏ ᴅᴀᴛᴀʙᴀsᴇ ғᴏʀ ʏᴏᴜʀ ᴏ̨ᴜᴇʀʏ {search}. Kɪɴᴅʟʏ ᴜsᴇ ɪɴʟɪɴᴇ sᴇᴀʀᴄʜ ᴏʀ ᴍᴀᴋᴇ ᴀ ɢʀᴏᴜᴘ ᴀɴᴅ ᴀᴅᴅ ᴍᴇ ᴀs ᴀᴅᴍɪɴ ᴛᴏ ɢᴇᴛ ᴍᴏᴠɪᴇ ғɪʟᴇs. Tʜɪs ɪs ᴀ sᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ sᴏ ᴛʜᴀᴛ ʏᴏᴜ ᴄᴀɴ'ᴛ ɢᴇᴛ ғɪʟᴇs ғʀᴏᴍ ʜᴇʀᴇ...</b>")
        else:
            fuk = await message.reply_photo(photo=NOR_IMG, caption=cap, reply_markup=InlineKeyboardMarkup(btn))
            try:
                if settings['auto_delete']:
                    await asyncio.sleep(600)
                    await fuk.delete()
                    await message.delete()
            except KeyError:
                grpid = await active_connection(str(message.from_user.id))
                await save_group_settings(grpid, 'auto_delete', True)
                settings = await get_settings(message.chat.id)
                if settings['auto_delete']:
                    await asyncio.sleep(600)
                    await fuk.delete()
                    await message.delete()
    
    if spoll:
        await msg.message.delete()


async def advantage_spell_chok(client, msg):
    mv_id = msg.id
    mv_rqst = msg.text
    reqstr1 = msg.from_user.id if msg.from_user else 0
    reqstr = await client.get_users(reqstr1)
    settings = await get_settings(msg.chat.id)
    query = re.sub(
        r"\b(pl(i|e)*?(s|z+|ease|se|ese|(e+)s(e)?)|((send|snd|giv(e)?|gib)(\sme)?)|movie(s)?|new|latest|br((o|u)h?)*|^h(e|a)?(l)*(o)*|mal(ayalam)?|t(h)?amil|file|that|find|und(o)*|kit(t(i|y)?)?o(w)?|thar(u)?(o)*w?|kittum(o)*|aya(k)*(um(o)*)?|full\smovie|any(one)|with\ssubtitle(s)?)",
        "", msg.text, flags=re.IGNORECASE)  # plis contribute some common words
    RQST = query.strip()
    query = query.strip() + " movie"
    try:
        movies = await get_poster(mv_rqst, bulk=True)
    except Exception as e:
        logger.exception(e)
        await client.send_message(chat_id=LOG_CHANNEL, text=(script.NORSLTS.format(reqstr.id, reqstr.mention, mv_rqst)))
        k = await msg.reply(script.I_CUDNT.format(reqstr.mention))
        await asyncio.sleep(8)
        await k.delete()
        return
    movielist = []
    if not movies:
        reqst_gle = mv_rqst.replace(" ", "+")
        button = [[
                   InlineKeyboardButton("Gᴏᴏɢʟᴇ", url=f"https://www.google.com/search?q={reqst_gle}")
        ]]
        await client.send_message(chat_id=LOG_CHANNEL, text=(script.NORSLTS.format(reqstr.id, reqstr.mention, mv_rqst)))
        k = await msg.reply_photo(
            photo=SPELL_IMG, 
            caption=script.I_CUDNT.format(mv_rqst),
            reply_markup=InlineKeyboardMarkup(button)
        )
        await asyncio.sleep(30)
        await k.delete()
        return
    movielist += [movie.get('title') for movie in movies]
    movielist += [f"{movie.get('title')} {movie.get('year')}" for movie in movies]
    SPELL_CHECK[mv_id] = movielist
    btn = [
        [
            InlineKeyboardButton(
                text=movie_name.strip(),
                callback_data=f"spol#{reqstr1}#{k}",
            )
        ]
        for k, movie_name in enumerate(movielist)
    ]
    btn.append([InlineKeyboardButton(text="Close", callback_data=f'spol#{reqstr1}#close_spellcheck')])
    spell_check_del = await msg.reply_photo(
        photo=(SPELL_IMG),
        caption=(script.CUDNT_FND.format(reqstr.mention)),
        reply_markup=InlineKeyboardMarkup(btn)
        )

    try:
        if settings['auto_delete']:
            await asyncio.sleep(600)
            await spell_check_del.delete()
    except KeyError:
            grpid = await active_connection(str(message.from_user.id))
            await save_group_settings(grpid, 'auto_delete', True)
            settings = await get_settings(message.chat.id)
            if settings['auto_delete']:
                await asyncio.sleep(600)
                await spell_check_del.delete()

async def manual_filters(client, message, text=False):
    settings = await get_settings(message.chat.id)
    group_id = message.chat.id
    name = text or message.text
    reply_id = message.reply_to_message.id if message.reply_to_message else message.id
    keywords = await get_filters(group_id)
    for keyword in reversed(sorted(keywords, key=len)):
        pattern = r"( |^|[^\w])" + re.escape(keyword) + r"( |$|[^\w])"
        if re.search(pattern, name, flags=re.IGNORECASE):
            reply_text, btn, alert, fileid = await find_filter(group_id, keyword)

            if reply_text:
                reply_text = reply_text.replace("\\n", "\n").replace("\\t", "\t")

            if btn is not None:
                try:
                    if fileid == "None":
                        if btn == "[]":
                            joelkb = await client.send_message(
                                group_id, 
                                reply_text, 
                                disable_web_page_preview=True,
                                protect_content=True if settings["file_secure"] else False,
                                reply_to_message_id=reply_id
                            )
                            try:
                                if settings['auto_ffilter']:
                                    await auto_filter(client, message)
                            except KeyError:
                                grpid = await active_connection(str(message.from_user.id))
                                await save_group_settings(grpid, 'auto_ffilter', True)
                                settings = await get_settings(message.chat.id)
                                if settings['auto_ffilter']:
                                    await auto_filter(client, message)
                            try:
                                if settings['auto_delete']:
                                    await joelkb.delete()
                            except KeyError:
                                grpid = await active_connection(str(message.from_user.id))
                                await save_group_settings(grpid, 'auto_delete', True)
                                settings = await get_settings(message.chat.id)
                                if settings['auto_delete']:
                                    await joelkb.delete()

                        else:
                            button = eval(btn)
                            hmm = await client.send_message(
                                group_id,
                                reply_text,
                                disable_web_page_preview=True,
                                reply_markup=InlineKeyboardMarkup(button),
                                protect_content=True if settings["file_secure"] else False,
                                reply_to_message_id=reply_id
                            )
                            try:
                                if settings['auto_ffilter']:
                                    await auto_filter(client, message)
                            except KeyError:
                                grpid = await active_connection(str(message.from_user.id))
                                await save_group_settings(grpid, 'auto_ffilter', True)
                                settings = await get_settings(message.chat.id)
                                if settings['auto_ffilter']:
                                    await auto_filter(client, message)
                            try:
                                if settings['auto_delete']:
                                    await hmm.delete()
                            except KeyError:
                                grpid = await active_connection(str(message.from_user.id))
                                await save_group_settings(grpid, 'auto_delete', True)
                                settings = await get_settings(message.chat.id)
                                if settings['auto_delete']:
                                    await hmm.delete()

                    elif btn == "[]":
                        oto = await client.send_cached_media(
                            group_id,
                            fileid,
                            caption=reply_text or "",
                            protect_content=True if settings["file_secure"] else False,
                            reply_to_message_id=reply_id
                        )
                        try:
                            if settings['auto_ffilter']:
                                await auto_filter(client, message)
                        except KeyError:
                            grpid = await active_connection(str(message.from_user.id))
                            await save_group_settings(grpid, 'auto_ffilter', True)
                            settings = await get_settings(message.chat.id)
                            if settings['auto_ffilter']:
                                await auto_filter(client, message)
                        try:
                            if settings['auto_delete']:
                                await oto.delete()
                        except KeyError:
                            grpid = await active_connection(str(message.from_user.id))
                            await save_group_settings(grpid, 'auto_delete', True)
                            settings = await get_settings(message.chat.id)
                            if settings['auto_delete']:
                                await oto.delete()

                    else:
                        button = eval(btn)
                        dlt = await message.reply_cached_media(
                            fileid,
                            caption=reply_text or "",
                            reply_markup=InlineKeyboardMarkup(button),
                            reply_to_message_id=reply_id
                        )
                        try:
                            if settings['auto_ffilter']:
                                await auto_filter(client, message)
                        except KeyError:
                            grpid = await active_connection(str(message.from_user.id))
                            await save_group_settings(grpid, 'auto_ffilter', True)
                            settings = await get_settings(message.chat.id)
                            if settings['auto_ffilter']:
                                await auto_filter(client, message)
                        try:
                            if settings['auto_delete']:
                                await dlt.delete()
                        except KeyError:
                            grpid = await active_connection(str(message.from_user.id))
                            await save_group_settings(grpid, 'auto_delete', True)
                            settings = await get_settings(message.chat.id)
                            if settings['auto_delete']:
                                await dlt.delete()

                except Exception as e:
                    logger.exception(e)
                break
    else:
        return False

async def global_filters(client, message, text=False):
    settings = await get_settings(message.chat.id)
    group_id = message.chat.id
    name = text or message.text
    reply_id = message.reply_to_message.id if message.reply_to_message else message.id
    keywords = await get_gfilters('gfilters')
    for keyword in reversed(sorted(keywords, key=len)):
        pattern = r"( |^|[^\w])" + re.escape(keyword) + r"( |$|[^\w])"
        if re.search(pattern, name, flags=re.IGNORECASE):
            reply_text, btn, alert, fileid = await find_gfilter('gfilters', keyword)

            if reply_text:
                reply_text = reply_text.replace("\\n", "\n").replace("\\t", "\t")

            if btn is not None:
                try:
                    if fileid == "None":
                        if btn == "[]":
                            joelkb = await client.send_message(
                                group_id, 
                                reply_text, 
                                disable_web_page_preview=True,
                                reply_to_message_id=reply_id
                            )
                            
                        else:
                            button = eval(btn)
                            hmm = await client.send_message(
                                group_id,
                                reply_text,
                                disable_web_page_preview=True,
                                reply_markup=InlineKeyboardMarkup(button),
                                reply_to_message_id=reply_id
                            )

                    elif btn == "[]":
                        oto = await client.send_cached_media(
                            group_id,
                            fileid,
                            caption=reply_text or "",
                            reply_to_message_id=reply_id
                        )

                    else:
                        button = eval(btn)
                        dlt = await message.reply_cached_media(
                            fileid,
                            caption=reply_text or "",
                            reply_markup=InlineKeyboardMarkup(button),
                            reply_to_message_id=reply_id
                        )

                except Exception as e:
                    logger.exception(e)
                break
    else:
        return False

