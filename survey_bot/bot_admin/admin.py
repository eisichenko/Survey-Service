from django.contrib import admin

from .models import *


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 
                    'telegram_id', 
                    'telegram_username', 
                    'telegram_chat_id',
                    'real_name',
                    'group')
    

@admin.register(TelegramMessage)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('student', 
                    'telegram_message_id',
                    'text',
                    'answer',
                    'image_ids',
                    'message_group_id',
                    'is_closed',
                    'created_at')

@admin.register(TelegramPoll)
class PollAdmin(admin.ModelAdmin):
    list_display = ('student', 
                    'telegram_message_id', 
                    'telegram_poll_id',
                    'poll_group_id', 
                    'question', 
                    'created_at', 
                    'option_number',
                    'selected_options',
                    'correct_options',
                    'is_student_passed',
                    'is_manually_closed',
                    'open_period')
