from threading import current_thread
from typing import Match
from django.core.management.base import BaseCommand
from telegram import (
    Bot, 
    Update, 
    Poll,
    KeyboardButton, 
    ReplyKeyboardMarkup,
    ParseMode,
)
import telegram
from telegram.ext import (
    CallbackContext, 
    Filters, 
    Updater, 
    CommandHandler, 
    MessageHandler,
    PollAnswerHandler,
)
from telegram.ext.dispatcher import DispatcherHandlerStop
from telegram.ext import ConversationHandler
from telegram.utils.request import Request
from bot_admin.models import *
import os
import logging
from . import is_valid_group, is_valid_name
from dotenv import load_dotenv


load_dotenv()
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)

EDIT_NAME_KEYBOARD_VALUE = 'Edit name'
EDIT_GROUP_KEYBOARD_VALUE = 'Edit group'
CANCEL_KEYBOARD_VALUE = '/cancel'

EDIT_PROFILE_KEYBOARD_VALUE = '/edit_profile'
SHOW_PROFILE_KEYBOARD_VALUE = '/show_profile'
SIGN_UP_KEYBOARD_VALUE = '/signup'
HELP_KEYBOARD_VALUE = '/help'

edit_keyboard = [[EDIT_NAME_KEYBOARD_VALUE, 
                  EDIT_GROUP_KEYBOARD_VALUE, 
                  CANCEL_KEYBOARD_VALUE]]
edit_markup = ReplyKeyboardMarkup(keyboard=edit_keyboard, 
                                  one_time_keyboard=False, 
                                  resize_keyboard=True)

main_keyboard = [[SHOW_PROFILE_KEYBOARD_VALUE, 
                  EDIT_PROFILE_KEYBOARD_VALUE, 
                  HELP_KEYBOARD_VALUE,
                  SIGN_UP_KEYBOARD_VALUE]]
main_markup = ReplyKeyboardMarkup(keyboard=main_keyboard, 
                                  one_time_keyboard=False, 
                                  resize_keyboard=True)

CHOOSE_OPTION_ACTION = 0
GET_TYPED_USERNAME_ACTION = 1
GET_TYPED_GROUP_ACTION = 2

REAL_NAME_DATA = 'real_name'
GROUP_DATA = 'group'


# @log_errors
# def do_echo(update: Update, context: CallbackContext):
#     chat_id = update.message.chat_id
#     text = update.message.text
    
#     p, just_created = Profile.objects.get_or_create(
#         external_id=chat_id,
#         defaults={
#             'username': update.message.from_user.username
#         }
#     )
    
#     msg = Message(
#         profile=p,
#         text=text
#     )
#     msg.save()
    
#     button = [[KeyboardButton('Press Me!', request_poll=KeyboardButtonPollType())]]
    
    
#     # reply_text = f'Your ID: {p.id}\nMessage ID: {msg.id}\n\n{text}'
#     # update.effective_message.reply_text(
#     #     text=reply_text,
#     #     reply_markup=button
#     # )
    
    
#     # button = [[KeyboardButton("Press me!", request_poll=KeyboardButtonPollType())]]
#     # message = "Press the button to let the bot generate a preview for your poll"
#     # update.effective_message.reply_text(
#     #     message, reply_markup=ReplyKeyboardMarkup(button, one_time_keyboard=True, resize_keyboard=True)
#     # )
    
#     questions = ["Good", "Really good", "Fantastic", "Great"]
#     message = context.bot.send_poll(
#         update.effective_chat.id,
#         "How are you?",
#         questions,
#         is_anonymous=False,
#         allows_multiple_answers=True,
#     )
#     # Save some info about the poll the bot_data for later use in receive_poll_answer
#     payload = {
#         message.poll.id: {
#             "questions": questions,
#             "message_id": message.message_id,
#             "chat_id": update.effective_chat.id,
#             "answers": 0,
#         }
#     }
#     context.bot_data.update(payload)

# @log_errors
# def count_messages(update: Update, context: CallbackContext):
#     chat_id = update.message.chat_id
    
#     profile, just_created = Profile.objects.get_or_create(
#         external_id=chat_id,
#         defaults={
#             'username': update.message.from_user.username
#         }
#     )
    
#     count = Message.objects.filter(profile=profile).count()
    
#     update.message.reply_text(
#         text=f'You have {count} messages'
#     )
    

# def quiz(update: Update, context: CallbackContext) -> None:
#     """Send a predefined poll"""
#     questions = ["1", "2", "4", "20"]
#     message = update.effective_message.reply_poll(
#         "How many eggs do you need for a cake?", questions, type=Poll.QUIZ, correct_option_id=2
#     )
#     # Save some info about the poll the bot_data for later use in receive_quiz_answer
#     payload = {
#         message.poll.id: {"chat_id": update.effective_chat.id, "message_id": message.message_id}
#     }
#     context.bot_data.update(payload)


def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        text=('Welcome to Survey Bot!\n' + 
              'If don\'t know how to use this bot send /help command.')
    )
    
    if (Student.objects.filter(telegram_id=update.effective_user.id).exists()):
        current_student: Student = Student.objects.get(telegram_id=update.effective_user.id)
        update.message.reply_text(
            text=f'Welcome back, {current_student.telegram_username}!',
            reply_markup=main_markup
            
        )
    else:
        update.message.reply_text(
            text='Please, sign up to receive surveys by /signup.\nWe need to get your real name and group.',
            reply_markup=main_markup,
        )
        

def edit_profile(update: Update, context: CallbackContext):
    if (Student.objects.filter(telegram_id=update.effective_user.id).exists()):
        update.message.reply_text(
            text='Please choose which option you want to edit',
            reply_markup=edit_markup
        )
        
        return CHOOSE_OPTION_ACTION
    else:
        update.message.reply_text(
            text='Student not found. Please sign up by /signup command.',
            reply_markup=main_markup
        )
        
        return ConversationHandler.END
    
        
def edit_name(update: Update, context: CallbackContext) -> int:
    logging.info(f'{update.effective_user.username} edits name')
    
    update.message.reply_text('Please send your real name (100 characters limit)')
    
    return GET_TYPED_USERNAME_ACTION
        
        
def edit_group(update: Update, context: CallbackContext) -> int:
    logging.info(f'{update.effective_user.username} edits group')
    update.message.reply_text('Please send your group (100 characters limit)')
    
    return GET_TYPED_GROUP_ACTION


def get_edit_typed_username(update: Update, context: CallbackContext) -> int:
    res = update.message.text
    
    logging.info(f'{update.effective_user.username} typed {res}')
    
    res = res.strip().replace('  ', ' ')
    
    if (is_valid_name(res)):
        current_student: Student = Student.objects.get(telegram_id=update.effective_user.id)
        
        current_student.real_name = res
        current_student.save()
        
        update.message.reply_text(
            text=f'Name was edited successfully\nCurrent name: {current_student.real_name}',
            reply_markup=main_markup
        )
        
        return ConversationHandler.END
        
    else:
        update.message.reply_text(
            text='Invalid name. Try again',
            reply_markup=edit_markup
        )    


def get_edit_typed_group(update: Update, context: CallbackContext) -> int:
    res = update.message.text
    
    logging.info(f'{update.effective_user.username} typed {res}')
    
    if (is_valid_group(res)):
        current_student: Student = Student.objects.get(telegram_id=update.effective_user.id)
        
        current_student.group = res
        current_student.save()
        
        update.message.reply_text(
            text=f'Group was edited successfully\nCurrent group: {current_student.group}',
            reply_markup=main_markup
        )
        
        return ConversationHandler.END
    else:
        update.message.reply_text(
            text='Invalid group. Try again.',
            reply_markup=edit_markup
        )    


def get_signup_typed_username(update: Update, context: CallbackContext) -> int:
    res = update.message.text
    
    logging.info(f'{update.effective_user.username} typed {res}')
    
    res = res.strip().replace('  ', ' ')
    
    if (is_valid_name(res)):
        context.user_data[REAL_NAME_DATA] = res
        
        update.message.reply_text(
            text='Name was added successfully',
            reply_markup=main_markup
        )
        
        update.message.reply_text(
            text='Please send your group (100 characters limit)',
            reply_markup=main_markup
        )
        
        return GET_TYPED_GROUP_ACTION
    else:
        update.message.reply_text(
            text='Invalid name. Try again.',
            reply_markup=main_markup
        )


def get_signup_typed_group(update: Update, context: CallbackContext) -> int:
    res = update.message.text
    
    logging.info(f'{update.effective_user.username} typed {res}')
    
    if (is_valid_group(res)):
        context.user_data[GROUP_DATA] = res
        
        update.message.reply_text(
            text='Group was added successfully',
            reply_markup=main_markup
        )
        
        real_name = context.user_data[REAL_NAME_DATA]
        group = res
        
        current_student: Student = Student.objects.create(
            telegram_id=update.effective_user.id,
            telegram_username=update.effective_user.username,
            telegram_chat_id=update.effective_chat.id,
            real_name=real_name,
            group=group
        )
        
        update.message.reply_text(
            text=(f'Sign up was successfull.\nWelcome, {current_student.real_name} (group {current_student.group})!\n' + 
                  f'You can check your data by /show_profile.'),
            reply_markup=main_markup
        )
        
        return ConversationHandler.END
    else:
        update.message.reply_text(
            text='Invalid group. Try again.',
            reply_markup=main_markup
        )


def sign_up(update: Update, context: CallbackContext):
    if (Student.objects.filter(telegram_id=update.effective_user.id).exists()):
        update.message.reply_text(
            text='You are already signed up. But you can edit your profile by /edit_profile.',
            reply_markup=main_markup
        )
    else:
        if REAL_NAME_DATA in context.user_data:
            del context.user_data[REAL_NAME_DATA]
            
        if GROUP_DATA in context.user_data:
            del context.user_data[GROUP_DATA]
        
        update.message.reply_text(
            text='Please send your real name (100 characters limit)',
            reply_markup=main_markup
        )
        
        return GET_TYPED_USERNAME_ACTION


def cancel(update: Update, context: CallbackContext):
    update.message.reply_text(
            text='Operation was canceled',
            reply_markup=main_markup
        )
    return ConversationHandler.END


def help(update: Update, context: CallbackContext):
    text = ('• With this bot you can receive surveys and quizes from an instructor\n\n' +
        '• Edit your profile by /edit_profile\n\n' +
        '• Show profile by /show_profile\n\n')
    
    update.message.reply_text(
        text=text,
        reply_markup=main_markup
    )
    

def show_profile_info(update: Update, context: CallbackContext):
    if (Student.objects.filter(telegram_id=update.effective_user.id).exists()):
        current_student: Student = Student.objects.get(telegram_id=update.effective_user.id)
        
        text = (f'Telegram username: {current_student.telegram_username}\n\n' + 
                f'Real name: {current_student.real_name}\n\n' + 
                f'Group: {current_student.group}\n\n')
        
        update.message.reply_text(
            text=text,
            reply_markup=main_markup
        )
    else:
        update.message.reply_text(
            text='Student not found. Please sign up by /signup command.',
            reply_markup=main_markup
        )

def receive_answer(update: Update, context: CallbackContext):
    
    # update.poll.options[0].voter_count
    
    logging.info(update.poll_answer.user.username + 
                 ' answered ' + str(update.poll_answer.option_ids) + 
                 'to poll (id: ' + str(update.poll_answer.poll_id) + ')')
    
    # if context.bot_data[poll_id]["answers"] == 3:
    #     context.bot.stop_poll(
    #         context.bot_data[poll_id]["chat_id"], context.bot_data[poll_id]["message_id"]
    #     )
    
    
class Command(BaseCommand):
    help = 'Survey Bot'
    
    def handle(self, *args, **options):
        updater = Updater(os.getenv('TOKEN'), use_context=True)
        dispatcher = updater.dispatcher
        
        # dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, quiz))
        # dispatcher.add_handler(CommandHandler('count', count_messages))
        
        # dispatcher.add_handler(PollAnswerHandler(receive_answer))
        
        edit_conversation_handler = ConversationHandler(
            entry_points=[CommandHandler('edit_profile', edit_profile)],
            states={
                CHOOSE_OPTION_ACTION: [
                    MessageHandler(Filters.regex(f'^{EDIT_NAME_KEYBOARD_VALUE}$'), edit_name),
                    MessageHandler(Filters.regex(f'^{EDIT_GROUP_KEYBOARD_VALUE}$'), edit_group),
                    CommandHandler('cancel', cancel)
                ],
                GET_TYPED_USERNAME_ACTION: [
                    MessageHandler(Filters.text & ~(Filters.command), get_edit_typed_username),
                    CommandHandler('cancel', cancel)
                ],
                GET_TYPED_GROUP_ACTION: [
                    MessageHandler(Filters.text & ~(Filters.command), get_edit_typed_group),
                    CommandHandler('cancel', cancel)
                ]
            },
            fallbacks=[]
        )
        
        signup_conversation_handler = ConversationHandler(
            entry_points=[CommandHandler('start', start),
                          CommandHandler('signup', sign_up)],
            states={
                GET_TYPED_USERNAME_ACTION: [
                    MessageHandler(Filters.text & ~(Filters.command), get_signup_typed_username),
                ],
                GET_TYPED_GROUP_ACTION: [
                    MessageHandler(Filters.text & ~(Filters.command), get_signup_typed_group),
                ]
            },
            fallbacks=[]
        )
        
        dispatcher.add_handler(edit_conversation_handler)
        dispatcher.add_handler(signup_conversation_handler)
        dispatcher.add_handler(CommandHandler('help', help))
        dispatcher.add_handler(CommandHandler('show_profile', show_profile_info))
        
        updater.start_polling()
        updater.idle()
