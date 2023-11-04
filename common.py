import json
import logging

from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from text import SERVER, USER, SUB, LINK, SAVE, URL

with open("config.json") as config_file:
    config = json.load(config_file)

admin = config["telegram"]["admin"]
token = config["telegram"]["token"]

logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

start_kb = InlineKeyboardMarkup([
    [InlineKeyboardButton(SERVER, callback_data="server")],
    [InlineKeyboardButton(USER, callback_data="user")],
    [InlineKeyboardButton(SUB, callback_data="sub")],
    [InlineKeyboardButton(URL, callback_data="url")],
    [InlineKeyboardButton(LINK, callback_data="link")],
    [InlineKeyboardButton(SAVE, callback_data="save_sub")]
])
