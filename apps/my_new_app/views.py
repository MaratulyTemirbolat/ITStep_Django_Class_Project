"""Controllers connects the Models to the Views."""
from django.shortcuts import (
    render,  # Function returns HttpResponse filled of template with context
    redirect,  # Function that returns HttpResponseRedirect by URL name
)
from django.http import HttpResponse  # HttpResponse class instance
# from django.contrib.auth.models import User
from django.db.models import QuerySet  # QuerySet type
from django.core.handlers.wsgi import WSGIRequest
from django.contrib.auth import (
    login,  # Fill the request.user with data of sent user instance
    logout,  # Errase the current authenticated user's ID from the request
    authenticate,
)

from my_new_app.models import (
    Student,
    StudentHomework,  # Imported model class StudentHomework
)
from my_new_app.forms import (
    CustomUserRegisterForm,  # Class CustomUserRegisterForm for registration
    CustomerUserLoginForm,  # Class CustomerUserLoginForm for authentication
)
from auths.models import CustomUser  # Imported class CustomUser
from auths.forms import CustomUserForm


def index(request: WSGIRequest) -> HttpResponse:
    """View in form of function for main page."""
    if not request.user.is_authenticated:  # condition for non-authentication
        return render(  # HttpResponse with request, relative template's path
            request,
            'my_new_app/login.html'
        )
    homeworks: QuerySet = StudentHomework.objects.filter(
        user=request.user,
        is_passed=False
    )  # authenticated user's homeworks
    context: dict = {  # context with user's homeworks for template
        'homeworks': homeworks,
    }

    # template's relative path to the user homeworks
    user_homerks_template: str = 'my_new_app/user_main_page.html'

    # HttpResponse filled of template path with context data
    return render(
        request,
        template_name=user_homerks_template,
        context=context
    )


def show(request: WSGIRequest, user_id: int) -> HttpResponse:
    """View in form of function for personal user info page."""
    # The user instance whose id was provided in URL
    user: CustomUser = CustomUser.objects.get(pk=user_id)

    # Context data for HTML template
    context: dict = {
        "ctx_title": 'Профиль пользователя',
        "ctx_user": user,
    }

    # template's relative path to the user information
    user_profile_template: str = "my_new_app/user_profile.html"

    # HttpResponse filled of template path with context data
    return render(
        request,
        template_name=user_profile_template,
        context=context
    )


def user_register(request: WSGIRequest) -> HttpResponse:  # noqa
    form: CustomUserForm = CustomUserForm(
        request.POST
    )
    if not form.is_valid():
        context: dict = {
            'form': form
        }
        return render(
            request=request,
            template_name="my_new_app/register_form.html",
            context=context
        )
    user: CustomUser = form.save(
        commit=False
    )
    email: str = form.cleaned_data['email']
    password: str = form.cleaned_data['password']
    user.email = email
    user.set_password(password)
    user.save()

    user: CustomUser = authenticate(
        email=email,
        password=password
    )
    if user and user.is_active:
        login(request, user)
        homeworks: QuerySet = StudentHomework.objects.filter(
            user=request.user
        )
        return render(
            request=request,
            template_name='my_new_app/user_main_page.html',
            context={'homeworks': homeworks}
        )

# def user_register(request: WSGIRequest) -> HttpResponse:
#     """Registration function view for general user creation."""
#     # checking request type method of function to be POST
#     if request.method == 'POST':
#         # Creating CustomUserRegistrationForm instance with filled data
#         form: CustomUserRegisterForm = CustomUserRegisterForm(request.POST)
#         if form.is_valid():  # checking if the form valid by the input fields
#             custom_user: CustomUser = form.save()  # creating and getting user
#             login(request, custom_user)  # authentication of the created user

#             # HttpResponse filled of template path with user hw list html
#             return render(
#                 request,
#                 template_name="my_new_app/user_list.html"
#             )
#     else:
#         # Creation of CustomUserRegisterForm empty instance
#         form: CustomUserRegisterForm = CustomUserRegisterForm()

#     # HttpResponse filled of template path with context form
#     return render(
#         request,
#         template_name="my_new_app/register_form.html",
#         context={"form": form}
#     )


def user_login(request: WSGIRequest) -> HttpResponse:  # noqa
    if request.method == 'POST':
        email: str = request.POST['email']
        password: str = request.POST['password']

        user: CustomUser = authenticate(
            email=email,
            password=password
        )
        if not user:
            return render(
                request=request,
                template_name="my_new_app/login.html",
                context={'error_message': 'Неверные данные'}
            )
        if not user.is_active:
            return render(
                request=request,
                template_name="my_new_app/login.html",
                context={'error_message': 'Ваш аккаунт был удалён'}
            )
        login(request, user)

        homeworks: QuerySet = StudentHomework.objects.filter(
            user=request.user,
            is_passed=False
        )
        return render(
            request=request,
            template_name='my_new_app/user_main_page.html',
            context={'homeworks': homeworks}
        )
    return render(
        request=request,
        template_name="my_new_app/login.html"
    )


def view_passed_homeworks(request: WSGIRequest) -> HttpResponse:  # noqa
    if request.user.is_authenticated:
        passed_homeworks: QuerySet = StudentHomework.objects.filter(
            user=request.user,
            is_passed=True
        )
        return render(
            request=request,
            template_name='my_new_app/user_main_page.html',
            context={'homeworks': passed_homeworks}
        )
    return render(
        request=request,
        template_name="my_new_app/login.html"
    )

# def user_login(request: WSGIRequest) -> HttpResponse:
#     """User authentication function view."""
#     # checking request type method of function to be POST
#     if request.method == 'POST':

#         # creation of CustomerUserLoginForm instance filled by sent data
#         form: CustomerUserLoginForm = CustomerUserLoginForm(data=request.POST)
#         if form.is_valid():  # checking if the form valid by the input fields
#             cur_user: CustomUser = form.get_user()  # getting enterred user
#             login(request, cur_user)  # Set user to request.user

#             # HttpResponse filled of template path with user hw list html
#             return render(
#                 request=request,
#                 template_name="my_new_app/user_list.html"
#             )
#     else:
#         # Creation of CustomerUserLoginForm empty instance
#         form: CustomerUserLoginForm = CustomerUserLoginForm()

#     # HttpResponse filled of template path with context form
#     return render(
#         request=request,
#         template_name="my_new_app/login.html",
#         context={"form": form}
#     )


def user_logout(request: WSGIRequest) -> HttpResponse:
    """User logout function view."""
    logout(request)

    # creation of CustomerUserLoginForm instance filled by sent data
    form: CustomUserForm = CustomUserForm(request.POST)

    # HttpResponse filled of template path with context form
    return render(
        request=request,
        template_name="my_new_app/login.html",
        context={"form": form}
    )

# def user_logout(request: WSGIRequest) -> HttpResponse:
#     """User logout function view."""
#     logout(request)

#     # creation of CustomerUserLoginForm instance filled by sent data
#     form: CustomerUserLoginForm = CustomerUserLoginForm(data=request.POST)

#     # HttpResponse filled of template path with context form
#     return render(
#         request=request,
#         template_name="my_new_app/login.html",
#         context={"form": form}
#     )
