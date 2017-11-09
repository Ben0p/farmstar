from django.http import HttpResponse
from django.contrib.staticfiles.storage import staticfiles_storage
from django.http.response import StreamingHttpResponse
from django.views.decorators.http import require_http_methods

def livegeojson(request): 
    response = StreamingHttpResponse(staticfiles_storage.open('live.geojson'))
    return response

