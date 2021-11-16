from django.core.management.base import BaseCommand
from telegram import Bot, ParseMode
from telegram.utils.request import Request
from bot_admin.models import *
import os


class Command(BaseCommand):
    help = 'Close polls'
    
    def handle(self, *args, **kwargs):
        request = Request(
            connect_timeout=2.0,
            read_timeout=2.0
        )
        
        bot = Bot(
            request=request,
            token=os.getenv('TOKEN')
        )
        
        print()
        
        try:
            message_group_ids: str = input('Enter message group IDs divided by space (you can find them by "list_questions" command): ')
            message_group_ids = [int(id) for id in message_group_ids.split()]
            
            choice = input('Are you sure to close questions? (y/n)')
            
            if choice == 'y':
                for message_group_id in message_group_ids:
                    try:
                        questions = TelegramMessage.objects.filter(message_group_id=message_group_id).all()
                        
                        print()
                        
                        if len(questions) == 0:
                            self.stdout.write(self.style.ERROR(f'Message group id {message_group_id} was not found'))
                        
                        print(f'Closing message group ID: {questions[0].message_group_id}; Question: {questions[0].text}; Time (UTC): {questions[0].created_at}\n')
                    
                        for question in questions:
                            question: TelegramMessage
                            
                            question.is_closed = True
                            question.save()
                            
                            if question.answer != None:
                                msg_text = ('<b><i>[ЗАКРЫТ]</i></b>\n\n<b><i>Вопрос (<u>ОТВЕЧЕНО</u>)</i></b>:\n\n' + question.text + 
                                    '\n\n<b><i>Ваш ответ</i></b>:\n\n' + question.answer)
                            else:
                                msg_text = ('<b><i>[ЗАКРЫТ]</i></b>\n\n<b><i>Вопрос</i></b>:\n\n' + question.text)
        

                            bot.edit_message_text(
                                chat_id=question.student.telegram_chat_id,
                                message_id=question.telegram_message_id,
                                text=msg_text,
                                parse_mode=ParseMode.HTML
                            )
                            
                            bot.edit_message_reply_markup(
                                chat_id=question.student.telegram_chat_id,
                                message_id=question.telegram_message_id,
                                reply_markup=None
                            )
                            
                    except Exception as e:
                        print(str(e) + '\n')
                        
                self.stdout.write(self.style.SUCCESS('Questions were closed successfully!'))
            else:
                self.stdout.write(self.style.ERROR('Operaiton was declined.'))
            
        except Exception as e:
            print(e)
            return
        
        print()
