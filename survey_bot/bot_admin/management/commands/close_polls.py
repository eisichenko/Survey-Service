from django.core.management.base import BaseCommand
from telegram import Bot
from telegram.utils.request import Request
from bot_admin.models import *
import os


class Command(BaseCommand):
    help = 'Close polls'
    
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
            poll_group_ids: str = input('Enter poll group IDs divided by space (you can find them by "list_polls" command): ')
            poll_group_ids = [int(id) for id in poll_group_ids.split()]
            
            choice = input('Are you sure to close all polls? (y/n)')
            
            if choice == 'y':
                for poll_group_id in poll_group_ids:
                    try:
                        polls = TelegramPoll.objects.filter(poll_group_id=poll_group_id).all()
                        
                        if len(polls) == 0:
                            raise Exception(f'Poll group id {poll_group_id} was not found')
                        
                        print(f'Closing poll group ID: {polls[0].poll_group_id}; Question: {polls[0].question}; Time (UTC): {polls[0].created_at}\n')
                    
                        for poll in polls:
                            poll: TelegramPoll
                            
                            bot.stop_poll(
                                chat_id=poll.student.telegram_chat_id,
                                message_id=poll.telegram_message_id
                            )
                    except Exception as e:
                        print(str(e) + '\n')
                        
                print('Polls were closed successfully!')
            else:
                print('Operaiton was declined.')
            
        except Exception as e:
            print(e)
            return
        
        print()
