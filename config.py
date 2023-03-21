import os
import os

from dotenv import load_dotenv
load_dotenv()

class Config(object):
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
    API_ID = int(os.environ.get("APP_ID", 12345))
    API_HASH = os.environ.get("API_HASH", "")
    
    BOT_USERNAME = os.environ.get("BOT_USERNAME", "")

# mdisk

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
MDISK_API = os.environ.get("MDISK_API")
MDISK_CHANNEL = list(int(i.strip()) for i in os.environ.get("MDISK_CHANNEL").split(" ")) if os.environ.get("CHANNEL_ID") else []
FORWARD_MESSAGE = bool(os.environ.get("FORWARD_MESSAGE"))
ADMINS = list(int(i.strip()) for i in os.environ.get("ADMINS").split(",")) if os.environ.get("ADMINS") else []
SOURCE_CODE = "💕SHARE AND SUPPORT💕"
CHANNELS = bool(os.environ.get("CHANNELS"))







