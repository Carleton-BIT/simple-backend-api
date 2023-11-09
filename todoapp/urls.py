from django.urls import path
from .views import TaskList, TaskDetail, TaskToggle

urlpatterns = [
    path('tasks/', TaskList.as_view(), name='task-list'),
    path('tasks/<int:task_id>/', TaskDetail.as_view(), name='task-detail'),
    path('tasks/<int:task_id>/toggle/', TaskToggle.as_view(), name='task-toggle'),
]
