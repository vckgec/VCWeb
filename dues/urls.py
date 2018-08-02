from django.conf.urls import url
from . import views
app_name = 'dues'
urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^printscan/$', views.printScan, name='printscan'),
    url(r'^logs/(?P<boarder_id>[0-9]+)/$',views.getLogs,name='getlogs'),
    url(r'^(?P<field>[a-z?_]+)/$', views.manage, name='manage'),
]
