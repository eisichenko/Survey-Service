from django.core.management.base import BaseCommand
from telegram import Bot, Poll, Message
from telegram.utils.request import Request
from bot_admin.models import *
import os


class Command(BaseCommand):
    help = 'Send poll'
    
    def handle(self, *args, **kwargs):
        request = Request(
            connect_timeout=2.0,
            read_timeout=2.0
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
            self.stdout.write(self.style.WARNING('\nYou can close your poll manually by close_poll command'))
        
        try:
            current_question = input('\nPlease, enter poll question (up to 300 characters): ')
            
            if len(current_question) == 0 or len(current_question) > 300:
                raise Exception('Poll question valid length from 1 to 300 characters')
            
            option_number = int(input('\nPlease, enter number of options from 2 to 10: '))
            if option_number < 2 or option_number > 10:
                raise Exception('Invalid option number')
        except Exception as e:
            self.stdout.write(self.style.ERROR(e))
            return
        
        self.stdout.write(self.style.WARNING('\nOption text limit is 100 characters'))
        
        for i in range(option_number):
            option = input(f'\nEnter the option #{i + 1}: ')
            if len(option) > 0 and len(option) <= 100:
                current_options.append(option)
            else:
                self.stdout.write(self.style.ERROR('ERROR: invalid option length'))
                return
                
            choice = input(f'Is option correct? (y/n)')
            if choice == 'y':
                current_correct_options.append(i)
                self.stdout.write(self.style.SUCCESS('Marked as correct'))
            else:
                self.stdout.write(self.style.ERROR('Marked as wrong'))
        
        if len(current_correct_options) == 0:
            self.stdout.write(self.style.ERROR('At least 1 correct option is required'))
            return
            
        print('\nPoll group ID: ' + str(next_id) + '\n')
        
        choice = input('Would you like to specify GROUPS to send (you can find them by "list_students" command)? (y/n) ')
        
        if choice == 'y':
            students = []
            
            groups = input('\nEnter student GROUPS divided by space which will receive poll: ').split()
            
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
            student: Student
            
            try:
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
                    open_period=current_open_period,
                    options_text=current_options
                )
                
                self.stdout.write(self.style.SUCCESS(f'\nSending to {student.real_name} from group {student.group}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'ERROR: ({student}) {e}'))
        
        self.stdout.write(self.style.SUCCESS('\nPoll was successfully sent'))
        
        print()
