from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from main import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    
    url(r'^accounts/login/$', auth_views.login),
    url(r'^accounts/logout/$', auth_views.logout, kwargs={'next_page':'/'}),

]