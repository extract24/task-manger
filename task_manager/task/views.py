from django.shortcuts import render, get_object_or_404, redirect
from core.models import Task
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def task_response(request, pk):
    task = get_object_or_404(Task, assign_user=request.user, pk=pk)

    if task.response == 'P':
        if request.method == 'POST':
            response = request.POST.get('response')
            if response == 'accept':
                task.assign_user = request.user
                task.start_date = datetime.today()
                task.response = 'A'
                task.task_status = 'AT'
                task.save()
                messages.success(request, 'Task has been sucessfully accepted')
                return redirect('core:detail', task.id)

            elif response == 'reject':
                task.response = "R"
                task.assign_user = None
                task.task_status = 'UN'
                task.save()
                messages.warning(request, 'Task has been rejected by user')
                return redirect('core:detail', task.id)
        
    else:
        return redirect('core:detail', task.id)

    context = {
        'task': task

    }
    return render(request, 'task/response.html', context)

def pending_responses(request):
    tasks = Task.objects.filter(assign_user= request.user, response='P')

    context = {
        'tasks': tasks,
    }

    return render(request, 'task/pending_responses.html', context)