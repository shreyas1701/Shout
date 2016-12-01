from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^register/$', views.register, name="register"),
    url(r'^login/$', views.user_login, name="login"),
    url(r'^logout/$', views.user_logout, name="logout"),
    url(r'^shout/$', views.shout, name="shout"),
    url(r'^createEvent/$', views.events, name="event"),
    url(r'^profile/(?P<id>\d+)/$', views.profile_view, name="profile"),
    url(r'^notify/$', views.notify, name="notify"),
    url(r'^edit_event/(?P<id>\d+)/$', views.edit_event, name='edit_event'),
    url(r'^updateSeen/$', views.updateSeen, name="updateSeen"),
    url(r'^hashtag/$', views.hashResults, name="hashResults"),
]
