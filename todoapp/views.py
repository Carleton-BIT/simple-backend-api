# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Task
from .serializers import TaskSerializer
from django.shortcuts import get_object_or_404
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')
class TaskList(APIView):
    def get(self, request):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskDetail(APIView):

    def delete(self, request, task_id):
        task = get_object_or_404(Task, pk=task_id)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class TaskToggle(APIView):

    def post(self, request, task_id):
        task = get_object_or_404(Task, pk=task_id)
        task.completed = not task.completed
        task.save()
        return Response(TaskSerializer(task).data)
