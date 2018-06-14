from django.conf.urls import url
from . import views
app_name = 'dues'
urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^printscan/$', views.printScan, name='printscan'),
]
