from django.core.management.base import BaseCommand
from telegram import Bot, Poll, Message
from telegram.utils.request import Request
from bot_admin.models import *
import os


class Command(BaseCommand):
    help = 'Send poll results to students'
    
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
            poll_group_ids: str = input('Enter poll group IDs divided by space (you can find them by "list_polls" command): ')
            poll_group_ids = [int(id) for id in poll_group_ids.split()]
            
            total_polls = len(poll_group_ids)
            correct_answers = {}
            
            poll_questions = []
            
            for poll_group_id in poll_group_ids:
                polls = TelegramPoll.objects.filter(poll_group_id=poll_group_id).all()
                
                if len(polls) == 0:
                    raise Exception(f'Poll group (group id: {poll_group_id}) was not found')
                
                poll_questions.append(polls[0].question)
            
                for poll in polls:
                    poll: TelegramPoll
                    current_student: Student = poll.student
                    
                    if not current_student in correct_answers.keys():
                        correct_answers[current_student] = 0
                    
                    if poll.is_student_passed:
                        correct_answers[current_student] += 1
                        
            print('\nResults were received successfully!\n')
            
            for student, correct_number in correct_answers.items():
                student: Student
                
                print(f'Sending to student Name: {student.real_name}; Group: {student.group}; ' + 
                      f'Correct: {correct_number}/{total_polls} ({correct_number / float(total_polls) * 100.0 :0.2f}%)\n')
                
                text = f'Your result in polls:\n\n'
                
                for i in range(len(poll_questions)):
                    text += f'#{i + 1} Question: "{poll_questions[i]}"\n'
                
                text += '\n'
                text += f'Correct answers: {correct_number}/{total_polls} ({correct_number / float(total_polls) * 100.0 :0.2f}%)\n'
                
                bot.send_message(
                    chat_id=student.telegram_chat_id,
                    text=text
                )
            
        except Exception as e:
            print(e)
            return
        
        print()
