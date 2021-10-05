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
import logging


question = 'How are you?'
options = ['Good', 'Perfect', 'Happy', 'Bad']
correct_options = [1]


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
        
        students = Student.objects.all()
        polls = TelegramPoll.objects.all()
        
        max_poll: TelegramPoll = polls.order_by('-poll_group_id').first()
        
        if max_poll != None:
            next_id = max_poll.poll_group_id + 1
        else:
            next_id = 0
            
        print('Poll group ID: ' + str(next_id))
        
        for student in students:
            student: Student
            print(f'Survey was sent to {student.real_name} from group {student.group}')
            
            message: Message = bot.send_poll(
                chat_id=student.telegram_chat_id,
                question=question,
                options=options,
                type=Poll.REGULAR,
                allows_multiple_answers=True,
                is_anonymous=False,
                open_period=30,
                explanation=None
            )
            
            telegram_poll: TelegramPoll = TelegramPoll.objects.create(
                student=student,
                telegram_message_id=message.message_id,
                telegram_poll_id=message.poll.id,
                correct_options=correct_options,
                poll_group_id=next_id,
                question=question,
            )
        
        print()
        