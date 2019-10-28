# encoding: utf-8
__author__ = 'lianggao'
__date__ = '2019/10/27 3:10 PM'
from rest_framework import serializers
from .models import Gua, GuaRModel


class GuaSerializer(serializers.Serializer):
    gua_number = serializers.CharField()
    gua_sub_title = serializers.CharField()
    gua_title = serializers.CharField()
    gua_serial_text = serializers.CharField()
    gua_serial = serializers.CharField()
    gua_one = serializers.CharField()
    gua_two = serializers.CharField()
    gua_three = serializers.CharField()
    gua_four = serializers.CharField()
    gua_five = serializers.CharField()

    class Meta:
        model = Gua
        fields = '__all__'


class GuaReportSerializer(serializers.Serializer):
    appVersion = serializers.CharField()
    checkNum = serializers.CharField()
    guaName = serializers.CharField()
    reportTime = serializers.CharField()
    nickName = serializers.CharField()
    avatarUrl = serializers.CharField()
    city = serializers.CharField()
    province = serializers.CharField()
    country = serializers.CharField()
    gender = serializers.CharField()
    fromPage = serializers.CharField()
    dayTime = serializers.CharField()
    class Meta:
        model = GuaRModel
        fields = '__all__'