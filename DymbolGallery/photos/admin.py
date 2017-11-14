# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from photos.models import *

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Album)
admin.site.register(AlbumGroup)
admin.site.register(Photo)