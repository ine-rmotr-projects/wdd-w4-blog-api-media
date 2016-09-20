from django.contrib import admin
from blog.models import Blog, User, Entry


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('id', 'name')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'accesskey', 'is_active')
    search_fields = ('id', 'username')


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ('id', 'blog', 'headline', 'number_comments', 'scoring')
    list_filter = ('blog',)
