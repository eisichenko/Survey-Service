from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('polls/', views.polls, name='polls'),
    path('polls/<int:group_id>/', views.poll_group, name='poll_group'),
    path('questions/', views.questions, name='questions'),
    path('students/', views.students, name='students')
]
