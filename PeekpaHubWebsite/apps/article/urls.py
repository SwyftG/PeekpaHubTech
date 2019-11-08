# encoding: utf-8
__author__ = 'lianggao'
__date__ = '2019/11/4 4:20 PM'

from django.urls import path
from .views import ArticleDetailView, ArticleListView, CategoryListView, CategoryArticleListView, TagListView, TagArticleListView
from PeekpaHubWebsite.settings.base import CONFIG_JSON

urlpatterns = [
        path("post/<str:article_id>", ArticleDetailView.as_view()),
        path("post/", ArticleListView.as_view()),
        path("category", CategoryListView.as_view()),
        path("category/<str:category_id>", CategoryArticleListView.as_view()),
        path("tag", TagListView.as_view()),
        path("tag/<str:tag_id>", TagArticleListView.as_view())
    ]