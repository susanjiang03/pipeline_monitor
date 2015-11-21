from django.conf.urls import patterns, url
from news import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^newspaper/(?P<newspaperlink>\w{0,50})/$', views.newspaper, name='newspaper'),
    url(r'^filterfeeds$', views.filterfeeds, name='filterfeeds'),
    url(r'^userfeeds$', views.userfeeds, name='userfeeds'),
    url(r'^images/(?P<urlid>[0-9]+)$', views.images, name='images'),
    url(r'^allimages$', views.allimages, name='allimages'),
    url(r'^login/$', views.user_login, name='user_login'),
    url(r'^process_login$', views.process_login, name='process_login'),
    url(r'^loginout/$', views.user_logout, name='user_logout'),
    url(r'^register$', views.register, name='register'),
    url(r'^process_register$', views.process_register, name='process_register'),
    url(r'^reset_password$', views.reset_password, name='reset_password'),
    )
