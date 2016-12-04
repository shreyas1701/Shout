from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
import datetime

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')

    'extra fields'
    dateOfBirth = models.DateField(auto_now=False, auto_now_add=False, default=datetime.date.today())
    bio = models.CharField(max_length=250)

    def __str__(self):
        return 'Profile of user: {}'.format(self.user.username)

class Shouts(models.Model):
    shout = models.CharField(max_length=160)
    user = models.CharField(max_length=150)
    shout_at = models.DateTimeField(max_length=50)
    likes = models.IntegerField(default=0)

class Events(models.Model):
    event_name = models.CharField(max_length=160)
    event_descp = models.CharField(max_length=250)
    location = models.CharField(max_length=200)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    username = models.CharField(max_length=150)
    invitees = models.CharField(max_length=1000)

    def __str__(self):
        return 'Event name'.format(self.event_nme)

class Notification(models.Model):
    notif_text = models.CharField(max_length=300)
    when = models.DateTimeField()
    
class NotifMap(models.Model):
    user = models.CharField(max_length=100)
    notif = models.ForeignKey(Notification)
    seen = models.BooleanField(default=False)

    def __unicode__(self):
        return self.notif.notif_text

class FollowMap(models.Model):    
    follower = models.CharField(max_length=100)
    following = models.CharField(max_length=100)

class Likers(models.Model):
    liker = models.CharField(max_length=100)
    shout_id = models.CharField(max_length=100)
