from django.core.management.base import BaseCommand
from bot_admin.models import *


class Command(BaseCommand):
    help = 'List students'
    
    def handle(self, *args, **kwargs):
        print()
        
        students = Student.objects.all().order_by('telegram_username')
        
        for student in students:
            student: Student
            print(f'Username: {student.telegram_username}; ' + 
                  f'Real name: {student.real_name}; ' + 
                  f'Group: {student.group}\n')
        
        print()
        