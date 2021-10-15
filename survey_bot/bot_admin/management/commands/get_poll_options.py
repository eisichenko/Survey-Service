from django.core.management.base import BaseCommand
from bot_admin.models import *


class Command(BaseCommand):
    help = 'Get poll options'
    
    def handle(self, *args, **kwargs):
        print()
        
        try:
            poll_group_id = int(input('Enter poll group id (you can find it in "list_polls" command): '))
            poll = TelegramPoll.objects.filter(poll_group_id=poll_group_id).first()
            
            if poll == None:
                raise Exception('Poll group was not found')
            
            print(f'\nQuestion: {poll.question}')
            
            print('\nOptions:\n')
            
            
            for i in range(len(poll.options_text)):
                is_correct = i in poll.correct_options
                print(f'#{i}: {poll.options_text[i]} ', end='')
                if is_correct:
                    self.stdout.write(self.style.SUCCESS('correct'))
                else:
                    self.stdout.write(self.style.ERROR('wrong'))
        
            print()
        except Exception as e:
            self.stdout.write(self.style.ERROR(e))
        