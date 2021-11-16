from django.core.management.base import BaseCommand
from telegram import (
    Update, 
    ReplyKeyboardMarkup,
    ParseMode,
    Bot
)
from telegram.ext import (
    CallbackContext, 
    Filters, 
    Updater,
    CommandHandler, 
    MessageHandler,
    PollAnswerHandler,
    CallbackQueryHandler,    
)
from telegram.utils.request import Request
from telegram.ext import ConversationHandler
from bot_admin.models import *
import os
import logging
from . import is_valid_group, is_valid_name, log_errors
from .send_question import answer_edit_markup, ANSWER_DATA, EDIT_DATA
from datetime import datetime


EDIT_NAME_KEYBOARD_VALUE = 'Редатировать имя'
EDIT_GROUP_KEYBOARD_VALUE = 'Редактировать группу'
CANCEL_KEYBOARD_VALUE = '/cancel'

EDIT_PROFILE_KEYBOARD_VALUE = '/edit_profile'
SHOW_PROFILE_KEYBOARD_VALUE = '/show_profile'
SIGN_UP_KEYBOARD_VALUE = '/signup'
HELP_KEYBOARD_VALUE = '/help'

edit_keyboard = [[EDIT_NAME_KEYBOARD_VALUE], 
                  [EDIT_GROUP_KEYBOARD_VALUE], 
                  [CANCEL_KEYBOARD_VALUE]]
edit_markup = ReplyKeyboardMarkup(keyboard=edit_keyboard, 
                                  one_time_keyboard=False, 
                                  resize_keyboard=True)

main_keyboard = [[SIGN_UP_KEYBOARD_VALUE,
                  HELP_KEYBOARD_VALUE],
                 [SHOW_PROFILE_KEYBOARD_VALUE, 
                  EDIT_PROFILE_KEYBOARD_VALUE]]
main_markup = ReplyKeyboardMarkup(keyboard=main_keyboard, 
                                  one_time_keyboard=False, 
                                  resize_keyboard=True)


CHOOSE_OPTION_ACTION = 0
GET_TYPED_USERNAME_ACTION = 1
GET_TYPED_GROUP_ACTION = 2

GET_TYPED_ANSWER_ACTION = 0

REAL_NAME_DATA = 'real_name'
GROUP_DATA = 'group'

ANSWERING_MESSAGE_ID_DATA = 'answer_msg_id'
EDITING_ANSWER_MESSAGE_ID_DATA = 'edit_ans_msg_id'
MEDIA_GROUP_IDS_DATA = 'media_group_ids'
IMAGE_IDS_DATA = 'image_ids'
GROUP_TARGET_ID_DATA = 'group_target_id'


@log_errors
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        text=('Добро пожаловать в бот для проведения опросов!\n' + 
              f'Если не знаете, как пользоваться, введите {HELP_KEYBOARD_VALUE}.')
    )
    
    if (Student.objects.filter(telegram_id=update.effective_user.id).exists()):
        current_student: Student = Student.objects.get(telegram_id=update.effective_user.id)
        update.message.reply_text(
            text=f'Добро пожаловать, {current_student.real_name}!',
            reply_markup=main_markup
            
        )
    else:
        update.message.reply_text(
            text=f'У вас нет аккаунта, введите {SIGN_UP_KEYBOARD_VALUE}.',
            reply_markup=main_markup,
        )
        

@log_errors
def edit_profile(update: Update, context: CallbackContext):
    if (Student.objects.filter(telegram_id=update.effective_user.id).exists()):
        update.message.reply_text(
            text='Выберите, что редактировать',
            reply_markup=edit_markup
        )
        
        return CHOOSE_OPTION_ACTION
    else:
        update.message.reply_text(
            text=f'У вас нет аккаунта, введите {SIGN_UP_KEYBOARD_VALUE}.',
            reply_markup=main_markup
        )
        
        return ConversationHandler.END
    
        
@log_errors
def edit_name(update: Update, context: CallbackContext) -> int:
    logging.info(f'{update.effective_user.username} edits name')
    
    update.message.reply_text('Отправьте ваше имя (максимум 100 символов)')
    
    return GET_TYPED_USERNAME_ACTION
        

@log_errors
def edit_group(update: Update, context: CallbackContext) -> int:
    logging.info(f'{update.effective_user.username} edits group')
    update.message.reply_text('Отправьте вашу группу (максимум 100 символов)')
    
    return GET_TYPED_GROUP_ACTION


@log_errors
def get_edit_typed_username(update: Update, context: CallbackContext) -> int:
    res = update.message.text
    
    logging.info(f'{update.effective_user.username} typed {res}')
    
    res = res.strip().replace('  ', ' ')
    
    if (is_valid_name(res)):
        current_student: Student = Student.objects.get(telegram_id=update.effective_user.id)
        
        current_student.real_name = res
        current_student.save()
        
        update.message.reply_text(
            text=f'Имя отредактировано успешно\nТеперь вас зовут: {current_student.real_name}',
            reply_markup=main_markup
        )
        
        return ConversationHandler.END
        
    else:
        update.message.reply_text(
            text='Неверное имя, попробуйте другое',
            reply_markup=edit_markup
        )    


@log_errors
def get_edit_typed_group(update: Update, context: CallbackContext) -> int:
    res = update.message.text
    
    logging.info(f'{update.effective_user.username} typed {res}')
    
    if (is_valid_group(res)):
        current_student: Student = Student.objects.get(telegram_id=update.effective_user.id)
        
        current_student.group = res
        current_student.save()
        
        update.message.reply_text(
            text=f'Группа была отредактирована успешно\nТеперь вы в группе: {current_student.group}',
            reply_markup=main_markup
        )
        
        return ConversationHandler.END
    else:
        update.message.reply_text(
            text='Неверная группа, попробуйте другую',
            reply_markup=edit_markup
        )    


@log_errors
def get_signup_typed_username(update: Update, context: CallbackContext) -> int:
    res = update.message.text
    
    logging.info(f'{update.effective_user.username} typed {res}')
    
    res = res.strip().replace('  ', ' ')
    
    if (is_valid_name(res)):
        context.user_data[REAL_NAME_DATA] = res
        
        update.message.reply_text(
            text='Имя успешно добавлено',
            reply_markup=main_markup
        )
        
        update.message.reply_text(
            text='Теперь отправьте вашу группу (максимум 100 символов)',
            reply_markup=main_markup
        )
        
        return GET_TYPED_GROUP_ACTION
    else:
        update.message.reply_text(
            text='Неверное имя, попробуйте другое',
            reply_markup=main_markup
        )


@log_errors
def get_signup_typed_group(update: Update, context: CallbackContext) -> int:
    res = update.message.text
    
    logging.info(f'{update.effective_user.username} typed {res}')
    
    if (is_valid_group(res)):
        chat_id = update.message.chat.id
        
        context.user_data[GROUP_DATA] = res
        
        update.message.reply_text(
            text='Группа была добавлена успешно',
            reply_markup=main_markup
        )
        
        real_name = context.user_data[REAL_NAME_DATA]
        group = res
        
        current_student: Student = Student.objects.create(
            telegram_id=chat_id,
            telegram_chat_id=chat_id,
            real_name=real_name,
            group=group
        )
        
        update.message.reply_text(
            text=(f'Регистрация успешно завершена.\nПривет, {current_student.real_name} из группы {current_student.group}!\n' + 
                  f'Посмотреть профиль - {SHOW_PROFILE_KEYBOARD_VALUE}.\n\n' + 
                  f'Теперь инструктор может отправлять вам опросы'),
            reply_markup=main_markup
        )
        
        return ConversationHandler.END
    else:
        update.message.reply_text(
            text='Неверная группа, попробуйте другую',
            reply_markup=main_markup
        )


@log_errors
def sign_up(update: Update, context: CallbackContext):
    if (Student.objects.filter(telegram_id=update.effective_user.id).exists()):
        update.message.reply_text(
            text=f'Вы уже зарегестрированы. Если хотите отредактировать профиль, введите {EDIT_PROFILE_KEYBOARD_VALUE}.',
            reply_markup=main_markup
        )
    else:
        if REAL_NAME_DATA in context.user_data:
            del context.user_data[REAL_NAME_DATA]
            
        if GROUP_DATA in context.user_data:
            del context.user_data[GROUP_DATA]
        
        update.message.reply_text(
            text=f'Если хотите отменить, введите {CANCEL_KEYBOARD_VALUE}\n\nОтправьте ваше имя (максимум 100 символов)',
            reply_markup=main_markup
        )
        
        return GET_TYPED_USERNAME_ACTION


@log_errors
def cancel(update: Update, context: CallbackContext):
    update.message.reply_text(
            text='Операция отменена',
            reply_markup=main_markup
        )
    return ConversationHandler.END


@log_errors
def help(update: Update, context: CallbackContext):
    text = ('• С помощью этого бота вы можете получать опросы от вашего инструктора\n\n' +
        f'• Редактировать профиль - {EDIT_PROFILE_KEYBOARD_VALUE}\n\n' +
        f'• Посмотреть профиль - {SHOW_PROFILE_KEYBOARD_VALUE}\n\n' + 
        f'• Зарегистрироваться - {SIGN_UP_KEYBOARD_VALUE}\n\n' + 
        f'• Отмена - {CANCEL_KEYBOARD_VALUE}\n\n')
    
    update.message.reply_text(
        text=text,
        reply_markup=main_markup
    )
    

@log_errors
def show_profile_info(update: Update, context: CallbackContext):
    if (Student.objects.filter(telegram_id=update.effective_user.id).exists()):
        current_student: Student = Student.objects.get(telegram_id=update.effective_user.id)
        
        text = (f'Имя: {current_student.real_name}\n\n' + 
                f'Группа: {current_student.group}\n\n')
        
        update.message.reply_text(
            text=text,
            reply_markup=main_markup
        )
    else:
        update.message.reply_text(
            text=f'У вас нет аккаунта, введите {SIGN_UP_KEYBOARD_VALUE}.',
            reply_markup=main_markup
        )
        

@log_errors
def receive_poll_answer(update: Update, context: CallbackContext):
    request = Request(
        connect_timeout=2.0,
        read_timeout=2.0
    )
    
    bot = Bot(
        request=request,
        token=os.getenv('TOKEN')
    )
    
    if not Student.objects.filter(telegram_id=update.effective_user.id).exists():
        bot.send_message(
            chat_id=update.poll_answer.user.id,
            text=f'Ответ не был записан, потому что у вас нет аккаунта, введите {SIGN_UP_KEYBOARD_VALUE}.'
        )
        return
    
    if not TelegramPoll.objects.filter(telegram_poll_id=update.poll_answer.poll_id).exists():
        bot.send_message(
            chat_id=update.poll_answer.user.id,
            text='Вы уже не можете отвечать на этот опрос, потому что он удален.'
        )
        return
    
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


@log_errors
def receive_answer_operation(update: Update, context: CallbackContext):    
    query = update.callback_query
    
    if not Student.objects.filter(telegram_id=query.from_user.id).exists():
        query.message.reply_text(
            text=f'У вас нет аккаунта, введите {SIGN_UP_KEYBOARD_VALUE}.'
        )
        return
    
    if not TelegramMessage.objects.filter(telegram_message_id=query.message.message_id).exists():
        query.message.reply_text(
            text='Вы не можете отвечать на этот вопрос, потому что он удален.'
        )
        return
    
    query.answer()
    
    logging.info(f'operation: ' + str(query.data))
    
    if query.data == ANSWER_DATA:
        context.user_data[ANSWERING_MESSAGE_ID_DATA] = query.message.message_id
        
    elif query.data == EDIT_DATA:
        context.user_data[EDITING_ANSWER_MESSAGE_ID_DATA] = query.message.message_id
        
    question: TelegramMessage = TelegramMessage.objects.get(telegram_message_id=query.message.message_id)
    
    query.message.reply_text(
        text=(f'Отправьте свой ответ на вопрос "{question.text}" картинками или текстом' + 
                '\n\n• Ограничение текстового сообщения 4096 символов' + 
                '\n\n• Сообщение с картинками - до 10 картинок и 1024 символов'+ 
                '\n\n• Отправьте /cancel_question чтобы отменить отправку')
    )


@log_errors
def unknown_command(update: Update, context: CallbackContext):
    target_data = None
    group_target_id = None
    
    if ANSWERING_MESSAGE_ID_DATA in context.user_data:
        target_data = ANSWERING_MESSAGE_ID_DATA
    elif EDITING_ANSWER_MESSAGE_ID_DATA in context.user_data:
        target_data = EDITING_ANSWER_MESSAGE_ID_DATA
    
    answer_text = update.message.text
    if answer_text == None:
        answer_text = update.message.caption
        
    if answer_text == '/cancel_question':
        if target_data != None:
            del context.user_data[target_data]
        update.message.reply_text('Sending answer was canceled')
        return
        
    if MEDIA_GROUP_IDS_DATA not in context.user_data:
        context.user_data[MEDIA_GROUP_IDS_DATA] = {}
        
    groups: dict = context.user_data[MEDIA_GROUP_IDS_DATA]

    media_group_id = update.message.media_group_id
    
    if media_group_id != None and target_data != None:
        if media_group_id not in groups:
            groups.clear()
            groups[media_group_id] = {}
            groups[media_group_id][IMAGE_IDS_DATA] = []
            groups[media_group_id][GROUP_TARGET_ID_DATA] = context.user_data[target_data]
            context.user_data[MEDIA_GROUP_IDS_DATA]
            
    if media_group_id != None and media_group_id in groups.keys():
        group_target_id = groups[media_group_id][GROUP_TARGET_ID_DATA]
    
    image = None
    
    if update.message.photo != None and len(update.message.photo) > 0:
        image = update.message.photo[-1]

    print('\n\nmedia group id: ' + str(media_group_id))
    if media_group_id != None and media_group_id in groups.keys():
        print('image ids: ' + str(groups[media_group_id][IMAGE_IDS_DATA]))
    print('target data: ' + str(target_data))
    print('group target id: ' + str(group_target_id))
    print('image: ' + str(image))
    print('groups: ' + str(groups))
    
    if group_target_id != None:
        # handle group of images
        target_msg_id = group_target_id
        is_first_image_in_group = target_data != None
        
        question_message: TelegramMessage = TelegramMessage.objects.get(
            telegram_message_id=target_msg_id
        )
        
        if question_message.is_closed:
            if target_data != None:
                del context.user_data[target_data]
            update.message.reply_text('Вопрос закрыт')
            return
        
        if is_first_image_in_group:
            question_message.answer = answer_text
        
        if image != None:
            image_ids = groups[media_group_id][IMAGE_IDS_DATA]
            image_ids.append(image.file_id)
            question_message.image_ids = image_ids
            
        question_message.save()
        
        if is_first_image_in_group:
            msg_text = '<b><i>Вопрос (<u>ОТВЕЧЕНО</u>)</i></b>:\n\n' + question_message.text
            
            if image != None:
                msg_text += f'\n\n<b><i>Картинки прикреплены {datetime.utcnow().strftime("%d/%m/%y %H:%M:%S")} (UTC)</i></b>'
            
            if answer_text != None and len(answer_text) > 0:
                msg_text += '\n\n<b><i>Ваш ответ</i></b>:\n\n' + answer_text
            
            try:
                context.bot.edit_message_text(
                    text=msg_text,
                    chat_id=update.message.chat_id,
                    reply_markup=answer_edit_markup,
                    message_id=target_msg_id,
                    parse_mode=ParseMode.HTML
                )
            except:
                print(f'message {target_msg_id} is too old to edit')
            
            if target_data == ANSWERING_MESSAGE_ID_DATA:
                update.message.reply_text(text=f'Ответ на вопрос "{question_message.text}" был успешно записан')
            elif target_data == EDITING_ANSWER_MESSAGE_ID_DATA:
                update.message.reply_text(text=f'Ответ на вопрос "{question_message.text}" был отредактирован успешно')
            
            del context.user_data[target_data]
    elif target_data != None:
        # handle text message
        target_msg_id = context.user_data[target_data]
        
        question_message: TelegramMessage = TelegramMessage.objects.get(
            telegram_message_id=target_msg_id
        )
        
        if question_message.is_closed:
            if target_data != None:
                del context.user_data[target_data]
            update.message.reply_text('Вопрос закрыт')
            return
        
        question_message.answer = answer_text
        
        if image != None:
            question_message.image_ids = [image.file_id]
        else:
            question_message.image_ids = None
            
        question_message.save()
        
        msg_text = '<b><i>Вопрос (<u>ОТВЕЧЕНО</u>)</i></b>:\n\n' + question_message.text
        
        if image != None:
            msg_text += f'\n\n<b><i>Картинки прикреплены {datetime.utcnow().strftime("%d/%m/%y %H:%M:%S")} (UTC)</i></b>'
        
        if answer_text != None and len(answer_text) > 0:
            msg_text += '\n\n<b><i>Ваш ответ</i></b>:\n\n' + answer_text
        
        try:
            context.bot.edit_message_text(
                text=msg_text,
                chat_id=update.message.chat_id,
                message_id=target_msg_id,
                reply_markup=answer_edit_markup,
                parse_mode=ParseMode.HTML
            )
        except:
            print(f'message {target_msg_id} is too old to edit')
        
        if target_data == ANSWERING_MESSAGE_ID_DATA:
            update.message.reply_text(text=f'Ответ на вопрос "{question_message.text}" был записан успешно')
        elif target_data == EDITING_ANSWER_MESSAGE_ID_DATA:
            update.message.reply_text(text=f'Ответ на вопрос "{question_message.text}" был отредактирован успешно')
        
        del context.user_data[target_data]
    else:
        update.message.reply_text(text='Непонятная команда :(')


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
            fallbacks=[CommandHandler('cancel', cancel)]
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
            fallbacks=[CommandHandler('cancel', cancel)]
        )
        
        dispatcher.add_handler(edit_conversation_handler)
        dispatcher.add_handler(signup_conversation_handler)
        dispatcher.add_handler(CommandHandler('help', help))
        dispatcher.add_handler(CommandHandler('show_profile', show_profile_info))
        dispatcher.add_handler(PollAnswerHandler(receive_poll_answer))
        dispatcher.add_handler(CallbackQueryHandler(receive_answer_operation))
        dispatcher.add_handler(MessageHandler(Filters.photo | Filters.text, unknown_command))
        
        updater.start_polling()
        updater.idle()
