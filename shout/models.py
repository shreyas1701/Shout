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

class Events(models.Model):
    event_name = models.CharField(max_length=160)
    event_descp = models.CharField(max_length=250)
    location = models.CharField(max_length=200)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    username = models.CharField(max_length=150)
    invitees = models.CharField(max_length=1000)