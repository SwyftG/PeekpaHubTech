from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Post, Category
from .serializers import PostDetailSerializer, PostListSerializer, CategorySerializer, TagSerializer



class ArticleDetailView(APIView):
    def get(self, request, article_id):
        print("article_id: ",article_id, "/", type(article_id))
        result = Post.objects.filter(time_id=article_id).first()
        response = PostDetailSerializer(result)
        return Response(data=response.data, status=200)
        # return render(request, 'article.html', context={'article_list': response.data})


class ArticleListView(APIView):
    def get(self, request):
        response = {'code': 200}
        result = Post.objects.all()
        response['msg'] = 'success'
        serializer = PostListSerializer(result, many=True)
        response['data'] = serializer.data
        return Response(data=response, status=200)


class CategoryListView(APIView):
    def get(self, request):
        response = {'code': 200}
        result = Category.objects.all()
        response['msg'] = 'success'
        serializer = CategorySerializer(result, many=True)
        response['data'] = serializer.data
        return Response(data=response, status=200)


class CategoryArticleListView(APIView):
    def get(self, request, category_id):
        response = {'code': 200}
        result, tag = Post.get_by_category(category_id)
        response['msg'] = 'success'
        response['category'] = CategorySerializer(tag).data
        serializer = PostListSerializer(result, many=True)
        response['data'] = serializer.data
        return Response(data=response, status=200)


class TagListView(APIView):
    def get(self, request):
        response = {'code': 200}
        result = Category.objects.all()
        response['msg'] = 'success'
        serializer = TagSerializer(result, many=True)
        response['data'] = serializer.data
        return Response(data=response, status=200)


class TagArticleListView(APIView):
    def get(self, request, tag_id):
        response = {'code': 200}
        result, tag = Post.get_by_tag(tag_id)
        response['msg'] = 'success'
        response['tag'] = TagSerializer(tag).data
        serializer = PostListSerializer(result, many=True)
        response['data'] = serializer.data
        return Response(data=response, status=200)