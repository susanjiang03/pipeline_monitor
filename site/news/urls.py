from django.conf.urls import patterns, url
from news import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^newspaper/(?P<newspaperlink>\w{0,50})/$' ,views.newspaper),
    )
