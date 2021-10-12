from django.core.management.base import BaseCommand
from telegram import Bot, Poll, Message
from telegram.utils.request import Request
from bot_admin.models import *
import os


class Command(BaseCommand):
    help = 'Send poll'
    
    def handle(self, *args, **kwargs):
        request = Request(
            connect_timeout=0.5,
            read_timeout=1.0
        )
        
        bot = Bot(
            request=request,
            token=os.getenv('TOKEN')
        )
        
        polls = TelegramPoll.objects.all()
        
        current_open_period = None
        current_question = None
        current_options = []
        current_correct_options = []
        
        max_poll: TelegramPoll = polls.order_by('-poll_group_id').first()
        
        if max_poll != None:
            next_id = max_poll.poll_group_id + 1
        else:
            next_id = 0
            
        choice = input('Would you like to set open period (up to 600 seconds)? (y/n) ')
        
        if choice == 'y':
            try:
                current_open_period = int(input('Please, enter open period in seconds up to 600: '))
                if current_open_period < 1 or current_open_period > 600:
                    raise Exception('Invalid open period')
            except Exception as e:
                print(e)
                return
        else:
            print('\nYou can close your poll manually by close_poll command')
        
        current_question = input('\nPlease, enter poll question: ')
        
        try:
            option_number = int(input('\nPlease, enter number of options from 2 to 10: '))
            if option_number < 2 or option_number > 10:
                raise Exception('Invalid option number')
        except Exception as e:
            print(e)
            return
        
        for i in range(option_number):
            current_options.append(input(f'\nEnter the option #{i + 1}: '))
            choice = input(f'Is option correct? (y/n)')
            if choice == 'y':
                current_correct_options.append(i)
                print('Marked as correct')
            else:
                print('Marked as wrong')
        
        if len(current_correct_options) == 0:
            print('At least 1 correct option is required')
            return
            
        print('\nPoll group ID: ' + str(next_id) + '\n')
        
        choice = input('Would you like to specify student usernames (you can find them by "list_students" command)? (y/n) ')
            
        if choice == 'y':
            students = []
            
            usernames = input('\nEnter student usernames divided by space who will receive message: ').split()

            for username in usernames:
                student: Student = Student.objects.filter(
                    telegram_username=username
                ).first()
                
                if student == None:
                    self.stdout.write(self.style.ERROR(f'Student {username} was not found'))
                else:
                    students.append(student)
        else:
            students = Student.objects.all()
        
        for student in students:
            student: Student
            
            message: Message = bot.send_poll(
                chat_id=student.telegram_chat_id,
                question=current_question,
                options=current_options,
                type=Poll.REGULAR,
                allows_multiple_answers=True,
                is_anonymous=False,
                open_period=current_open_period,
                explanation=None
            )
            
            telegram_poll: TelegramPoll = TelegramPoll.objects.create(
                student=student,
                telegram_message_id=message.message_id,
                telegram_poll_id=message.poll.id,
                correct_options=current_correct_options,
                poll_group_id=next_id,
                option_number=option_number,
                question=current_question,
                open_period=current_open_period
            )
            
            self.stdout.write(self.style.SUCCESS(f'\nSending to {student.real_name} from group {student.group}'))
        
        print('\nPoll was successfully sent')
        
        print()
