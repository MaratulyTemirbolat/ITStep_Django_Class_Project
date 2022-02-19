from typing import Optional

from django.contrib import admin
from django.http import HttpRequest
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import (Account,
                     Student,
                     Group,
                     Professor,
                    )

class UserAdmin(UserAdmin):
    def get_readonly_fields(self, request: HttpRequest,
                            obj: Optional[User] = None) -> tuple:
        if obj:
            return self.readonly_fields + (
                'first_name','last_name',
                'email','username',
                'is_active','is_staff',
                'is_superuser','date_joined',
                'last_login')
        return self.readonly_fields


class AccountAdmin(admin.ModelAdmin):
    # readonly_fields = (
    #     'description',
    # )
    # list_display: tuple = ('user','full_name','description',)
    
    def get_readonly_fields(self, request: HttpRequest, 
                            obj: Optional[Account] = None) -> tuple:
        if obj:
            return self.readonly_fields + ('description',)
        return self.readonly_fields


class StudentAdmin(admin.ModelAdmin):
    
    MAX_STUDENT_EDITABLE_AGE = 16
    readonly_fields: tuple = (
        'datetime_created',
        'datetime_updated',
        'datetime_deleted',
        )
    list_filter = (
        'age',
        'gpa',
    )
    search_fields = (
        'account__full_name',
    )
    list_display = (
        'age',
        'gpa',
    )
    
    def student_edit_age_validator(self,
                                   obj: Optional[Student]) -> bool:
        validator_result: bool = (obj and obj.age > self.MAX_STUDENT_EDITABLE_AGE)
        return validator_result
    
    def get_readonly_fields(self, 
                            request: HttpRequest, 
                            obj: Optional[Student]) -> tuple:
        if(self.student_edit_age_validator(obj)):
            return self.readonly_fields + ('age',)
        return self.readonly_fields


class GroupAdmin(admin.ModelAdmin):
    pass


class ProfessorAdmin(admin.ModelAdmin):
    readonly_fields: tuple = (
        'datetime_created',
        'datetime_updated',
        'datetime_deleted',
        )



admin.site.register(Account,AccountAdmin)

admin.site.register(Student,StudentAdmin)

admin.site.register(Group,GroupAdmin)

admin.site.register(Professor,ProfessorAdmin)
