# serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import ContentTable,TagTable
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class ContentSerializer(serializers.ModelSerializer):
    user_first_name = serializers.CharField(source='created_by.first_name', read_only=True)
    tag_title = serializers.CharField(source='tag.title', read_only=True)
    timestamp = serializers.DateTimeField(format='%d/%m/%Y %H:%M')

    class Meta:
        model = ContentTable
        fields = ['id', 'title', 'content', 'timestamp', 'user_first_name', 'tag_title']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagTable
        fields = ['id', 'title']