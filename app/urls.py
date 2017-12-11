from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings

from . import views

app = "app"

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<tag_id>[0-9]+)/$', views.rso, name='rso'),
    url(r'^rso/(?P<organization_id>[0-9]+)/$', views.detail, name='detail'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)