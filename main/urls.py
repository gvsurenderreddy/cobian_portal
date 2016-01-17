from django.conf.urls import url
from django.contrib.auth import views as auth_views
from main import views

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^eula/$', views.eula),
    url(r'^ebridge/$', views.ebridge),

    url(r'^accounts/profile/$', views.profile),
    url(r'^accounts/login/$', auth_views.login),
    url(r'^accounts/logout/$', auth_views.logout, kwargs={'next_page':'/'}),

    url(r'^warranties/$', views.warranties),
    url(r'^warranty/(?P<warranty_id>\d+)/$', views.warranty),
    url(r'^warranty/new/$', views.warranty_new),
    url(r'^warranty/report/$', views.warranty_report),
]