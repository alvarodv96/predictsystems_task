from django.contrib.auth.models import User
from .models import Post
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField()
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']

class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('name',)

class PostSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField(read_only=True)
    user_full_name = serializers.SerializerMethodField(read_only=True)
    likes_count = serializers.SerializerMethodField(read_only=True)
    users_count_info = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'creator', 'name', 'created_date', 'username', 'user_full_name', 'likes_count', 'users_count_info')

    def get_username(self, obj):
        return obj.creator.username

    def get_user_full_name(self, obj):
        return obj.creator.first_name + ' ' + obj.creator.last_name

    def get_likes_count(self, obj):
        return len(obj.likes.all())

    def get_users_count_info(self, obj):
        return obj.likes.all().values('username', 'first_name', 'last_name')