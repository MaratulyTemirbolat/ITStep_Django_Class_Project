"""Controllers connects the Models to the Views."""
from typing import (
    Optional,
    Union,
)

from django.shortcuts import (
    # render,  # Function returns HttpResponse filled of template with context
    redirect,  # Function that returns HttpResponseRedirect by URL name
    get_object_or_404,
)
from django.http import (
    HttpResponse,  # HttpResponse class instance
    HttpResponseRedirect,
)
# from django.contrib.auth.models import User
from django.db.models import (
    QuerySet,  # QuerySet type
    Q,
)
from django.core.handlers.wsgi import WSGIRequest
from django.contrib.auth import (
    login,  # Fill the request.user with data of sent user instance
    logout,  # Errase the current authenticated user's ID from the request
    authenticate,
)
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

from my_new_app.models import (
    # Student,
    StudentHomework,  # Imported model class StudentHomework
    File,
)
from auths.models import CustomUser  # Imported class CustomUser
from auths.forms import CustomUserForm
from abstracts.handlers import ViewHandler
from abstracts.mixins import HttpResponseMixin
from my_new_app.forms import (
    CreateHWForm,
    FileForm,
)


class IndexView(ViewHandler, View):
    """Index View."""

    queryset: QuerySet = StudentHomework.objects.get_non_deleted()
    template_name: str = 'my_new_app/index.html'

    def get(
        self,
        request: WSGIRequest,
        *args: tuple,
        **kwargs: dict
    ) -> HttpResponse:
        """GET request handler."""
        response: Optional[HttpResponse] = \
            self.get_validated_response(
                request
            )
        if response:
            return response

        homeworks: QuerySet = self.queryset.filter(
            user=request.user
        )
        query: str = request.GET.get(
            'query', ''
        )
        if query:
            homeworks = homeworks.filter(
                Q(title__icontains=query) |
                Q(subject__icontains=query)
            ).distinct()

        if not homeworks:
            homeworks = self.queryset

        return self.get_http_response(
            request,
            template_name=self.template_name,
            context={
                'ctx_title': 'Главная страница',
                'ctx_homeworks': homeworks,
                'ctx_user': request.user,
            }
        )


class ShowView(ViewHandler, View):  # noqa
    def get(
        self,
        request: WSGIRequest,
        user_id: int
    ) -> HttpResponse:  # noqa
        response: Optional[HttpResponse] = self.get_validated_response(
            request=request
        )
        if response:
            return response
        user: CustomUser = CustomUser.objects.get(pk=user_id)
        context: dict = {
            "ctx_title": 'Профиль пользователя',
            "ctx_user": user,
        }
        return self.get_http_response(
            request=request,
            template_name="my_new_app/user_profile.html",
            context=context
        )


class UserRegisterView(HttpResponseMixin, View):  # noqa
    def get(
        self,
        request: WSGIRequest
    ) -> Union[HttpResponse, HttpResponseRedirect]:  # noqa
        if not request.user.is_authenticated:
            form: CustomUserForm = CustomUserForm(request.POST)
            return self.get_http_response(
                request=request,
                template_name="my_new_app/register_form.html",
                context={"form": form}
            )
        return redirect('page_main')

    def post(
        self,
        request: WSGIRequest
    ) -> HttpResponseRedirect:  # noqa
        form: CustomUserForm = CustomUserForm(
            request.POST
        )
        if form.is_valid():
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
        return redirect('register')


class UserLoginView(HttpResponseMixin, View):  # noqa    
    def get(
        self,
        request: WSGIRequest
    ) -> Union[HttpResponse, HttpResponseRedirect]:  # noqa
        if not request.user.is_authenticated:
            form: CustomUserForm = CustomUserForm(request.POST)
            return self.get_http_response(
                request=request,
                template_name="my_new_app/login.html",
                context={"form": form}
            )
        return redirect('page_main')

    def post(
        self,
        request: WSGIRequest
    ) -> Union[HttpResponse, HttpResponseRedirect]:  # noqa
        email: str = request.POST['email']
        password: str = request.POST['password']
        user: CustomUser = authenticate(
            email=email,
            password=password
        )
        if not user:
            return self.get_http_response(
                request=request,
                template_name='my_new_app/login.html',
                context={
                    'error_message': 'Неверные данные',
                    "form": CustomUserForm(request.POST)
                }
            )
        if not user.is_active:
            return self.get_http_response(
                request=request,
                template_name='my_new_app/login.html',
                context={
                    'error_message': 'Ваш аккаунт был удалён',
                    "form": CustomUserForm(request.POST)
                }
            )
        login(request, user)
        return redirect('page_main')


class PassedHomeworksView(ViewHandler, View):  # noqa
    def get(
        self,
        request: WSGIRequest
    ) -> HttpResponse:  # noqa
        response: Optional[HttpResponse] = self.get_validated_response(request)
        if response:
            return response
        passed_homeworks: QuerySet = StudentHomework.objects.filter(
            user=request.user,
            is_passed=True
        )
        return self.get_http_response(
            request=request,
            template_name='my_new_app/user_main_page.html',
            context={'homeworks': passed_homeworks}
        )


class UserLogoutView(LoginRequiredMixin, View):  # noqa
    raise_exception = True

    def get(self, request: WSGIRequest) -> HttpResponseRedirect:  # noqa
        logout(request)
        return redirect('login')


class CreateHomeworkView(LoginRequiredMixin, HttpResponseMixin, View):  # noqa
    raise_exception: bool = True
    form: CreateHWForm = CreateHWForm()

    def fill_form(
        self,
        request: WSGIRequest
    ) -> None:  # noqa
        if request.POST or request.FILES:
            self.form = CreateHWForm(request.POST, request.FILES)

    def get(
        self,
        request: WSGIRequest
    ) -> HttpResponse:  # noqa
        self.fill_form(request=request)
        return self.get_http_response(
            request=request,
            template_name='my_new_app/homework_create.html',
            context={"ctx_form": self.form}
        )

    def post(
        self,
        request: WSGIRequest
    ) -> Union[HttpResponseRedirect, HttpResponse]:  # noqa
        # self.form = CreateHWForm(request.POST, request.FILES)
        self.fill_form(request=request)
        if self.form.is_valid():
            print('You are validated')
            my_homework: StudentHomework = self.form.save(commit=False)
            my_homework.user = request.user
            logo_type: str = self.form.cleaned_data['logo'].\
                content_type.split('/')[1].lower()
            print(logo_type)
            if logo_type not in StudentHomework.IMAGE_TYPES:
                context: dict = {
                    "ctx_form": self.form,
                    'error_message': 'Данный формат картинки недоступен'
                }
                return self.get_http_response(
                    request=request,
                    template_name='my_new_app/homework_create.html',
                    context=context
                )
            my_homework.save()
            return redirect("page_main")
        return redirect("create_hw")


class DetailHomeworkView(LoginRequiredMixin, HttpResponseMixin, View):  # noqa
    """Homework Detail View."""

    template_name: str = 'my_new_app/homework_detail.html'

    def get(
        self,
        request: WSGIRequest,
        homework_id: int,
        *args: tuple,
        **kwargs: dict
    ) -> HttpResponse:
        """GET request handler."""
        homework: StudentHomework = get_object_or_404(
            StudentHomework,
            pk=homework_id
        )
        return self.get_http_response(
            request,
            template_name=self.template_name,
            context={
                'ctx_homework': homework,
            }
        )


class PageHomeworkFilesView(ViewHandler, View):  # noqa
    """Homework Files View."""

    queryset: QuerySet = StudentHomework.objects.get_non_deleted()
    template_name: str = 'my_new_app/homework_files.html'

    def get(
        self,
        request: WSGIRequest,
        filter_by: str,
        *args: tuple,
        **kwargs: dict
    ) -> HttpResponse:
        """GET request handler."""
        response: Optional[HttpResponse] = \
            self.get_validated_response(
                request
            )
        if response:
            return response

        files: list = []
        try:
            file_ids: list = []
            homework: StudentHomework
            for homework in self.queryset.filter(
                user=request.user
            ):
                file: File
                for file in homework.files.get_non_deleted():
                    file_ids.append(file.id)

            files: QuerySet = File.objects.filter(
                id__in=file_ids
            )
            if filter_by == 'checked':
                files = files.filter(
                    is_checked=True
                )
        except StudentHomework.DoesNotExist:
            pass

        context: dict = {
            'ctx_files': files,
            'ctx_filter_by': filter_by,
        }
        return self.get_http_response(
            request,
            self.template_name,
            context
        )


class DeleteHWView(ViewHandler, View):  # noqa
    """Homework Delete View."""

    template_name: str = 'my_new_app/index.html'

    def post(
        self,
        request: WSGIRequest,
        homework_id: int,
        *args: tuple,
        **kwargs: dict
    ) -> HttpResponse:
        """POST request handler."""
        response: Optional[HttpResponse] = \
            self.get_validated_response(
                request
            )
        if response:
            return response
        homework = StudentHomework.objects.get(id=homework_id)
        homework.delete()
        homeworks = StudentHomework.objects.filter(user=request.user)\
            .get_non_deleted()

        context: dict = {
            'ctx_homeworks': homeworks,
        }
        return self.get_http_response(
            request=request,
            template_name=self.template_name,
            context=context
        )


class HomeworkFilesCreateView(ViewHandler, View):  # noqa
    """Homework Files Create View."""

    queryset: QuerySet = StudentHomework.objects.get_non_deleted()
    form: FileForm = FileForm
    template_name: str = 'my_new_app/homework_files_create.html'

    def post(
        self,
        request: WSGIRequest,
        homework_id: int,
        *args: tuple,
        **kwargs: dict
    ) -> HttpResponse:
        """POST request handler."""
        _form: FileForm = self.form(
            request.POST or None,
            request.FILES or None
        )
        homework: StudentHomework = get_object_or_404(
            StudentHomework,
            id=homework_id
        )
        if not _form.is_valid():
            context: dict = {
                'ctx_form': _form,
                'ctx_homework': homework,
            }
            return self.get_http_response(
                request=request,
                template_name=self.template_name,
                context=context
            )
        files = homework.files.get_non_deleted()
        form_title: str = _form.cleaned_data.get('title')

        file: File
        for file in files:
            if file.title != form_title:
                continue

            context: dict = {
                'ctx_homework': homework,
                'ctx_form': _form,
                'error_message': 'Файл уже добавлен',
            }
            return self.get_http_response(
                request,
                self.template_name,
                context
            )
        file: File = _form.save(
            commit=False
        )
        file.homework = homework
        file.obj = request.FILES['file']
        file_type: str = file.obj.url.split('.')[-1].lower()

        if file_type not in File.FILE_TYPES:
            context: dict = {
                'ctx_homework': homework,
                'ctx_form': _form,
                'error_message': 'TXT, PDF',
            }
            return self.get_http_response(
                request,
                self.template_name,
                context
            )
        file.save()

        context: dict = {
            'ctx_homework': homework,
        }
        return self.get_http_response(
            request=request,
            template_name='my_new_app/homework_detail.html',
            context={
                'ctx_homework': homework,
            }
        )


class HomeworkFilesCheckView(ViewHandler, View):  # noqa
    """Homework Files Check View."""
    def get(
        self,
        request: WSGIRequest,
        file_id: int,
        *args: tuple,
        **kwargs: dict
    ) -> HttpResponse:
        """POST request handler."""
        from django.http import JsonResponse

        file: File = get_object_or_404(
            File, id=file_id
        )
        try:
            if file.is_checked:
                file.is_checked = False
            else:
                file.is_checked = True
            file.save()

        except (KeyError, File.DoesNotExist):
            return JsonResponse(
                {'success': False}
            )
        return JsonResponse(
            {'success': True}
        )


class HomeworkFilesDeleteView(ViewHandler, View):  # noqa
    """Homework Files Delete View."""

    template_name: str = 'my_new_app/homework_detail.html'

    def post(
        self,
        request: WSGIRequest,
        file_id: int,
        *args: tuple,
        **kwargs: dict
    ) -> HttpResponse:
        """POST request handler."""
        homework: StudentHomework = get_object_or_404(
            StudentHomework,
            id=1
        )
        file: File = StudentHomework.objects.get(
            id=file_id
        )
        file.delete()
        context: dict = {
            'ctx_homework': homework
        }
        return self.get_http_response(
            request=request,
            template_name=self.template_name,
            context=context
        )
