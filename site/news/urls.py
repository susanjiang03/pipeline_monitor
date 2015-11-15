from django.conf.urls import patterns, url
from news import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^filterfeeds$', views.filterfeeds, name='filterfeeds'),
    url(r'^userfeeds$', views.userfeeds, name='userfeeds')    
    )