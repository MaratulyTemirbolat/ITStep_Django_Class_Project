from django.shortcuts import render
from django.http import HttpResponse
# from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.core.handlers.wsgi import WSGIRequest
from django.contrib.auth import (
    login,
    logout,
)

from auths.models import CustomUser
from my_new_app.forms import (
    CustomUserRegisterForm,
    CustomerUserLoginForm,
)


def index(request: WSGIRequest) -> HttpResponse:  # noqa
    users: QuerySet = CustomUser.objects.all()
    context: dict = {
        'users': users
    }

    return render(request, 'my_new_app/user_list.html', context)


def show(request: WSGIRequest, user_id: int) -> HttpResponse:  # noqa
    user: CustomUser = CustomUser.objects.get(pk=user_id)
    context: dict = {
        "ctx_title": 'Профиль пользователя',
        "ctx_user": user,
    }
    return render(request, "my_new_app/user_info.html", context=context)


def user_register(request: WSGIRequest) -> HttpResponse:  # noqa
    if request.method == 'POST':
        form: CustomUserRegisterForm = CustomUserRegisterForm(request.POST)
        if form.is_valid():
            custom_user: CustomUser = form.save()
            login(request, custom_user)
            return render(request,
                          "my_new_app/successful_action.html",
                          {"message": "You are successfully registerred"})
    else:
        form: CustomUserRegisterForm = CustomUserRegisterForm()
    return render(request, "my_new_app/register_form.html", {"form": form})


def user_login(request: WSGIRequest) -> HttpResponse:  # noqa
    if request.method == 'POST':
        form: CustomerUserLoginForm = CustomerUserLoginForm(data=request.POST)
        if form.is_valid():
            cur_user: CustomUser = form.get_user()
            login(request, cur_user)
            return render(request,
                          "my_new_app/successful_action.html",
                          {"message": f"Hello {cur_user.email}"})
    else:
        form: CustomerUserLoginForm = CustomerUserLoginForm()
    return render(request, "my_new_app/login.html", {"form": form})


def user_logout(request: WSGIRequest) -> HttpResponse:  # noqa
    logout(request)
    return render(request,
                  "my_new_app/successful_action.html",
                  {"message": "Good buy!"})
