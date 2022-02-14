from django.contrib import admin

from .models import (Account,
                     Student,
                     Group,
                     Professor
                    )

from typing import Optional

from django.http import HttpRequest

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
        'datetime_deleted'
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
    pass

admin.site.register(
    Account,AccountAdmin
)
admin.site.register(
    Student,StudentAdmin
)

admin.site.register(
    Group,GroupAdmin
)
admin.site.register(Professor,ProfessorAdmin)
