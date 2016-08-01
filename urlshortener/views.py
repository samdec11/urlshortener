from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.views import generic

from .models import Link

def index(request):
    if request.method == 'GET':
        return render(request, 'urlshortener/index.html')
    else:
        link = Link.objects.find_or_create(request.POST['url'])
        return render(request, 'urlshortener/index.html', {'link': link})

def redirect(request, short_string):
    link = get_object_or_404(Link, short_string = short_string)
    return HttpResponseRedirect(link.base_url)
