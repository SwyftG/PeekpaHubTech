# encoding: utf-8
__author__ = 'lianggao'
__date__ = '2019/11/1 8:08 PM'

from rest_framework import serializers
from .models import JapLanguage


class JapSerializer(serializers.Serializer):
    levelNum = serializers.CharField()
    classNum = serializers.CharField()
    chinese = serializers.CharField()
    jp_only = serializers.CharField()
    jp_chinese = serializers.CharField()
    change = serializers.CharField()

    class Meta:
        model = JapLanguage
        fields = '__all__'