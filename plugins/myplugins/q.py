import logging.config
from info import *
from pyrogram.types import ChatPermissions, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import Client, filters, mime_types
# from database.connections_mdb import active_connection
# from database.locks_db import lock_db
from pyrogram.errors import ChatAdminRequired, BadRequest
import motor.motor_asyncio
from info import DATABASE_NAME, DATABASE_URI
from pyrogram.types import Chat, ChatMember

from plugins.admin_check import admin_check
from plugins.chat_status import *

import pymongo

from info import DATABASE_URI, DATABASE_NAME

from pyrogram.types import Message

from Script import script

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

myclient = pymongo.MongoClient(DATABASE_URI)
mydb = myclient[DATABASE_NAME]
mycol = mydb['CONNECTION']


# Get logging configurations
logging.config.fileConfig('logging.conf')
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("imdbpy").setLevel(logging.ERROR)



class Database:
    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.perm = self.db.permissions
        self.restr = self.db.restrictions

    def new_locks(self, chat_id, locked):
        return dict(
            chat_id=str(chat_id),
            audio=locked, voice=locked,
            contact=locked, video=locked,
            document=locked, photo=locked,
            sticker=locked, gif=locked,
            url=locked, bots=locked,
            forward=locked, game=locked,
            location=locked,
        )

    def new_restrictions(self, chat_id, locked):
        return dict(
            chat_id=str(chat_id),
            messages=locked, media=locked,
            other=locked, preview=locked,
        )

    async def add_locks(self, chat_id, locked):
        locks = self.new_locks(chat_id, locked)
        await self.perm.insert_one(locks)

    async def add_restrictions(self, chat_id, locked):
        restr = self.new_restrictions(chat_id, locked)
        await self.restr.insert_one(restr)

    async def is_locks_exist(self, chat_id):
        locks = await self.perm.find_one({'chat_id': str(chat_id)})
        return bool(locks)

    async def get_locks(self, chat_id):
        query = await self.perm.find_one({'chat_id': str(chat_id)})
        if query is not None:
            return query
        else:
            return None

    async def get_restrictions(self, chat_id):
        query = await self.restr.find_one({'chat_id': str(chat_id)})
        if query is not None:
            return query
        else:
            return None

    async def migrate_chat(self, old_chat_id, new_chat_id):
        await self.perm.update_one({'chat_id': str(old_chat_id)}, {'$set': {'chat_id': new_chat_id}})
        await self.restr.update_one({'chat_id': str(old_chat_id)}, {'$set': {'chat_id': new_chat_id}})

    async def update_locks(self, chat_id, lock_type, locked):
        if lock_type == "audio":
            await self.perm.update_one({'chat_id': str(chat_id)}, {'$set': {'audio': locked}})
        elif lock_type == "voice":
            await self.perm.update_one({'chat_id': str(chat_id)}, {'$set': {'voice': locked}})
        elif lock_type == "contact":
            await self.perm.update_one({'chat_id': str(chat_id)}, {'$set': {'contact': locked}})
        elif lock_type == "video":
            await self.perm.update_one({'chat_id': str(chat_id)}, {'$set': {'video': locked}})
        elif lock_type == "document":
            await self.perm.update_one({'chat_id': str(chat_id)}, {'$set': {'document': locked}})
        elif lock_type == "photo":
            await self.perm.update_one({'chat_id': str(chat_id)}, {'$set': {'photo': locked}})
        elif lock_type == "sticker":
            await self.perm.update_one({'chat_id': str(chat_id)}, {'$set': {'sticker': locked}})
        elif lock_type == "gif":
            await self.perm.update_one({'chat_id': str(chat_id)}, {'$set': {'gif': locked}})
        elif lock_type == 'url':
            await self.perm.update_one({'chat_id': str(chat_id)}, {'$set': {'url': locked}})
        elif lock_type == 'bots':
            await self.perm.update_one({'chat_id': str(chat_id)}, {'$set': {'bots': locked}})
        elif lock_type == 'forward':
            await self.perm.update_one({'chat_id': str(chat_id)}, {'$set': {'forward': locked}})
        elif lock_type == 'game':
            await self.perm.update_one({'chat_id': str(chat_id)}, {'$set': {'game': locked}})
        elif lock_type == 'location':
            await self.perm.update_one({'chat_id': str(chat_id)}, {'$set': {'location': locked}})


async def can_delete(client, grp_id, userid) -> bool:
    user_det = await client.get_chat_member(grp_id, userid)
    return user_det.can_delete_messages


async def is_bot_admin(chat, bot_id: int, bot_member: ChatMember = None) -> bool:
    if chat.type == 'private':      # or chat.all_members_are_administrators:
        return True

    if not bot_member:
        bot_member = await chat.get_member(bot_id)
    return bot_member.status in ['administrator', 'creator']


async def is_user_admin(chat: Chat, user_id: int) -> bool:
    try:
        chat_member = await chat.get_member(user_id)
        if chat_member.status in ['administrator', 'creator']:
            return True
        else:
            return False
    except Exception as e:
        pass


async def is_user_not_admin(chat, user_id: int) -> bool:
    chat_member = await chat.get_member(user_id)
    if chat_member.status not in ['administrator', 'creator']:
        return True
    else:
        return False


async def admin_check(message: Message) -> bool:
    if not message.from_user:
        return False

    if message.chat.type.name not in ["SUPERGROUP", "CHANNEL"]:
        return False

    if message.from_user.id in [
        777000,  # Telegram Service Notifications
        1087968824  # GroupAnonymousBot
    ]:
        return True

    client = message._client
    chat_id = message.chat.id
    user_id = message.from_user.id

    check_status = await client.get_chat_member(
        chat_id=chat_id,
        user_id=user_id
    )
    admin_strings = [
        "owner",
        "administrator"
    ]
    # https://git.colinshark.de/PyroBot/PyroBot/src/branch/master/pyrobot/modules/admin.py#L69
    if check_status.status.value not in admin_strings:
        return False
    else:
        return True

__help__ = """
{}
""".format(script.ADMIN_TXT)

__mod_name__ = "Admin"




    async def update_restrictions(self, chat_id, restr_type, locked):
        if restr_type == "messages":
            await self.restr.update_one({'chat_id': str(chat_id)}, {'$set': {'messages': locked}})
        elif restr_type == "media":
            await self.restr.update_one({'chat_id': str(chat_id)}, {'$set': {'media': locked}})
        elif restr_type == "other":
            await self.restr.update_one({'chat_id': str(chat_id)}, {'$set': {'other': locked}})
        elif restr_type == "previews":
            await self.restr.update_one({'chat_id': str(chat_id)}, {'$set': {'preview': locked}})
        elif restr_type == "all":
            await self.restr.update_one({'chat_id': str(chat_id)}, {'$set': {'messages': locked}})
            await self.restr.update_one({'chat_id': str(chat_id)}, {'$set': {'media': locked}})
            await self.restr.update_one({'chat_id': str(chat_id)}, {'$set': {'other': locked}})
            await self.restr.update_one({'chat_id': str(chat_id)}, {'$set': {'preview': locked}})

    async def is_locked(self, chat_id, lock_type):
        curr_perm = await self.perm.find_one({'chat_id': str(chat_id)})

        if not curr_perm:
            return False

        elif lock_type == "sticker":
            return curr_perm['sticker']
        elif lock_type == "photo":
            return curr_perm['photo']
        elif lock_type == "audio":
            return curr_perm['audio']
        elif lock_type == "voice":
            return curr_perm['voice']
        elif lock_type == "contact":
            return curr_perm['contact']
        elif lock_type == "video":
            return curr_perm['video']
        elif lock_type == "document":
            return curr_perm['document']
        elif lock_type == "gif":
            return curr_perm['gif']
        elif lock_type == "url":
            return curr_perm['url']
        elif lock_type == "bots":
            return curr_perm['bots']
        elif lock_type == "forward":
            return curr_perm['forward']
        elif lock_type == "game":
            return curr_perm['game']
        elif lock_type == "location":
            return curr_perm['location']

    async def is_restr_locked(self, chat_id, lock_type):
        curr_restr = await self.restr.find_one({'chat_id': str(chat_id)})

        if not curr_restr:
            return False

        if lock_type == "messages":
            return curr_restr['messages']
        elif lock_type == "media":
            return curr_restr['media']
        elif lock_type == "other":
            return curr_restr['other']
        elif lock_type == "previews":
            return curr_restr['preview']
        elif lock_type == "all":
            return curr_restr['messages'] and curr_restr['media'] and curr_restr['other'] and curr_restr['preview']


lock_db = Database(DATABASE_URI, DATABASE_NAME)





async def add_connection(group_id, user_id):
    query = mycol.find_one(
        {"_id": user_id},
        {"_id": 0, "active_group": 0}
    )
    if query is not None:
        group_ids = [x["group_id"] for x in query["group_details"]]
        if group_id in group_ids:
            return False

    group_details = {
        "group_id": group_id
    }

    data = {
        '_id': user_id,
        'group_details': [group_details],
        'active_group': group_id,
    }

    if mycol.count_documents({"_id": user_id}) == 0:
        try:
            mycol.insert_one(data)
            return True
        except:
            logger.exception('Some error occured!', exc_info=True)

    else:
        try:
            mycol.update_one(
                {'_id': user_id},
                {
                    "$push": {"group_details": group_details},
                    "$set": {"active_group": group_id}
                }
            )
            return True
        except:
            logger.exception('Some error occured!', exc_info=True)


async def active_connection(user_id):
    query = mycol.find_one(
        {"_id": user_id},
        {"_id": 0, "group_details": 0}
    )
    if not query:
        return None

    group_id = query['active_group']
    if group_id != None:
        return int(group_id)
    else:
        return None


async def all_connections(user_id):
    query = mycol.find_one(
        {"_id": user_id},
        {"_id": 0, "active_group": 0}
    )
    if query is not None:
        return [x["group_id"] for x in query["group_details"]]
    else:
        return None


async def if_active(user_id, group_id):
    query = mycol.find_one(
        {"_id": user_id},
        {"_id": 0, "group_details": 0}
    )
    return query is not None and query['active_group'] == group_id


async def make_active(user_id, group_id):
    update = mycol.update_one(
        {'_id': user_id},
        {"$set": {"active_group": group_id}}
    )
    return update.modified_count != 0


async def make_inactive(user_id):
    update = mycol.update_one(
        {'_id': user_id},
        {"$set": {"active_group": None}}
    )
    return update.modified_count != 0


async def delete_connection(user_id, group_id):
    try:
        update = mycol.update_one(
            {"_id": user_id},
            {"$pull": {"group_details": {"group_id": group_id}}}
        )
        if update.modified_count == 0:
            return False
        query = mycol.find_one(
            {"_id": user_id},
            {"_id": 0}
        )
        if len(query["group_details"]) >= 1:
            if query['active_group'] == group_id:
                prvs_group_id = query["group_details"][len(query["group_details"]) - 1]["group_id"]

                mycol.update_one(
                    {'_id': user_id},
                    {"$set": {"active_group": prvs_group_id}}
                )
        else:
            mycol.update_one(
                {'_id': user_id},
                {"$set": {"active_group": None}}
            )
        return True
    except Exception as e:
        logger.exception(f'Some error occured! {e}', exc_info=True)
        return False










URL = ("https://" or "http://")
LOCK_TYPES = {'sticker': filters.sticker,
              'audio': filters.audio,
              'voice': filters.voice,
              'document': filters.document,
              'video': filters.video,
              'contact': filters.contact,
              'photo': filters.photo,
              'gif': filters.document & filters.animation,
              'url': filters.regex("https://" or "http://"),
              'bots': filters.new_chat_members,
              'forward': filters.forwarded,
              'game': filters.game,
              'location': filters.location,
              }

GIF = filters.document & filters.animation
OTHER = filters.game | filters.sticker | GIF
MEDIA = filters.audio | filters.document | filters.video | filters.voice | filters.photo
MESSAGES = filters.text | filters.contact | filters.location | filters.venue | filters.command | MEDIA | OTHER
PREVIEWS = filters.regex("https://" or "http://")

RESTRICTION_TYPES = {'messages': MESSAGES,
                     'media': MEDIA,
                     'other': OTHER,
                     'previews': PREVIEWS,  # NOTE: this has been removed cos its useless atm.
                     'all': filters.all}

PERM_GROUP = 1
REST_GROUP = 2


# NOT ASYNC
async def restr_members(bot, chat_id, members, messages=False, media=False, other=False, previews=False):
    for mem in members:
        if (
                mem.status != 'administrator' and
                mem.status != 'creator' and
                str(mem.user.id) not in ADMINS and
                mem.user.is_bot != True
        ):
            try:
                await bot.restrict_chat_member(chat_id, mem.user.id,
                                               ChatPermissions(can_send_messages=messages,
                                                               can_send_media_messages=media,
                                                               can_send_other_messages=other,
                                                               can_add_web_page_previews=previews))
                # await bot.restrict_chat(chat_id,
                #                         ChatPermissions(can_send_messages=messages,
                #                                         can_send_media_messages=media,
                #                                         can_send_other_messages=other,
                #                                         can_add_web_page_previews=previews))
            except Exception as e:
                pass
        else:
            pass


# NOT ASYNC
async def unrestr_members(bot, chat_id, members, messages=True, media=True, other=True, previews=True):
    for mem in members:
        try:
            await bot.restrict_chat_member(chat_id, mem.user.id,
                                           ChatPermissions(can_send_messages=messages,
                                                           can_send_media_messages=media,
                                                           can_send_other_messages=other,
                                                           can_add_web_page_previews=previews))
        except Exception as e:
            pass


@Client.on_message(filters.command("locktypes") & filters.incoming)    # & ~filters.edited
async def locktypes(client, message):
    await message.reply_text("\n - ".join(["Locks: "] + list(LOCK_TYPES) + list(RESTRICTION_TYPES)), quote=True)


@Client.on_message(filters.command("lock") & filters.private)    # & ~filters.edited
async def lock(client, message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"You are anonymous admin. Use /connect {message.chat.id} in PM")
    chat_type = message.chat.type
    args = message.text.html.split(None, 1)

    if chat_type.name == "PRIVATE":
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

    elif chat_type.name in ["GROUP", "SUPERGROUP"]:
        grp_id = message.chat.id
        title = message.chat.title

    else:
        return

    st = await client.get_chat_member(grp_id, userid)
    if (
            st.status.value != "administrator"
            and st.status.value != "owner"
            and str(userid) not in ADMINS
    ):
        return

    if not await lock_db.is_locks_exist(str(grp_id)):
        await lock_db.add_locks(str(grp_id), False)
        await lock_db.add_restrictions(str(grp_id), False)

    if await can_delete(client, grp_id, client.bot_token.split(":")[0]):
        if len(args) >= 1:
            if args[1] in LOCK_TYPES:
                await lock_db.update_locks(grp_id, str(args[1]).lower(), True)
                await message.reply_text("Locked **{}** Messages!".format(str(args[1]).lower()))
                log = "**{}:**" \
                      "\n#LOCK" \
                      "\n**Admin:** {}" \
                      "\nLocked **{}**.".format(title, message.from_user.mention, str(args[1]).lower())
                if LOG_CHANNEL:
                    try:
                        return await client.send_message(LOG_CHANNEL, log)
                    except ChatAdminRequired:
                        await message.reply_text("Log Channel Error, Should Be Log Channel Admin With Write Permission")
                        return
                else:
                    return
            elif args[1] in RESTRICTION_TYPES:
                await lock_db.update_restrictions(grp_id, str(args[1]).lower(), True)
                members = await client.get_chat_members(chat_id=str(grp_id), limit=client.get_chat_members_count(str(grp_id)), filter="all")

                if args[1] == "messages":
                    await restr_members(client, str(grp_id), members, messages=False, media=True, other=True,
                                        previews=True)
                elif args[1] == "media":
                    await restr_members(client, str(grp_id), members, messages=False, media=False, other=True,
                                        previews=True)
                elif args[1] == "other":
                    await restr_members(client, str(grp_id), members, messages=False, media=False, other=False,
                                        previews=True)
                elif args[1] == "previews":
                    await restr_members(client, str(grp_id), members, messages=False, media=False, other=False,
                                        previews=False)
                elif args[1] == "all":
                    await restr_members(client, str(grp_id), members, messages=False, media=False, other=False,
                                        previews=False)
                """if args[0] == "previews":
                    members = users_sql.get_chat_members(str(history.chat_id1))
                    await restr_members(bot, history.chat_id1, members, messages=False, media=False, other=False,
                                        previews=False)"""

                await message.reply_text("Locked **{}** Messages!".format(str(args[1]).lower()))
                log = "**{}:**" \
                      "\n#LOCK" \
                      "\n**Admin:** {}" \
                      "\nLocked **{}**.".format(title, message.from_user.mention, str(args[1]).lower())
                if LOG_CHANNEL:
                    try:
                        return await client.send_message(LOG_CHANNEL, log)
                    except ChatAdminRequired:
                        await message.reply_text("Log Channel Error, Should Be Log Channel Admin With Write Permission")
                        return
                else:
                    return

            else:
                message.reply_text("What Are You Trying To Lock...? Try /locktypes For The List Of Lockable")
    else:
        await message.reply_text("I'm Not An Administrator, Or Haven't Got Delete Rights.", quote=True)
        return


@Client.on_message(filters.command("unlock") & filters.private)    # & ~filters.edited
async def unlock(client, message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"You are anonymous admin. Use /connect {message.chat.id} in PM")
    chat_type = message.chat.type
    args = message.text.html.split(None, 1)

    if chat_type.name == "PRIVATE":
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

    elif chat_type.name in ["GROUP", "SUPERGROUP"]:
        grp_id = message.chat.id
        title = message.chat.title

    else:
        return

    st = await client.get_chat_member(grp_id, userid)
    if (
            st.status.value != "administrator"
            and st.status.value != "owner"
            and str(userid) not in ADMINS
    ):
        return

    if not await lock_db.is_locks_exist(str(grp_id)):
        await lock_db.add_locks(str(grp_id), False)
        await lock_db.add_restrictions(str(grp_id), False)

    if await admin_check(message):
        if len(args) >= 1:
            if args[1] in LOCK_TYPES:
                await lock_db.update_locks(grp_id, str(args[1]).lower(), False)
                await message.reply_text("Unlocked **{}** For Everyone!".format(str(args[1]).lower()))
                log = "**{}:**" \
                      "\n#UNLOCK" \
                      "\n**Admin:** {}" \
                      "\nUnlocked **{}**.".format(title, message.from_user.mention, str(args[1]).lower())
                if LOG_CHANNEL:
                    try:
                        return await client.send_message(LOG_CHANNEL, log)
                    except ChatAdminRequired:
                        await message.reply_text("Log Channel Error, Should Be Log Channel Admin With Write Permission")
                        return
                else:
                    return
            elif args[1] in RESTRICTION_TYPES:
                await lock_db.update_restrictions(grp_id, str(args[1]).lower(), False)
                members = await client.get_chat_members(chat_id=str(grp_id), limit=client.get_chat_members_count(str(grp_id)), filter="all")

                if args[0] == "messages":
                    await unrestr_members(client, grp_id, members, media=False, other=False, previews=False)
                elif args[0] == "media":
                    await unrestr_members(client, grp_id, members, other=False, previews=False)
                elif args[0] == "other":
                    await unrestr_members(client, grp_id, members, previews=False)
                elif args[0] == "previews":
                    await unrestr_members(client, grp_id, members)
                elif args[0] == "all":
                    await unrestr_members(client, grp_id, members, True, True, True, True)

                await message.reply_text("Unlocked **{}** For Everyone!".format(str(args[1]).lower()))
                log = "**{}:**" \
                      "\n#UNLOCK" \
                      "\n**Admin:** {}" \
                      "\nUnlocked **{}**.".format(title, message.from_user.mention, str(args[1]).lower())
                if LOG_CHANNEL:
                    try:
                        return await client.send_message(LOG_CHANNEL, log)
                    except ChatAdminRequired:
                        await message.reply_text("Log Channel Error, Should Be Log Channel Admin With Write Permission")
                        return
                else:
                    return

            else:
                message.reply_text("What Are You Trying To Unlock...? Try /locktypes For The List Of Lockable")
        else:
            client.sendMessage(message.chat.id, "What Are You Trying To Unlock...?")
    else:
        await message.reply_text("I'm Not An Administrator, Or Haven't Got Delete Rights.", quote=True)
        return


async def build_lock_message(chat_id):
    locks = await lock_db.get_locks(chat_id)
    restr = await lock_db.get_restrictions(chat_id)
    if not (locks or restr):
        res = "There Are No Current Locks In This Chat."
    else:
        res = "These Are The Locks In This Chat:"
        if locks:
            res += "\n - sticker = `{}`" \
                   "\n - audio = `{}`" \
                   "\n - voice = `{}`" \
                   "\n - document = `{}`" \
                   "\n - video = `{}`" \
                   "\n - contact = `{}`" \
                   "\n - photo = `{}`" \
                   "\n - gif = `{}`" \
                   "\n - url = `{}`" \
                   "\n - bots = `{}`" \
                   "\n - forward = `{}`" \
                   "\n - game = `{}`" \
                   "\n - location = `{}`".format(locks["sticker"], locks["audio"], locks["voice"], locks["document"],
                                                 locks["video"], locks["contact"], locks["photo"], locks["gif"], locks["url"],
                                                 locks["bots"], locks["forward"], locks["game"], locks["location"])
        if restr:
            res += "\n - messages = `{}`" \
                   "\n - media = `{}`" \
                   "\n - other = `{}`" \
                   "\n - previews = `{}`" \
                   "\n - all = `{}`".format(restr["messages"], restr["media"], restr["other"], restr["preview"],
                                            all([restr["messages"], restr["media"], restr["other"], restr["preview"]]))
    return res


@Client.on_message(filters.command("locks") & filters.private)    # & ~filters.edited
async def list_locks(client, message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"You are anonymous admin. Use /connect {message.chat.id} in PM")
    chat_type = message.chat.type
    args = message.text.html.split(None, 1)

    if chat_type.name == "PRIVATE":
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

    elif chat_type.name in ["GROUP", "SUPERGROUP"]:
        grp_id = message.chat.id
        title = message.chat.title

    else:
        return

    st = await client.get_chat_member(grp_id, userid)
    if (
            st.status.value != "administrator"
            and st.status.value != "owner"
            and str(userid) not in ADMINS
    ):
        return

    if await is_user_admin(chat, userid):
        res = await build_lock_message(grp_id)

        await message.reply_text(res, quote=True)


@Client.on_message(filters.all & filters.group, group=PERM_GROUP)
async def del_lockables(client, message):
    chat = message.chat  # type: Optional[Chat]
    # message = update.effective_message  # type: Optional[Message]
    warner = "" #bot

    if await is_user_not_admin(chat, message.from_user.id):
        for lockable, m_filter in LOCK_TYPES.items():
            a_chat = await client.get_chat_member(chat.id, client.bot_token.split(":")[0])
            if filter(message, LOCK_TYPES.items()) and \
                    await lock_db.is_locked(chat.id, lockable) and \
                    await can_delete(client, chat.id, client.bot_token.split(":")[0]):
                if lockable == "bots":
                    new_members = message.new_chat_members
                    for new_mem in new_members:
                        if new_mem.is_bot:
                            if not await is_bot_admin(chat, client.bot_token.split(":")[0]):
                                message.reply_text("I see a bot, and I've been told to stop them joining... "
                                                   "but I'm not admin!")
                                return

                            # await client.ban_chat_member(chat.id, new_mem.id)     # int(time.time() + 86400
                            message.reply_text("Only Admins Are Allowed To Add Bots To This Chat! Get Outta Here.")
                else:
                    try:
                        if lockable == "url":
                            reason = "{} Has Sent A 🔗 Link WithOut Authorization".format(message.from_user.first_name)
                        else:
                            reason = "{} Is Locked In This Chat".format(lockable)
                        user_id = message.from_user.id
                        temp_message = message

                        if user_id:
                            if temp_message.from_user.id == user_id:
                                warn_lock(temp_message.from_user, chat, reason, temp_message, warner=None)
                            else:
                                warn_lock(chat.get_member(user_id).user, chat, reason, temp_message, warner=None)
                        else:
                            temp_message.reply_text("No user was designated!")

                        await message.delete()
                    except BadRequest as excp:
                        if excp.MESSAGE == "Message to delete not found":
                            pass
                        else:
                            logging.warning("ERROR in lockables")

                break


def warn_lock(user, chat, reason: str, message, warner=None):
    if is_user_admin(chat, user.id):
        message.reply_text("Damn admins, can't even be warned!")
        return

    if warner:
        warner_tag = f"<a href=tg://user?id={warner.id}>{warner.first_name}</a>"       # mention_html(warner.id, warner.first_name)
    else:
        warner_tag = "Automated Warn Filter."

    limit, soft_warn = warnsql.get_warn_setting(chat.id)
    num_warns, reasons = warnsql.warn_user(user.id, chat.id, reason)
    if num_warns >= limit:
        warnsql.reset_warns(user.id, chat.id)
        if soft_warn:  # kick
            chat.unban_member(user.id)
            reply = "{} warnings, {} has been kicked!".format(limit, user.mention)

        else:  # ban
            chat.kick_member(user.id)
            reply = "{} warnings, {} has been banned!".format(limit, user.mention)

        for warn_reason in reasons:
            reply += "\n - {}".format(warn_reason)

        message.bot.send_sticker(chat.id, BAN_STICKER)  #Coffin Elvira sticker
        keyboard = []
        log_reason = "<b>{}:</b>" \
                     "\n#WARN_BAN" \
                     "\n<b>Admin:</b> {}" \
                     "\n<b>User:</b> {}" \
                     "\n<b>Reason:</b> {}"\
                     "\n<b>Counts:</b> <code>{}/{}</code>".format(chat.title,
                                                                  warner_tag,
                                                                  user.mention,
                                                                  reason, num_warns, limit)

    else:
        keyboard = InlineKeyboardMarkup(
            [[InlineKeyboardButton("Remove warn (Admin only)", callback_data="rm_warn({})".format(user.id))]])

        reply = "{} has {}/{} warnings... watch out!".format(user.mention, num_warns,
                                                             limit)
        if reason:
            reply += "\nReason for last warn:\n{}".format(reason)

        log_reason = "<b>{}:</b>" \
                     "\n#WARN" \
                     "\n<b>Admin:</b> {}" \
                     "\n<b>User:</b> {}" \
                     "\n<b>Reason:</b> {}"\
                     "\n<b>Counts:</b> <code>{}/{}</code>".format(chat.title,
                                                                  warner_tag,
                                                                  user.mention,
                                                                  reason, num_warns, limit)

    try:
        message.reply_text(reply, reply_markup=keyboard)
    except BadRequest as excp:
        if excp.message == "Reply message not found":
            # Do not reply
            message.reply_text(reply, reply_markup=keyboard, quote=False)
        else:
            raise
    return


def __migrate__(old_chat_id, new_chat_id):
    lock_db.migrate_chat(old_chat_id, new_chat_id)


__help__ = """
 - /locktypes: a list of possible locktypes
*Admin only:*
 - /lock <type>: lock items of a certain type (not available in private)
 - /unlock <type>: unlock items of a certain type (not available in private)
 - /locks: the current list of locks in this chat.
Locks can be used to restrict a group's users.
eg:
Locking urls will auto-delete all messages with urls which haven't been whitelisted, locking stickers will delete all \
stickers, etc.
Locking bots will stop non-admins from adding bots to the chat.
"""

__mod_name__ = "Locks"
