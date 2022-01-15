from django.db import models
from django.contrib.auth.models import User  
from django.db.models.signals import post_save  
from django.dispatch import receiver

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_pk = models.IntegerField(null=True)
    userId = models.TextField(unique=True)
    detail = models.TextField(blank=True)

    def __str__(self):
        return self.userId