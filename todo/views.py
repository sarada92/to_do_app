from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from todo.models import TodoApp, TodoUsers
from django.utils import timezone
import requests
from bs4 import BeautifulSoup

# Create your views here.

def login(request):
    return render(request, 'login.html')

def authentication(request):
    if request.method == 'POST':
        name = request.POST.get('user_name')
        password = request.POST.get('user_password')
        userlogin = authenticate(username=name, password=password)
        
        if userlogin is not None:
            auth_login(request, userlogin)
            return userAddition(name)
        else:  
            messages.info(request, "Invalid Credentials !!!")
            return None
    elif request.user.username:
        return userAddition(request.user.username)
    else:
        return userAddition('Random')


def userAddition(user):
    print(user)
    try:
        userdetails = TodoUsers.objects.get(username=user)
        print('User is present', userdetails)
        return userdetails
    except Exception as e:
        new_user = TodoUsers.objects.create(username=user)
        print('User is present', new_user)
        return new_user


def home(request):

    userdetails = authentication(request)

    if not userdetails:
        return redirect('login')
    
    userdetails = authentication(request)
    userdetails.todoapp_set

    items = userdetails.todoapp_set.all().order_by("-added_date")

    """ Random Quotes """ 
    response = requests.get('https://zenquotes.io/api/random')
    soup = BeautifulSoup(response.text, 'html.parser')
    data = soup.find_all('blockquote')
    quote,author = data[0].text.split(' — ')
    """ <<< Random Quotes >>> """

    content = {"items": items, 'daily_quote': {'quote': quote, 'author': author}}

    return render(request, 'main/index.html', content)


def add_todo(request):
    if request.method == 'POST':
        todo_item = request.POST.get('content')
        current_date = timezone.now()
        userIs = ''
        if request.user.is_anonymous:
            userIs = TodoUsers.objects.get(username='Random')
        else:
            userIs = TodoUsers.objects.get(username=request.user.username)
        todo_item_obj = TodoApp.objects.create(added_date=current_date, username=userIs, text=todo_item)
    return redirect('home')


def delete_todo(request, todo_id):
    TodoApp.objects.get(id=todo_id).delete() 
    return redirect('home')   


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
    return redirect('home')       