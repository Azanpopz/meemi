from pyrogram.types import Message

from Script import script


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
