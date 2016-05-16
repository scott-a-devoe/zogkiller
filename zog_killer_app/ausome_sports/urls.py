from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^api/user/current$', views.get_user_profile, name='user_profile'),
    url(r'^api/user/new$', views.post_create_user, name='create_user'),
    url(r'^api/user/update$', views.post_update_profile, name='update_profile'),
    url(r'^api/user/join$', views.post_join_team, name='join_team'),
    url(r'^api/leagues/(?P<sport>.*)/(?P<status>.*)$', views.get_leagues_by_sport_status, name='leagues_by_sport_status'),
    url(r'^login$', views.post_login, name='post_login'),
    url(r'^.*$', views.index, name='index'),
]
