# <C> MoTechYT


import os

class Config(object):
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "2034622427:AAGzgpj4Viycp2rjB5TwgYdaYzfP3ImXSoA")
    API_ID = int(os.environ.get("API_ID", 1778836))
    API_HASH = os.environ.get("API_HASH", "7bcf61fcd32b8652cd5876b02dcf57ae")
    CAPTION = os.environ.get("CAPTION", "💕💕")
    BUTTON_TEXT = os.environ.get("BUTTON", "🔻Join Channel🔻")
    URL_LINK = os.environ.get("LINK", "T.ME/nasrani_update")
    BOT_USERNAME = os.environ.get("BOT_USERNAME", "KOCHU_KALLAN_RoBOT")
