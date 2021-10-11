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
            connect_timeout=0.5,
            read_timeout=1.0
        )
        
        bot = Bot(
            request=request,
            token=os.getenv('TOKEN')
        )
        
        print()
        
        students = Student.objects.all()
        telegram_messages = TelegramMessage.objects.all()
        
        max_message: TelegramMessage = telegram_messages.order_by('-message_group_id').first()
        
        if max_message != None:
            next_id = str(int(max_message.message_group_id) + 1)
        else:
            next_id = str(0)
        
        try:
            question_text = input('Please enter the question text: ')
                    
            if len(question_text.strip()) == 0:
                raise Exception('Empty question is not allowed')
            
            print()
            
            choice = input('Would you like to specify student usernames (you can find them by "list_students" command)? (y/n)')
            
            if choice == 'y':
                usernames = input('\nEnter student usernames divided by space who will receive message: ').split()

                print()

                for username in usernames:
                    student: Student = Student.objects.filter(
                        telegram_username=username
                    ).first()
                    
                    if student == None:
                        print(f'Student {username} was not found')
                    else:
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
                        
                        print(f'Sending question to {username}')
            else:
                students = Student.objects.all()
                
                print()
                
                for student in students:
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
                    
                    print(f'Sending question to {student.telegram_username}')
                
            self.stdout.write(self.style.SUCCESS('\nQuestion was sent successfully\n'))
        except Exception as e:
            print(e)
        
        print()
