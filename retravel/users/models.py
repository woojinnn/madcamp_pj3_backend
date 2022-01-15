from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    nickname = models.CharField(max_length=20, blank=False, null=False)
    detail = models.TextField(blank=True)

    def __str__(self):
        return self.username