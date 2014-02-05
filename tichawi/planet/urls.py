from django.conf.urls import patterns, url
from planet import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^logout$', views.logout_view, name='logout'),
                       url(r'^(?P<article_id>\d+)/$', views.detail, name='detail'),
                       url(r'^(?P<article_id>\d+)/vote/$', views.vote, name='vote'),
)
