from django.conf.urls import url

from . import views

app_name = 'urlshortener'
urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^(?P<short_string>\w+)$', views.redirect, name = 'redirect')
]
