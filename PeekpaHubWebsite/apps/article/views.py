from django.shortcuts import render

# Create your views here.

from .models import Article
from django.views.generic import ListView
from .models import Article
import mistune
from rest_framework.views import APIView
from .serializers import ArticleSerializer
from rest_framework.response import Response

class ArticleView(ListView):
    def get(self, request):
#         article = Article()
#         article.title = '零基础教你玩转Django之03篇 —— 完善Gua的API，分页和POST请求'
#         article.author = '皮克啪的铲屎官'
#         article.content = """### RESTful规范设计
#
# 我们在上一篇文章讨论了RESTful API的设计规范，但是在前一篇文章，我们的接口只是很简单的：
#
# ```
# http://127.0.0.1:8000/gua?checkNum=111111
# ```
#
# 这个不符合我们的规范啊，我们的规范，至少应该是长这个样子的：
#
# ```
# http://127.0.0.1:8000/v1/api/gua?checkNum=111111
# ```
#
# 那么，我们今天就来实现这样的接口。
#
# 首先，还是需要来修改我们的`urls.py` 文件，将之前的:"""
#         article.context_html = mistune.markdown(article.content)
#         article.image = 'https://wx2.sinaimg.cn/mw690/a726c4d3ly1g17fkc592hj213w0u0qcx.jpg'
#         article.save()
        article = Article.objects.all()
        return render(request, 'article.html', context={'article_list':article})

class ArticleListView(APIView):
    def get(self, request):
        response = {'code': 200}
        result = Article.objects.all()
        response['msg'] = 'success'
        serializer = ArticleSerializer(result, many=True)
        response['data'] = serializer.data
        return Response(data=response, status=200)
