from django.core.management.base import BaseCommand
from bot_admin.models import *


class Command(BaseCommand):
    help = 'Get poll results'
    
    def handle(self, *args, **kwargs):
        print()
        
        try:
            poll_group_ids: str = input('Enter poll group IDs divided by space (you can find them by "list_polls" command): ')
            poll_group_ids = [int(id) for id in poll_group_ids.split()]
            
            total_polls = len(poll_group_ids)
            correct_answers = {}
            
            for poll_group_id in poll_group_ids:
                polls = TelegramPoll.objects.filter(poll_group_id=poll_group_id).all()
                
                if len(polls) == 0:
                    self.stdout.write(self.style.ERROR(f'Poll group (group id: {poll_group_id}) was not found'))
                    continue
            
                for poll in polls:
                    poll: TelegramPoll
                    current_student: Student = poll.student
                    
                    if not current_student in correct_answers.keys():
                        correct_answers[current_student] = 0
                    
                    if poll.is_student_passed:
                        correct_answers[current_student] += 1
                        
            self.stdout.write(self.style.SUCCESS('\nResults were received successfully!\n'))
            
            for student, correct_number in sorted(correct_answers.items(), key=lambda item: (item[0].group, item[0].real_name.lower())):
                student: Student
                
                print(f'Name: {student.real_name}; Group: {student.group}; ' + 
                      f'Correct: {correct_number}/{total_polls} ({correct_number / float(total_polls) * 100.0 :0.2f}%)\n')
            
        except Exception as e:
            print(e)
            return
        
        print()
