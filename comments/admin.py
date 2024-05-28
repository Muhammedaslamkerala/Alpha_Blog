from django.contrib import admin
from .models import Comment
# Register your models here.

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'published_date')
    search_fields = ('post__title', 'author')
    list_filter = ('published_date',)
    date_hierarchy = 'published_date'
    ordering = ('-published_date',)
    
     