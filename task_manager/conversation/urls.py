from django.urls import path
from . import views

app_name = 'conversation'

urlpatterns = [
    path('<int:pk>/messages', views.task_messages, name='task_messages'),
    path('<int:pk>/sendmessage/', views.send_messages, name='send_messages'),
    path('inbox/', views.inbox, name='inbox'),
]