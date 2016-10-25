from django.db import models


class PostQuerySet(models.QuerySet):
    def search(self, query):
        return self.filter(title__contains=query)


class PostManager(models.Manager):
    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db)

    def search(self, query):
        return self.get_queryset().search(query)


class TimeStampedModel(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
