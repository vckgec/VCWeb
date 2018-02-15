from django.conf.urls import url
from . import views
app_name = 'gallery'
urlpatterns = [
    url(r'^$', views.Youtube, name='gallery'),
    #url(r'^youtube/$', views.Youtube, name='youtube'),
    ]