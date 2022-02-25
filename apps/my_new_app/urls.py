from django.urls import (
    path,
    re_path,
)
from .views import *


urlpatterns = [
    path('', index, name="page_index"),
    re_path(r'^show/(?P<username>\w+)/$', show, name="page_show"),
]