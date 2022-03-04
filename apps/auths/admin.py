from lib2to3.pgen2.token import OP
from typing import Optional

from django.contrib import admin
from django.http import HttpRequest

from auths.models import (
    CustomUser,
)

class CustomUserAdmin(admin.ModelAdmin):
    readonly_fields: tuple = tuple()
    
    def get_readonly_fields(
        self,
        request: HttpRequest,
        obj: Optional[CustomUser] = None
        ) -> tuple:
        if obj:
            return self.readonly_fields + (
                'email',
                'is_root',
                'is_staff',
                'datetime_joined',
            )
        return self.readonly_fields
    

admin.site.register(CustomUser,CustomUserAdmin)