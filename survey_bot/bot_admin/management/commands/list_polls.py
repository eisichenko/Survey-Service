from django.core.management.base import BaseCommand
from bot_admin.models import *


class Command(BaseCommand):
    help = 'List polls'
    
    def handle(self, *args, **kwargs):
        print()
        
        polls = TelegramPoll.objects.all().order_by('poll_group_id')
        
        if (len(polls) == 0):
            self.stdout.write(self.style.SUCCESS('No polls in database'))
        
        for poll in polls:
            poll: TelegramPoll
            self.stdout.write(self.style.SUCCESS(f'Poll group ID: {poll.poll_group_id}; Question: {poll.question}; Time (UTC): {poll.created_at}; Is closed: {poll.is_closed()}\n'))
        
        print()
        