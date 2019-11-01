from rest_framework.response import Response
from rest_framework.views import APIView
from .models import JapLanguage
from .serializers import JapSerializer


class JapView(APIView):
    """
    search japanese word.
    :parameter chinese: search key work, chinese
    :parameter jp_ch: search key work, kannjinn
    :parameter jp_only: search key work, japanese
    """
    def get(self, request):
        response = {'code': 200}
        search_type, search_key = self.process_paramter(request)
        print('search_type: ', search_type)
        result = None
        if search_type == 1:
            result = JapLanguage.objects.filter(chinese__contains=search_key).all().order_by('levelNum').order_by('classNum')
        elif search_type == 2:
            result = JapLanguage.objects.filter(jp_chinese__contains=search_key).all().order_by('levelNum').order_by('classNum')
        elif search_type == 3:
            result = JapLanguage.objects.filter(jp_only__contains=search_key).all().order_by('levelNum').order_by('classNum')
        response['search_word'] = search_key
        response['size'] = 0 if result is None else len(result)
        response['data'] = JapSerializer(result, many=True).data
        return Response(data=response, status=200)

    def process_paramter(self, request):
        if request.GET.get('chinese') is not None:
            return 1, request.GET.get('chinese')
        elif request.GET.get('jp_ch') is not None:
            return 2, request.GET.get('jp_ch')
        elif request.GET.get('jp_only') is not None:
            return 3, request.GET.get('jp_only')
        else:
            return 0, None
