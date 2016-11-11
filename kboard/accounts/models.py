from django.db import models
from django.conf import settings

from core.models import TimeStampedModel


class Account(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
    )
    fullName = models.CharField(max_length=150)
    status = models.CharField(max_length=20)

    def __str__(self):
        return self.fullName
