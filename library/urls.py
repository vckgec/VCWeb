from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.views.generic import TemplateView
from . import views
app_name = 'library'

urlpatterns = [
	url(r'^$', views.LibHome, name='LibHome'),
	url(r'^index/$', views.BookIndex.as_view(), name='library'),
	url(r'^book/(?P<id>[0-9]+)/$', views.BookDetail, name='detail'),
	url(r'^book/edit/(?P<pk>[0-9]+)/$', views.BookEdit.as_view(), name='edit'),
	url(r'^new/$', views.NewForm, name='new'),
	url(r'^add/$', views.BookAdd.as_view(), name='add'),
	url(r'^request/$', views.Requests.as_view(), name='req'),
	url(r'^request/(?P<id>[0-9]+)/issue/$', views.IssueBook, name='issue'),
	url(r'^request/(?P<id>[0-9]+)/return/$', views.ReturnBook, name='return'),
	url(r'^request/(?P<id>[0-9]+)/collect/$', views.CollectBook, name='collect'),
	url(r'^request/(?P<id>[0-9]+)/undoreturn/$', views.UndoReturn, name='undoreturn'),
	url(r'^search/$', views.Search, name='search'),
	url(r'^libgen/$', views.libgen, name='libgen'),
    url(r'^date/$', views.dateFix, name='date'),
	url(r'^dashboard/$', views.UserDashboard, name='user_dashboard')
]