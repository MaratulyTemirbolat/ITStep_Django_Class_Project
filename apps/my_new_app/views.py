from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.db.models import QuerySet

from .models import Student

def index(request) -> HttpResponse:
    users: QuerySet = User.objects.all()
    context: dict = {
        'ctx_title': 'Главная страница',
        'ctx_users': users
    }
    
    return render(request,'my_new_app/index.html',context)
