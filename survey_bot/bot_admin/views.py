from django.shortcuts import render

from .models import *


def home(request):
    return render(request, 'bot_admin/home.html')


def polls(request):
    group_ids = TelegramPoll.objects.all().order_by('-poll_group_id').values_list('poll_group_id').distinct()
    
    poll_groups = []
    
    for group_id in group_ids:
        poll: TelegramPoll = TelegramPoll.objects.filter(poll_group_id=group_id[0]).first()
        if poll != None:
            poll_groups.append([poll, poll.is_closed()])
    
    context = {
        'poll_groups': poll_groups
    }
    
    return render(request, 'bot_admin/polls.html', context=context)


def poll_group(request, group_id):
    polls = TelegramPoll.objects.filter(poll_group_id=group_id).order_by('student__group', 'student__real_name').all()
    
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


def questions(request):
    return render(request, 'bot_admin/questions.html')


def students(request):
    return render(request, 'bot_admin/students.html')
