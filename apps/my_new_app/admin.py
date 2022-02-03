from django.contrib import admin

from .models import Account

from typing import Optional

from django.http import HttpRequest

class AccountAdmin(admin.ModelAdmin):
    # readonly_fields = (
    #     'description',
    # )
    list_display: tuple = ('user','full_name','description',)
    
    def get_readonly_fields(self, request: HttpRequest, 
                            obj: Optional[Account] = None) -> tuple:
        if obj:
            return self.readonly_fields + ('description',)
        return self.readonly_fields


admin.site.register(
    Account,AccountAdmin
)
