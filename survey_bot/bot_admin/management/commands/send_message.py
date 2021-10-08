from django.core.management.base import BaseCommand
from telegram import Bot, Poll, Message
from telegram.utils.request import Request
from bot_admin.models import *
import os


class Command(BaseCommand):
    help = 'Send no reply message to all students'
    
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
            msg_text = input('Please enter the message text: ')
                    
            if len(msg_text.strip()) == 0:
                raise Exception('Empty message is not allowed')
            
            print()
            
            choice = input('Would you like to specify student usernames (you can find them by "list_students" command)? (y/n)')
            
            if choice == 'y':
                usernames = input('\nEnter student usernames divided by space who will receive message: ').split()

                for username in usernames:
                    student: Student = Student.objects.filter(
                        telegram_username=username
                    ).first()
                    
                    if student == None:
                        print(f'Student {username} was not found')
                    else:
                        bot.send_message(
                            chat_id=student.telegram_chat_id,
                            text=msg_text
                        )
                        print(f'Sending to {username}')
            else:
                students = Student.objects.all()
                
                for student in students:
                    student: Student
                    
                    bot.send_message(
                        chat_id=student.telegram_chat_id,
                        text=msg_text
                    )
                    
                    print(f'Sending to {student.telegram_username}')
                
            print('\nMessage was sent successfully\n')
        except Exception as e:
            print(e)
        
        print()
