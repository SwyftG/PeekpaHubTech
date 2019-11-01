# encoding: utf-8
__author__ = 'lianggao'
__date__ = '2019/11/1 8:10 PM'


from django.urls import path
from PeekpaHubWebsite.settings.base import CONFIG_JSON
from .views import JapView

urlpatterns = [
        path(CONFIG_JSON.get("urls").get("jap")[1], JapView.as_view()),
    ]