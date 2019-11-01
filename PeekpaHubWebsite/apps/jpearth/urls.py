# encoding: utf-8
__author__ = 'lianggao'
__date__ = '2019/11/1 3:31 PM'

from django.urls import path
from PeekpaHubWebsite.settings.base import CONFIG_JSON
from .views import JpEarthView, JpEarthListView

urlpatterns = [
        path(CONFIG_JSON.get("urls").get("jpearth")[1], JpEarthListView.as_view()),
        path(CONFIG_JSON.get("urls").get("jpearth")[2], JpEarthView.as_view()),
    ]