import datetime
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Gua, GuaRModel
from .serializers import GuaSerializer, GuaReportSerializer
from rest_framework.pagination import PageNumberPagination
from PeekpaHubWebsite.settings.base import CONFIG_JSON

# Create your views here.
class GuaView(APIView):
    def get(self, request, check_num):
        response = {'code': 200}
        result = Gua.objects.filter(gua_serial=check_num).first()
        if result is None:
            response['code'] = '100090'
            response['msg'] = 'search_failed'
            return Response(data=response, status=200)
        response['msg'] = 'success'
        serializer = GuaSerializer(result)
        response['data'] = serializer.data
        return Response(data=response, status=200)


class GuaListView(APIView):
    def get(self, request):
        response = {'code': 200}
        result = Gua.objects.all()
        if result is None:
            response['code'] = '100091'
            response['msg'] = 'search_failed'
            return Response(data=response, status=200)
        response['msg'] = 'success'
        serializer = GuaSerializer(result, many=True)
        response['data'] = serializer.data
        return Response(data=response, status=200)


class GuaRPagination(PageNumberPagination):
    page_size = 30  # 表示每页的默认显示数量
    page_size_query_param = 'page_size'  # 表示url中每页数量参数
    page_query_param = 'page'  # 表示url中的页码参数
    max_page_size = 100  # 表示每页最大显示数量，做限制使用，避免突然大量的查询数据，数据库崩溃


class GuaRView(APIView):

    def get(self, request,*args,**kwargs):
        response = {'code': 200}
        day_time = request.GET.get('time')
        if day_time is None:
            result = GuaRModel.objects.all()
        else:
            result = GuaRModel.objects.filter(dayTime=day_time).all()
        if result is None:
            response['code'] = '100092'
            response['msg'] = 'search_failed'
            return Response(data=response, status=200)
        response['msg'] = 'success'
        response['size'] = len(result)
        pg = GuaRPagination()
        page_role = pg.paginate_queryset(queryset=result, request=request, view=self)
        serializer = GuaReportSerializer(page_role, many=True)
        response['data'] = serializer.data
        return Response(data=response, status=200)

    def post(self, request):
        app_version = request.data.get('appVersion')
        checkNum = request.data.get('checkNum')
        gender = request.data.get('gender', "")
        fromPage = request.data.get('fromPage')
        gua_r = GuaRModel()
        gua_r.appVersion = app_version
        gua_r.checkNum = checkNum
        gua_r.gender = gender
        gua_r.fromPage = fromPage
        year = str(datetime.datetime.now().year)
        month = str(datetime.datetime.now().month).zfill(2)
        day = str(datetime.datetime.now().day).zfill(2)
        gua_r.dayTime = "{}{}{}".format(year, month, day)
        gua_r.guaName = Gua.objects.filter(gua_serial=checkNum).first().gua_title
        result = gua_r.save()
        response = {}
        if result is None:
            response['code'] = '100093'
            response['msg'] = 'Report failed'
            return Response(datetime=response)
        response['code'] = '200'
        response['msg'] = 'success'
        serializer = GuaReportSerializer(gua_r)
        response['data'] = serializer.data
        return Response(data=response)


class GuaConfigView(APIView):
    local_config = CONFIG_JSON.get("gua_config")
    def get(self, request):
        response = {'success':True}
        response['message'] = 'success'
        response['data'] = self.local_config
        return Response(data=response)

    def post(self, request):
        self.local_config['show_auther'] = request.data.get('show_auther', self.local_config['show_auther'])
        self.local_config['version_time'] = request.data.get('version_time', self.local_config['version_time'])
        self.local_config['open_report'] = request.data.get('open_report', self.local_config['open_report'])
        self.local_config['system_message'] = request.data.get('system_message', self.local_config['system_message'])
        self.local_config['is_force'] = request.data.get('is_force', self.local_config['is_force'])
        self.local_config['open_share'] = request.data.get('open_share', self.local_config['open_share'])
        self.local_config['test'] = request.data.get('test', self.local_config['test'])
        self.local_config['open_login'] = request.data.get('open_login', self.local_config['open_login'])
        self.local_config['max_time'] = request.data.get('max_time', self.local_config['max_time'])
        return Response(data=self.local_config)