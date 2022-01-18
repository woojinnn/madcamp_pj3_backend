from django.db import models
# Create your models here.

from django.contrib.auth import get_user_model
from .storage import OverwriteStorage

User = get_user_model()


class Post(models.Model):
    author = models.ForeignKey(
        User, related_name="posts", on_delete=models.CASCADE,
        related_query_name="posts")
    contents = models.TextField()
    publish_date = models.DateField(auto_now=True)
    travel_date = models.TextField()
    city = models.CharField(max_length=20)
    expense = models.PositiveIntegerField()
    # likes = models.PositiveBigIntegerField(default=0)
    like_users = models.ManyToManyField(User, blank=True)
    place = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    image = models.ImageField(upload_to='post_imgs', blank=True, null=True)

    @property
    def author_full_name(self):
        try:
            return f'{self.author.nickname}'
        except:
            return "Name Not Set"

    class Meta:
        ordering = ['-publish_date']
