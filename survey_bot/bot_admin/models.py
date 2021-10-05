from django.db import models
from django.db.models.deletion import PROTECT


class Student(models.Model):
    telegram_id = models.PositiveIntegerField(
        verbose_name='Telegram ID',
        unique=True
    )
    
    telegram_username = models.TextField(
        verbose_name='Telegram username',
        null=False,
        unique=True
    )
    
    telegram_chat_id = models.PositiveBigIntegerField(
        verbose_name='Telegram chat ID',
        null=False,
        unique=True
    )
    
    real_name = models.TextField(
        verbose_name='Real name',
        null=False
    )
    
    group = models.TextField(
        verbose_name='Group',
        null=False
    )
    
    class Meta:
        verbose_name='Student'
    
    def __str__(self):
        return f'Student({self.telegram_username}, group: {self.group})'
    

class TelegramMessage(models.Model):
    student = models.ForeignKey(
        to='bot_admin.Student',
        verbose_name='Student',
        on_delete=PROTECT,
        null=False
    )
    
    telegram_message_id = models.PositiveBigIntegerField(
        null=False,
        verbose_name='Telegram message ID',
        unique=True
    )
    
    text = models.TextField(
        null=False,
        verbose_name='Message text',
    )
    
    message_group_id = models.TextField(
        null=False,
        verbose_name='Message group ID'
    )
    
    created_at = models.DateTimeField(
        verbose_name='Time',
        auto_now_add=True
    )
    
    def __str__(self):
        return f'Message {self.pk} to {self.student}'
    
    class Meta:
        verbose_name = 'Telegram Message'
    

class TelegramPoll(models.Model):
    student = models.ForeignKey(
        to='bot_admin.Student',
        verbose_name='Student',
        on_delete=PROTECT,
        null=False
    )
    
    telegram_message_id = models.PositiveBigIntegerField(
        null=False,
        verbose_name='Telegram message ID',
        unique=True
    )
    
    telegram_poll_id = models.TextField(
        null=False,
        verbose_name='Telegram poll ID',
        unique=True
    )
    
    poll_group_id = models.PositiveBigIntegerField(
        null=False,
        verbose_name='Poll group id'
    )
    
    question = models.TextField(
        null=False,
        verbose_name='Poll question'
    )
    
    created_at = models.DateTimeField(
        verbose_name='Time',
        auto_now_add=True
    )
    
    correct_options = models.JSONField(
        verbose_name='Correct options',
        null=False
    )
    
    is_student_passed = models.BooleanField(
        verbose_name='Is student passed',
        default=False
    )
    
    def __str__(self):
        return f'Poll {self.pk} to {self.student}'
    
    class Meta:
        verbose_name = 'Telegram Poll'
    