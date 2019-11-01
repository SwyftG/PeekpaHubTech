# encoding: utf-8
__author__ = 'lianggao'
__date__ = '2019/11/1 9:00 PM'

from django.urls import path
from .views import CaoliuView
from PeekpaHubWebsite.settings.base import CONFIG_JSON

urlpatterns = [
        path(CONFIG_JSON.get("urls").get("caoliu")[1], CaoliuView.as_view()),
    ]