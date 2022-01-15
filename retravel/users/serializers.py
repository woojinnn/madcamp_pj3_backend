from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'user_pk', 'userId', 'detail')


class CreateUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    userId = serializers.CharField()
    password = serializers.CharField()
    def create(self, validated_data):
        user = User.objects.create_user(
            username = validated_data['username'],
            password = validated_data['password']
        )
        profile = Profile(user = user,
                            user_pk = user.id,
                            userId = validated_data['userId'])
        profile.save()
        return (user, profile)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")