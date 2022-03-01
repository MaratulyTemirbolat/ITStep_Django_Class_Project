from django.urls import (
    path,
    re_path,
)

from my_new_app.views import *


urlpatterns = [
    path('', index, name="page_index"),
    # re_path(r'^show/(?P<username>\w+)/$', show, name="page_show"),
    path('show/<int:user_id>/',show,name="page_show")

]