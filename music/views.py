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

class NewTrackView(View):
    def get(self, request):
        limit = request.GET.get('limit', None)

        if limit:
            all_tracks = Track.objects.filter()

            if int(limit) > len(all_tracks):
                return JsonResponse({'message' : 'INVALID_KEY'}, status = 400)

            tracks          = Track.objects.all().order_by('album__released_date')[:int(limit)]
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

        return JsonResponse({'message' : 'INVALID_KEYWORD'}, status = 400)

class NewAlbumView(View):
    def get(self, request):
        limit = request.GET.get('limit', None)

        if limit:
            all_albums = Album.objects.filter()

            if int(limit) > len(all_albums):
                return JsonResponse({'message' : 'INVALID_KEY'}, status = 400)

            albums          = Album.objects.all().order_by('released_date')[:int(limit)]
            album_attribute = [
                {
                    'id'            : album.id,
                    'name'          : album.name,
                    'artist'        : list(album.artist_set.values('id', 'name').distinct()),
                    'thumbnail_url' : album.thumbnail_url,

                } for album in albums
            ]
            return JsonResponse({'albums' : album_attribute}, status = 200)

        return JsonResponse({'message' : 'INVALID_KEYWORD'}, status = 400)

class MusicStreamingView(View):
    def get(self, request):
        track_id    = request.GET.get('track_id', None)

        if track_id:

            if int(track_id) > len(Track.objects.filter()) or int(track_id) <= 0:
                return JsonResponse({'message' : 'INVALID_KEY'}, status = 400)

            track       = Track.objects.get(id = track_id)
            music_file  = track.music_url
            stream      = self.iteration('media/'+music_file)
            response    = StreamingHttpResponse(stream, status = 200)  

            response['Cache-Control']       = 'no-cache'
            response['Content-Type']        = 'audio/mpeg'
            response['Content-Disposition'] = f'filename = {music_file}'

            return response

        return JsonResponse({'message' : 'INVALID_KEYWORD'}, status = 400)

    def iteration(self, file_name):
        with open(file_name, 'rb+') as f:
            while True:
                content = f.read()
                if content: 
                    yield content
                else:   
                    break

