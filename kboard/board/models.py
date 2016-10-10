from django.db import models


class Board(models.Model):
    name = models.TextField(default='')


class Post(models.Model):
    title = models.TextField(default='')
    content = models.TextField(default='')
    board = models.ForeignKey(Board, null=True)


class Comment(models.Model):
    content = models.TextField(default='')
    post = models.ForeignKey(Post, null=True)
