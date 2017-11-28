from django.conf.urls import url

from . import views

app = "app"

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<tag_id>[0-9]+)/$', views.rso, name='rso'),
    url(r'^rso/(?P<organization_id>[0-9]+)/$', views.detail, name='detail'),
]
