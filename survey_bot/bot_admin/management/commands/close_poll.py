from django.core.management.base import BaseCommand
from telegram import (
    Bot, 
    Update, 
    Poll,
    Message,
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
        
        print()
        
        print()
