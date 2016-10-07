from django.db import models

class Post(models.Model):
    title = models.TextField(default='')
    content = models.TextField(default='')
