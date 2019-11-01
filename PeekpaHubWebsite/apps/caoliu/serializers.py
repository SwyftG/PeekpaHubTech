# encoding: utf-8
__author__ = 'lianggao'
__date__ = '2019/11/1 8:58 PM'
from rest_framework import serializers
from .models import CaoliuBase,CaoliuFid7


class CaoliuSerializer(serializers.Serializer):
    block_id = serializers.CharField()
    post_id = serializers.CharField()
    post_title = serializers.CharField()
    post_time = serializers.CharField()
    post_url = serializers.CharField()
    post_part_url = serializers.CharField()
    post_day_time = serializers.CharField()

    class Meta:
        model = CaoliuBase
        fields = '__all__'
