from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
from django_summernote import models as summer_model
from django_summernote import fields as summer_fields


class Board(models.Model):
    def get_absolute_url(self):
        return reverse('board:post_list', args=[self.id])

    slug = models.TextField(default='', unique=True)
    name = models.TextField(default='')


class Post(models.Model):
    def get_absolute_url(self):
        return reverse('board:view_post', args=[self.board.slug, self.id])

    title = models.TextField(default='')
    content = models.TextField(default='')
    board = models.ForeignKey(Board, null=True)
    is_delete = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)


class SummerNote(summer_model.Attachment):
    summer_field = summer_fields.SummernoteTextField(default='')


class Comment(models.Model):
    content = models.TextField(default='')
    post = models.ForeignKey(Post, null=True)
