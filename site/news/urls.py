from django.conf.urls import patterns, url
from news import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^newspaper/(?P<newspaperlink>\w{0,50})/$', views.newspaper, name='newspaper'),
    url(r'^filterfeeds$', views.filterfeeds, name='filterfeeds'),
    url(r'^userfeeds$', views.userfeeds, name='userfeeds'),
    url(r'^images/(?P<urlid>[0-9]+)$', views.images, name='images'),
    )
