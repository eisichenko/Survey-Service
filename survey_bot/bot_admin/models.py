from time import strftime
from django.db import models
from django.db.models.deletion import PROTECT
from datetime import datetime, timedelta


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
    
    answer = models.TextField(
        null=True,
        verbose_name='Question answer'
    )
    
    image_ids = models.JSONField(
        verbose_name='Image answer IDs',
        null=True
    )
    
    message_group_id = models.PositiveBigIntegerField(
        null=False,
        verbose_name='Message group ID'
    )
    
    is_closed = models.BooleanField(
        null=False,
        verbose_name='Is question closed'
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
    
    selected_options = models.JSONField(
        verbose_name='Selected options by student',
        null=True
    )
    
    correct_options = models.JSONField(
        verbose_name='Correct options',
        null=False
    )
    
    is_manually_closed = models.BooleanField(
        verbose_name='Is poll manually closed',
        default=False
    )
    
    open_period = models.PositiveIntegerField(
        verbose_name='Open period',
        null=True
    )
    
    option_number = models.PositiveIntegerField(
        verbose_name='Option number',
        null=False
    )
    
    is_student_passed = models.BooleanField(
        verbose_name='Is student passed',
        default=False
    )
    
    def is_closed(self):
        if self.open_period != None:
            created_at = datetime.fromisoformat(str(self.created_at)).replace(tzinfo=None)
            is_finished = datetime.utcnow() - created_at  > timedelta(seconds=self.open_period)
            return is_finished
        return self.is_manually_closed
        
    def __str__(self):
        return f'Poll {self.pk} to {self.student}'
    
    class Meta:
        verbose_name = 'Telegram Poll'
    