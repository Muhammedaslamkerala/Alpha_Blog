from django.contrib import admin
from .models import Author
# Register your models here.

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('username', 'is_staff','is_active', 'is_superuser')
    search_fields = ('user__username',)
    
    def username(self, obj):
        return obj.user.username
    
    username.short_decription = "Username"
    
    
    def is_staff(self, obj):
        return obj.user.is_staff
    
    is_staff.short_description = "Staff"

    def is_active(self, obj):
        return obj.user.is_active
    
    is_active.short_description = "Active"

    def is_superuser(self, obj):
        return obj.user.is_superuser
    
    is_superuser.short_description = "Superuser"