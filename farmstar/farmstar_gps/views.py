from django.http import HttpResponse
from django.contrib.staticfiles.storage import staticfiles_storage
from django.http.response import StreamingHttpResponse
from django.views.decorators.http import require_http_methods
import subprocess
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .import forms


def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = forms.NameForm()

    return render(request, 'name.html', {'form': form})
