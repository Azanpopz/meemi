from pyrogram import Client, filters

@Client.on_message(filters.command(["file"]))
async def file(bot, message):   
    if message.reply_to_message.file:
       await message.reply(f"**file ID is**  \n `{message.reply_to_message.file.file_id}` \n \n ** Unique ID is ** \n\n`{message.reply_to_message.file.file_unique_id}`", quote=True)
    else: 
       await message.reply("Oops !! Not a file")
