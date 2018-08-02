from django.conf.urls import url
from . import views
app_name = 'committee'
urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^logs/(?P<committee>[a-z]+)/$', views.getLogs, name='logs'),
    url(r'^account/(?P<boarder_id>[0-9]+)/$', views.account, name='account'),
    url(r'^manage/(?P<committee>[a-z]+)/$', views.manage, name='manage'),
]
