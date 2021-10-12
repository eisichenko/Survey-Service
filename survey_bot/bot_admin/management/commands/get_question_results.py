from django.core.management.base import BaseCommand
from bot_admin.models import *
import os
from datetime import datetime
from telegram import Bot
from telegram.utils.request import Request


ALL_ANSWERS_DIRECTORY = 'answers ' + datetime.now().strftime('%d.%m.%Y %H:%M:%S')
QUESTION_FILENAME = 'question.txt'


class Command(BaseCommand):
    help = 'Get question results'
    
    def handle(self, *args, **kwargs):
        print()
        
        request = Request(
            connect_timeout=5.0,
            read_timeout=5.0
        )
            
        bot = Bot(
            request=request,
            token=os.getenv('TOKEN')
        )
        
        try:
            if os.path.isdir(ALL_ANSWERS_DIRECTORY):
                raise Exception(f'Directory {ALL_ANSWERS_DIRECTORY} already exists')
            
            os.mkdir(ALL_ANSWERS_DIRECTORY)
            
            message_group_ids: str = input('Enter message group IDs divided by space (you can find them by "list_questions" command): ')
            message_group_ids = [int(id) for id in message_group_ids.split()]
            
            TEXT_CHOICE = input('\nWould you like to download TEXT answers if present? (y/n) ')
            IMAGE_CHOICE = input('\nWould you like to download IMAGE answers if present? (y/n) ')
            
            for message_group_id in message_group_ids:
                questions = TelegramMessage.objects.filter(message_group_id=message_group_id).all()
                
                if len(questions) == 0:
                    self.stdout.write(self.style.ERROR(f'\nMessage group (group id: {message_group_id}) was not found'))
                    continue
                
                question_directory_name = f'Question (group id: {message_group_id})'
                os.mkdir(os.path.join(ALL_ANSWERS_DIRECTORY, question_directory_name))
                    
                with open(os.path.join(ALL_ANSWERS_DIRECTORY, 
                                       question_directory_name, 
                                       QUESTION_FILENAME), 'w') as file:
                    file.write(questions[0].text)
            
                for question in questions:
                    question: TelegramMessage
                    current_student: Student = question.student
                    
                    student_directory_name = f'{current_student.group}.{current_student.real_name}'
                    
                    os.mkdir(os.path.join(ALL_ANSWERS_DIRECTORY, question_directory_name, student_directory_name))
                    
                    if TEXT_CHOICE == 'y':
                        if question.answer == None or len(question.answer) == 0:
                            with open(os.path.join(ALL_ANSWERS_DIRECTORY, 
                                                question_directory_name, 
                                                student_directory_name,
                                                f'empty.{student_directory_name}.txt'), 'w') as file:
                                file.write('')
                        else:
                            with open(os.path.join(ALL_ANSWERS_DIRECTORY, 
                                                question_directory_name, 
                                                student_directory_name,
                                                f'{student_directory_name}.txt'), 'w') as file:
                                file.write(question.answer)
                    
                    if IMAGE_CHOICE == 'y':
                        image_ids: list = question.image_ids
                        
                        if image_ids != None:
                            for id in image_ids:
                                print(f'\nDownloading file (id: {id})')
                                bot.get_file(id).download(os.path.join(
                                    ALL_ANSWERS_DIRECTORY,
                                    question_directory_name,
                                    student_directory_name,
                                    f'{student_directory_name} image #{image_ids.index(id)}'
                                ))
                    
            self.stdout.write(self.style.SUCCESS('\nResults were received successfully!\n'))
            
        except Exception as e:
            print(e)
            return
        
        print()
