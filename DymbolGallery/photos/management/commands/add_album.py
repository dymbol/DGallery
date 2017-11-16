#-*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from photos.models import *
import datetime
import time
import os
from PIL import Image
from resizeimage import resizeimage
from django.conf import settings
import sys
import json
import exifread
import threading



def verbose(text):
    if settings.DEBUG == True:
        print text
ImageExtensions=[".jpg", ".jpeg", ".png", ".gif"]
VideoExtensions=[".avi", ".mpg", ".mpeg", ".mov", ".mp4"]


class Command(BaseCommand):
    help = "Creates and adds album to gallery.\nRequires path to dir with photos"
    exif_data = {}
    def add_arguments(self, parser):
        parser.add_argument('SrcAlbumsDirs', nargs='+', type=str)

    def handle(self, *args, **options):

        ###########################################
        SrcAlbumsDirs = options['SrcAlbumsDirs']
        photos_list = [] #dict for json output file

        exit_read = False
        threads_list = []
        max_threads = settings.II_MAX_THREADS
        max_threads += 1  # doliczamy główny wątek skryptu
        ###########################################


        print("Operating in {} threads".format(max_threads))
        for SrcAlbumDir in SrcAlbumsDirs:
            Command.exif_data["read"] = False
            album_name = os.path.basename(os.path.normpath(SrcAlbumDir))
            Command.exif_read = False #True if exif data were received from file (creation date fo exambple)


            # First check if album with that name exists
            num_results = Album.objects.filter(name=album_name).exists()
            if num_results == True:
                print "Album with name '{}' already exists. Skipping...".format(album_name)
            else:
                #create new album in db to get ID
                album = Album()
                album.name = album_name
                album.visible_name = album_name
                print "Creating album {}".format(os.path.basename(os.path.normpath(SrcAlbumDir)))
                album.save()

                #create album dir
                output_dir=settings.ALBUMS_DIR+str(album.id)
                os.makedirs(output_dir)


                def resize_image(image, index, imagesCount, baseName, inputExtensionLower):
                    #sys.stdout.flush()
                    #sys.stdout.write("Processing image, {} {}/{} \r".format(image, index, imagesCount))
                    # dict = name: desired width of image
                    exif_data= {}
                    image_sizes = {
                        baseName: 800,
                        baseName + "-375": 375,
                        baseName + "-480": 480,
                        baseName + "-1600": 1600,
                        "thumb-" + baseName: 348
                    }
                    with open(SrcAlbumDir+"/"+image, 'rb') as f:
                        # get album creation date from the first image file (from EXIF)
                        with Image.open(f) as image2:
                            for img_size in image_sizes.keys():
                                output = resizeimage.resize_height(image2, image_sizes[img_size],validate=False)
                                out_path = output_dir + "/" + img_size + inputExtensionLower
                                output.save(out_path, image2.format)

                def check_if_can_start_thread():
                    if threading.activeCount() >= max_threads:
                        time.sleep(0.1)
                        check_if_can_start_thread()
                    else:
                        verbose(("Starting thread {}".format(watek)))
                        watek.start()
                        verbose("Aktualna liczba aktywnych wątków: {}".format(threading.activeCount()))



                ##############################################
                ################ Main algorythm ##############
                ##############################################


                #start threads according to max_threads number
                imagesCount = len(os.listdir(SrcAlbumDir))
                for index, file in enumerate(os.listdir(SrcAlbumDir)):
                    basename = os.path.splitext(file)[0]
                    extension = os.path.splitext(file)[1]

                    if extension.lower() in ImageExtensions: #if image is in supported images
                        if Command.exif_data["read"] == False:  #get creation date if not read before
                            with open(SrcAlbumDir + "/" + file, 'rb') as img:
                                tags = exifread.process_file(img)
                                Command.exif_data["creation_date"] = datetime.datetime.strptime(str(tags["EXIF DateTimeOriginal"]), '%Y:%m:%d %H:%M:%S')
                                Command.exif_data["read"] = True
                        watek = threading.Thread(target=resize_image, args=(file, index, imagesCount, basename, extension.lower())) #resize image
                        watek.setName(file)
                        check_if_can_start_thread()
                        #save to db
                        photo_new = Photo()
                        photo_new.album = album
                        photo_new.name = basename
                        photo_new.type = extension.lower()[1:]
                        verbose("Creating photo {}".format(photo_new.name))
                        photo_new.save()

                    elif extension.lower() in VideoExtensions:  # if image is in supported videos
                        print "FoundVideo: {}".format(file)

                        #convert wideo to some browser-friendly format

                        #save video to
                        #ffmpeg -i rajsa.mp4 -c:v libvpx -b:v 1M -c:a libvorbis rajsa.webm
                        #out_path = output_dir + "/" + "1600" + inputExtensionLower

                        #create thumnail from wideo with name 'thumb-filename.jpg'
                        #out_path = output_dir + "/" + "thumb-"" + inputExtensionLower


                        # wideo_new = Photo()
                        # wideo_new.album = album
                        # wideo_new.name = basename
                        # wideo_new.type = extension.lower()[1:]
                        # verbose("Creating photo {}".format(photo_new.name))
                        # wideo_new.save()



                #tell threading to wait for all threads to finish
                for watek in threads_list:
                    watek.join()

                # write  creation date from exif
                if "creation_date" not in Command.exif_data.keys():
                    album.creation_date = datetime.datetime.now()
                elif Command.exif_data["creation_date"] is None:
                    album.creation_date = datetime.datetime.now()
                else:
                    album.creation_date = Command.exif_data["creation_date"]
                    album.save()

                print "Album {} created".format(album.name)
