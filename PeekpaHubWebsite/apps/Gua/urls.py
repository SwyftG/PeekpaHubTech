# encoding: utf-8
__author__ = 'lianggao'
__date__ = '2019/10/28 12:47 AM'

from django.urls import path
from .views import GuaView, GuaListView, GuaRView, GuaConfigView
from PeekpaHubWebsite.settings.base import CONFIG_JSON

urlpatterns = [
        path(CONFIG_JSON.get("urls").get("gua")[1], GuaRView.as_view()),
        path(CONFIG_JSON.get("urls").get("gua")[2], GuaView.as_view()),
        path(CONFIG_JSON.get("urls").get("gua")[3], GuaListView.as_view()),
        path(CONFIG_JSON.get("urls").get("gua")[3], GuaListView.as_view()),
        path("config/", GuaConfigView.as_view()),
    ]