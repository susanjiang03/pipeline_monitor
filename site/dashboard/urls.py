from django.conf.urls import patterns, url
from dashboard import views

urlpatterns = patterns('',
                       url(r'^$',
                           views.index, name='index'),
                       url(r'^rssurl/(?P<rssurl_id>[0-9]+)$',views.rssurl,name='rssurl'),
                        url(r'^articles$',views.articles,name='articles')
                      )
