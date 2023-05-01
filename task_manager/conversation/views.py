from django.shortcuts import render, redirect, get_object_or_404
from core.models import Task
from .forms import SendMessageForm
from .models import Conversation
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required

# Create your views here.

#function to handle when the request user is sender and reciever which is task.assign_user are both request user the filter will return empty value because no value exist
def message_check(request, task):
    if request.user == task.created_by:
        messages = Conversation.objects.filter(Q(sender=request.user, reciever=task.assign_user)|Q(sender=task.assign_user, reciever=request.user), task=task).order_by('sent_at')
    else:
        messages = Conversation.objects.filter(Q(sender=request.user, reciever=task.created_by)|Q (sender=task.created_by, reciever=request.user), task=task ).order_by('sent_at')
    return messages

@login_required
def send_messages(request, pk):
    task = get_object_or_404(Task, pk=pk)

    # To make only those who are assign or created task can send message
    if task.assign_user == request.user or task.created_by == request.user:

        if request.method == 'POST':

            form = SendMessageForm(request.POST)
            message = form.save(commit=False)
            message.sender = request.user
            message.task = task

            if request.user == task.created_by:
                message.reciever = task.assign_user

            else:
                message.reciever = task.created_by

            message.save()
            messages.success(request, f'Message has been succesfully sent to {message.reciever}')
            return redirect('conversation:task_messages', pk)
        else:
            form = SendMessageForm()
    else:
        messages.warning(request, 'you cannot send message')        
        return redirect('core:detail', pk)

    
    context = {
        'form': form,
        'task': task,
        'messages': send_messages(request, task)
    }

    return render(request, 'conversation/task_messages.html', context)

@login_required
def task_messages(request, pk):
    task= Task.objects.filter(pk=pk).first()

    context = {
        'task': task,
        'messages': message_check(request, task),
        'form': SendMessageForm()
    }
    return render(request, 'conversation/task_messages.html', context)

def inbox(request):
    conversations = Conversation.objects.filter(Q(sender=request.user)|Q(reciever=request.user)).order_by('task','-sent_at')
    task_ids = conversations.values('task').distinct()
    latest_conversations = []
    for task_id in task_ids:
        conversation = conversations.filter(task_id=task_id['task']).first()
    latest_conversations.append(conversation)

    

    context = {
        'conversations': latest_conversations
    }
    return render(request, 'conversation/inbox.html', context)