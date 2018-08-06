from django.conf.urls import url
from . import views
app_name = 'mess'
urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^getlist/$', views.getList, name='getlist'),
    url(r'^change/$', views.changeStatus, name='change'),
    url(r'^mealdish/$', views.mealDish, name='mealdish'),
    url(r'^guestmeal/$', views.guestMeal, name='guestmeal'),
    url(r'^extraadjustment/$', views.extraAdjustment, name='extraadjustment'),
    url(r'^storekeeper/$', views.storeKeeper, name='storekeeper'),
    url(r'^storekeeperedit/$', views.storeKeeperEdit, name='storekeeperedit'),
    url(r'^allon/$', views.allOn, name='allon'),
]