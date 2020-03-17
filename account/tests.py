import  json
import  jwt
import  bcrypt

from django.test            import TestCase, Client
from unittest.mock          import patch, MagicMock

from .utils                 import signin_decorator
from my_settings            import SECRET_KEY, ALGORITHM



from .models                import User, FavoriteAlbum, FavoriteArtist, FavoriteTrack
from music.models           import Artist, Album, Track, AlbumTrack, ArtistTrack, ArtistAlbum

user    = User.objects.get(id=2)
token   = jwt.encode({'user_id': user.id}, SECRET_KEY['secret'], algorithm = ALGORITHM).decode('utf-8')

class UserTest(TestCase):
    def setUp(self):
        check = '12Ab34Cd!!'
        User.objects.create(
            email       = 'skim1025@abc.abc',
            password    = bcrypt.hashpw(check.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        )

    def tearDown(self):
        User.objects.all().delete()

#usercheck test
    def test_user_check_view_post_success(self):
        user = {'email': 'skim1025@abc.abc'}
        response = Client().post('/account/', json.dumps(user), content_type='applications/json')

        self.assertEqual(response.status_code, 200)

    def test_user_check_view_post_fail(self):
        user = {'email': 'xxxxx@abc.abc'}
        response = Client().post('/account/', json.dumps(user), content_type='applications/json')

        self.assertEqual(response.status_code, 400)

#signup test
    def test_signup_view_post_success(self):
        user    = {
            'email'     : 'skim1026@abc.abc',
            'password'  : '12Ab34Cd!!'
        }
        response    = Client().post('/account/signup', json.dumps(user), content_type='applications/json')

        self.assertEqual(response.status_code, 200)

    def test_signup_view_post_invalid_password(self):
        user    = {
            'email'     : 'skim1026@abc.abc',
            'password'  : '12345'
        }
        response = Client().post('/account/signup', json.dumps(user), content_type='applications/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                "message": "INVALID_PASSWORD"
            }
        )

    def test_signup_view_post_existing_user(self):
        user    = {
            'email'     : 'skim1025@abc.abc',
            'password'  : '12Ab34Cd!!'
        }
        response = Client().post('/account/signup', json.dumps(user), content_type='applications/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                "message": "USER_EXISTS"
            }
        )

    def test_signup_view_post_invalid_format(self):
        user    = {
            'email'     : '.@.',
            'password'  : '12Ab34Cd!!'
        }
        response = Client().post('/account/signup', json.dumps(user), content_type='applications/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                "message": "INVALID_FORMAT"
            }
        )

    def test_signup_view_post_invalid_keys(self):
        user    = {
            'name'      : 'skim1026@abc.abc',
            'password'  : '12Ab34Cd!!'
        }
        response = Client().post('/account/signup', json.dumps(user), content_type='applications/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                "message": "INVALID_KEYS"
            }
        )

# signin test
    def test_signin_view_post_success(self):
        user    = {
            'email'     : 'skim1025@abc.abc',
            'password'  : '12Ab34Cd!!',
        }
        response    = Client().post('/account/signin', json.dumps(user), content_type='applications/json')
        token       = response.json()['Authorization']

        self.assertEqual(response.status_code, 200)

    def test_signin_view_post_incorrect_password(self):
        user    = {
            'email'     : 'skim1025@abc.abc',
            'password'  : '12Ab34Cd!',
        }
        response = Client().post('/account/signin', json.dumps(user), content_type='applications/json')

        self.assertEqual(response.status_code, 401)

    def test_signin_view_post_invalid_user(self):
        user    = {
            'email'     : 'skim1027@abc.abc',
            'password'  : '12Ab34Cd!!',
        }
        response = Client().post('/account/signin', json.dumps(user), content_type='applications/json')

        self.assertEqual(response.status_code, 400)

    def test_signin_view_post_key_error(self):
        user    = {
            'name'      : 'skim1025@abc.abc',
            'password'  : '12Ab34Cd!!',
        }
        response = Client().post('/account/signin', json.dumps(user), content_type='applications/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                "message": "INVALID_KEYS"
            }
        )

class SocialSignInTest(TestCase):
    def setUp(self):
        check = '12Ab34Cd!!'
        User.objects.create(
            email           = 'skim1025@abc.abc',
            social_email    = 'skim1025@abc.abc',
            password        = bcrypt.hashpw(check.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            thumbnail_url   = 'me.jpeg',
            first_name      = 'Soo',
            last_name       = 'Kim'
        )

    def tearDown(self):
        User.objects.all().delete()

    @patch('account.views.requests')
    def test_social_sign_in_view_get_success(self, mocked_request):
        class FakeResponse:
            def json(self):
                return {
                    'email' : 'skim1025@abc.abc'
                }
        mocked_request.get  = MagicMock(return_value = FakeResponse())
        header = {'HTTP_Authorization': 'access_token'}
        response = Client().get('/account/social_signin', content_type='applications/json', **header)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
            {
                "thumbnail_url" :"me.jpeg",
                "name"          :"Soo Kim"
            }
        )

class MyCollectionTest(TestCase):
    def setUp(self):
        check = '12AB34cd!!'
        User.objects.create(
            email       = 'joker@abc.abc',
            password    = bcrypt.hashpw(check.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        )

        Artist.objects.create(
            id="1",
            name="Vampire Weekend",
            thumbnail_url="VW.jpeg"
        )
        Album.objects.create(
            id="1",
            name="FOTB",
            is_single=True,
            is_live=False,
            thumbnail_url="FOTB.jpeg",
            released_date="2020-03-07 12:54:18.000000"
        )
        Track.objects.create(
            id="1",
            name="Harmony Hall",
            time="00:03:30",
            music_url= "track1.mp3",
            credit=[
                {'Producer': ['Brandon Finessin', 'Bugz Ronin']},
                {'Writer':['Cousin Vinny', 'Ike Beatz']},
                {'Featured Artist' :'Brandon Finessin'},
                {'Lyricist':['Bugz Ronin', 'Supah Mario']},
                {'Composer' : 'OOGIE MANE'}
            ],
            is_explicit=True,
            is_master=False,
        )
        ArtistTrack.objects.create(
            artist_id='1',
            track_id='1'
        )
        AlbumTrack.objects.create(
            album_id='1',
            track_id='1'
        )
        ArtistAlbum.objects.create(
            artist_id='1',
            album_id='1'
        )
        FavoriteArtist.objects.create(
            user_id='1',
            artist_id='1'
        )
        FavoriteAlbum.objects.create(
            user_id='1',
            album_id='1'
        )
        FavoriteTrack.objects.create(
            user_id='1',
            track_id='1',
            date_added="2020-03-14 20:40:43.305173"
        )

    def tearDown(self):
        User.objects.all().delete()
        Artist.objects.all().delete()
        Album.objects.all().delete()
        Track.objects.all().delete()
        FavoriteArtist.objects.all().delete()
        FavoriteAlbum.objects.all().delete()
        FavoriteTrack.objects.all().delete()

 #collection test
    def test_collection_view_get_artist_success(self):
        response = Client().get(
            "/account/collection?category=artist",
            **{"HTTP_AUTHORIZATION":token,
                "content_type" : "application/json"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
             {
                 'artists': [{
                     'id': 1,
                     'name': "Vampire Weekend",
                     'thumbnail_url': 'VW.jpeg',}]
             }
        )

    def test_collection_view_get_album_success(self):
        response = Client().get(
            "/account/collection?category=album",
            **{"HTTP_AUTHORIZATION":token,
                "content_type" : "application/json"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
             {
                 'albums': [{
                     'id'           : 1,
                     'name'         : "FOTB",
                     'thumbnail_url': "FOTB.jpeg",
                     'is_live'      : False,
                     'is_single'    : True,
                     'artist'       : "Vampire Weekend"}]
             }
        )

    def test_collection_view_get_track_success(self):
        response = Client().get(
            "/account/collection?category=track",
            **{"HTTP_AUTHORIZATION":token,
                "content_type" : "application/json"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
             {
                 'tracks':[{
                     'id': 1,
                     'name': "Harmony Hall",
                     'music': "track1.mp3",
                     'time': "00:03:30",
                     'is_explicit': True,
                     'is_master': False,
                     'artist': "Vampire Weekend",
                     'album': "FOTB",
                 }]
             }
        )

    def test_collection_view_post_artist_success(self):
        test        = {"artist_id":"1"}
        response    = Client().post(
            "/account/collection?category=artist",
            json.dumps(test),
            **{"HTTP_AUTHORIZATION":token,
                "content_type" : "application/json"})
        self.assertEqual(response.status_code, 200)

    def test_collection_view_post_album_success(self):
        test        = {"album_id":"1"}
        response    = Client().post(
            "/account/collection?category=album",
            json.dumps(test),
            **{"HTTP_AUTHORIZATION":token,
                "content_type" : "application/json"})
        self.assertEqual(response.status_code, 200)

    def test_collection_view_post_track_success(self):
        test = {"track_id": "1"}
        response = Client().post(
            "/account/collection?category=track",
            json.dumps(test),
            **{"HTTP_AUTHORIZATION":token,
                "content_type" : "application/json"})
        self.assertEqual(response.status_code, 200)

    def test_collection_view_post_artist_key_error(self):
        test            = {'ARTIST_ID':"1"}
        response = Client().post(
            "/account/collection?category=artist",
            json.dumps(test),
            **{"HTTP_AUTHORIZATION":token,
               "content_type" : "application/json"})
        self.assertEqual(response.status_code, 400)

    def test_collection_view_post_album_key_error(self):
        test = {'ALBUM_ID': "1"}
        response = Client().post(
            "/account/collection?category=album",
            json.dumps(test),
            **{"HTTP_AUTHORIZATION":token,
               "content_type" : "application/json"})
        self.assertEqual(response.status_code, 400)

    def test_collection_view_post_track_key_error(self):
        test = {'TRACK_ID': "1"}
        response = Client().post(
            "/account/collection?category=track",
            json.dumps(test),
            **{"HTTP_AUTHORIZATION":token,
               "content_type" : "application/json"})
        self.assertEqual(response.status_code, 400)

    def test_collection_view_delete_artist_success(self):
        test    = {'artist_id':"1"}
        response = Client().delete(
            "/account/collection?category=artist",
            json.dumps(test),
            **{"HTTP_AUTHORIZATION":token,
               "content_type" : "application/json"})
        self.assertEqual(response.status_code, 200)

    def test_collection_view_delete_album_success(self):
        test    = {'album_id':"1"}
        response = Client().delete(
            "/account/collection?category=album",
            json.dumps(test),
            **{"HTTP_AUTHORIZATION":token,
               "content_type" : "application/json"})
        self.assertEqual(response.status_code, 200)

    def test_collection_view_delete_track_success(self):
        test    = {'track_id':'1'}
        response = Client().delete(
            "/account/collection?category=track",
            json.dumps(test),
            **{"HTTP_AUTHORIZATION": token,
               "content_type": "application/json"})
        self.assertEqual(response.status_code, 200)

    def test_collection_view_delete_artist_key_error(self):
        test = {'ARTIST_ID':'1'}
        response = Client().delete(
            "/account/collection?category=artist",
            json.dumps(test),
            **{"HTTP_AUTHORIZATION": token,
               "content_type": "application/json"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message': 'INVALID_KEYS'
            }
        )

    def test_collection_view_delete_album_key_error(self):
        test = {'ARTIST_ID': '1'}
        response = Client().delete(
            "/account/collection?category=album",
            json.dumps(test),
            **{"HTTP_AUTHORIZATION": token,
               "content_type": "application/json"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message': 'INVALID_KEYS'
            }
        )

    def test_collection_view_delete_track_key_error(self):
        test = {'ARTIST_ID':'1'}
        response = Client().delete(
            "/account/collection?category=track",
            json.dumps(test),
            **{"HTTP_AUTHORIZATION": token,
               "content_type": "application/json"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message': 'INVALID_KEYS'
            }
        )
