# Generated by Django 3.2.7 on 2021-10-05 19:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telegram_id', models.PositiveIntegerField(unique=True, verbose_name='Telegram ID')),
                ('telegram_username', models.TextField(unique=True, verbose_name='Telegram username')),
                ('telegram_chat_id', models.PositiveBigIntegerField(unique=True, verbose_name='Telegram chat ID')),
                ('real_name', models.TextField(verbose_name='Real name')),
                ('group', models.TextField(verbose_name='Group')),
            ],
            options={
                'verbose_name': 'Student',
            },
        ),
        migrations.CreateModel(
            name='TelegramPoll',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telegram_poll_id', models.TextField(unique=True, verbose_name='Telegram poll ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Time')),
                ('correct_options', models.JSONField(verbose_name='Correct options')),
                ('is_student_passed', models.BooleanField(default=False, verbose_name='Is student passed')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='bot_admin.student', verbose_name='Student')),
            ],
            options={
                'verbose_name': 'Telegram Poll',
            },
        ),
        migrations.CreateModel(
            name='TelegramMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telegram_message_id', models.PositiveIntegerField(unique=True, verbose_name='Telegram message ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Time')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='bot_admin.student', verbose_name='Student')),
            ],
            options={
                'verbose_name': 'Telegram Message',
            },
        ),
    ]