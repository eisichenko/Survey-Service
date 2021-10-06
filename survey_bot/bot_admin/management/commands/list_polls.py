from django.core.management.base import BaseCommand
from bot_admin.models import *


class Command(BaseCommand):
    help = 'List polls'
    
    def handle(self, *args, **kwargs):
        print()
        
        polls = TelegramPoll.objects.all().order_by('-poll_group_id')
        
        for poll in polls:
            poll: TelegramPoll
            print(f'Poll group ID: {poll.poll_group_id}; Question: {poll.question}; Time (UTC): {poll.created_at}\n')
        
        print()
        