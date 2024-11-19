from django.urls import path
from . import views

urlpatterns = [
    path('', views.TaskList.as_view(), name='index'),
    path('details/<int:task_id>/', views.TaskDetail.as_view(), name='details'),
    path('register/', views.UserCreateView.as_view(), name='register'),
    path('hello/', views.HelloWorldView.as_view(), name='hello_world'),
    #path('add/', views.add_task, name='add_task'),

    #path('toggle/<int:task_id>/', views.toggle_task, name='toggle_task'),
    #path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
    #path('edit/<int:task_id>/', views.edit_task, name='edit_task'),

]