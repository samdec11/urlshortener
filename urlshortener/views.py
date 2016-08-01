from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.views import generic

def index(request):
    return render(request, 'urlshortener/index.html')

def redirect(request, short_string):
    link = get_object_or_404(Link, short_string = short_string)
    return HttpResponseRedirect(link.base_url)
