from django.conf.urls import patterns, url
from dashboard import views

urlpatterns = patterns('',
                       url(r'^$',
                           views.index, name='index'),
                       url(r'^rssurl/(?P<rssurl_id>[0-9]+)$',views.rssurl,name='rssurl'),
                       url(r'^rss$',views.rss,name='rss'),
                        url(r'^articles$',views.articles,name='articles'),
                       url(r'^images$',views.images,name='images'),
                       url(r'^texts$',views.texts,name='texts'),
                       url(r'^downloadall$',views.downloadall,name='downloadall'),
                       url(r'^downloadrssCSV$',views.downloadrssCSV,name='downloadrssCSV'),
                       url(r'^downloadrssTXT$',views.downloadrssTXT,name='downloadrssTXT'),
                      )
