from django.contrib import admin
from .models import BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'published', 'created_at')
    list_filter = ('published',)
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at')
