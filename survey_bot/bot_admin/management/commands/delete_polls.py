from django.core.management.base import BaseCommand
from telegram import Bot
from telegram.utils.request import Request
from bot_admin.models import *
import os


class Command(BaseCommand):
    help = 'Delete polls'
    
    def handle(self, *args, **kwargs):
        request = Request(
            connect_timeout=2.0,
            read_timeout=2.0
        )
        
        bot = Bot(
            request=request,
            token=os.getenv('TOKEN')
        )
        
        print()
        
        try:
            poll_group_ids: str = input('Enter poll group IDs divided by space (you can find them by "list_polls" command): ')
            poll_group_ids = [int(id) for id in poll_group_ids.split()]
            
            print()
            
            for poll_group_id in poll_group_ids:
                polls = TelegramPoll.objects.filter(poll_group_id=poll_group_id).all()
                
                if len(polls) == 0:
                    print(f'Poll group (group id: {poll_group_id}) was not found')
                    continue
            
                print(f'\nDeleting poll with question: "{polls[0].question}"')
            
                for poll in polls:
                    poll: TelegramPoll
                    student: Student = poll.student
                    
                    bot.delete_message(
                        chat_id=student.telegram_chat_id,
                        message_id=poll.telegram_message_id
                    )
                        
                polls.delete()
                        
            print('\nPolls were deleted successfully!\n')
            
        except Exception as e:
            print(e)
            return
        
        print()
