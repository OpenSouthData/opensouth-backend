from rest_framework_simplejwt.token_blacklist import models, admin


class CustomOutstandingTokenAdmin(admin.OutstandingTokenAdmin):
    
    def has_delete_permission(self, *args, **kwargs):
        return True # or whatever logic you want

from django.contrib import admin
from accounts.models import User, ActivationOtp
from django.contrib.auth.models import Permission

# Register your models here.
    
    
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["email", "role", "is_active", "is_admin"]
    list_editable = ["role", "is_active", "is_admin"]
    
    
admin.site.register(ActivationOtp)
admin.site.unregister(models.OutstandingToken)
admin.site.register(models.OutstandingToken, CustomOutstandingTokenAdmin)
