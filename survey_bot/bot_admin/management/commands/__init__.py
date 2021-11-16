import logging
import re
from re import Match
from telegram import Bot
from telegram.utils.request import Request
from telegram.ext.callbackcontext import CallbackContext
from telegram.update import Update
import os
from dotenv import load_dotenv


load_dotenv()
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)


def is_valid_name(name: str) -> bool:
    match: Match = re.match('^[A-Za-zА-Яа-я\' ]+$', name)
    return len(name) > 0 and match != None and len(name) <= 100

def is_valid_group(name: str) -> bool:
    return len(name) > 0 and len(name) <= 100


def log_errors(f):
    def wrapper(update: Update, callback: CallbackContext):
        try:
            return f(update, callback)
        except Exception as e:
            request = Request(
                connect_timeout=0.5,
                read_timeout=1.0
            )
            
            bot = Bot(
                request=request,
                token=os.getenv('TOKEN')
            )
            
            bot.send_message(
                chat_id=update.message.chat_id,
                text='Бот сломался, это печально :('
            )
            
            raise e
    return wrapper
