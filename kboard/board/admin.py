from django.contrib import admin

from .models import Post, Board

admin.site.register(Post)
admin.site.register(Board)