from django.conf.urls import url
from . import views


urlpatterns = [
    #url(r'^question/(?P<id>\w{0,50})/$', views.question, name='question'),
    url(r'^score/$', views.score, name='score'),
    url(r'^loader/$', views.loader, name='loader'),
    url(r'^top-scores/$', views.topscores, name='top-scores'),
    url(r'^questions/$', views.questions, name='questions'),
    url(r'^index/$', views.index, name='index'),
    url(r'^$', views.index, name='index'),
]
