from django.contrib import admin
from .models import *


# Register your models here.
class ReqestAdmin(admin.ModelAdmin):
    list_display = ('subject', 'status', 'time_create', 'time_update', 'author', 'tag', 'file')
    list_display_links = ('subject', 'status', 'time_create', 'time_update', 'author', 'tag')
    search_fields = ('subject', 'status', 'time_create', 'time_update', 'author', 'tag')


class TagsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')
    list_display_links = ('pk', 'name')
    search_fields = ('pk', 'name')


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('answeron', 'time_create', 'author')
    list_display_links = ('answeron', 'time_create', 'author')
    search_fields = ('answeron', 'time_create', 'author')


class PostsAdmin(admin.ModelAdmin):
    list_display = ('name', 'Photo', 'author')
    list_display_links = ('name', 'Photo', 'author')
    search_fields = ('name', 'Photo', 'author')


class StatusesAdmin(admin.ModelAdmin):
    list_display = ('name', 'author')
    list_display_links = ('name', 'author')
    search_fields = ('name', 'author')


class LogsAdmin(admin.ModelAdmin):
    list_display = ('date', 'author', 'log')
    list_display_links = ('date', 'author', 'log')
    search_fields = ('date', 'author', 'log')


admin.site.register(Logs, LogsAdmin)
admin.site.register(Tags, TagsAdmin)
admin.site.register(Posts, PostsAdmin)
admin.site.register(RequestAnswer, AnswerAdmin)
admin.site.register(Request, ReqestAdmin)
admin.site.register(Statuses, StatusesAdmin)
