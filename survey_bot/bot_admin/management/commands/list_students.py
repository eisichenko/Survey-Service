from django.core.management.base import BaseCommand
from django.db.models.functions import Lower
from bot_admin.models import *


class Command(BaseCommand):
    help = 'List students'
    
    def handle(self, *args, **kwargs):
        print()
        
        students = Student.objects.all().order_by('group', Lower('real_name'))
        
        for student in students:
            student: Student
            print(f'Group: {student.group}; ' + 
                  f'Real name: {student.real_name}; ' + 
                  f'Username: {student.telegram_username}\n')
        
        print()
        