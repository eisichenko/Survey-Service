from django.core.management.base import BaseCommand
from telegram import Bot
from telegram.utils.request import Request
from bot_admin.models import *
import os


class Command(BaseCommand):
    help = 'Delete text questions'
    
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
            message_group_ids: str = input('Enter message group IDs divided by space (you can find them by "list_questions" command): ')
            message_group_ids = [int(id) for id in message_group_ids.split()]
            
            print()
            
            for message_group_id in message_group_ids:
                questions = TelegramMessage.objects.filter(message_group_id=message_group_id).all()
                
                if len(questions) == 0:
                    print(f'Message group (group id: {message_group_id}) was not found')
                    continue
            
                print(f'\nDeleting message with question: "{questions[0].text}"')
            
                for question in questions:
                    question: TelegramMessage
                    student: Student = question.student
                    
                    try:
                        bot.delete_message(
                            chat_id=student.telegram_chat_id,
                            message_id=question.telegram_message_id
                        )
                    except:
                        pass
                        
                questions.delete()
                        
            print('\nQuestions were deleted successfully!\n')
            
        except Exception as e:
            print(e)
            return
        
        print()
