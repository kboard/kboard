from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]

class Account(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET(get_sentinel_user)
    )
    fullName = models.CharField(max_length=150)
    STATUSES = (
        ('created', 'Created'),
        ('deleted', 'Deleted')
    )
    status = models.CharField(max_length=20, choices=STATUSES)

    # Automatic timestamps
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.fullName
