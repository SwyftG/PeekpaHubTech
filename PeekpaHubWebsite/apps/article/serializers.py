# encoding: utf-8
__author__ = 'lianggao'
__date__ = '2019/11/1 11:15 AM'

from rest_framework import serializers
from .models import Post, Category, Tag


class PostDetailSerializer(serializers.ModelSerializer):
    tag = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )
    category = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )
    owner = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    class Meta:
        model = Post
        fields = ('time_id', 'title', 'desc', 'desc_image', 'owner', 'tag', 'category', 'created_time', 'content_html', 'created_time', 'pv', 'uv')


class PostListSerializer(serializers.ModelSerializer):
    tag = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )
    category = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )
    owner = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    class Meta:
        model = Post
        fields = ('time_id', 'title', 'desc', 'desc_image', 'owner', 'tag', 'category', 'created_time', 'pv', 'uv')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'