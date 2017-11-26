from django.http import HttpResponse
from django.contrib.staticfiles.storage import staticfiles_storage
from django.http.response import StreamingHttpResponse
from django.views.decorators.http import require_http_methods
import subprocess
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .import forms
from static_root import gps

def GPSon(request):
    if request.is_ajax():
        message = StreamingHttpResponse(staticfiles_storage.open('GPSstatus.json'), content_type="application/json")
        gps.GPSstatus(True)
        return message
    else:
        message = StreamingHttpResponse(staticfiles_storage.open('GPSstatus.json'), content_type="application/json")
        gps.GPSstatus(True)
        return message        

def GPSoff(request):
    if request.is_ajax():
        message = StreamingHttpResponse(staticfiles_storage.open('GPSstatus.json'), content_type="application/json")
        gps.GPSstatus(False)
        return message
    else:
        message = StreamingHttpResponse(staticfiles_storage.open('GPSstatus.json'), content_type="application/json")
        gps.GPSstatus(False)
        return message   
