from django.db import models
from django.conf import settings


class Account(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
    )
    fullName = models.CharField(max_length=150)
    status = models.CharField(max_length=20)

    # Automatic timestamps
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.fullName
