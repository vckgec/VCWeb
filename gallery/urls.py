from django.conf.urls import url
from . import views
app_name = 'gallery'
urlpatterns = [
    url(r'^youtube/$', views.Youtube, name='youtube'),
    url(r'^(?P<path>.*)/play/$',views.play),
    url(r'^(?P<path>.*)$',views.ftp,name='home'),
]