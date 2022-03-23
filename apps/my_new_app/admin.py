from typing import Optional

from django.contrib import admin
from django.http import HttpRequest
from django.utils.safestring import mark_safe
# from django.contrib.auth.admin import UserAdmin
# from django.contrib.auth.models import User

from my_new_app.models import (
    Student,
    Group,
    Professor,
    StudentHomework,
    File,
)


# class CustomUserAdmin(UserAdmin):
#     readonly_fields: tuple = ()
#     def get_readonly_fields(self, request: HttpRequest,
#                             obj: Optional[User] = None) -> tuple:
#         if obj:
#             return self.readonly_fields + (
#                 'first_name', 'last_name',
#                 'email', 'username',
#                 'is_active', 'is_staff',
#                 'is_superuser', 'date_joined',
#                 'last_login')
#         return self.readonly_fields


# class AccountAdmin(admin.ModelAdmin):
#     # readonly_fields = (
#     #     'description',
#     # )
#     # list_display: tuple = ('user','full_name','description',)

#     def get_readonly_fields(self, request: HttpRequest,
#                             obj: Optional[Account] = None) -> tuple:
#         if obj:
#             return self.readonly_fields + ('description',)
#         return self.readonly_fields


class StudentAdmin(admin.ModelAdmin):  # noqa
    MAX_STUDENT_EDITABLE_AGE = 16
    readonly_fields: tuple = (
        'datetime_created',
        'datetime_updated',
        'datetime_deleted',
    )
    list_filter: tuple = (
        'age',
        'gpa',
    )
    list_display: tuple = (
        'full_name',
        'age',
        'gpa',
    )

    def student_edit_age_validator(self,
                                   obj: Optional[Student]) -> bool:  # noqa
        validator_result: bool = (obj and
                                  obj.age > self.MAX_STUDENT_EDITABLE_AGE)
        return validator_result

    def get_readonly_fields(self,
                            request: HttpRequest,
                            obj: Optional[Student]) -> tuple:  # noqa
        if(self.student_edit_age_validator(obj)):
            return self.readonly_fields + ('age',)
        return self.readonly_fields


class GroupAdmin(admin.ModelAdmin):  # noqa
    readonly_fields: tuple = (
        'datetime_created',
        'datetime_updated',
        'datetime_deleted',
    )


class ProfessorAdmin(admin.ModelAdmin):
    readonly_fields: tuple = (
        'datetime_created',
        'datetime_updated',
        'datetime_deleted',
        )


class StudentHomeworkAdmin(admin.ModelAdmin):
    readonly_fields = (
        'datetime_created',
        'datetime_updated',
        'datetime_deleted',
    )
    list_filter = ('datetime_deleted',)
    list_display = ('title', 'subject', 'get_logo', 'user')

    def get_logo(self, obj: StudentHomework) -> str:
        if obj.logo:
            return mark_safe(f'<img src="{obj.logo.url}" width="150">')
        return "-"
    get_logo.short_description = 'Логотип'

    def get_readonly_fields(self, request: HttpRequest,
                            obj: Optional[StudentHomework] = None) -> tuple:
        if obj:
            return self.readonly_fields + ('title', 'subject',
                                           'logo', 'user'
                                           )
        return self.readonly_fields


class FileAdmin(admin.ModelAdmin):
    readonly_fields = ()

    def get_readonly_fields(self, request: HttpRequest,
                            obj: Optional[File] = None) -> tuple:
        if obj:
            return self.readonly_fields + ('title', 'file', 'homework')
        return self.readonly_fields


# admin.site.unregister(User)

# admin.site.register(User, CustomUserAdmin)

admin.site.register(Student, StudentAdmin)

admin.site.register(Group, GroupAdmin)

admin.site.register(Professor, ProfessorAdmin)

admin.site.register(StudentHomework, StudentHomeworkAdmin)

admin.site.register(File, FileAdmin)
