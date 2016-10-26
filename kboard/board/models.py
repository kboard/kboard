from django.core.urlresolvers import reverse
from django.db import models
from django_summernote import fields as summer_fields
from django_summernote import models as summer_model

from core.models import TimeStampedModel, PostManager


class Board(models.Model):
    def get_absolute_url(self):
        return reverse('board:post_list', args=[self.slug])

    slug = models.TextField(default='', unique=True)
    name = models.TextField(default='')


class Post(TimeStampedModel):
    def get_absolute_url(self):
        return reverse('board:view_post', args=[self.board.slug, self.id])

    objects = PostManager()

    title = models.TextField(default='')
    content = models.TextField(default='')
    board = models.ForeignKey(Board, null=True)
    is_deleted = models.BooleanField(default=False)
    page_view_count = models.IntegerField(default=0)


class SummerNote(summer_model.Attachment):
    summer_field = summer_fields.SummernoteTextField(default='')


class Comment(TimeStampedModel):
    content = models.TextField(default='')
    post = models.ForeignKey(Post, null=True)
    is_deleted = models.BooleanField(default=False)
