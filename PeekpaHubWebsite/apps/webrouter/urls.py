# encoding: utf-8
__author__ = 'lianggao'
__date__ = '2019/11/2 4:28 PM'

from django.urls import path
from PeekpaHubWebsite.settings.base import CONFIG_JSON
from .views import TestView

urlpatterns = [
        path("", TestView.as_view()),
    ]