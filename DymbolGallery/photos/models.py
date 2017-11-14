# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch.dispatcher import receiver
from django.conf import settings
import shutil

# Create your models here.
class UserProfile(models.Model):
    #required by the auth model
    user = models.OneToOneField(User)
    phone1 = models.DecimalField(decimal_places=0, max_digits=9, blank=True)
    phone2 = models.DecimalField(decimal_places=0, max_digits=9, default=0)
    phone3 = models.DecimalField(decimal_places=0, max_digits=9, default=0)
    def __str__(self):
        return self.user.username

class Album(models.Model):
    name = models.CharField(max_length=256)
    visible_name = models.CharField(max_length=256)
    creation_date = models.DateField(null=True)
    def __unicode__(self):
        if self.creation_date is not None:
            return str(self.creation_date.year)+"_"+self.name
        else:
            return self.name




class AlbumGroup(models.Model):
    album = models.ManyToManyField(Album)
    group = models.OneToOneField(Group)
    def __str__(self):
        return self.group.name


class Photo(models.Model):
    album = models.ForeignKey(Album)
    type = models.CharField(max_length=10)
    name = models.CharField(max_length=256)
    desc = models.CharField(max_length=256, null=True)
    iso = models.DecimalField(max_digits=10, decimal_places=9, null=True)
    exposure_time = models.CharField(max_length=20, null=True)
    camera_model = models.CharField(max_length=20, null=True)

    def __unicode__(self):
        return self.name

@receiver(post_delete, sender=Album)
def Album_delete(sender, instance, **kwargs):
    try:
        shutil.rmtree("{}/{}".format(settings.ALBUMS_DIR,instance.id))
    except:
        pass
