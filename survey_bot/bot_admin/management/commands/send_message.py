from django.core.management.base import BaseCommand
from telegram import Bot, ParseMode
from telegram.utils.request import Request
from bot_admin.models import *
import os


class Command(BaseCommand):
    help = 'Send no reply message to all students'
    
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
            msg_text = input('Please enter the message text (4096 characters limit): ')
                    
            if len(msg_text.strip()) == 0:
                raise Exception('Empty message is not allowed')
            
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
                student: Student
                
                try:
                    bot.send_message(
                        chat_id=student.telegram_chat_id,
                        text=f'<b><i>?????????????????? ???? ??????????????????????:</i></b>\n\n{msg_text}',
                        parse_mode=ParseMode.HTML
                    )
                    
                    self.stdout.write(self.style.SUCCESS(f'\nSending to {student.real_name} from group {student.group}'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'ERROR: ({student}) {e}'))
            
            self.stdout.write(self.style.SUCCESS('\nMessage was sent successfully\n'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(e))
        
        print()
