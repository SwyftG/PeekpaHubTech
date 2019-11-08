from django.shortcuts import render

from django.views.generic import ListView
from django.http import StreamingHttpResponse
from PeekpaHubWebsite.settings.base import CONFIG_JSON
# Create your views here.


def file_iterator(file_name, chunk_size=512):
    with open(file_name, 'rb') as f:
        while True:
            chunk_buffer = f.read(chunk_size)
            if chunk_buffer:
                yield chunk_buffer
            else:
                break


class StaticView(ListView):
    def get(self, request, file_name):
        image_path = CONFIG_JSON.get("local_file_path") + file_name
        response = StreamingHttpResponse(file_iterator(image_path))
        if '.png' in file_name:
            response['Content-Type'] = 'image/png'
        elif '.jpeg' in file_name or '.jpg' in file_name:
            response['Content-Type'] = 'image/jpeg'
        elif '.gif' in file_name:
            response['Content-Type'] = 'image/gif'
        else:
            response['Content-Type'] = 'text/plain'
        return response


class StreamDownloadView(ListView):
    def get(self, request, file_name):
        file_path = CONFIG_JSON.get("local_file_path") + file_name
        response = StreamingHttpResponse(file_iterator(file_path))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename={}'.format(file_name)
        return response
