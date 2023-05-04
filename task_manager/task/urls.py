from django.urls import path
from . import views

app_name = 'task'

urlpatterns = [
    path('<int:pk>/assign_reponse/', views.task_response, name='task_response'),
    path('all_response/', views.pending_responses, name='pending_response'),
]