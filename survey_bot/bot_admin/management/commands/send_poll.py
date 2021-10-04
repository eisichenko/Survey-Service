from django.core.management.base import BaseCommand
from telegram import (
    Bot, 
    Update, 
    Poll,
    KeyboardButton, 
    KeyboardButtonPollType,
    ReplyKeyboardMarkup,
    ParseMode,
)
from telegram.ext import (
    CallbackContext, 
    Filters, 
    Updater, 
    CommandHandler, 
    MessageHandler,
    PollAnswerHandler,
    dispatcher,
)
from telegram.utils.request import Request
from bot_admin.models import *
import os
import logging
from dotenv import load_dotenv


load_dotenv()
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)

question = 'How are you?'
options = ['Good', 'Perfect', 'Happy', 'Bad']


class Command(BaseCommand):
    help = 'Send Poll'
    
    def handle(self, *args, **kwargs):
        request = Request(
            connect_timeout=0.5,
            read_timeout=1.0
        )
        
        bot = Bot(
            request=request,
            token=os.getenv('TOKEN')
        )
        
        bot.send_poll(
            chat_id=452706517,
            question=question,
            options=options,
            type=Poll.REGULAR,
            correct_option_id=None,
            is_anonymous=False,
            open_period=30,
            explanation='No explanations here :D'
        )
        