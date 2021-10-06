from django.core.management.base import BaseCommand
from telegram import Bot
from telegram.utils.request import Request
from bot_admin.models import *
import os


class Command(BaseCommand):
    help = 'Close Poll'
    
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
        
        try:
            poll_group_id = int(input('Enter poll group id (you can find it in "list_polls" command): '))
            polls = TelegramPoll.objects.filter(poll_group_id=poll_group_id).all()
            
            if (len(polls) == 0):
                raise Exception('Poll group was not found')
            
            print('Was chosen')
            print(f'Poll group ID: {polls[0].poll_group_id}; Question: {polls[0].question}; Time (UTC): {polls[0].created_at}\n')
            
            choice = input('Are you sure to close all polls? (y/n)')
            if choice == 'y':
                for poll in polls:
                    poll: TelegramPoll
                    
                    bot.stop_poll(
                        chat_id=poll.student.telegram_chat_id,
                        message_id=poll.telegram_message_id
                    )
                    
            print('Polls were closed successfully')
            
        except Exception as e:
            print(e)
            return
        
        print()
