# Spotify-Downloader

### This download from saavn.me an unofficial api
from pyrogram import Client,filters
import requests,os,wget
from info import BATCH_GROUP, REQST_CHANNEL, SUPPORT_CHAT_ID, ADMINS
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import asyncio
from info import LOG_CHANNEL
BUTTONS = InlineKeyboardMarkup([[InlineKeyboardButton('💖🇮🇳✨ Made By ✨🇮🇳💖', url='https://t.me/nasrani_update')]])
A = """{} with user id:- {} used /git command."""



@Client.on_message(filters.text & filters.chat(BATCH_GROUP))
async def song(client, message):
    
    args = message.text.split(None)

    r = requests.get(f"https://saavn.me/search/songs?query={args}&page=1&limit=1").json()
    sname = r['data']['results'][0]['name']
    slink = r['data']['results'][0]['downloadUrl'][4]['link']
    ssingers = r['data']['results'][0]['primaryArtists']
#    album_id = r.json()[0]["albumid"]
    img = r['data']['results'][0]['image'][2]['link']
    thumbnail = wget.download(img)
    file = wget.download(slink)
    ffile = file.replace("mp4", "mp3")
    os.rename(file, ffile)
    buttons = [[
        InlineKeyboardButton("JOIN MOVIES", url="https://t.me/NASRANI_UPDATE")
    ]]                           
    await message.reply_audio(
    audio=ffile, title=sname, performer=ssingers,caption=f"[{sname}]({r['data']['results'][0]['url']}) - from @nasrani_update ",thumb=thumbnail,
    reply_markup=InlineKeyboardMarkup(buttons)
)

    os.remove(ffile)
    os.remove(thumbnail)


    await client.send_message(LOG_CHANNEL, A.format(message.from_user.mention, message.from_user.id)) 
    await k.delete()    



# Spotify-Downloader


#@Client.on_message(filters.command('saavn') & filters.text)
#async def song(client, message):
#    try:
#       args = message.text.split(None, 1)[1]
#    except:
#        return await message.reply("/saavn requires an argument.")
#    if args.startswith(" "):
#        await message.reply("/saavn requires an argument.")
#        return ""
#    pak = await message.reply('Downloading...')
#    try:
#        r = requests.get(f"https://saavn.me/search/songs?query={args}&page=1&limit=1").json()
#    except Exception as e:
#        await pak.edit(str(e))
#        return
#    sname = r['data']['results'][0]['name']
#    slink = r['data']['results'][0]['downloadUrl'][4]['link']
#    ssingers = r['data']['results'][0]['primaryArtists']
  #  album_id = r.json()[0]["albumid"]
#    img = r['data']['results'][0]['image'][2]['link']
#    thumbnail = wget.download(img)
#    file = wget.download(slink)
#    ffile = file.replace("mp4", "mp3")
#    os.rename(file, ffile)
#    await pak.edit('Uploading...')
#    k = await message.reply_audio(audio=ffile, title=sname, performer=ssingers,caption=f"[{sname}]({r['data']['results'][0]['url']}) - from saavn ",thumb=thumbnail)
#    os.remove(ffile)
#    os.remove(thumbnail)
#    await asyncio.sleep(180)
#    await k.delete()
#    await pak.delete()


@Client.on_message(filters.command('vsaavn') & filters.text)
async def video(client, message): 
    try:
        args = message.text.split(None)
    except:
         
        
        return
    pak = await message.reply('Downloading...')
    try:
        r = requests.get(f"https://saavn.me/search/songs?query={args}&page=1&limit=1").json()
    except Exception as e:
        await pak.edit(str(e))
        return
    
    r = requests.get(f"https://saavn.me/search/songs?query={args}&page=2&limit=2").json()
    sname = r['data']['results'][0]['name']
    slink = r['data']['results'][0]['downloadUrl'][4]['link']
    ssingers = r['data']['results'][0]['primaryArtists']
#   album_id = r.json()[0]["albumid"]
    img = r['data']['results'][0]['image'][2]['link']
    thumbnail = wget.download(img)
    file = wget.download(slink)
    ffile = file.replace("mp3", "mp4")
    os.rename(file, ffile)
    buttons = [[
        InlineKeyboardButton("JOIN MOVIES", url="https://t.me/NASRANI_UPDATE")
    ]]                           
    await message.reply_video(
    video=ffile, caption=f"[{sname}]({r['data']['results'][0]['url']}) - from @nasrani_update ",thumb=thumbnail,
    reply_markup=InlineKeyboardMarkup(buttons)
)
    await message.reply_text(text="download mp3 song @nasrani_batch_store")
    os.remove(ffile)
    os.remove(thumbnail)
    await pak.delete()

    await client.send_message(LOG_CHANNEL, A.format(message.from_user.mention, message.from_user.id)) 
    await k.delete()




@Client.on_message(filters.text & filters.chat(BATCH_GROUP))
async def song(client, message):
    try:
        args = message.text.split(None)
    except:
         
        
        return
    pak = await message.reply('Downloading...')
    try:
        r = requests.get(f"https://saavn.me/search/songs?query={args}&page=1&limit=1").json()
    except Exception as e:
        await pak.edit(str(e))
        return

    r = requests.get(f"https://saavn.me/search/songs?query={args}&page=2&limit=2").json()
    sname = r['data']['results'][0]['name']
    slink = r['data']['results'][0]['downloadUrl'][4]['link']
    ssingers = r['data']['results'][0]['primaryArtists']
#   album_id = r.json()[0]["albumid"]
    img = r['data']['results'][0]['image'][2]['link']
    thumbnail = wget.download(img)
    file = wget.download(slink)
    ffile = file.replace("mp4", "mp3")
    os.rename(file, ffile)
    buttons = [[
        InlineKeyboardButton("JOIN MOVIES", url="https://t.me/NASRANI_UPDATE")
    ]]                           
    await message.reply_audio(
    audio=ffile, title=sname, performer=ssingers,caption=f"[{sname}]({r['data']['results'][0]['url']}) - from @nasrani_update ",thumb=thumbnail,
    reply_markup=InlineKeyboardMarkup(buttons)
)
    os.remove(ffile)
    os.remove(thumbnail)
    await pak.delete()

    await client.send_message(LOG_CHANNEL, A.format(message.from_user.mention, message.from_user.id)) 
    

