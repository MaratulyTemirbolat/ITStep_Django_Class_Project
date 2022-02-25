from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.core.handlers.wsgi import WSGIRequest


def index(request: WSGIRequest) -> HttpResponse:
    users: QuerySet = User.objects.all()
    context: dict = {
        'users': users
    }
    
    return render(request,'my_new_app/index.html',context)

def show(request: WSGIRequest, username: str) -> HttpResponse:
    user: User = User.objects.get(username=username)
    context: dict = {
        "ctx_title": 'Профиль пользователя',
        "ctx_user": user,
    }
    return render(request,"my_new_app/index_2.html",context=context)
