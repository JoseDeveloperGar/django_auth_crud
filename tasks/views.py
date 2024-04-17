from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import taskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request, 'home.html')

def singup(request):
    if request.method == 'GET':
        return render(request, 'singup.html', {
            'form': UserCreationForm(),
        })
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            #register user
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'singup.html', {
                    'form': UserCreationForm(),
                    'error': 'User alredy exists'
                })
        else: 
            return render(request, 'singup.html', {
                'form': UserCreationForm(),
                'error': 'User alredy exists'
            })

@login_required #este decorador nos ayuda a evitar que los usuarios ingresen a esas funciones sin estar logueados
def tasks(request):
    tasks = Task.objects.filter(user = request.user, datecompleted__isnull=True)
    return render(request, 'tasks.html', {
        'tasks': tasks
    })

@login_required
def singout(request):
    logout(request)
    return redirect('home')

def singin(request):
    if request.method == 'GET':
        return render(request, 'singin.html', {
            'form': AuthenticationForm(),
        })
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'singin.html', {
                'form': AuthenticationForm(),
                'error': 'Username or password is incorrect'
            })
        else:
            login(request, user)
            return redirect('tasks')

@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_new_task.html', {
            'form': taskForm(),
        })
    if request.method == 'POST':
        try:
            form = taskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            #Con request.user estamos accediento a la cookie que contiene al usuario, por lo tanto a su id
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_new_task.html', {
                'form': taskForm(),
                'error': 'Please provide valid data'
            })

@login_required
def task_detail(request, id):
    if request.method == 'GET':
        task = get_object_or_404(Task, id=id, user=request.user)
        form = taskForm(instance=task) #de esta forma creamos una instancia de form taskForm con los datos traidos en task
        return render(request, 'task_detail.html', {
            'task': task,
            'form': form,
        })
    if request.method == 'POST':
        try:
            task = get_object_or_404(Task, id=id, user=request.user)
            form = taskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {
                'task': task,
                'form': form,
                'error': 'Error updating task'
            })

@login_required
def task_completed(request, id):
    task = get_object_or_404(Task, id=id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')

@login_required
def task_delete(request, id):
    task = get_object_or_404(Task, id=id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')

@login_required
def task_completed_yet(request):
    tasks = Task.objects.filter(user = request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'tasks.html', {
        'tasks': tasks
    })