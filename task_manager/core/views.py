from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm, SignUpForm, AssignUserForm
from django.utils import timezone

# Create your views here.

@login_required
def index(request):
    tasks = Task.objects.all()
    context = {
        'tasks': tasks
    }
    return render(request, 'core/index.html', context )

def signup(request):

    if request.method == "POST":
        form = SignUpForm(request.POST)
        form.save()
        return redirect('/')

    else:
        form = SignUpForm()

    context = {
        'form': form
    }

    return render(request, 'core/signup.html', context)

@login_required
def signout(request):
    logout(request)
    return redirect('core:signin')

@login_required
def create_task(request):

    if request.method == "POST":
        form = TaskForm(request.POST)

        if form.is_valid():
            f = form.save(commit=False)
            f.created_by = request.user
            f.save()
            return redirect('core:detail', f.id)
    else:    
        form = TaskForm()
        for field in ['completed_date', 'start_date', 'task_status']:
            form.fields.pop(field)

    context = {
        'form': form,
        'title': 'Create Task',
    }
    return render(request, 'core/form.html', context)

@login_required
def dashboard(request):
    task_created = Task.objects.filter(created_by = request.user)

    task_completed_by_user = Task.objects.filter(assign_user=request.user, task_status='CO')
    task_completed_by_other_user = Task.objects.filter(created_by=request.user, task_status='CO')

    task_assign_to_user = Task.objects.filter(assign_user=request.user, task_status='PR')
    task_assign_to_other_user = Task.objects.filter(created_by=request.user, task_status='PR')


    context ={
        'task_created': task_created,
        'task_completed_by_user':task_completed_by_user,
        'task_completed_by_other_user': task_completed_by_other_user,
        'task_assign_to_user':  task_assign_to_user,
        'tasks_created_by_user_but_assigned_to_other_user' : task_assign_to_other_user,
    }
    return render(request, 'core/dashboard.html', context)

@login_required
def detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    context = {
        'task': task
    }
    return render(request, 'core/detail.html', context)

@login_required
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk, created_by=request.user)
    task.delete()
    return redirect('core:dashboard')

@login_required
def edit_task(request, pk):
    task = get_object_or_404(Task, pk=pk, created_by=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)

        if form.is_valid():
            form.save()
            return redirect('core:detail', task.id)
    
    else:
        form = TaskForm(instance=task)

        for field in ['completed_date', 'start_date', 'task_status']:
            form.fields.pop(field)
        

    context = {
        'form':form,
        'title': 'Edit Task',
    }
    return render(request, 'core/form.html', context)

@login_required
def completed(request, pk):

    task = get_object_or_404(Task, pk=pk, assign_user=request.user)
    if task.assign_user:
        task.task_status = 'CO'
        task.completed_date= timezone.now()
        task.save()
        messages.success(request, f"Task has been completed")
        return redirect('core:detail', task.id)

    else: 
        messages.warning(request, f'The task canot be completed unless it is assign to a user')
        return redirect('core:assign_user', task.id)

@login_required
def assign_user(request, pk):
    task = get_object_or_404(Task, pk=pk, created_by=request.user)
    
    if request.method == 'POST':
        form = AssignUserForm(request.POST)

        if form.is_valid():
            task.assign_user = form.cleaned_data['assign_user']
            task.task_status = 'PR'
            task.start_date = timezone.now()
            task.save()
            messages.success(request, f'{task.assign_user} has been assigned to {task.name}.')
            return redirect('core:detail', task.id)
    
    else:
        form= AssignUserForm(initial={'assign_user': task.assign_user})
    context = {
        'form': form,
        'task': task
    }
    return render(request, 'core/assign_user.html', context)

