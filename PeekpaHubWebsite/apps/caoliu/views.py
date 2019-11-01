import datetime
from rest_framework.response import Response
from rest_framework.views import APIView
# Create your views here.
from .models import CaoliuFid2, CaoliuFid4, CaoliuFid7, CaoliuFid15, CaoliuFid25, CaoliuFid26
from .serializers import CaoliuSerializer
from mongoengine.queryset.visitor import Q


class CaoliuView(APIView):
    FID_2 = 2
    FID_4 = 4
    FID_7 = 7
    FID_15 = 15
    FID_25 = 25
    FID_26 = 26
    TYPE_DAILY = 1
    TYPE_SEARCH = 2

    def get(self, request):
        response = {'code': 200}
        handle_type, fid, day, search_key = self.process_paramter(request)
        print("param:: type:{} fid:{} day:{} search_key:{}".format(handle_type, fid, day, search_key))
        result = self.process_database(handle_type, fid, day, search_key)
        response['size'] = result.count()
        response['data'] = CaoliuSerializer(result, many=True).data
        return Response(data=response, status=200)

    def process_paramter(self, request):
        fid = request.GET.get('fid', self.FID_7)
        search_key = request.GET.get('search')
        day = request.GET.get('day', datetime.datetime.now().strftime('%Y-%m-%d'))
        handle_type = self.TYPE_DAILY if search_key is None else self.TYPE_SEARCH
        return handle_type, int(fid), day, search_key

    def process_database(self, handle_type, fid, day, search_key):
        result = None
        if handle_type == self.TYPE_DAILY:
            if fid == self.FID_2:
                result = CaoliuFid2.objects.filter(post_day_time=day).order_by('-post_time').all()
            elif fid == self.FID_4:
                result = CaoliuFid4.objects.filter(post_day_time=day).order_by('-post_time').all()
            elif fid == self.FID_7:
                result = CaoliuFid7.objects.filter(post_day_time=day).order_by('-post_time').all()
            elif fid == self.FID_15:
                result = CaoliuFid15.objects.filter(post_day_time=day).order_by('-post_time').all()
            elif fid == self.FID_25:
                result = CaoliuFid25.objects.filter(post_day_time=day).order_by('-post_time').all()
            elif fid == self.FID_26:
                result = CaoliuFid26.objects.filter(post_day_time=day).order_by('-post_time').all()
        elif handle_type == self.TYPE_SEARCH:
            query_set = Q(post_title__contains=search_key) | Q(post_title__contains=search_key.upper()) | Q(post_title__contains=search_key.lower())
            if fid == self.FID_2:
                result = CaoliuFid2.objects(query_set).order_by('-post_time').all()
            elif fid == self.FID_4:
                result = CaoliuFid4.objects(query_set).order_by('-post_time').all()
            elif fid == self.FID_7:
                result = CaoliuFid7.objects(query_set).order_by('-post_time').all()
            elif fid == self.FID_15:
                result = CaoliuFid15.objects(query_set).order_by('-post_time').all()
            elif fid == self.FID_25:
                result = CaoliuFid25.objects(query_set).order_by('-post_time').all()
            elif fid == self.FID_26:
                result = CaoliuFid26.objects(query_set).order_by('-post_time').all()
        return result
