from django.urls import (
    path,
    # re_path,
)

from my_new_app.views import (
    IndexView,
    ShowView,

    UserRegisterView,
    UserLoginView,
    UserLogoutView,

    CreateHomeworkView,
    DetailHomeworkView,
    DeleteHWView,

    PageHomeworkFilesView,
    HomeworkFilesCreateView,
    HomeworkFilesCheckView,
    HomeworkFilesDeleteView,
)


urlpatterns = [
    path(
        '',
        IndexView.as_view(),
        name="page_main"
    ),
    # re_path(r'^show/(?P<username>\w+)/$', show, name="page_show"),
    path(
        'show/<int:homework_id>/',
        ShowView.as_view(),
        name="user_info"
    ),
    # ------------------------------------------------------|
    # Auths
    #
    path(
        'register/',
        UserRegisterView.as_view(),
        name='register'
    ),
    path(
        'login/',
        UserLoginView.as_view(),
        name='login'
    ),
    path(
        'logout/',
        UserLogoutView.as_view(),
        name='logout'
    ),
    # ------------------------------------------------------|
    # Homework
    #
    path(
        'create_homework/',
        CreateHomeworkView.as_view(),
        name='create_hw'
    ),
    path(
        'detail_homework/<int:homework_id>/',
        DetailHomeworkView.as_view(),
        name="page_homework_detail"
    ),
    path(
        "delete_hw/<int:homework_id>/",
        DeleteHWView.as_view(),
        name="page_homework_delete"
    ),
    # ------------------------------------------------------|
    # Files
    #
    path(
        'view_hw_files/<str:filter_by>/',
        PageHomeworkFilesView.as_view(),
        name="page_homework_files"
    ),
    path(
        "hw_files/<int:homework_id>/",
        HomeworkFilesCreateView.as_view(),
        name="page_homework_file_create"
    ),
    path(
        'homework_files_checked/<int:file_id>/',
        HomeworkFilesCheckView.as_view(),
        name='page_homework_files_check'
    ),
    path(
        'homework_files_delete/<int:file_id>/',
        HomeworkFilesDeleteView.as_view(),
        name='page_homework_files_delete'
    ),
]
