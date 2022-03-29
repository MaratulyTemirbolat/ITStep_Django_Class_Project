from django.urls import (
    path,
    # re_path,
)

from my_new_app.views import (
    # index,
    # show,
    # user_register,
    # user_login,
    # user_logout,
    # view_passed_homeworks,
    IndexView,
    ShowView,
    UserRegisterView,
    UserLoginView,
    UserLogoutView,
    PassedHomeworksView,
    CreateHomeworkView,
)


urlpatterns = [
    path('', IndexView.as_view(), name="page_main"),
    # re_path(r'^show/(?P<username>\w+)/$', show, name="page_show"),
    path('show/<int:user_id>/', ShowView.as_view(), name="user_info"),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('passed_homeworks/', PassedHomeworksView.as_view(),
         name='passed_homeworks'),
    path('create_homework/', CreateHomeworkView.as_view(),
         name='create_hw'),
]
