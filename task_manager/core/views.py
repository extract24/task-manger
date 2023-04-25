from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm, SignUpForm

# Create your views here.

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

def signout(request):
    logout(request)
    return redirect('core:signin')

def create_task(request):

    if request.POST == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.created_by = request.user
            f.save()
    else:    
        form = TaskForm()
        form.fields.pop('task_status')

    context = {
        'form': form,
    }
    return render(request, 'core/form.html', context)


def dashboard(request):
    task_assign = Task.objects.filter(assign_user= request.user)
    task_created = Task.objects.filter(created_by = request.user)
    
    context ={
        'task_assign': task_assign,
        'task_created': task_created,
    }
    return render(request, 'core/dashboard.html', context)