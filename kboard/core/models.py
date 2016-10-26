from django.db import models


class PostQuerySet(models.QuerySet):
    def search(self, query):
        return self.filter(title__contains=query)

    def remain(self):
        return self.filter(is_deleted=False)

    def get_from_board(self, board):
        return self.filter(board=board)


class PostManager(models.Manager):
    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db)

    def search(self, query):
        return self.get_queryset().search(query)

    def remain(self):
        return self.get_queryset().remain()

    def get_from_board(self, board):
        return self.get_queryset().get_from_board(board)


class TimeStampedModel(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
