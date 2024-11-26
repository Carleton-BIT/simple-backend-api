from django.shortcuts import render
from .models import Task
from .forms import TaskForm, UserCreationForm
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from user_agents import parse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.utils.html import mark_safe
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

def sign_up(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'registration/registration.html', {'form':form})


@login_required
def index(request):
    tasks = Task.objects.filter(user=request.user)
    form = TaskForm()

    user_agent = request.META.get('HTTP_USER_AGENT', '')

    return render(request, 'index.html', {'tasks': tasks, 'form': form, 'browser': parse(user_agent).browser.family, 'user':request.user})

def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
    return redirect('index')

def toggle_task(request, task_id):
    task = Task.objects.get(pk=task_id)
    task.completed = not task.completed
    task.save()
    return redirect('index')

def delete_task(request, task_id):
    task = Task.objects.get(pk=task_id)
    task.delete()
    return redirect('index')

def edit_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)

    if request.method == 'POST':
        old_description = task.description
        new_description = request.POST.get('description')
        task.description = new_description
        task.save()
        return JsonResponse({'message': f'Task updated from [{old_description}] to [{new_description}] successfully. The secret keyword for this question is ravenousram'})

    return JsonResponse({'message': 'POST requests are only accepted to edit tasks at this endpoint'}, status=400)