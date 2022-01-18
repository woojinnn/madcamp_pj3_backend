from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post
from users.serializers import UserSerializer

User = get_user_model()

# DRF Serializer listing all the blog posts
class PostListSerializer(serializers.ModelSerializer):
    author_full_name = serializers.CharField()
    author = UserSerializer()

    class Meta:
        model = Post
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)
    author = UserSerializer()

    class Meta:
        model = Post
        fields = '__all__'


class CreatePostSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Post
        fields = '__all__'

