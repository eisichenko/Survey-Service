from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.db.models.functions import Lower
from telegram import Bot, ParseMode
from telegram.utils.request import Request
from .models import *
from .forms import *
import os


def home(request):
    return render(request, 'bot_admin/home.html')


def polls(request):
    group_ids = TelegramPoll.objects.all().order_by('-poll_group_id').values_list('poll_group_id').distinct()
    
    poll_groups = []

    for i in range(len(group_ids)):
        group_id = group_ids[i]
        poll: TelegramPoll = TelegramPoll.objects.filter(poll_group_id=group_id[0]).first()
        if poll != None:
            poll_groups.append([poll, poll.is_closed(), i])

    context = {
        'poll_groups': poll_groups
    }

    return render(request, 'bot_admin/polls.html', context=context)


def poll_group(request, group_id):
    polls = TelegramPoll.objects.filter(poll_group_id=group_id).order_by('student__group', 'student__real_name').all()
    
    if polls != None and len(polls) > 0:
        options = []
        
        for option in polls[0].options_text:
            is_correct = polls[0].options_text.index(option) in polls[0].correct_options
            options.append([option, is_correct])
        
        context = {
            'group_id': group_id,
            'polls': polls,
            'options': options,
            'question': polls[0].question,
            'is_closed': polls[0].is_closed()
        }
        
        return render(request, 'bot_admin/poll_group.html', context=context)
    else:
        return HttpResponseRedirect(reverse('polls'))


def close_poll_group(request, group_id):
    bot_request = Request(
        connect_timeout=2.0,
        read_timeout=2.0
    )
        
    bot = Bot(
        request=bot_request,
        token=os.getenv('TOKEN')
    )
    
    polls = TelegramPoll.objects.filter(poll_group_id=group_id).all()
    
    if polls != None and len(polls) > 0:
        for poll in polls:
            try:
                poll: TelegramPoll
                                
                bot.stop_poll(
                    chat_id=poll.student.telegram_chat_id,
                    message_id=poll.telegram_message_id
                )
                
                poll.is_manually_closed = True
                poll.save()
            except Exception as e:
                print(e)
    
        return HttpResponseRedirect(reverse('poll_group', args=(group_id,)))
    else:
        return HttpResponseRedirect(reverse('polls'))


def delete_poll_group(request, group_id):
    bot_request = Request(
        connect_timeout=2.0,
        read_timeout=2.0
    )
    
    bot = Bot(
        request=bot_request,
        token=os.getenv('TOKEN')
    )
    
    polls = TelegramPoll.objects.filter(poll_group_id=group_id).all()
    
    if polls != None and len(polls) > 0:
        for poll in polls:
            try:
                poll: TelegramPoll
                                
                bot.delete_message(
                    chat_id=poll.student.telegram_chat_id,
                    message_id=poll.telegram_message_id
                )
            except Exception as e:
                print(e)
                
        polls.delete()
    
        return HttpResponseRedirect(reverse('poll_group', args=(group_id,)))
    else:
        return HttpResponseRedirect(reverse('polls'))


def poll_results(request):
    if request.method == 'POST':
        correct_answers = {}
        group_id_choices = []
        total_questions = 0
        
        if 'choices' in request.POST:
            checkbox_id_choices = [int(i) for i in request.POST.getlist('choices')]
            group_ids = TelegramPoll.objects.all().order_by('-poll_group_id').values_list('poll_group_id').distinct()
            
            group_id_choices = [group_ids[i][0] for i in checkbox_id_choices]
            total_questions = len(group_id_choices)
            
            for poll_group_id in group_id_choices:
                polls = TelegramPoll.objects.filter(poll_group_id=poll_group_id).all()
                
                if polls != None and len(polls) > 0:
                    for poll in polls:
                        poll: TelegramPoll
                        current_student: Student = poll.student
                        
                        if not current_student in correct_answers.keys():
                            correct_answers[current_student] = [0]
                        
                        if poll.is_student_passed:
                            correct_answers[current_student][0] += 1
                
            for student in correct_answers:
                correct_answers[student].append(f'{float(correct_answers[student][0]) / total_questions * 100.0 : .2f}')
            
        context = {
            'correct_answers': dict(sorted(correct_answers.items(), key=lambda item: (item[0].group, item[0].real_name.lower()))),
            'total_questions': total_questions
        }
        
        request.session['group_id_choices'] = group_id_choices
        
        return render(request, 'bot_admin/poll_results.html', context=context)
    return HttpResponseRedirect(reverse('polls'))
    

def send_poll_results(request):
    if request.method == 'POST':
        bot_request = Request(
            connect_timeout=2.0,
            read_timeout=2.0
        )
            
        bot = Bot(
            request=bot_request,
            token=os.getenv('TOKEN')
        )
        
        group_id_choices = request.session.get('group_id_choices')
        
        if group_id_choices != None:
            correct_answers = {}
            total_questions = len(group_id_choices)
            poll_questions = []
            
            for poll_group_id in group_id_choices:
                polls = TelegramPoll.objects.filter(poll_group_id=poll_group_id).all()
                
                if polls != None and len(polls) > 0:
                    poll_questions.append(polls[0].question)
                    
                    for poll in polls:
                        poll: TelegramPoll
                        current_student: Student = poll.student
                        
                        if not current_student in correct_answers.keys():
                            correct_answers[current_student] = 0
                        
                        if poll.is_student_passed:
                            correct_answers[current_student] += 1
                            
            for student, correct_number in correct_answers.items():
                student: Student
                
                text = f'<b><i>Your result in polls:</i></b>\n\n'
                
                for i in range(len(poll_questions)):
                    text += f'#{i + 1} Question: "{poll_questions[i]}"\n'
                
                text += '\n'
                text += f'<b><i>Correct answers:</i></b> {correct_number}/{total_questions} ({correct_number / float(total_questions) * 100.0 : .2f}%)\n'
                
                bot.send_message(
                    chat_id=student.telegram_chat_id,
                    text=text,
                    parse_mode=ParseMode.HTML
                )
            
            context = {
                'students': sorted(correct_answers.keys(), key=lambda student: (student.group, student.real_name.lower()))
            }
            
            return render(request, 'bot_admin/send_results_report.html', context=context)
        else:
            return HttpResponseRedirect(reverse('polls'))
    return HttpResponseRedirect(reverse('polls'))


def questions(request):
    group_ids = TelegramMessage.objects.all().order_by('-message_group_id').values_list('message_group_id').distinct()
    
    message_groups = []

    for i in range(len(group_ids)):
        group_id = group_ids[i]
        question: TelegramMessage = TelegramMessage.objects.filter(message_group_id=group_id[0]).first()
        if question != None:
            message_groups.append([question, question.is_closed, i])

    context = {
        'message_groups': message_groups
    }

    return render(request, 'bot_admin/questions.html', context=context)


def message_group(request, group_id):
    questions = TelegramMessage.objects.filter(message_group_id=group_id).order_by('student__group', 'student__real_name').all()
    
    if questions != None and len(questions) > 0:
        context = {
            'group_id': group_id,
            'questions': questions,
            'question_text': questions[0].text,
            'is_closed': questions[0].is_closed
        }
        
        return render(request, 'bot_admin/question_group.html', context=context)
    else:
        return HttpResponseRedirect(reverse('questions'))


def close_message_group(request, group_id):
    bot_request = Request(
        connect_timeout=2.0,
        read_timeout=2.0
    )
        
    bot = Bot(
        request=bot_request,
        token=os.getenv('TOKEN')
    )
    
    questions = TelegramMessage.objects.filter(message_group_id=group_id).all()
    
    if questions != None and len(questions) > 0:
        for question in questions:
            try:
                question: TelegramMessage
                
                question.is_closed = True
                question.save()
                
                if question.answer != None:
                    msg_text = ('<b><i>[CLOSED]</i></b>\n\n<b><i>Question (<u>ANSWERED</u>)</i></b>:\n\n' + question.text + 
                        '\n\n<b><i>Your answer</i></b>:\n\n' + question.answer)
                else:
                    msg_text = ('<b><i>[CLOSED]</i></b>\n\n<b><i>Question</i></b>:\n\n' + question.text)


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
                print(e)
    
        return HttpResponseRedirect(reverse('message_group', args=(group_id,)))
    else:
        return HttpResponseRedirect(reverse('questions'))


def delete_message_group(request, group_id):
    bot_request = Request(
        connect_timeout=2.0,
        read_timeout=2.0
    )
        
    bot = Bot(
        request=bot_request,
        token=os.getenv('TOKEN')
    )
    
    questions = TelegramMessage.objects.filter(message_group_id=group_id).all()
    
    if questions != None and len(questions) > 0:
        for question in questions:
            try:
                question: TelegramMessage
                                
                bot.delete_message(
                    chat_id=question.student.telegram_chat_id,
                    message_id=question.telegram_message_id
                )
            except Exception as e:
                print(e)
                
        questions.delete()
    
        return HttpResponseRedirect(reverse('message_group', args=(group_id,)))
    else:
        return HttpResponseRedirect(reverse('questions'))


def students(request):
    students = Student.objects.all().order_by('group', Lower('real_name'))
    
    context = {
        'students': students
    }
    
    return render(request, 'bot_admin/students.html', context=context)
