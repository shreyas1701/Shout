from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
import datetime

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User)

    #extra fields
    dateOfBirth = models.DateField(auto_now=False, auto_now_add=False, default=datetime.date.today())
    bio = models.CharField(max_length=250)
    
    def __str__(self):
        return self.user.username
        