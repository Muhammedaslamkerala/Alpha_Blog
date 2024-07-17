from django.contrib import admin
from django.contrib.auth import get_user_model

# Register your models here.

User = get_user_model()
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    search_fields = ('email','first_name', 'last_name',)
    date_hierarchy = 'date_joined'
    fieldsets = (
        ('None',{
            'fields': ('profile_picture','first_name', 'last_name', 'bio','email', 'password',
                       'is_active', 'is_staff', 'is_superuser', 'date_joined', 'last_login')
        }),
    )
