from django.contrib import admin
from .models import *


# Register your models here.
class ReqestAdmin(admin.ModelAdmin):
    list_display = ('subject', 'description', 'status', 'time_create', 'time_update', 'author')
    list_display_links = ('subject', 'description', 'status', 'time_create', 'time_update', 'author')
    search_fields = ('subject', 'description', 'status', 'time_create', 'time_update', 'author')


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('answeron', 'description', 'time_create', 'author')
    list_display_links = ('answeron', 'description', 'time_create', 'author')
    search_fields = ('answeron', 'description', 'time_create', 'author')


class PostsAdmin(admin.ModelAdmin):
    list_display = ('name', 'Photo', 'description', 'author')
    list_display_links = ('name', 'Photo', 'description', 'author')
    search_fields = ('name', 'Photo', 'description', 'author')


class StatusesAdmin(admin.ModelAdmin):
    list_display = ('name', 'author')
    list_display_links = ('name', 'author')
    search_fields = ('name', 'author')


admin.site.register(Posts, PostsAdmin)
admin.site.register(RequestAnswer, AnswerAdmin)
admin.site.register(Request, ReqestAdmin)
admin.site.register(Statuses, StatusesAdmin)
