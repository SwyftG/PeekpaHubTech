"""PeekpaHubWebsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from PeekpaHubWebsite.settings.base import CONFIG_JSON
from apps.article.views import ArticleView, ArticleListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('article/', ArticleView.as_view()),
    path('aa/', ArticleListView.as_view()),
    path(CONFIG_JSON.get("urls").get("jpearth")[0], include('apps.jpearth.urls')),
    path(CONFIG_JSON.get("urls").get("gua")[0], include('apps.gua.urls')),
    path(CONFIG_JSON.get("urls").get("jap")[0], include('apps.jap.urls')),

]
