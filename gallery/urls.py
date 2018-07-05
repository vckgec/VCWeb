from django.conf.urls import url
from . import views
app_name = 'gallery'
urlpatterns = [
    url(r'^$', views.Home, name='home'),
    url(r'^youtube/$', views.Youtube, name='youtube'),
    ]