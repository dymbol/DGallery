from django.conf.urls import url, include
from photos import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^login/$', views.login_user, name='login_user'),
    url(r'^accounts/login/$', views.login_user, name='login_user'),

    url(r'^logoutuser/$', views.logoutuser, name='logoutuser'),

    url(r'^$', views.index, name='index'),
    url(r'^year/(?P<year>\d+)$', views.listAlbums, name='listAlbums'),
    url(r'^album/(?P<Album_id>\d+)$', views.servealbum, name='servealbum'),
    url(r'^image/(?P<album_id>\d+)/(?P<photo_name>[^/]+)$', views.retrieve_photo, name='retrievePhoto'),
    #url(r'^test/$', views.TestConnection, name='TestConnection'),
    #url(r'^help/$', views.Help, name='Help'),

    #url(r'^user_profile/$', views.user_profile, name='user_profile'),
]
