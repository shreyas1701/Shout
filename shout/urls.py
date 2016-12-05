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
    url(r'^hashtag/(?P<text>\w+)/$', views.hashResults, name="hashResults"),
    url(r'^follow/(?P<id>\d+)/$', views.followUser, name="follow"),
    url(r'^like/$', views.like, name="like"),
    url(r'^unlike/$', views.unlike, name="unlike"),
    url(r'^event_info/(?P<id>\d+)/$', views.event_info, name="event_info"),
    url(r'^getShouts/$', views.getShouts, name="getShouts"),
    url(r'^getEvents/$', views.getEvents, name="getEvents"),
    url(r'^myevents/$', views.myevents, name="myevents"),
    url(r'^updateevent/$', views.updateevent, name='updateevent'),
]
