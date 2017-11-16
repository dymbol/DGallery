# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from photos.models import *
import json
from django.conf import settings
from django.http import HttpRequest
from django.db.models import Count
from django.http import HttpResponse
from sendfile import sendfile



# Create your views here.
def login_user(request):
    if request.method == "POST":
        phoneno = request.POST['phoneno']
        if phoneno.isdigit() is True and len(phoneno) < 10:
            #phone no is correct enough
            try:
                CurrentUserProfile = UserProfile.objects.get(phone1=phoneno)
            except:
                CurrentUserProfile = None
            print CurrentUserProfile
            if CurrentUserProfile is not None:
                if CurrentUserProfile.user.is_active:
                    login(request, CurrentUserProfile.user)
                    messages.info(request, "{0},\n zostałeś zalogowany".format(CurrentUserProfile.user.username))
                    return redirect('index')
                else:
                    # Return a 'disabled account' error message
                    messages.error(request, "{0},\n Konto wyłączone")
                    return redirect('login_user')
            else:
                # Return a 'disabled account' error message
                messages.error(request, "{0},\n Konto nie istnieje")
                return redirect('login_user')
        else:
            # Return an 'invalid login' error message.
            messages.error(request, "{0},\n Wymagane mniej niż 10 cyfr")
            return redirect('login_user')
    else:
        return render(request, 'login.html', {})


def logoutuser(request):
    from django.contrib.auth import logout
    logout(request)
    messages.info(request, "Zostałeś wylogowany ")
    return redirect('login_user')


@login_required(login_url='login_user')
def index(request):
    context = {}
    albums = []

    if request.user.groups.values_list('name', flat=True).count() == 0:
        #user doesn't belong to any group
        print "User {} doesn't belong to any group".format(request.user.username)
    else:
        #get albums list for that user
        DistinctYears = Album.objects.order_by().dates('creation_date','year').distinct()
        context["years"] = DistinctYears

    return render(request, 'index.html', context)

@login_required
def listAlbums(request, year):
    context = {}
    albums = []

    if request.user.groups.values_list('name', flat=True).count() == 0:
        # user doesn't belong to any group
        print "User {} doesn't belong to any group".format(request.user.username)
    else:
        # get albums list for that user
        albumsgroups = AlbumGroup.objects.filter(group__name=request.user.groups.values_list('name', flat=True)[0])
        MyAlbumGroup = albumsgroups[0]
        for album in MyAlbumGroup.album.all().order_by('-creation_date'):
            print album
            if album.creation_date is not None and str(album.creation_date.year) == str(year):
                albums.append(album)

        context["albums"] = albums
    return render(request, 'albums_list.html', context)

@login_required
def servealbum(request, Album_id):
    context = {}
    album = Album.objects.filter(id=Album_id)
    context["album"] = album[0]
    if album[0].creation_date is not None:
        context["back_url"] = album[0].creation_date.year

    AlbumData=Photo.objects.filter(album__id=Album_id).order_by('name')
    #AlbumData=json.load(open("{0}{1}/photos_list.json".format(settings.ALBUMS_DIR, album[0].id)))
    context["photos_data"]=AlbumData

    return render(request, 'gallery.html', context)


@login_required
def retrieve_photo(request, album_id, photo_name ):
#def retrieve_photo(request, album_id):
    abs_filename = settings.ALBUMS_DIR+album_id+"/"+photo_name
    print abs_filename

    return sendfile(request, abs_filename, attachment=False)
    #response = HttpResponse() # 200 OK
    #response['content-type'] # We'll let the web server guess this.
    #response['X-Sendfile'] = abs_filename
    #return response
