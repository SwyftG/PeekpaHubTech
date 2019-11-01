import datetime
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import JpEarthQuake
from .serializers import JpEarthSerializer
from mongoengine.queryset.visitor import Q
# Create your views here.


class JpEarthView(APIView):
    """
    get earchquake data by day
    :parameter days: get the last <days> days data. default is 3.
    """
    def get(self, request):
        response = {'code': 200}
        days = int(request.GET.get('days', 3))
        response['days'] = days
        now = datetime.datetime.now()
        time_day_one = now.strftime('%Y-%m-%d')
        query_set = Q(jp_time_num__startswith=time_day_one)
        for i in range(days):
            before_day = (now + datetime.timedelta(days=-i)).strftime('%Y-%m-%d')
            query_set = Q(jp_time_num__startswith=before_day) | query_set
        result = JpEarthQuake.objects(query_set).order_by('-jp_id').all()
        jp_serialiazer = JpEarthSerializer(result, many=True)
        response['data'] = jp_serialiazer.data
        return Response(data=response, status=200)


class JpEarthListView(APIView):
    """
    acquire earthquake data list.
    :parameter limit: the size of the data list. default size is 100,
                      if limit is 'null', it will get all data.
    """
    def get(self, request):
        response = {'code': 200}
        limit_num = request.GET.get('limit', 100)
        result = JpEarthQuake.objects.all().order_by('-jp_id')
        print('/limit:', limit_num)
        if limit_num == 'null':
            jp_searilizer = JpEarthSerializer(result, many=True)
            response['size'] = result.count()
        else:
            jp_searilizer = JpEarthSerializer(result[:int(limit_num)], many=True)
            response['size'] = int(limit_num)
        response['data'] = jp_searilizer.data
        return Response(data=response, status=200)