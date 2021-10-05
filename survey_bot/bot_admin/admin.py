from django.contrib import admin

from .models import *


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'telegram_id', 'telegram_username', 'telegram_chat_id')
    

@admin.register(TelegramMessage)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('student', 'telegram_message_id', 'created_at')
