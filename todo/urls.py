from django.contrib import admin
from django.urls import path
from todo import views

urlpatterns = [
    path('todos', views.home, name='home'),
    path('add_todo', views.add_todo, name='add_todo'),
    path('delete_todo/<int:todo_id>/', views.delete_todo, name='delete_todo'),
    path('modify_todo/<int:todo_id>/', views.modify_todo, name='modify_todo'),
    path('modify_action/<int:todo_id>/', views.modify_action, name='modify_action'),
    path('', views.login, name='login'),
]
