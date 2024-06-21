from django.contrib import admin
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

@admin.register(CustomUser)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active', 'is_superuser')
    search_fields = ('username', 'email')
    
    def username(self, obj):
        return obj.username
    
    username.short_description = "Username"
    
    def email(self, obj):
        return obj.email
    
    email.short_description = "Email"
    
    def is_staff(self, obj):
        return obj.is_staff
    
    is_staff.short_description = "Staff"

    def is_active(self, obj):
        return obj.is_active
    
    is_active.short_description = "Active"

    def is_superuser(self, obj):
        return obj.is_superuser
    
    is_superuser.short_description = "Superuser"
