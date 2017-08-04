from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^new$', views.newUserPage, name='newUserPage'),
    url(r'^create_new$', views.createNewUser, name='createNewUser'),
    url(r'^edit$', views.userEditUserPage, name='userEditUserPage'),
    url(r'^edit_profile$', views.edit_profile, name='editProfile'),
    url(r'^edit/(?P<id>\d+)$', views.editUserPage, name='editUserPage'),
    url(r'^edit_user$', views.edit_user, name='editUser'),
    url(r'^edit_password$', views.edit_password, name='editPassword'),
    url(r'^edit__user_password$', views.edit_user_password, name='editUserPassword'),
    url(r'^edit__description$', views.edit_description, name='editDescription'),
    url(r'^show/(?P<id>\d+)$', views.showUserPage, name='showUserPage'),
    url(r'^postMessage$', views.postMessage, name='postMessage'),
    url(r'^postComment/(?P<messageId>\d+)$', views.postComment, name='postComment'),
]
