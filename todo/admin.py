from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(TodoApp)
class TodoAppAdmin(admin.ModelAdmin):
    list_display = ['id', 'text', 'username', 'added_date']

@admin.register(TodoUsers)    
class TodoUsersAdmin(admin.ModelAdmin):
    list_display = ['id', 'username']