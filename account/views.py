import json
import re
import bcrypt
import jwt

from django.views           import View
from django.http            import HttpResponse, JsonResponse
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from .utils                 import signin_decorator
from my_settings            import SECRET_KEY, ALGORITHM
from .models                import User, FavoriteAlbum, FavoriteArtist, FavoriteTrack
from music.models           import Artist, Album, Track


PASSWORD_REGEX = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{8,})"

class SignUpView(View):

    def post(self, request):
        data = json.loads(request.body)

        try:
            validate_email(data['email'])

            if not re.match(PASSWORD_REGEX, data['password']):
                return JsonResponse({"message": "INVALID_PASSWORD"}, status = 400)

            if User.objects.filter(email=data['email']).exists():
                return JsonResponse({"message": "USER_EXISTS"}, status = 400)

            password    = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            User(
                email       = data['email'],
                password   = password,
            ).save()

            return HttpResponse(status = 200)

        except ValidationError:
            return JsonResponse({"message": "INVALID_FORMAT"}, status = 400)

        except KeyError:
            return JsonResponse({"message": "INVALID_KEYS"}, status = 400)

class UserCheckView(View):
    def post(self, request):
        data = json.loads(request.body)

        if User.objects.filter(email = data['email']).exists():

            return HttpResponse(status=200)

        return HttpResponse(status=400)

class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            user = User.objects.get(email = data['email'])

            if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                access_token = jwt.encode({'email': user.email}, SECRET_KEY['secret'], algorithm = ALGORITHM).decode('utf-8')

                return JsonResponse({"access_token": access_token}, status = 200)

            return HttpResponse(status = 401)

        except User.DoesNotExist:
            return HttpResponse(status = 400)

        except KeyError:
            return JsonResponse({"message": "INVALID_KEYS"}, status = 400)

class CollectionView(View):
    @signin_decorator
    def get(self, request):
        user        = User.objects.get(id=request.user)
        category    = request.GET.get('category', None)

        if category == 'artist':
            artists = user.artist.all()
            artist_attribute = [
                {
                    'id'                : prop.id,
                    'name'              : prop.name,
                    'thumbnail_url'     : prop.thumbnail_url,
                } for prop in artists
            ]
            return JsonResponse({'artists': artist_attribute}, status=200)

        elif category == 'album':
            albums = user.album.all()
            album_attributes = [
                {
                    'id'                : prop.id,
                    'name'              : prop.name,
                    'thumbnail_url'     : prop.thumbnail_url,
                    'is_live'           : prop.is_live,
                    'is_single'         : prop.is_single,
                    'artist'            : Album.objects.get(id=prop.id).artist_set.get(album__id=prop.id).name,
                } for prop in albums
            ]
            return JsonResponse({'albums': album_attributes}, status=200)

        else:
            tracks = user.track.all()
            track_attributes = [
                {
                    'id'            : prop.id,
                    'name'          : prop.name,
                    'music'         : prop.music_url,
                    'time'          : prop.time,
                    'is_explicit'   : prop.is_explicit,
                    'is_master'     : prop.is_master,
                    'artist'        : Track.objects.get(id=prop.id).artist_set.get(track__id=prop.id).name,
                    'album'         : Album.objects.get(track__id=prop.id).name,
                } for prop in tracks
            ]
            return JsonResponse({'tracks': track_attributes}, status=200)

    @signin_decorator
    def post(self, request):
        data        = json.loads(request.body)
        category    = request.GET.get('category', None)
        try:
            if category == 'artist':
                FavoriteArtist.objects.create(user_id=request.user, artist_id=data['artist_id'])
            elif category == 'album':
                FavoriteAlbum.objects.create(user_id=request.user, album_id=data['album_id'])
            else:
                FavoriteTrack.objects.create(user_id=request.user, track_id=data['track_id'])

            return HttpResponse(status=200)

        except KeyError:
            return JsonResponse({'message': 'INVALID_KEYS'}, status=400)

    @signin_decorator
    def delete(self, request):
        data        = json.loads(request.body)
        category    = request.GET.get('category', None)
        try:
            if category == 'artist':
                FavoriteArtist.objects.get(user_id=request.user, artist_id=data['artist_id']).delete()
            elif category == 'album':
                FavoriteAlbum.objects.get(user_id=request.user, album_id=data['album_id']).delete()
            else:
                FavoriteTrack.objects.get(user_id=request.user, track_id=data['track_id']).delete()

            return HttpResponse(status=200)

        except KeyError:
            return JsonResponse({'message': 'INVALID_KEYS'}, status=400)