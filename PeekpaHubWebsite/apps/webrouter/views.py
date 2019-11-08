from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from PeekpaHubWebsite.settings.base import CONFIG_JSON


class TestView(ListView):
    def get(self, request):
        url = "http://javpop.com/"
        # url = "http://www.baidu.com/"
        # url = "https://s.taobao.com/search?q=%E6%97%85%E8%A1%8C%E7%AE%B1&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306"
        response = requests.get(url)
        print(response.encoding)
        # response.encoding = 'GBK'
        # router_detail = str(response.content, 'utf-8')
        router_detail = response.text
        print(response.content)
        return render(request, 'routerdetail.html', context={'router_detail': router_detail})


