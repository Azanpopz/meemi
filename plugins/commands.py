import imp
import os
import logging
import random
import asyncio
from Script import script
from pyrogram import Client, filters, enums
from pyrogram.errors import ChatAdminRequired, FloodWait
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.users_chats_db import db
from database.ia_filterdb import Media, get_file_details, unpack_new_file_id, get_bad_files


from info import CHANNELS, ADMINS, AUTH_CHANNEL, LOG_CHANNEL, PICS, BATCH_FILE_CAPTION, CUSTOM_FILE_CAPTION, PROTECT_CONTENT, MSG_ALRT, MAIN_CHANNEL, MY_CHANNEL, BATCH_GROUP, IMDB_TEMPLATE, IMDB
from info import CHANNELS, ADMINS, AUTH_CHANNEL, LOG_CHANNEL, PICS, BATCH_FILE_CAPTION, CUSTOM_FILE_CAPTION, PROTECT_CONTENT, CHNL_LNK, GRP_LNK, REQST_CHANNEL, SUPPORT_CHAT_ID, MAX_B_TN, VERIFY, MVG_LNK, OWN_LNK

from utils import get_size, is_subscribed, get_poster, search_gagala, temp, get_settings, save_group_settings, get_shortlink

from plugins.fsub import ForceSub
from utils import get_settings, get_size, is_subscribed, save_group_settings, temp, verify_user, check_token, check_verification, get_token

from database.connections_mdb import active_connection
import re
import json
import base64
logger = logging.getLogger(__name__)

BATCH_FILES = {}

force_channel = "nasrani_batch_store"


@Client.on_message(filters.command("start") & filters.incoming)
async def start(client, message):
    if message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        buttons = [
            [
                InlineKeyboardButton('🤖 Updates', url=(MAIN_CHANNEL))
            ],
            [
                InlineKeyboardButton('ʜᴇʟᴘ', url=f"https://t.me/{temp.U_NAME}?start=help"),
            ]
            ]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply(script.START_TXT.format(message.from_user.mention if message.from_user else message.chat.title, temp.U_NAME, temp.B_NAME), reply_markup=reply_markup)
        await asyncio.sleep(2) # 😢 https://github.com/EvamariaTG/EvaMaria/blob/master/plugins/p_ttishow.py#L17 😬 wait a bit, before checking.
        if not await db.get_chat(message.chat.id):
            total=await client.get_chat_members_count(message.chat.id)
            await client.send_message(LOG_CHANNEL, script.LOG_TEXT_G.format(message.chat.title, message.chat.id, total, "Unknown"))       
            await db.add_chat(message.chat.id, message.chat.title)
        return 
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id, message.from_user.first_name)
        await client.send_message(LOG_CHANNEL, script.LOG_TEXT_P.format(message.from_user.id, message.from_user.mention))
    if len(message.command) != 2:
        buttons = [[
            InlineKeyboardButton('× ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘs ×', url=f'http://t.me/{temp.U_NAME}?startgroup=true')
        ], [
            InlineKeyboardButton('🔹ᴀᴜᴛᴏ', callback_data='autofilter'),
            InlineKeyboardButton('ᴀᴅᴅ🔹', callback_data='add')
        ], [
            InlineKeyboardButton('🔹ᴀᴜᴅʙᴏᴏᴋ', callback_data='abook'),
            InlineKeyboardButton('ᴄʜᴀᴛ🔹', callback_data='chat')
        ], [
            InlineKeyboardButton('🔹ᴄᴀʀʙᴏɴ', callback_data='carb'),
            InlineKeyboardButton('ᴄᴏɴɴᴇᴄᴛ🔹', callback_data='coct')
        ], [
            InlineKeyboardButton('🔹ᴄᴏᴠɪᴅ', callback_data='corona'),
            InlineKeyboardButton('ᴄᴏᴜɴᴛʀʏ🔹', callback_data='country')
        ], [
            InlineKeyboardButton('🔹ᴅᴇᴘʟᴏʏ', callback_data='deploy'),
            InlineKeyboardButton('ᴇxᴛʀᴀ🔹', callback_data='extra')
        ], [
            InlineKeyboardButton('🔹ꜰᴏɴᴛ', callback_data='font'),
            InlineKeyboardButton('ɢᴀᴍᴇꜱ🔹', callback_data='fun')
        ], [
            InlineKeyboardButton('🔹ɪᴅ', callback_data='id'),
            InlineKeyboardButton('ᴊꜱᴏɴ🔹', callback_data='json')
        ], [
            InlineKeyboardButton('🔹ᴋᴀɴɢ', callback_data='kang'),
            InlineKeyboardButton('ᴍᴀɴᴜᴇʟ🔹', callback_data='manuelfilter')
        ], [
            InlineKeyboardButton('🔹ᴘɪɴɢ', callback_data='pings'),
            InlineKeyboardButton('Qᴜᴛᴏᴇꜱ🔹', callback_data='quote')
        ], [
            InlineKeyboardButton('🔹ʀᴇQᴜᴇꜱᴛ', callback_data='request'),
            InlineKeyboardButton('ꜱᴛᴀᴛᴜꜱ🔹', callback_data='status')
        ], [
            InlineKeyboardButton('🔹ꜱᴏɴɢ', callback_data='song'),
            InlineKeyboardButton('ꜱᴛɪᴄᴋᴇʀ🔹', callback_data='sticker')
        ], [
            InlineKeyboardButton('🔹ᴛᴛꜱ', callback_data='tts'),
            InlineKeyboardButton('ᴛɢʀᴀᴘʜ🔹', callback_data='tele')
        ], [
            InlineKeyboardButton('🔹ᴛᴏʀʀᴇɴᴛ', callback_data='torrent'),
            InlineKeyboardButton('ᴜʀʟꜱʜᴏʀᴛ🔹', callback_data='urlshort')
        ], [
            InlineKeyboardButton('🔹ᴠɪᴅᴇᴏ', callback_data='video'),
            InlineKeyboardButton('ᴡʜᴏɪꜱ🔹', callback_data='whois')
        ], [
            InlineKeyboardButton('🔹𝐇𝐢𝐝𝐞 𝐂𝐨𝐦𝐦𝐚𝐧𝐝', callback_data='help'),
            InlineKeyboardButton('𝐬𝐩𝐞𝐜𝐢𝐚𝐥🔹', callback_data='about')
        ], [
            InlineKeyboardButton('🔹𝐆𝐫𝐨𝐮𝐩', callback_data='help'),
            InlineKeyboardButton('𝐔𝐩𝐝𝐚𝐭𝐞🔹', callback_data='about')
        ], [
            InlineKeyboardButton('🔹🔸𝐂𝐋𝐎𝐒𝐄🔸🔹', callback_data='close_data')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        m=await message.reply_sticker("CAACAgUAAxkBAAINdmL9uWnC3ptj9YnTjFU4YGr5dtzwAAIEAAPBJDExieUdbguzyBAeBA") 
        await asyncio.sleep(1)
        await m.delete()        
        await message.reply_text(            
            text=script.START_TXT.format(message.from_user.mention, temp.U_NAME, temp.B_NAME),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
        return
    if AUTH_CHANNEL and not await is_subscribed(client, message):
        try:
            invite_link = await client.create_chat_invite_link(int(AUTH_CHANNEL))
        except ChatAdminRequired:
            logger.error("Make sure Bot is admin in Forcesub channel")
            return
        btn = [
                [
                    InlineKeyboardButton(
                        "JOIN CHANNEL", url=invite_link.invite_link
                    ),
                    InlineKeyboardButton(
                        text="NEW MOVIES",
                        url="https://t.me/+cACZdXU2LH8xOGE1"
                    ),
                ]
                
            ]
        
        if message.command[1] != "subscribe":
            try:
                kk, file_id = message.command[1].split("_", 1)
                pre = 'checksubp' if kk == 'filep' else 'checksub' 
                btn.append([InlineKeyboardButton(" 🔄 Try Again", callback_data=f"{pre}#{file_id}")])
            except (IndexError, ValueError):
                btn.append([InlineKeyboardButton(" 🔄 Try Again", url=f"https://t.me/{temp.U_NAME}?start={message.command[1]}")])
        m=await message.reply_sticker("CAACAgUAAxkBAAINdmL9uWnC3ptj9YnTjFU4YGr5dtzwAAIEAAPBJDExieUdbguzyBAeBA")
        await asyncio.sleep(1)
        await m.delete()
        await client.send_message(
            chat_id=message.from_user.id,
            text="**PLEASE JOIN MY UPDATES CHANNEL TO USE TRY AGAIN BUTTON!**",
            reply_markup=InlineKeyboardMarkup(btn),
            parse_mode=enums.ParseMode.MARKDOWN
            )
        
        return
    data = message.command[1]
    try:
        pre, file_id = data.split('_', 1)
    except:
        file_id = data
        pre = ""

    if data.split("-", 1)[0] == "BATCH":
        sts = await message.reply(f"<b><a href='https://t.me/nasrani_batch_store'>ʏᴏᴜʀ ᴍᴏᴠɪᴇ ꜰɪʟᴇꜱ ꜱᴇɴᴅᴇᴅ ᴛʜɪꜱ ɢʀᴏᴜᴘ.. ᴄʜᴀᴇᴄᴋ</a></b>")
        file_id = data.split("-", 1)[1]
        msgs = BATCH_FILES.get(file_id)
        if not msgs:
            file = await client.download_media(file_id)
            try: 
                with open(file) as file_data:
                    msgs=json.loads(file_data.read())
            except:
                await sts.edit("FAILED")
                return await client.send_message(LOG_CHANNEL, "UNABLE TO OPEN FILE.")
            os.remove(file)
            BATCH_FILES[file_id] = msgs
        for msg in msgs:
            title = msg.get("title")
            size=get_size(int(msg.get("size", 0)))
            f_caption=msg.get("caption", "")
            if BATCH_FILE_CAPTION:
                try:
                    f_caption=BATCH_FILE_CAPTION.format(file_name= '' if title is None else title, file_size='' if size is None else size, file_caption='' if f_caption is None else f_caption)
                except Exception as e:
                    logger.exception(e)
                    f_caption=f_caption
            if f_caption is None:
                f_caption = f"{title}"
            try:
                k = await client.send_cached_media(
                    chat_id=force_channel,
                    file_id=msg.get("file_id"),
                    caption=f_caption,      
                    protect_content=msg.get('protect', False),
                    parse_mode=enums.ParseMode.MARKDOWN,
                    reply_markup=InlineKeyboardMarkup(
                                     [
                                         [
                                             InlineKeyboardButton('1🎁𝐀𝐝𝐝 𝐌𝐞 𝐓𝐨 𝐘𝐨𝐮𝐫 𝐆𝐫𝐨𝐮𝐩𝐬🎁', callback_data=f"{pre}#{file_id}")
                                         ],
                                         [
                                             InlineKeyboardButton('🧩𝐆𝐨𝐨𝐠𝐥𝐞🧩', url=f"https://t.me/{temp.U_NAME}?start={message.command[1]}"),
                                             InlineKeyboardButton('☘𝐈𝐦𝐝𝐛☘', url="https://t.me/+YCA-JWZDNsJkNmI1")
                                         ]                            
                                     ]
                                 )
                             )
                
                await message.reply_text(
                    chat_id=BATCH_GROUP,
                    text=script.BATCH_TXT.format(message.from_user.mention, temp.U_NAME, temp.B_NAME),)
                    
                
                
                
            except FloodWait as e:
                await asyncio.sleep(e.x)
                logger.warning(f"Floodwait of {e.x} sec.")
                
                k = await client.send_cached_media(
                    chat_id=message.from_user.id,
                    file_id=msg.get("file_id"),
                    caption=f_caption,      
                    protect_content=msg.get('protect', False),
                    parse_mode=enums.ParseMode.MARKDOWN,
                    reply_markup=InlineKeyboardMarkup(
                                     [
                                         [
                                             InlineKeyboardButton('2🎁𝐀𝐝𝐝 𝐌𝐞 𝐓𝐨 𝐘𝐨𝐮𝐫 𝐆𝐫𝐨𝐮𝐩𝐬🎁', url="https://t.me/+YCA-JWZDNsJkNmI1")
                                         ],
                                         [
                                             InlineKeyboardButton('🧩𝐆𝐨𝐨𝐠𝐥𝐞🧩', url="https://t.me/NasraniChatGroup"),
                                             InlineKeyboardButton('☘𝐈𝐦𝐝𝐛☘', url="https://t.me/+YCA-JWZDNsJkNmI1")
                                         ]                            
                                     ]
                                 )
                             )
                await asyncio.sleep(5)
                await k.delete()
                await message.reply(f"<b><a href='https://t.me/NasraniChatGroup'>Thank For Using Me...</a></b>")
                
                
                
        
                


            except Exception as e:
                logger.warning(e, exc_info=True)
                continue
            
        return
    elif data.split("-", 1)[0] == "DSTORE":
        sts = await message.reply("<b>Please wait...</b>")
        b_string = data.split("-", 1)[1]
        decoded = (base64.urlsafe_b64decode(b_string + "=" * (-len(b_string) % 4))).decode("ascii")
        try:
            f_msg_id, l_msg_id, f_chat_id, protect = decoded.split("_", 3)
        except:
            f_msg_id, l_msg_id, f_chat_id = decoded.split("_", 2)
            protect = "/pbatch" if PROTECT_CONTENT else "batch"
        diff = int(l_msg_id) - int(f_msg_id)
        async for msg in client.iter_messages(int(f_chat_id), int(l_msg_id), int(f_msg_id)):
            if msg.media:
                media = getattr(msg, msg.media.value)
                if BATCH_FILE_CAPTION:
                    try:
                        f_caption=BATCH_FILE_CAPTION.format(file_name=getattr(media, 'file_name', ''), file_size=getattr(media, 'file_size', ''), file_caption=getattr(msg, 'caption', ''))
                    except Exception as e:
                        logger.exception(e)
                        f_caption = getattr(msg, 'caption', '')
                else:
                    media = getattr(msg, msg.media.value)
                    file_name = getattr(media, 'file_name', '')
                    f_caption = getattr(msg, 'caption', file_name)
                try:
                    await msg.copy(message.chat.id, caption=f_caption, protect_content=True if protect == "/pbatch" else False)
                except FloodWait as e:
                    await asyncio.sleep(e.x)
                    await msg.copy(message.chat.id, caption=f_caption, protect_content=True if protect == "/pbatch" else False)
                except Exception as e:
                    logger.exception(e)
                    continue
            elif msg.empty:
                continue
            else:
                try:
                    await msg.copy(message.chat.id, protect_content=True if protect == "/pbatch" else False)
                except FloodWait as e:
                    await asyncio.sleep(e.x)
                    await msg.copy(message.chat.id, protect_content=True if protect == "/pbatch" else False)
                except Exception as e:
                    logger.exception(e)
                    continue
            await asyncio.sleep(1) 
        return await sts.delete()

    elif data.split("-", 1)[0] == "verify":
        userid = data.split("-", 2)[1]
        token = data.split("-", 3)[2]
        if str(message.from_user.id) != str(userid):
            return await message.reply_text(
                text="<b>Invalid link or Expired link !</b>",
                protect_content=True
            )
        is_valid = await check_token(client, userid, token)
        if is_valid == True:
            await message.reply_text(
                text=f"<b>Hey {message.from_user.mention}, You are successfully verified !\nNow you have unlimited access for all movies till today midnight.</b>",
                protect_content=True
            )
            await verify_user(client, userid, token)
        else:
            return await message.reply_text(
                text="<b>Invalid link or Expired link !</b>",
                protect_content=True
            )

    files_ = await get_file_details(file_id)           
    if not files_:
        pre, file_id = ((base64.urlsafe_b64decode(data + "=" * (-len(data) % 4))).decode("ascii")).split("_", 1)
        try:
            if not await check_verification(client, message.from_user.id) and VERIFY == True:
                btn = [[
                    InlineKeyboardButton("Verify", url=await get_token(client, message.from_user.id, f"https://telegram.me/{temp.U_NAME}?start="))
                ]]
                await message.reply_text(
                    text="<b>You are not verified !\nKindly verify to continue !</b>",
                    protect_content=True,
                    reply_markup=InlineKeyboardMarkup(btn)
                )
                return
            msg = await client.send_cached_media(
                chat_id=message.from_user.id,
                file_id=msg.get("file_id"),
                caption=f_caption,      
                protect_content=msg.get('protect', False),
                parse_mode=enums.ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                                 [
                                     [
                                         InlineKeyboardButton('🎁3', url="https://t.me/+YCA-JWZDNsJkNmI1")
                                     ],
                                     [
                                     InlineKeyboardButton('🧩𝐆𝐨𝐨𝐠𝐥𝐞🧩', url="https://t.me/NasraniChatGroup"),
                                     InlineKeyboardButton('☘𝐈𝐦𝐝𝐛☘', url="https://t.me/NasraniChatGroup")
                                     ]                            
                                 ]
                             )
                         )

                
            await message.reply(f"<b><a href='https://t.me/NasraniChatGroup'>Thank For Using Me...</a></b>")
     
            filetype = msg.media
            file = getattr(msg, filetype.value)
            title = file.file_name
            size=get_size(file.file_size)
            f_caption = f"<code>{title}</code>"
            if CUSTOM_FILE_CAPTION:
                try:
                    f_caption=CUSTOM_FILE_CAPTION.format(file_name= '' if title is None else title, file_size='' if size is None else size, file_caption='')
                except:
                    return
            await msg.edit_caption(f_caption)
            return
        except:
            pass
        return await message.reply('No such file exist.')
    files = files_[0]
    title = files.file_name
    size=get_size(files.file_size)
    f_caption=files.caption
    if CUSTOM_FILE_CAPTION:
        try:
            f_caption=CUSTOM_FILE_CAPTION.format(file_name= '' if title is None else title, file_size='' if size is None else size, file_caption='' if f_caption is None else f_caption)
        except Exception as e:
            logger.exception(e)
            f_caption=f_caption
    if f_caption is None:
        f_caption = f"{files.file_name}"
    if not await check_verification(client, message.from_user.id) and VERIFY == True:
        btn = [[
            InlineKeyboardButton("Verify", url=await get_token(client, message.from_user.id, f"https://telegram.me/{temp.U_NAME}?start="))
        ]]
        await message.reply_text(
            text="<b>You are not verified !\nKindly verify to continue !</b>",
            protect_content=True,
            reply_markup=InlineKeyboardMarkup(btn)
        )
        return
    

    await client.send_cached_media(
        chat_id=message.from_user.id,
        file_id=file_id,
        caption=f_caption,      
        protect_content=True if pre == 'filep' else False,
        parse_mode=enums.ParseMode.MARKDOWN,
        reply_markup=InlineKeyboardMarkup(
                         [
                             [
                                 InlineKeyboardButton('4🎁𝐀𝐝𝐝 𝐌𝐞 𝐓𝐨 𝐘𝐨𝐮𝐫 𝐆𝐫𝐨𝐮𝐩𝐬🎁', url="https://t.me/+YCA-JWZDNsJkNmI1")
                             ],
                             [
                                 InlineKeyboardButton('🧩𝐆𝐨𝐨𝐠𝐥𝐞🧩', url="https://imdb.com"),
                                 InlineKeyboardButton('☘𝐈𝐦𝐝𝐛☘', url="https://imdb.com")
                             ]                            
                         ]
                     )
                 )
                    
        
    await message.reply(f"<b><a href='https://t.me/NasraniChatGroup'>Thank For Using Me...</a></b>")
    


@Client.on_message(filters.command('channel') & filters.user(ADMINS))
async def channel_info(bot, message):
           
    """Send basic information of channel"""
    if isinstance(CHANNELS, (int, str)):
        channels = [CHANNELS]
    elif isinstance(CHANNELS, list):
        channels = CHANNELS
    else:
        raise ValueError("Unexpected type of CHANNELS")

    text = '📑 **Indexed channels/groups**\n'
    for channel in channels:
        chat = await bot.get_chat(channel)
        if chat.username:
            text += '\n@' + chat.username
        else:
            text += '\n' + chat.title or chat.first_name

    text += f'\n\n**Total:** {len(CHANNELS)}'

    if len(text) < 4096:
        await message.reply(text)
    else:
        file = 'Indexed channels.txt'
        with open(file, 'w') as f:
            f.write(text)
        await message.reply_document(file)
        os.remove(file)


@Client.on_message(filters.command('logs') & filters.user(ADMINS))
async def log_file(bot, message):
    """Send log file"""
    try:
        await message.reply_document('TelegramBot.log')
    except Exception as e:
        await message.reply(str(e))

@Client.on_message(filters.command('delete') & filters.user(ADMINS))
async def delete(bot, message):
    """Delete file from database"""
    reply = message.reply_to_message
    if reply and reply.media:
        msg = await message.reply("Processing...⏳", quote=True)
    else:
        await message.reply('Reply to file with /delete which you want to delete', quote=True)
        return

    for file_type in ("document", "video", "audio"):
        media = getattr(reply, file_type, None)
        if media is not None:
            break
    else:
        await msg.edit('This is not supported file format')
        return
    
    file_id, file_ref = unpack_new_file_id(media.file_id)

    result = await Media.collection.delete_one({
        '_id': file_id,
    })
    if result.deleted_count:
        await msg.edit('File is successfully deleted from database')
    else:
        file_name = re.sub(r"(_|\-|\.|\+)", " ", str(media.file_name))
        result = await Media.collection.delete_many({
            'file_name': file_name,
            'file_size': media.file_size,
            'mime_type': media.mime_type
            })
        if result.deleted_count:
            await msg.edit('File is successfully deleted from database')
        else:
            # files indexed before https://github.com/EvamariaTG/EvaMaria/commit/f3d2a1bcb155faf44178e5d7a685a1b533e714bf#diff-86b613edf1748372103e94cacff3b578b36b698ef9c16817bb98fe9ef22fb669R39 
            # have original file name.
            result = await Media.collection.delete_many({
                'file_name': media.file_name,
                'file_size': media.file_size,
                'mime_type': media.mime_type
            })
            if result.deleted_count:
                await msg.edit('File is successfully deleted from database')
            else:
                await msg.edit('File not found in database')


@Client.on_message(filters.command('deleteall') & filters.user(ADMINS))
async def delete_all_index(bot, message):
    await message.reply_text(
        'This will delete all indexed files.\nDo you want to continue??',
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="YES", callback_data="autofilter_delete"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="CANCEL", callback_data="close_data"
                    )
                ],
            ]
        ),
        quote=True,
    )


@Client.on_callback_query(filters.regex(r'^autofilter_delete'))
async def delete_all_index_confirm(bot, message):
    await Media.collection.drop()
    await message.answer(MSG_ALRT)
    await message.message.edit('Succesfully Deleted All The Indexed Files.')


@Client.on_message(filters.command('settings'))
async def settings(client, message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"You are anonymous admin. Use /connect {message.chat.id} in PM")
    chat_type = message.chat.type

    if chat_type == enums.ChatType.PRIVATE:
        grpid = await active_connection(str(userid))
        if grpid is not None:
            grp_id = grpid
            try:
                chat = await client.get_chat(grpid)
                title = chat.title
            except:
                await message.reply_text("Make sure I'm present in your group!!", quote=True)
                return
        else:
            await message.reply_text("I'm not connected to any groups!", quote=True)
            return

    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grp_id = message.chat.id
        title = message.chat.title

    else:
        return

    st = await client.get_chat_member(grp_id, userid)
    if (
            st.status != enums.ChatMemberStatus.ADMINISTRATOR
            and st.status != enums.ChatMemberStatus.OWNER
            and str(userid) not in ADMINS
    ):
        return

    settings = await get_settings(grp_id)

    try:
        if settings['max_btn']:
            settings = await get_settings(grp_id)
    except KeyError:
        await save_group_settings(grp_id, 'max_btn', False)
        settings = await get_settings(grp_id)
    if 'is_shortlink' not in settings.keys():
        await save_group_settings(grp_id, 'is_shortlink', False)
    else:
        pass

    if settings is not None:
        buttons = [
            [
                InlineKeyboardButton(
                    'Filter Button',
                    callback_data=f'setgs#button#{settings["button"]}#{grp_id}',
                ),
                InlineKeyboardButton(
                    'Single' if settings["button"] else 'Double',
                    callback_data=f'setgs#button#{settings["button"]}#{grp_id}',
                ),
            ],
            [
                InlineKeyboardButton(
                    'Redirect To',
                    callback_data=f'setgs#botpm#{settings["botpm"]}#{grp_id}',
                ),
                InlineKeyboardButton(
                    'Bot PM' if settings["botpm"] else 'Channel',
                    callback_data=f'setgs#botpm#{settings["botpm"]}#{grp_id}',
                ),
            ],
            [
                InlineKeyboardButton(
                    'File Secure',
                    callback_data=f'setgs#file_secure#{settings["file_secure"]}#{grp_id}',
                ),
                InlineKeyboardButton(
                    '✅ Yes' if settings["file_secure"] else '❌ No',
                    callback_data=f'setgs#file_secure#{settings["file_secure"]}#{grp_id}',
                ),
            ],
            [
                InlineKeyboardButton(
                    'IMDB',
                    callback_data=f'setgs#imdb#{settings["imdb"]}#{grp_id}',
                ),
                InlineKeyboardButton(
                    '✅ Yes' if settings["imdb"] else '❌ No',
                    callback_data=f'setgs#imdb#{settings["imdb"]}#{grp_id}',
                ),
            ],
            [
                InlineKeyboardButton(
                    'Spell Check',
                    callback_data=f'setgs#spell_check#{settings["spell_check"]}#{grp_id}',
                ),
                InlineKeyboardButton(
                    '✅ Yes' if settings["spell_check"] else '❌ No',
                    callback_data=f'setgs#spell_check#{settings["spell_check"]}#{grp_id}',
                ),
            ],
            [
                InlineKeyboardButton(
                    'Welcome',
                    callback_data=f'setgs#welcome#{settings["welcome"]}#{grp_id}',
                ),
                InlineKeyboardButton(
                    '✅ Yes' if settings["welcome"] else '❌ No',
                    callback_data=f'setgs#welcome#{settings["welcome"]}#{grp_id}',
                ),
            ],
            [
                InlineKeyboardButton(
                    'Auto Delete',
                    callback_data=f'setgs#auto_delete#{settings["auto_delete"]}#{grp_id}',
                ),
                InlineKeyboardButton(
                    '10 Mins' if settings["auto_delete"] else 'OFF',
                    callback_data=f'setgs#auto_delete#{settings["auto_delete"]}#{grp_id}',
                ),
            ],
            [
                InlineKeyboardButton(
                    'Aᴜᴛᴏ-Fɪʟᴛᴇʀ',
                    callback_data=f'setgs#auto_ffilter#{settings["auto_ffilter"]}#{grp_id}',
                ),
                InlineKeyboardButton(
                    '✔ Oɴ' if settings["auto_ffilter"] else '✘ Oғғ',
                    callback_data=f'setgs#auto_ffilter#{settings["auto_ffilter"]}#{grp_id}',
                ),
            ],
            [
                InlineKeyboardButton(
                    'Mᴀx Bᴜᴛᴛᴏɴs',
                    callback_data=f'setgs#max_btn#{settings["max_btn"]}#{grp_id}',
                ),
                InlineKeyboardButton(
                    '10' if settings["max_btn"] else f'{MAX_B_TN}',
                    callback_data=f'setgs#max_btn#{settings["max_btn"]}#{grp_id}',
                ),
            ],
            [
                InlineKeyboardButton(
                    'ShortLink',
                    callback_data=f'setgs#is_shortlink#{settings["is_shortlink"]}#{grp_id}',
                ),
                InlineKeyboardButton(
                    '✅ ON' if settings["is_shortlink"] else '❌ OFF',
                    callback_data=f'setgs#is_shortlink#{settings["is_shortlink"]}#{grp_id}',
                ),
            ],
        ]
        
        reply_markup = InlineKeyboardMarkup(buttons)

        await message.reply_text(
            text=f"<b>Change Your Settings for {title} As Your Wish ⚙</b>",
            reply_markup=reply_markup,
            disable_web_page_preview=True,
            parse_mode=enums.ParseMode.HTML,
            reply_to_message_id=message.id
        )





@Client.on_message(filters.command('set_template'))
async def save_template(client, message):
    sts = await message.reply("Checking template")
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"You are anonymous admin. Use /connect {message.chat.id} in PM")
    chat_type = message.chat.type

    if chat_type == enums.ChatType.PRIVATE:
        grpid = await active_connection(str(userid))
        if grpid is not None:
            grp_id = grpid
            try:
                chat = await client.get_chat(grpid)
                title = chat.title
            except:
                await message.reply_text("Make sure I'm present in your group!!", quote=True)
                return
        else:
            await message.reply_text("I'm not connected to any groups!", quote=True)
            return

    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grp_id = message.chat.id
        title = message.chat.title

    else:
        return

    st = await client.get_chat_member(grp_id, userid)
    if (
            st.status != enums.ChatMemberStatus.ADMINISTRATOR
            and st.status != enums.ChatMemberStatus.OWNER
            and str(userid) not in ADMINS
    ):
        return

    if len(message.command) < 2:
        return await sts.edit("No Input!!")
    template = message.text.split(" ", 1)[1]
    await save_group_settings(grp_id, 'template', template)
    await sts.edit(f"Successfully changed template for {title} to\n\n{template}")

@Client.on_message((filters.command(["request", "Request"]) | filters.regex("#request") | filters.regex("#Request")) & filters.group)
async def requests(bot, message):
    if REQST_CHANNEL is None or SUPPORT_CHAT_ID is None: return # Must add REQST_CHANNEL and SUPPORT_CHAT_ID to use this feature
    if message.reply_to_message and SUPPORT_CHAT_ID == message.chat.id:
        message = msg
        search = message.text
        mv_id = message.id
        


        chat_id = message.chat.id
        reporter = str(message.from_user.id)
        mention = message.from_user.mention
        success = True
        content = message.reply_to_message.text
        imdb = await get_poster(search) if IMDB else None
      
        if imdb:
            caption = IMDB_TEMPLATE.format(
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
        
            if imdb and imdb.get('poster'):
                try:
                                                        
                    btn = [[
                            InlineKeyboardButton('View Request', url=f"{message.reply_to_message.link}"),
                            InlineKeyboardButton('Show Options', callback_data=f'show_option#{reporter}')
                          ]]
                    reported_post = await bot.send_message(chat_id=admins, text=f"🤯𝖱𝖾𝗉𝗈𝗋𝗍𝖾𝗋 : {mention} ({reporter})\n\n 𝖬𝖾𝗌𝗌𝖺𝗀𝖾 : {content}", reply_markup=InlineKeyboardMarkup(btn))
                for admin in ADMINS:
                    btn = [[
                            InlineKeyboardButton('View Request', url=f"{message.reply_to_message.link}"),
                            InlineKeyboardButton('Show Options', callback_data=f'show_option#{reporter}')
                          ]]
                   reported_post = await bot.send_message(chat_id=admin, text=f"🙂𝖱𝖾𝗉𝗈𝗋𝗍𝖾𝗋 : {mention} ({reporter})\n \n𝖬𝖾𝗌𝗌𝖺𝗀𝖾 : {content}", reply_markup=InlineKeyboardMarkup(btn))
                   success = True
                    
                    
                                                
                except (MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty):
                    pic = imdb.get('poster')
                    poster = pic.replace('.jpg', "._V1_UX360.jpg")
                    await bot.send_message(chat_id=REQST_CHANNEL, photo=imdb['poster'], text=f"😍𝖱𝖾𝗉𝗈𝗋𝗍𝖾𝗋 : {mention} ({reporter})  \n𝖬𝖾𝗌𝗌𝖺𝗀𝖾 : {content}", reply_markup=InlineKeyboardMarkup(btn))
                                                
                except Exception as e:
                    logger.exception(e)
                    
                try:
                    if REQST_CHANNEL is not None:
                        btn = [[
                                InlineKeyboardButton('View Request', url=f"{message.reply_to_message.link}"),
                                InlineKeyboardButton('Show Options', callback_data=f'show_option#{reporter}')
                               ]]
                        reported_post = await bot.send_message(chat_id=REQST_CHANNEL, text=f"🤯𝖱𝖾𝗉𝗈𝗋𝗍𝖾𝗋 : {mention} ({reporter})\n\n 𝖬𝖾𝗌𝗌𝖺𝗀𝖾 : {content}", reply_markup=InlineKeyboardMarkup(btn))
                        success = True
                    elif len(content) >= 3:
                        for admin in ADMINS:
                            btn = [[
                                InlineKeyboardButton('View Request', url=f"{message.reply_to_message.link}"),
                                InlineKeyboardButton('Show Options', callback_data=f'show_option#{reporter}')
                              ]]
                            reported_post = await bot.send_message(chat_id=admin, text=f"🙂𝖱𝖾𝗉𝗈𝗋𝗍𝖾𝗋 : {mention} ({reporter})\n \n𝖬𝖾𝗌𝗌𝖺𝗀𝖾 : {content}", reply_markup=InlineKeyboardMarkup(btn))
                            success = True
                    else:
                        if len(content) < 3:
                            await message.reply_text("<b>You must type about your request [Minimum 3 Characters]. Requests can't be empty.</b>")
                    if len(content) < 3:
                        success = False
                except Exception as e:
                    await message.reply_text(f"Error: {e}")
                    pass
        
            elif SUPPORT_CHAT_ID == message.chat.id:
                chat_id = message.chat.id
                reporter = str(message.from_user.id)
                mention = message.from_user.mention
                success = True
                content = message.text
                keywords = ["#request", "/request", "#Request", "/Request"]
                for keyword in keywords:
                    if keyword in content:
                        content = content.replace(keyword, "")
                try:
                    if REQST_CHANNEL is not None and len(content) >= 3:
                        btn = [[
                                InlineKeyboardButton('View Request', url=f"{message.link}"),
                                InlineKeyboardButton('Show Options', callback_data=f'show_option#{reporter}')
                              ]]
                        reported_post = await bot.send_message(chat_id=REQST_CHANNEL, text=f"😍𝖱𝖾𝗉𝗈𝗋𝗍𝖾𝗋 : {mention} ({reporter})  \n𝖬𝖾𝗌𝗌𝖺𝗀𝖾 : {content}", reply_markup=InlineKeyboardMarkup(btn))
                        success = True
                    elif len(content) >= 3:
                        for admin in ADMINS:
                            btn = [[
                                InlineKeyboardButton('View Request', url=f"{message.link}"),
                                InlineKeyboardButton('Show Options', callback_data=f'show_option#{reporter}')
                              ]]
                            reported_post = await bot.send_message(chat_id=admin, text=f"🥺𝖱𝖾𝗉𝗈𝗋𝗍𝖾𝗋 : {mention} ({reporter})\n 𝖬𝖾𝗌𝗌𝖺𝗀𝖾 : {content}", reply_markup=InlineKeyboardMarkup(btn))
                            success = True
                    else:
                        if len(content) < 3:
                            await message.reply_text("You must type about your request [Minimum 3 Characters]. Requests can't be empty.")
                    if len(content) < 3:
                        success = False
                except Exception as e:
                    await message.reply_text(f"Error: {e}")
                    pass

            else:
                success = False
    
            if success:
                btn = [[
                        InlineKeyboardButton('View Request', url=f"{reported_post.link}")
                      ]]
                await message.reply_text("<b>Your request has been added! Please wait for some time.</b>", reply_markup=InlineKeyboardMarkup(btn))

        
        




@Client.on_message(filters.command("deletefiles") & filters.user(ADMINS))
async def deletemultiplefiles(bot, message):
    btn = [[
            InlineKeyboardButton("Delete PreDVDs", callback_data="predvd"),
            InlineKeyboardButton("Delete CamRips", callback_data="camrip")
          ]]
    await message.reply_text(
        text="<b>Select the type of files you want to delete !\n\nThis will delete 100 files from the database for the selected type.</b>",
        reply_markup=InlineKeyboardMarkup(btn)
    )


@Client.on_message(filters.command("send") & filters.user(ADMINS))
async def send_msg(bot, message):
    if message.reply_to_message:
        target_id = message.text.split(" ", 1)[1]
        out = "Users Saved In DB Are:\n\n"
        success = False
        try:
            user = await bot.get_users(target_id)
            users = await db.get_all_users()
            async for usr in users:
                out += f"{usr['id']}"
                out += '\n'
            if str(user.id) in str(out):
                await message.reply_to_message.copy(int(user.id))
                success = True
            else:
                success = False
            if success:
                await message.reply_text(f"<b>Your message has been successfully send to {user.mention}.</b>")
            else:
                await message.reply_text("<b>This user didn't started this bot yet !</b>")
        except Exception as e:
            await message.reply_text(f"<b>Error: {e}</b>")
    else:
        await message.reply_text("<b>Use this command as a reply to any message using the target chat id. For eg: /send userid</b>")

@Client.on_message(filters.command("shortlink") & filters.user(ADMINS))
async def shortlink(bot, message):
    chat_type = message.chat.type
    if chat_type == enums.ChatType.PRIVATE:
        return await message.reply_text(f"<b>Hey {message.from_user.mention}, This command only works on groups !</b>")
    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grpid = message.chat.id
        title = message.chat.title
    else:
        return
    data = message.text
    userid = message.from_user.id
    user = await bot.get_chat_member(grpid, userid)
    if user.status != enums.ChatMemberStatus.ADMINISTRATOR and user.status != enums.ChatMemberStatus.OWNER and str(userid) not in ADMINS:
        return await message.reply_text("<b>You don't have access to use this command !</b>")
    else:
        pass
    try:
        command, shortlink_url, api = data.split(" ")
    except:
        return await message.reply_text("<b>Command Incomplete :(\n\nGive me a shortlink and api along with the command !\n\nFormat: <code>/shortlink shorturllink.in 95a8195c40d31e0c3b6baa68813fcecb1239f2e9</code></b>")
    reply = await message.reply_text("<b>Please Wait...</b>")
    await save_group_settings(grpid, 'shortlink', shortlink_url)
    await save_group_settings(grpid, 'shortlink_api', api)
    await save_group_settings(grpid, 'is_shortlink', True)
    await reply.edit_text(f"<b>Successfully added shortlink API for {title}.\n\nCurrent Shortlink Website: <code>{shortlink_url}</code>\nCurrent API: <code>{api}</code></b>")




