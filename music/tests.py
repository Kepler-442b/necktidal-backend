import json

from .models        import (
    Artist,
    Track,
    Album,
    ArtistTrack,
    ArtistAlbum,
    AlbumTrack
)

from django.test    import TestCase
from django.test    import Client

class ArtistDetailTest(TestCase):

    def setUp(self):
        client = Client()
        Artist.objects.create(
            id = 1,
            name = 'Future',
            thumbnail_url = 'https://resources.tidal.com/images/8faf1ca1/6130/45da/9d10/6d9f4b825605/480x480.jpg',
        )

    def test_artist_detail_get_success(self):
        client = Client()
        response = client.get('/music/artist/1')
        self.assertEqual(response.json(),
            {
               'artist':{
                    'id'            : 1,
                    'name'          : 'Future',
                    'thumbnail_url' : 'https://resources.tidal.com/images/8faf1ca1/6130/45da/9d10/6d9f4b825605/480x480.jpg',
                    'description'   : None,
                }
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_artist_detail_get_fail(self):
        client = Client()
        response = client.get('/music/artist/20000')
        self.assertEqual(response.json(),
            {
               'message':'NO_ARTIST'
            }
        )
        self.assertEqual(response.status_code, 400)

    def test_artist_detail_get_not_found(self):
        client = Client()
        response = client.get('/music/aritst?artist_id=84')
        self.assertEqual(response.status_code, 404)

class ArtistTopTrackTest(TestCase):

    def setUp(self):
        client = Client()
        Artist.objects.create(
            id   = 1,
            name = 'Future',
        )
        Track.objects.create(
            id          = 1,
            name        = 'Baby Pluto',
            time        = '00:03:30.000000',
            music_url   = None,
            is_master   = 0,
            is_explicit = 0,
        )

        ArtistTrack.objects.create(artist_id = 1, track_id = 1)

        Album.objects.create(
            id = 1,
            name = 'Eternal Atake',
            thumbnail_url = 'https://resources.tidal.com/images/cd542e79/dce0/4809/9f3e/1c3cb2203436/320x320.jpg'
        )

        AlbumTrack.objects.create(album_id = 1, track_id = 1)

    def test_artist_toptrack_get_success(self):
        client = Client()
        response = client.get('/music/artist/1/toptrack')
        self.assertEqual(response.json(),
            {
                'tracks':[{
                    'id'            : 1,
                    'name'          : 'Baby Pluto',
                    'time'          : '00:03:30',
                    'music_url'     : None,
                    'is_master'     : False,
                    'is_explicit'   : False,
                    'artist_info'   : [{
                        'id'    : 1,
                        'name'  : 'Future'
                    }],
                    'album_info'    : [{
                        'id'            : 1,
                        'name'          : 'Eternal Atake',
                        'thumbnail_url' : 'https://resources.tidal.com/images/cd542e79/dce0/4809/9f3e/1c3cb2203436/320x320.jpg',
                        }
                    ]
                }]
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_artist_toptrack_get_fail(self):
        client = Client()
        response = client.get('/music/artist/2/toptrack')
        self.assertEqual(response.json(),
            {
               'message':'NO_TRACK'
            }
        )
        self.assertEqual(response.status_code, 400)

    def test_artist_toptrack_get_not_found(self):
        client = Client()
        response = client.get('/music/aritst/toptrack?artist_id=84')
        self.assertEqual(response.status_code, 404)

class NewTrackTest(TestCase): 

    def setUp(self):
        client = Client()

        Artist.objects.create(
            id   = 1,
            name = 'Future',
        )
        Track.objects.create(
            id          = 1,
            name        = 'Baby Pluto',
            time        = '00:03:30.000000',
            music_url   = None,
            is_master   = 0,
            is_explicit = 0,
        )

        Track.objects.create(
            id          = 2,
            name        = 'Lo Mein',
            time        = '00:03:15.000000',
            music_url   = None,
            is_master   = 0,
            is_explicit = 0,
        )

        ArtistTrack.objects.create(
            artist_id = 1, 
            track_id = 1
        )

        ArtistTrack.objects.create(
            artist_id = 1,
            track_id = 2
        )

        Album.objects.create(
            id = 1,
            name = 'Eternal Atake',
            thumbnail_url = 'https://resources.tidal.com/images/cd542e79/dce0/4809/9f3e/1c3cb2203436/320x320.jpg',
            released_date = '2020-03-07 12:54:18.000000'
        )

        Album.objects.create(
            id = 2,
            name = 'Luv Is Rage 2',
            thumbnail_url = 'https://resources.tidal.com/images/f5b50041/48e1/4a8b/9634/32f06c0185b0/320x320.jpg',
            released_date = '2020-03-10 12:00:18.000000'
        )

        AlbumTrack.objects.create(
            track_id = 1,
            album_id = 1
        )

        AlbumTrack.objects.create(
            album_id = 2,
            track_id = 2
        )

    def test_new_track_get_success(self):
        client = Client()
        response = client.get('/music/track/new?limit=2')
        self.assertEqual(response.json(),{
            'tracks':[
                {
                    'id'            : 1,
                    'name'          : 'Baby Pluto',
                    'time'          : '00:03:30',
                    'music_url'     : None,
                    'is_master'     : False,
                    'is_explicit'   : False,
                    'artist_info'   : [
                        {
                            'id'    : 1,
                            'name'  : 'Future'
                        }
                    ],
                    'album_info'    : [
                        {
                            'id'            : 1,
                            'name'          : 'Eternal Atake',
                            'thumbnail_url' : 'https://resources.tidal.com/images/cd542e79/dce0/4809/9f3e/1c3cb2203436/320x320.jpg'
                        }
                    ]
                },
                {
                    'id'            : 2,
                    'name'          : 'Lo Mein',
                    'time'          : '00:03:15',
                    'music_url'     : None,
                    'is_master'     : False,
                    'is_explicit'   : False,
                    'artist_info'   : [
                        {
                            'id'    : 1,
                            'name'  : 'Future'
                        }],
                    'album_info'    : [
                        {
                            'id'            : 2,
                            'name'          : 'Luv Is Rage 2',
                            'thumbnail_url' : 'https://resources.tidal.com/images/f5b50041/48e1/4a8b/9634/32f06c0185b0/320x320.jpg'
                        }]
                }]
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_new_track_get_fail(self):
        client = Client()
        response = client.get('/music/track/new')
        self.assertEqual(response.json(),
            {
                'message' : 'INVALID_KEYWORD'
            }
        )
        self.assertEqual(response.status_code, 400)

    def test_new_track_get_too_many_items(self):
        client = Client()
        response = client.get('/music/track/new?limit=50000000')
        self.assertEqual(response.json(),
            {
                'message' : 'INVALID_KEY'
            }
        )
        self.assertEqual(response.status_code, 400)

class NewAlbumTest(TestCase):

    def setUp(self):
        client = Client()

        Artist.objects.create(
            id   = 1,
            name = 'Future',
        )

        Album.objects.create(
            id = 1,
            name = 'Eternal Atake',
            thumbnail_url = 'https://resources.tidal.com/images/cd542e79/dce0/4809/9f3e/1c3cb2203436/320x320.jpg',
            released_date = '2020-03-07 12:54:18.000000'
        )

        ArtistAlbum.objects.create(
            artist_id = 1,
            album_id = 1
        )

    def test_new_album_get_success(self):
        client = Client()
        response = client.get('/music/album/new?limit=1')
        self.assertEqual(response.json(),{
            'albums' : [
                {
                    'id'        : 1,
                    'name'      : 'Eternal Atake',
                    'artist'    : [
                        {
                            'id' : 1,
                            'name' : 'Future',
                        }],
                    'thumbnail_url' : 'https://resources.tidal.com/images/cd542e79/dce0/4809/9f3e/1c3cb2203436/320x320.jpg'
                }]
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_new_album_get_fail(self):
        client = Client()
        response = client.get('/music/album/new')
        self.assertEqual(response.json(),
            {
                'message' : 'INVALID_KEYWORD'
            }
        )
        self.assertEqual(response.status_code, 400)

    def test_new_album_get_too_many_items(self):
        client = Client()
        response = client.get('/music/album/new?limit=50000000')
        self.assertEqual(response.json(),
            {
                'message' : 'INVALID_KEY'
            }
        )
        self.assertEqual(response.status_code, 400)
