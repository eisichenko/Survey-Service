from django.core.management.base import BaseCommand
from telegram import Update, ReplyKeyboardMarkup
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
                  f'You can check your data by /show_profile.\n\n' + 
                  f'Now instructors can send you polls and questions'),
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
        

def unknown_command(update: Update, context: CallbackContext):
    update.message.reply_text(text='Unknown command')


def receive_answer(update: Update, context: CallbackContext):
    
    poll: TelegramPoll = TelegramPoll.objects.get(
        telegram_poll_id=update.poll_answer.poll_id
    )
    
    user_answers = set(update.poll_answer.option_ids)
    correct_answers = set(poll.correct_options)
    
    poll.selected_options = update.poll_answer.option_ids
    poll.is_student_passed = (user_answers == correct_answers)
    poll.save()
    
    logging.info(update.poll_answer.user.username + 
                 ' answered ' + str(user_answers) + 
                 ' to poll (id: ' + str(update.poll_answer.poll_id) + ') ' + 
                 'correct: ' + str(correct_answers) + ' passed: '
                 + str(user_answers == correct_answers))
    
    # if context.bot_data[poll_id]["answers"] == 3:
    #     context.bot.stop_poll(
    #         context.bot_data[poll_id]["chat_id"], context.bot_data[poll_id]["message_id"]
    #     )
    
    
class Command(BaseCommand):
    help = 'Starts the bot'
    
    def handle(self, *args, **options):
        updater = Updater(os.getenv('TOKEN'), use_context=True)
        dispatcher = updater.dispatcher
        
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
        dispatcher.add_handler(PollAnswerHandler(receive_answer))
        dispatcher.add_handler(MessageHandler(Filters.text, unknown_command))
        
        updater.start_polling()
        updater.idle()
