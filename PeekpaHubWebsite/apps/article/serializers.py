# encoding: utf-8
__author__ = 'lianggao'
__date__ = '2019/11/1 11:15 AM'

from rest_framework import serializers
from .models import Article

class ArticleSerializer(serializers.Serializer):
    title = serializers.CharField()
    author = serializers.CharField()
    image = serializers.CharField()
    content = serializers.CharField()
    context_html = serializers.CharField()

    class Meta:
        model = Article
        fields = '__all__'