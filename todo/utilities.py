import requests
from bs4 import BeautifulSoup
from django.utils import timezone
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *


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
    try:
        userdetails = TodoUsers.objects.get(username=user)
        return userdetails
    except Exception as e:
        new_user = TodoUsers.objects.create(username=user)
        return new_user


def get_item_details(id):
    try:
        item = TodoApp.objects.get(pk=id)
        return item
    except Exception as e:
        print("Error in getting Item details for ID - ", id)


def get_allitems_details(args):
    user = None
    if isinstance(args, TodoUsers):
        user = args
    elif isinstance(args, (str, int)):
        try:
            item = TodoApp.objects.get(pk=args)
            user = item.username
        except Exception as e:
            print('Oh Oh !! This ID is not present. You might be diverted ?')
    
    if user:
        items_queryset = user.todoapp_set.values().order_by("-added_date")
        items = list(items_queryset)
        return items
    else:
        return [0]


def create_todo(**kargs):
    current_date = timezone.now()
    username = kargs.get('username')
    text = kargs.get('text')
    item_id = kargs.get('id')
    item = ''
    if not item_id:
        item = TodoApp(added_date=current_date, username=username, text=text)
    elif item_id:
        item = TodoApp(id=item_id, added_date=current_date, username=username, text=text)
    
    item.save()
    return item.id


def delete_item(id):
    try:
        item = get_item_details(id)
        item.delete()
    except Exception as e:
        print("Error in Deleting ItemID - ", id)


def randomQuoteGenerator():
    BASE_URL = 'https://zenquotes.io/api/random'
    try:
        response = requests.get(BASE_URL)
        soup = BeautifulSoup(response.text, 'html.parser')
        data = soup.find_all('blockquote')
        quote,author = data[0].text.split(' — ')
        return {'quote': quote, 'author': author}
    except Exception as e:
        print("Today is a dry day !!!")
        return None
