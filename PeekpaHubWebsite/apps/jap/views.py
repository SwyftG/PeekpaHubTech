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
        search_key_chinese = request.GET.get('chinese')
        search_key_jap_chinese = request.GET.get('jp_ch')
        search_key_jap_only = request.GET.get('jp_only')
        response = {'code': 200}
        result = None
        if search_key_chinese is not None:
            result = JapLanguage.objects.filter(chinese__contains=search_key_chinese).all().order_by('levelNum').order_by('classNum')
            response['search_word'] = search_key_chinese
        elif search_key_jap_chinese is not None:
            result = JapLanguage.objects.filter(jp_chinese__contains=search_key_jap_chinese).all().order_by('levelNum').order_by('classNum')
            response['search_word'] = search_key_jap_chinese
        elif search_key_jap_only is not None:
            result = JapLanguage.objects.filter(jp_only__contains=search_key_jap_only).all().order_by('levelNum').order_by('classNum')
            response['search_word'] = search_key_jap_only
        if result is None:
            response['size'] = 0
        else:
            response['size'] = len(result)
        response['data'] = JapSerializer(result, many=True).data
        return Response(data=response, status=200)
