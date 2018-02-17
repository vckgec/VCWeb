from django.conf.urls import url
from . import views
app_name = 'mess'
urlpatterns = [
    url(r'^$', views.Home, name='home'),
    url(r'^change/$', views.Change_Current_Status, name='change'),
    url(r'^future/$', views.Future, name='future'),
    url(r'^mealdish/$', views.Meal_Dish, name='mealdish'),
    url(r'^guestmeal/$', views.guestmeal, name='guestmeal'),
    url(r'^extraadjustment/$', views.ExtraAdjustment, name='extraadjustment'),
    url(r'^storekeeper/$', views.Store_Keeper, name='storekeeper'),
    url(r'^storekeeperedit/$', views.Store_Keeper_Edit, name='storekeeperedit'),
    ]