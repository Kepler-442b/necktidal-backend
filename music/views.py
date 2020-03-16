import json

from .models    import (
    Artist,
    Track,
    Album,
    ArtistAlbum,
    ArtistTrack,
    AlbumTrack
)

from account.models import(
    Playlist
)

from django.views       import View
from django.http        import HttpResponse, JsonResponse, StreamingHttpResponse
from django.db.models   import Q

class ArtistDetailView(View):
    def get(self, request, artist_id):

        if Artist.objects.filter(id = artist_id).exists():
            artist              = Artist.objects.get(id = artist_id)
            artist_attribute    = {
                'id'            : artist.id,
                'name'          : artist.name,
                'thumbnail_url' : artist.thumbnail_url,
                'description'   : artist.description,
            }

            return JsonResponse({'artist':artist_attribute}, status = 200)

        return JsonResponse({'message':'NO_ARTIST'}, status = 400)

class ArtistTopTrackView(View):
    def get(self, request, artist_id):
        if Track.objects.filter(artist__id = artist_id).exists():
            tracks  = Track.objects.filter(artist__id = artist_id).order_by('count')
            track_attribute = [
                {
                    'id'            : track.id,
                    'name'          : track.name,
                    'time'          : track.time,
                    'music_url'     : track.music_url,
                    'is_master'     : track.is_master,
                    'is_explicit'   : track.is_explicit,
                    'artist_info'   : list(track.artist_set.values('id', 'name')),
                    'album_info'    : list(track.album_set.values('id', 'name', 'thumbnail_url'))
                } for track in tracks
            ]

            return JsonResponse({'tracks' : track_attribute}, status = 200)

        return JsonResponse({'message' : 'NO_TRACK'}, status = 400)
