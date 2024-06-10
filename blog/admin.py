from django.contrib import admin
from .models import Category, Post
from comments.models import Comment
# Register your models here.

admin.site.site_header = "Alpha Blog Admin"

class CommentInline(admin.StackedInline):
    model = Comment
    extra = 1

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title','author','published_date', 'is_published')
    list_filter = ('is_published','categories','tags')
    search_fields = ('title',)
    date_hierarchy = 'published_date'
    ordering = ('-published_date',)
    filter_horizontal = ('categories','tags', )
    inlines = [CommentInline]
    fieldsets = (
        ('None',{
            'fields': ('title', 'body', 'author', 'categories', 'tags','is_published' )
        }),
        
    )

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)



