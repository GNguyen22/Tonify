from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url('returnPlaylist', views.returnPlaylist, name='returnPlaylist'),
    url('storeUser', views.storeUser, name='storeUser'),
    url('storeGenre', views.storeGenre, name='storeGenre'),
]
