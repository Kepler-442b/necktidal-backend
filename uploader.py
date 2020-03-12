import os
import django
import csv

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'necktidal.settings')
django.setup()

from music.models import *

#track
with open('data/track.csv') as hand:
    reader = csv.reader(hand)
    bulk_list = []
    for row in reader:
        bulk_list.append(Track(
            name            = row[0],
            time            = row[1],
            is_explicit     = row[2],
            is_master       = row[3],
            credit          = row[4]
        ))
Track.objects.bulk_create(bulk_list)

#artist
with open('data/artist.csv') as hand:
    reader = csv.reader(hand)
    bulk_list = []
    for row in reader:
        bulk_list.append(Artist(
            name            = row[0],
            thumbnail_url   = row[1],
            facebook        = row[2],
            twitter         = row[3],
            description     = row[4],
        ))

Artist.objects.bulk_create(bulk_list)

#album
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

