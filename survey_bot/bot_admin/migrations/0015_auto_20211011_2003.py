# Generated by Django 3.2.7 on 2021-10-11 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot_admin', '0014_telegrammessage_image_answer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='telegrammessage',
            name='image_answer',
        ),
        migrations.AddField(
            model_name='telegrammessage',
            name='image_id_answer',
            field=models.TextField(null=True, verbose_name='Image answer ID'),
        ),
    ]