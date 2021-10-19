from django.core.management.base import BaseCommand
from telegram import Bot, ParseMode
from telegram.utils.request import Request
from bot_admin.models import *
import os


class Command(BaseCommand):
    help = 'Delete students'
    
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
            choice = input('\nWould you like to specify GROUPS to delete (you can find them by "list_students" command)? (y/n) ')
        
            if choice == 'y':
                students = []
                
                groups = input('\nEnter student GROUPS divided by space which will be deleted: ').split()
                
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
                    choice = input('\nDo you want to delete ALL students? (y/n) ')
                    if choice == 'y':
                        students = Student.objects.all()
                    else:
                        self.stdout.write(self.style.ERROR('\nOperation was declined.'))
                        return
            
            print()
            
            for student in students:
                student: Student
                polls = TelegramPoll.objects.filter(student=student).all()
                messages = TelegramMessage.objects.filter(student=student).all()
                
                if polls != None and len(polls) > 0:
                    for poll in polls:
                        poll: TelegramPoll
                        
                        try:
                            bot.delete_message(
                                chat_id=student.telegram_chat_id,
                                message_id=poll.telegram_message_id
                            )
                        except:
                            pass
                        
                    polls.delete()
                    
                if messages != None and len(messages) > 0:
                    for message in messages:
                        message: TelegramMessage
                        
                        try:
                            bot.delete_message(
                                chat_id=student.telegram_chat_id,
                                message_id=message.telegram_message_id
                            )
                        except:
                            pass
                    messages.delete()
                
                try:
                    bot.send_message(
                        chat_id=student.telegram_chat_id,
                        text='<b><i>Your account was deleted by instructor</i></b>',
                        parse_mode=ParseMode.HTML
                    )
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'ERROR: {student} {e}'))
                
                student.delete()
                
                self.stdout.write(self.style.SUCCESS(f'{student} was deleted successfully'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(e))
            return
        
        print()
