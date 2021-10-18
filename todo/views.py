from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from todo.models import TodoUsers
from .forms import *
from .utilities import *

# Create your views here.

def login(request):
    return render(request, 'login.html')


def home(request):
    fm = ShowItems()
    userAuthentication = authentication(request)

    if not userAuthentication:
        return redirect('login')
    else:
        items = get_allitems_details(userAuthentication)
        content = {"items": items, 'daily_quote': randomQuoteGenerator(), 'form': fm}
        return render(request, 'main/index.html', content)


def add_todo(request):
    if request.method == 'POST':
        todo_item = request.POST.get('item')
        item_id = request.POST.get('item_id')
        userIs = ''
        if request.user.is_anonymous:
            userIs = TodoUsers.objects.get(username='Random')
        else:
            userIs = TodoUsers.objects.get(username=request.user.username)

        if not item_id:
            item_id = create_todo(username=userIs, text=todo_item)
        elif item_id:
            create_todo(id=item_id, username=userIs, text=todo_item)

        items = get_allitems_details(item_id)
        return JsonResponse({'status': 1, 'items': items})
    else:
        return JsonResponse({'status': 0})


def delete_todo(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        delete_item(item_id)
        items = get_allitems_details(item_id)
        return JsonResponse({'status': 1, 'items': items})
    else:
        return JsonResponse({'status': 0})


def modify_todo(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        item = get_item_details(item_id)

        text = item.text
        id = item.id
        data = {'text': text, 'id': id}
        return JsonResponse({'status': 1, 'item': data})
    else:
        return JsonResponse({"status": 0})


def random_quote(request):
    daily_quote = randomQuoteGenerator()
    return JsonResponse({'quote': daily_quote})

    