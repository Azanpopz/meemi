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






# Mandatory variables for the bot to start
API_ID = int(os.getenv("API_ID", "Your Api Id"))
API_HASH = os.environ.get("API_HASH", "Your Api Hash")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "Bot Token")
ADMINS = [int(i.strip()) for i in os.environ.get("ADMINS").split("Owner Id")] if os.environ.get("ADMINS") else []
ADMIN = ADMINS
DATABASE_NAME = os.environ.get("DATABASE_NAME", "Db Name")
DATABASE_URL = os.getenv("DATABASE_URL", "Monfo url") 
#  Optionnal variables
LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "Logs Channels Id")) 
BATCH_GROUP = os.environ.get("BATCH_GROUP", "Batch Group User name Without @") # For Force Subscription
BROADCAST_AS_COPY = os.environ.get('BROADCAST_AS_COPY', "True") # true if forward should be avoided
WELCOME_IMAGE = os.environ.get("WELCOME_IMAGE", '') # image when someone hit /start # image when someone hit /start
LINK_BYPASS = "False"


