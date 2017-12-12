from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings

from . import views

app = "app"

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^tag/(?P<tag_id>[0-9]+)/$', views.tag, name='tag'),
    url(r'^rso/(?P<organization_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^search-suggest/', views.search_suggest, name='search-suggest')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)