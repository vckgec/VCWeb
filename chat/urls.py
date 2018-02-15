from django.conf.urls import url
from . import views
app_name = 'chat'
urlpatterns = [ 
    url(r'^index/$', views.Index, name='index'),
    ]