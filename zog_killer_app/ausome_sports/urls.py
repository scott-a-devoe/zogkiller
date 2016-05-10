from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^api/user/current$', views.get_user_profile, name='user_profile'),
    url(r'^login$', views.post_login, name='post_login'),
    url(r'^.*$', views.index, name='index'),
]
