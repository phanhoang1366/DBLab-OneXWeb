from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Novel, Chapter, Rating, Author, Genre
from django.db import models
from django.utils import timezone

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['author_id', 'author_name', 'description', 'profile_picture']

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['genre_id', 'genre_name', 'genre_description']

class NovelSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True, read_only=True)
    genre = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Novel
        fields = ['novel_id', 'name', 'authors', 'genre', 'description', 'cover', 'status', 'last_updated', 'created_at']