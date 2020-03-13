import os
import django
import csv
import time

from datetime   import datetime
from time       import strptime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'necktidal.settings')
django.setup()

from music.models import *

#Track
def add_track():
#    Track.objects.all().delete()
    with open('data/track.csv') as hand:
        reader = csv.reader(hand)
        bulk_list = []
        for row in reader:
            time_csv    = row[1]
            new_time    = time.strptime(row[1], '%M:%S')
            timestamp   = time.mktime(new_time)
            my_time     = datetime.fromtimestamp(timestamp).time()

            bulk_list.append(Track(
                name        = row[0],
                time        = my_time,
                is_explicit = row[2],
                is_master   = row[3],
                credit      = row[4]
            ))
    Track.objects.bulk_create(bulk_list)

#Artist
def add_artist():
#    Artist.objects.all().delete()
    with open('data/artist.csv') as hand:
        reader = csv.reader(hand)
        bulk_list = []
        for row in reader:
            bulk_list.append(Artist(
                name            = row[0],
                thumbnail_url   = row[1],
                description     = row[4],
            ))

    Artist.objects.bulk_create(bulk_list)

#Album
def add_album():
#    Album.objects.all().delete()
    with open('data/album.csv') as hand:
        reader = csv.reader(hand)
        bulk_list = []
        for row in reader:
            bulk_list.append(Album(
                name            = row[0],
                thumbnail_url   = row[1],
                released_date   = row[2],
                is_live         = row[3],
                is_single       = row[4]))

    Album.objects.bulk_create(bulk_list)


#ArtistAlbum
def add_artist_album():
#    ArtistAlbum.objects.all().delete()
    with open('data/featured_album_page_m.csv') as hand:
        reader = csv.reader(hand)
        bulk_list = []
        next(reader, None)
        for row in reader:
            album_csv = row[2]
            artist_csv = row[3]
            album = Album.objects.filter(name=album_csv, is_single = 0, is_live = 0)
            artist = Artist.objects.filter(name=artist_csv)
            bulk_list.append(ArtistAlbum(
                album_id = album[0].id,
                artist_id = artist[0].id))

    ArtistAlbum.objects.bulk_create(bulk_list)


#ArtistTrack
def add_artist_track():
#    ArtistTrack.objects.all().delete()
    with open('data/featured_album_page_m.csv') as hand:
        reader = csv.reader(hand)
        bulk_list = []
        for row in reader:
            replacer = '='
            tracks_csv = row[5].strip('[ ] \'').replace('\', \'', replacer).replace('\', \"',replacer).replace('\", \'', replacer).split(replacer)
            artist_csv = row[6].strip('[ ] \'').replace('\', \'', replacer).split(replacer)
            
            for i in range(len(tracks_csv)):
                track_s = tracks_csv[i].strip('\' \"')
                artist_s = artist_csv[i].strip('\'').split(',')
                
                track = Track.objects.filter(name = track_s)
                
                for person in artist_s:
                    artist = Artist.objects.filter(name=person)
                    if artist.exists() and len(track) == 1:
                        bulk_list.append(ArtistTrack(
                            track_id = track[0].id,
                            artist_id = artist[0].id))

    ArtistTrack.objects.bulk_create(bulk_list)

#AlbumTrack
def add_album_track():
#    AlbumTrack.objects.all().delete()
    with open('data/featured_album_page_m.csv') as hand:
        reader = csv.reader(hand)
        bulk_list = []
        next(reader, None)
        for row in reader:
            album_csv = row[2]
            album = Album.objects.get(name=album_csv, is_single = 0, is_live = 0)

            tracks_csv = row[5].strip('[ ]').split(',')
            for item in tracks_csv:
                track_name = item.strip().strip("''")
                track = Track.objects.filter(name = track_name)
                if len(track) == 1:
                    bulk_list.append(AlbumTrack(
                        album_id = album.id,
                        track_id = track[0].id))

        bulk_list.append(AlbumTrack(album_id = 81, track_id = 49))
        bulk_list.append(AlbumTrack(album_id = 177, track_id = 86))

    AlbumTrack.objects.bulk_create(bulk_list)

#SocialMedia
def add_social_media():
#    SocialMedia.objects.all().delete()
    bulk_list = []
    bulk_list.append(SocialMedia(name = 'facebook'))
    bulk_list.append(SocialMedia(name = 'twitter'))
    SocialMedia.objects.bulk_create(bulk_list)

def add_artist_social_media():
#    ArtistSocialMedia.objects.all().delete()
    with open('data/artist.csv') as hand:
        reader = csv.reader(hand)
        bulk_list = []

        for row in reader:
            name_csv    = row[0]
            facebook    = row[2]
            twitter     = row[3]
            
            artist      = Artist.objects.filter(name = name_csv)

            if len(artist) == 1:
                if len(facebook) > 0:
                    media_id    = SocialMedia.objects.filter(name = 'facebook')[0].id
                    bulk_list.append(ArtistSocialMedia(
                        social_media_id = media_id,
                        account_url=facebook,
                        artist_id = artist[0].id))

                if len(twitter) > 0:
                    media_id    = SocialMedia.objects.filter(name = 'twitter')[0].id
                    bulk_list.append(ArtistSocialMedia(
                        social_media_id = media_id,
                        account_url = twitter,
                        artist_id = artist[0].id))

    ArtistSocialMedia.objects.bulk_create(bulk_list)

add_artist()
add_track()
add_album()
add_artist_album()
add_artist_track()
add_album_track()
#add_social_media()
add_artist_social_media()
