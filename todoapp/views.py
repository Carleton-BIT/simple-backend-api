from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from django.http import JsonResponse
from rest_framework.response import Response
from .models import Task
from .forms import TaskForm
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from user_agents import parse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import generics
from django.http import JsonResponse
from django.utils.html import mark_safe
import time
from .serializers import TaskSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny

class TaskList(APIView):
    #Below can be used to allow unauth access
    #permission_classes = [AllowAny]

    def get(self, request):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskDetail(APIView):
    #Below can be used to allow unauth access
    #permission_classes = [AllowAny]

    def get(self, request, task_id):
        task = get_object_or_404(Task, pk=task_id)
        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, task_id):
        task = get_object_or_404(Task, pk=task_id)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request, task_id):
        task = get_object_or_404(Task, pk=task_id)
        task.completed = not task.completed
        task.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, task_id):
        task = get_object_or_404(Task, pk=task_id)
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Simple authenticated view (for testing)
class HelloWorldView(APIView):
    def get(self, request):
        return Response({'message': 'Hello, World!'})

# views.py
class UserCreateView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Note that the below is a shortform for the above (generics.CreateApiView is a helpful shortcut)
#class UserCreateView(generics.CreateAPIView):
#    queryset = User.objects.all()
#    serializer_class = UserSerializer


"""
@csrf_exempt
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            # Use mark_safe to prevent HTML escaping
            task = form.save(commit=False)
            task.description = mark_safe(form.cleaned_data['description'])
            task.save()
    return redirect('index')
@csrf_exempt
def toggle_task(request, task_id):
    task = Task.objects.get(pk=task_id)
    task.completed = not task.completed
    task.save()
    return redirect('index')

@csrf_exempt
def delete_task(request, task_id):
    task = Task.objects.get(pk=task_id)
    task.delete()
    return redirect('index')

@csrf_exempt
def edit_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)

    if request.method == 'POST':
        old_description = task.description
        new_description = request.POST.get('description')
        task.description = new_description
        task.save()
        return JsonResponse({'message': f'Task updated from [{old_description}] to [{new_description}] successfully. The secret keyword for this question is ravenousram'})

    return JsonResponse({'message': 'POST requests are only accepted to edit tasks at this endpoint'}, status=400)
"""