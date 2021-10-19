from django.core.management.base import BaseCommand
from telegram import Bot, InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
from telegram.message import Message
from telegram.utils.request import Request
from bot_admin.models import *
import os


ANSWER_DATA = 'answer'
EDIT_DATA = 'edit'

answer_keyboard = [[InlineKeyboardButton(text='📨 Send answer', callback_data=ANSWER_DATA)]]
answer_markup = InlineKeyboardMarkup(answer_keyboard)

answer_edit_keyboard = [[InlineKeyboardButton(text='✍️ Edit answer', callback_data=EDIT_DATA)]]
answer_edit_markup = InlineKeyboardMarkup(answer_edit_keyboard)


class Command(BaseCommand):
    help = 'Send text question to students'
    
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
        
        telegram_messages = TelegramMessage.objects.all()
        
        max_message: TelegramMessage = telegram_messages.order_by('-message_group_id').first()
        
        if max_message != None:
            next_id = str(int(max_message.message_group_id) + 1)
        else:
            next_id = str(0)
        
        try:
            question_text = input('Please enter the question text (4096 characters limit): ')
                    
            if len(question_text.strip()) == 0:
                raise Exception('Empty question is not allowed')
            
            print()
            
            choice = input('Would you like to specify GROUPS to send (you can find them by "list_students" command)? (y/n) ')
            
            if choice == 'y':
                students = []
                
                groups = input('\nEnter student GROUPS divided by space which will receive question: ').split()
                
                print()
                
                for group in groups:
                    group_students = Student.objects.filter(group=group).all()
                    
                    if group_students != None and len(group_students) > 0:
                        students.extend(group_students)
                    else:
                        self.stdout.write(self.style.ERROR(f'Group {group} was not found'))
            else:
                choice = input('\nWould you like to specify student IDs to delete (you can find them by "list_students" command)? (y/n) ')
                
                if choice == 'y':
                    students = []
                    
                    ids = input('\nEnter student IDs divided by space who will be deleted: ').split()

                    for id in ids:
                        try:
                            id = int(id)
                            student: Student = Student.objects.filter(
                                id=id
                            ).first()
                            
                            if student == None:
                                self.stdout.write(self.style.ERROR(f'Student ID {id} was not found'))
                            else:
                                students.append(student)
                        except Exception as e:
                            self.stdout.write(self.style.ERROR(e))
                else:
                    students = Student.objects.all()
                
            for student in students:
                try:
                    message: Message = bot.send_message(
                        chat_id=student.telegram_chat_id,
                        text=('<b><i>Question</i></b>:\n\n' + question_text),
                        reply_markup=answer_markup,
                        parse_mode=ParseMode.HTML
                    )
                    
                    telegram_message: TelegramMessage = TelegramMessage.objects.create(
                        student=student,
                        telegram_message_id=message.message_id,
                        text=question_text,
                        message_group_id=next_id,
                        is_closed=False
                    )
                
                    self.stdout.write(self.style.SUCCESS(f'\nSending question to {student.real_name} from group {student.group}'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR((f'ERROR: ({student}) {e}')))
            
            self.stdout.write(self.style.SUCCESS('\nQuestion was sent successfully\n'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(e))
        
        print()
