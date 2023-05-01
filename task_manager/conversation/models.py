from django.db import models
from django.contrib.auth.models import User
from core.models import Task
# Create your models here.

class Conversation(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='conversations')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Sent_conversation')
    reciever = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recieved_conversation')
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
