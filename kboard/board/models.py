from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q
from django_summernote import fields as summer_fields
from django_summernote import models as summer_model

from core.models import TimeStampedModel


class Board(models.Model):
    def get_absolute_url(self):
        return reverse('board:post_list', args=[self.slug])

    slug = models.TextField(default='', unique=True)
    name = models.TextField(default='')


class PostQuerySet(models.QuerySet):
    def search(self, search_flag, query):
        if search_flag == 'TITLE':
            return self.filter(title__contains=query)
        elif search_flag == 'CONTENT':
            return self.filter(content__contains=query)
        elif search_flag == 'BOTH':
            return self.filter(Q(title__contains=query) | Q(content__contains=query))
        else:
            return self.all()

    def remain(self):
        return self.filter(is_deleted=False)

    def board(self, board):
        return self.filter(board=board)


class PostManager(models.Manager):
    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db)

    def search(self, search_flag, query):
        return self.get_queryset().search(search_flag, query)

    def remain(self):
        return self.get_queryset().remain()

    def board(self, board):
        return self.get_queryset().board(board)


class Post(TimeStampedModel):
    SEARCH_FLAG = [
        ('TITLE', '제목'),
        ('CONTENT', '내용'),
        ('BOTH', '제목+내용')
    ]

    objects = PostManager()

    title = models.CharField(blank=False, max_length=100)
    content = models.TextField(default='')
    file = models.FileField(null=True)
    board = models.ForeignKey(Board, null=True)
    is_deleted = models.BooleanField(default=False)
    page_view_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse('board:view_post', args=[self.id])


class Comment(TimeStampedModel):
    content = models.TextField(default='')
    post = models.ForeignKey(Post, null=True)
    is_deleted = models.BooleanField(default=False)


class EditedPostHistory(TimeStampedModel):
    post = models.ForeignKey(Post, null=False, default=None)
    title = models.TextField(default='')
    content = models.TextField(default='')
    file = models.FileField(null=True)
