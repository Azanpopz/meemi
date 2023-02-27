import asyncio

from info import TG_MAX_MSG_SELECT
from pyrogram import Client, filters
from plugins.helpers.admin_check import admin_check
from plugins.helpers.custom_filter.py import f_onw_fliter


@Client.on_message(filters.command(["pr"]) & f_onw_fliter)
async def purge(client, message):
    """ purge upto the replied message """
    if message.chat.type not in ("SUPERGROUP", "CHANNEL"):
        # https://t.me/c/1312712379/84174
        return

    is_admin = await admin_check(message)

    if not is_admin:
        return

    status_message = await message.reply_text("Started Purging...", quote=True)
    await message.delete()
    message_ids = []
    count_del_etion_s = 0

    if message.reply_to_message:
        for a_s_message_id in range(
            message.reply_to_message.id,
            message.id
        ):
            message_ids.append(a_s_message_id)
            if len(message_ids) == TG_MAX_MSG_SELECT:
                await client.delete_messages(
                    chat_id=message.chat.id,
                    message_ids=message_ids,
                    revoke=True
                )
                count_del_etion_s += len(message_ids)
                message_ids = []
        if len(message_ids) > 0:
            await client.delete_messages(
                chat_id=message.chat.id,
                message_ids=message_ids,
                revoke=True
            )
            count_del_etion_s += len(message_ids)

    await status_message.edit_text(
        f"Deleted {count_del_etion_s} Messages"
    )
    await asyncio.sleep(5)
    await status_message.delete()

