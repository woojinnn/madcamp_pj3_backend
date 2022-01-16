from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post

User = get_user_model()

# DRF Serializer listing all the blog posts
class PostListSerializer(serializers.ModelSerializer):
    author_full_name = serializers.CharField()

    class Meta:
        model = Post
        fields = '__all__'

# Serializer for creating a post for logged in users
class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

# Serializer for creating a post for logged in users
class PostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'