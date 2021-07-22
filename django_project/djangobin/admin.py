from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from . import models

# Register your models here.


class LanguageAdmin(admin.ModelAdmin):
    """Attributes for model list page customize"""
    list_display = ('name', 'lang_code', 'slug', 'mime', 'created_on')
    search_fields = ['name', 'mime']
    ordering = ['name']
    list_filter = ['created_on']
    date_hierarchy = 'created_on'


class SnippetAdmin(admin.ModelAdmin):
    """Attributes for model list page customize"""
    list_display = ('language', 'title', 'expiration', 'exposure', 'user')
    search_fields = ['title', 'user']
    ordering = ['-created_on']
    list_filter = ['created_on']
    date_hierarchy = 'created_on'

    # """Attributes for object editing page or form page customize"""
    raw_id_fields = ['tags']
    readonly_fields = ('highlighted_code', 'hits', 'slug', )
    fields = ('title', 'original_code', 'highlighted_code', 'expiration', 'exposure',
              'hits', 'slug', 'language', 'user', 'tags')


class TagAdmin(admin.ModelAdmin):
    """Attributes for model list page customize"""
    list_display = ('name', 'slug',)
    search_fields = ('name',)

    # """Attributes for object editing page or form page customize"""
    readonly_fields = ['slug']


class AuthorInline(admin.StackedInline):
    model = models.Author


class CustomUserAdmin(UserAdmin):
    inlines = (AuthorInline,)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(models.Author)
admin.site.register(models.Language, LanguageAdmin)
admin.site.register(models.Snippet, SnippetAdmin)
admin.site.register(models.Tag, TagAdmin)
