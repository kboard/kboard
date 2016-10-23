from django.db import models


class TimeStampedModel(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
