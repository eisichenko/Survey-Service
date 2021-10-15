from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('polls/', views.polls, name='polls'),
    path('polls/<int:group_id>/', views.poll_group, name='poll_group'),
    path('polls/close/<int:group_id>/', views.close_poll_group, name='close_poll_group'),
    path('polls/delete/<int:group_id>/', views.delete_poll_group, name='delete_poll_group'),
    path('polls/results/', views.poll_results, name='poll_results'),
    path('polls/results/send/', views.send_poll_results, name='send_poll_results'),
    path('questions/', views.questions, name='questions'),
    path('students/', views.students, name='students')
]
