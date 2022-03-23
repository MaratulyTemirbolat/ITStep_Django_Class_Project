from django.urls import (
    path,
    # re_path,
)

from my_new_app.views import (
    index,
    show,
    user_register,
    user_login,
    user_logout,
    view_passed_homeworks,
)


urlpatterns = [
    path('', index, name="page_main"),
    # re_path(r'^show/(?P<username>\w+)/$', show, name="page_show"),
    path('show/<int:user_id>/', show, name="user_info"),
    path('register/', user_register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('passed_homeworks/', view_passed_homeworks, name='passed_homeworks'),
]
