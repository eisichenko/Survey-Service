from django.core.management.base import BaseCommand
from bot_admin.models import *


class Command(BaseCommand):
    help = 'List text questions'
    
    def handle(self, *args, **kwargs):
        print()
        
        questions = TelegramMessage.objects.all().order_by('message_group_id')
        
        if len(questions) == 0:
            self.stdout.write(self.style.SUCCESS('No text questions in database'))
        
        for question in questions:
            question: TelegramMessage
            self.stdout.write(self.style.SUCCESS(f'Message group ID: {question.message_group_id}; Question: {question.text}; Time (UTC): {question.created_at} Is closed: {question.is_closed}\n'))
        
        print()
