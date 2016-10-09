from django.db import models
from django.core.paginator import Paginator

class Board(models.Model):
    name = models.TextField(default='')


class Post(models.Model):
    title = models.TextField(default='')
    content = models.TextField(default='')
    board = models.ForeignKey(Board, null=True)

    class Meta:
        unique_together = ('board', 'title')
