# Generated by Django 3.2.7 on 2021-10-19 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot_admin', '0002_telegrampoll_options_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='group',
            field=models.TextField(max_length=100, verbose_name='Group'),
        ),
        migrations.AlterField(
            model_name='student',
            name='real_name',
            field=models.TextField(max_length=100, verbose_name='Real name'),
        ),
        migrations.AlterField(
            model_name='telegrammessage',
            name='answer',
            field=models.TextField(max_length=4096, null=True, verbose_name='Question answer'),
        ),
        migrations.AlterField(
            model_name='telegrammessage',
            name='text',
            field=models.TextField(max_length=4096, verbose_name='Message text'),
        ),
        migrations.AlterField(
            model_name='telegrampoll',
            name='question',
            field=models.TextField(max_length=300, verbose_name='Poll question'),
        ),
    ]
