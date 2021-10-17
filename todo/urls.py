from django.contrib import admin
from django.urls import path
from todo import views

urlpatterns = [
    path('', views.login, name='login'),
    path('todos', views.home, name='home'),
    path('add_todo', views.add_todo, name='add_todo'),
    path('delete_todo', views.delete_todo, name='delete_todo'),
    path('modify_todo', views.modify_todo, name='modify_todo'),
    path('random_quote', views.random_quote, name='random_quote'),
]
