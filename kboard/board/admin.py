from django.contrib import admin

from django_summernote.admin import SummernoteModelAdmin

from .models import Post, Board


class PostModelAdmin(SummernoteModelAdmin):
    pass

admin.site.register(Post, PostModelAdmin)
admin.site.register(Board)
