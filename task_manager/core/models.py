from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.

def one_week_hence():
    return timezone.now() + timezone.timedelta(7)


class Task(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateTimeField(null=True, blank=True)
    due_date = models.DateTimeField(default=one_week_hence)
    assign_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    completed_date = models.DateTimeField(blank=True, null=True)
    task_status_choices = (
        ('UN', 'Unassign'),
        ('PR', 'In progress'),
        ('AT', 'Task Accepted'),
        ('CO', 'Completed'),
    )
    response_choice = (
        ('P', 'Pending'),
        ('R', 'Rejected'),
        ('A', 'Accepted'),
    )

    response = models.CharField(choices=response_choice, default='P', max_length=1, blank=True, null=True)

    task_status = models.CharField(choices=task_status_choices, default="UN", max_length=2, blank=True, null=True)

    def duration(self):

        if self.start_date is not None and self.completed_date is not None:
            return self.completed_date - self.start_date
        
        else:
            return timedelta()

    def __str__(self):
        return f'{self.name} created by {self.created_by} at {self.created_at}'


