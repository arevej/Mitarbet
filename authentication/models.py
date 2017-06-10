from django.db import models
from django.contrib.auth.models import User
from annoying.fields import AutoOneToOneField

class Profile(models.Model):
    user = AutoOneToOneField(User, primary_key=True)
    avatar = models.ImageField(upload_to='images')
