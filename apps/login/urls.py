from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^create_user$', views.create_user, name='createUser'),
    url(r'^login$', views.login, name='login'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^register$', views.register, name='register'),
    url(r'^dashboard$', views.userpage, name='user'),
    url(r'^dashboard/admin$', views.adminpage, name='admin'),
    url(r'^dashboard/admin/remove/(?P<id>\d+)$', views.remove_user, name='removeUser'),
]
