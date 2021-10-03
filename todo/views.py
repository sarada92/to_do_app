from django.shortcuts import render, redirect
from django.http import HttpResponse
from todo.models import TodoApp
from django.utils import timezone
import requests
from bs4 import BeautifulSoup

# Create your views here.

def home(request):
    items = TodoApp.objects.all().order_by("-added_date")

    """ Random Quotes """ 
    response = requests.get('https://zenquotes.io/api/random')
    soup = BeautifulSoup(response.text, 'html.parser')

    data = soup.find_all('blockquote')
    quote,author = data[0].text.split(' — ')

    content = {"items": items, 'daily_quote': {'quote': quote, 'author': author}}
    return render(request, 'main/index.html', content)


def add_todo(request):
    if request.method == 'POST':
        todo_item = request.POST.get('content')
        current_date = timezone.now()
        todo_item_obj = TodoApp.objects.create(added_date=current_date, text=todo_item)
    return redirect('/')


def delete_todo(request, todo_id):
    TodoApp.objects.get(id=todo_id).delete() 
    return redirect('/')   


def modify_todo(request, todo_id):
    content = TodoApp.objects.get(id=todo_id)
    return render(request, 'main/modify.html', {'content': content})      

def modify_action(request, todo_id):
    a = TodoApp.objects.get(id=todo_id)
    if request.method == 'POST' and request.POST.get('action') == 'modify':
        content = request.POST.get('new_content')
        a.text = content
        a.save()
    print(request.POST)
    return redirect('/')       