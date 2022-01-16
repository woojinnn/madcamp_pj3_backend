from django.db import models
# Create your models here.

from django.contrib.auth import get_user_model

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone

from posts.utils import unique_slug_generator
User = get_user_model()


class Post(models.Model):
    title = models.CharField(max_length=120)
    author = models.ForeignKey(
        User, related_name="posts", on_delete=models.CASCADE,
        related_query_name="posts")
    contents = models.TextField()
    slug = models.SlugField(blank=True, null=True)
    publish_date = models.DateField(auto_now=True)
    travel_date = models.DateField(auto_now=False)
    city = models.CharField(max_length=20)
    expense = models.PositiveIntegerField()
    place = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    # image = models.ImageField()/

    def __str__(self):
        return self.title

    @property
    def author_full_name(self):
        try:
            return f'{self.author.username}'
        except:
            return "Name Not Set"
    
    class Meta:
        indexes = [models.Index(fields=['slug'])]
        ordering = ['-publish_date']

@receiver(post_save, sender=Post)
def generate_unique_slug_for_posts(sender, instance, created, *args, **kwargs):
    if created:
        instance.slug = unique_slug_generator(instance)
        instance.save()


@receiver(pre_save, sender=Post)
def update_published_on(sender, instance, **kwargs):
    if instance.id:
        old_value = Post.objects.get(pk=instance.id).publish_date
        if not old_value:
            instance.publish_date = timezone.now()