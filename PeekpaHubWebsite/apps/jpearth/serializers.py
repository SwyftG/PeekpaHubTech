# encoding: utf-8
__author__ = 'lianggao'
__date__ = '2019/11/1 3:21 PM'

from rest_framework import serializers
from .models import JpEarthQuake


class JpEarthSerializer(serializers.Serializer):
    jp_id = serializers.CharField()
    jp_title = serializers.CharField()
    jp_location = serializers.CharField()
    jp_level = serializers.CharField()
    jp_max_level = serializers.CharField()
    jp_location_image_url = serializers.CharField()
    jp_url = serializers.URLField()
    jp_create_time = serializers.CharField()
    jp_time_num = serializers.CharField()
    jp_time_text = serializers.CharField()

    class Meta:
        model = JpEarthQuake
        fields = '__all__'